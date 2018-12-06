from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .jobs import preflight_job
from .models import Job, Plan, PreflightResult, Product, Version
from .serializers import (
    JobSerializer,
    PlanSerializer,
    PreflightResultSerializer,
    ProductSerializer,
    VersionSerializer,
)


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("plan", "user")

    def get_queryset(self):
        if self.request.user.is_staff:
            return Job.objects.all()
        if self.request.user.is_anonymous:
            filters = Q(is_public=True)
        else:
            filters = Q(is_public=True) | Q(user=self.request.user)
        return Job.objects.filter(filters)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(
            Q(visible_to__isnull=True)
            | Q(visible_to__organization_ids__contains=[self.request.user.org_id])
        ).published()


class VersionViewSet(viewsets.ModelViewSet):
    serializer_class = VersionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("product", "label")

    def get_queryset(self):
        return Version.objects.all()


class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer

    def get_queryset(self):
        return Plan.objects.filter(
            Q(visible_to__isnull=True)
            | Q(visible_to__organization_ids__contains=[self.request.user.org_id])
        )

    def preflight_get(self, request):
        plan = self.get_object()
        preflight = PreflightResult.objects.most_recent(
            user=request.user, plan=plan, is_valid_and_complete=False
        )
        if preflight is None:
            return Response("", status=status.HTTP_404_NOT_FOUND)
        serializer = PreflightResultSerializer(instance=preflight)
        return Response(serializer.data)

    def preflight_post(self, request):
        plan = self.get_object()
        preflight_job.delay(request.user, plan)
        return Response("", status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["post", "get"])
    def preflight(self, request, pk=None):
        if request.method == "GET":
            return self.preflight_get(request)
        if request.method == "POST":
            return self.preflight_post(request)

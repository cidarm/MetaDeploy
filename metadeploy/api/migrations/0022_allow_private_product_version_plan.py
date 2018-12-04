# Generated by Django 2.1.4 on 2018-12-04 20:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("api", "0021_plan_post_install_message")]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="visible_to",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=1024),
                blank=True,
                default=list,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="visible_to",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=1024),
                blank=True,
                default=list,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="version",
            name="visible_to",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=1024),
                blank=True,
                default=list,
                size=None,
            ),
        ),
    ]

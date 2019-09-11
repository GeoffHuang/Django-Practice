# Generated by Django 2.2.5 on 2019-09-11 17:51

from django.db import migrations
from django.utils import timezone

import yaml

FORTUNE100_FILEPATH = "polls/fortune100.yaml"


def populate_db_with_fortune100(apps, schema_editor):
    Company = apps.get_model('polls', 'Company')
    with open(FORTUNE100_FILEPATH, 'r') as stream:
        fortune100 = yaml.safe_load(stream)
    for company_name in fortune100:
        now = timezone.now()
        company = Company(name=company_name, created_at=now, updated_at=now)
        company.save()


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_company'),
    ]

    operations = [
        migrations.RunPython(populate_db_with_fortune100),
    ]
# Generated by Django 2.2.5 on 2019-09-11 23:46

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
                ('classification', models.CharField(default='B2A', max_length=200)),
                ('created_at', models.DateTimeField(editable=False, verbose_name=datetime.datetime(2019, 9, 11, 23, 46, 29, 54833, tzinfo=utc))),
                ('updated_at', models.DateTimeField(editable=False, verbose_name=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question')),
            ],
        ),
    ]

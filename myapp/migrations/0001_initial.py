# Generated by Django 5.1.5 on 2025-04-21 14:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bulk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.CharField(max_length=50)),
                ('hangUp_time', models.CharField(max_length=50)),
                ('cli', models.CharField(max_length=100)),
                ('call_status', models.CharField(max_length=100)),
                ('talk_time', models.CharField(max_length=100)),
                ('login_id', models.CharField(max_length=100)),
                ('citrix_id', models.CharField(max_length=100)),
                ('call_picked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DailyCallLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citrix_id', models.CharField(max_length=100)),
                ('login_id', models.CharField(max_length=100)),
                ('call_count', models.IntegerField()),
                ('date', models.DateField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('citrix_id', 'login_id', 'date')},
            },
        ),
        migrations.CreateModel(
            name='DailyCallLogHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citrix_id', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('call_count', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('citrix_id', 'date')},
            },
        ),
        migrations.CreateModel(
            name='MonthlyCallLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citrix_id', models.CharField(max_length=100)),
                ('call_count', models.IntegerField()),
                ('month_start', models.DateField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('citrix_id', 'month_start')},
            },
        ),
        migrations.CreateModel(
            name='MonthlyCallLogHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citrix_id', models.CharField(max_length=100)),
                ('call_count', models.IntegerField()),
                ('month_start', models.DateField()),
                ('month_end', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('citrix_id', 'month_start')},
            },
        ),
        migrations.CreateModel(
            name='WeeklyCallLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citrix_id', models.CharField(max_length=100)),
                ('call_count', models.IntegerField()),
                ('week_start', models.DateField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('citrix_id', 'week_start')},
            },
        ),
        migrations.CreateModel(
            name='WeeklyCallLogHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citrix_id', models.CharField(max_length=100)),
                ('call_count', models.IntegerField()),
                ('week_start', models.DateField()),
                ('week_end', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('citrix_id', 'week_start')},
            },
        ),
        migrations.CreateModel(
            name='CallPool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citrix_id', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('bulk_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='randomizar.bulk')),
            ],
            options={
                'unique_together': {('bulk_table',)},
            },
        ),
    ]

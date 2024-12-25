# Generated by Django 4.2.16 on 2024-11-27 02:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('file_path', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedDataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algorithm_type', models.CharField(max_length=3)),
                ('processed_file_path', models.CharField(max_length=255)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataShieldMDApp.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='AlgorithmParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algorithm_type', models.CharField(max_length=3)),
                ('k_value', models.IntegerField(blank=True, null=True)),
                ('l_value', models.IntegerField(blank=True, null=True)),
                ('t_value', models.IntegerField(blank=True, null=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataShieldMDApp.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=20)),
                ('action_date', models.DateTimeField(auto_now_add=True)),
                ('action_success', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
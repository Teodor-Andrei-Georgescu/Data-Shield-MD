# Generated by Django 4.2.16 on 2024-12-05 00:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('DataShieldMDApp', '0003_rename_k_value_algorithmparameter_k_anonymity_k_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='processeddataset',
            name='processed_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='processeddataset',
            name='algorithm_type',
            field=models.CharField(max_length=1),
        ),
    ]

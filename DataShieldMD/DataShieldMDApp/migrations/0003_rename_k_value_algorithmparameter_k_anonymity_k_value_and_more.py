# Generated by Django 4.2.16 on 2024-12-04 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataShieldMDApp', '0002_alter_algorithmparameter_t_value'),
    ]

    operations = [
        migrations.RenameField(
            model_name='algorithmparameter',
            old_name='k_value',
            new_name='k_anonymity_k_value',
        ),
        migrations.AddField(
            model_name='algorithmparameter',
            name='l_diversity_k_value',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='algorithmparameter',
            name='t_closeness_k_value',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

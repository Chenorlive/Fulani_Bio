# Generated by Django 5.0.1 on 2024-02-22 18:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_member_is_head'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='is_head',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origin', to='core.country'),
        ),
    ]

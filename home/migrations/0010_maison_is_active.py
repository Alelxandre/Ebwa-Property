# Generated by Django 5.1.6 on 2025-03-02 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_rename_is_masque_proprietaire_is_deleted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='maison',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]

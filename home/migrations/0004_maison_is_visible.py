# Generated by Django 5.1.6 on 2025-03-01 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_maison_type_maison'),
    ]

    operations = [
        migrations.AddField(
            model_name='maison',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]

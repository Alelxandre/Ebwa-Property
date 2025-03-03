# Generated by Django 5.1.6 on 2025-03-01 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_maison_preciser_la_localisation_de_votre_maison'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maison',
            name='type_maison',
            field=models.CharField(choices=[('VILLA', 'Villa'), ('APPARTEMENT', 'Appartement'), ('MAISON SIMPLE', 'Maison simple'), ('MAISON DE LUXE', 'Maison de luxe'), ('MAISON DE CAMPAGNE', 'Maison de campagne'), ('STUDIO', 'Studio'), ('CHAMBRE MODERNE', 'Chambre moderne'), ('CHAMBRE', 'Chambre')], max_length=100),
        ),
    ]

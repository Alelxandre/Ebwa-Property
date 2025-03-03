from django.db import models

from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.models import User

class Proprietaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Champ pour lier le propriétaire à un utilisateur
    nom = models.CharField(max_length=255, unique=False)
    sexe = models.CharField(max_length=10, choices=[('homme', 'Homme'), ('femme', 'Femme')], blank=True, default='')
    ville = models.CharField(max_length=255, blank=True, default='Douala')
    mot_de_passe = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    last_login = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    telephone = models.BigIntegerField(blank=False,null=True)
    whatsapp = models.URLField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.mot_de_passe and not self.mot_de_passe.startswith('pbkdf2_'):
            self.mot_de_passe = make_password(self.mot_de_passe)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom




class Maison(models.Model):

    
    TYPE_MAISON_CHOICES = [
        ('VILLA', 'Villa'),
        ('APPARTEMENT', 'Appartement'),
        ('MAISON SIMPLE', 'Maison simple'),
        ('MAISON DE LUXE', 'Maison de luxe'),
        ('MAISON DE CAMPAGNE', 'Maison de campagne'),
        ('STUDIO', 'Studio'),
        ('CHAMBRE MODERNE','Chambre moderne'),
        ('CHAMBRE','Chambre'),

    ]
    STATUS_CHOICES = [
        ('libre', 'Libre'),
        ('occupee', 'Occupée'),
    ]
    type_maison = models.CharField(max_length=100, choices=TYPE_MAISON_CHOICES)
    
    #def __str__(self):
     #   return self.type_maison
    prix = models.DecimalField(max_digits=10, decimal_places=0)
    localisation = models.CharField(max_length=255)
    nombre_de_chambre = models.IntegerField(blank=True, null=True)
    nombre_de_douche = models.IntegerField(blank=True, null=True)
    nombre_de_cuisine = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='media/', null=True, blank=False,)
    photo_douche = models.ImageField(upload_to='media/douches/', null=True, blank=True)
    photo_chambre = models.ImageField(upload_to='media/chambres/', null=True, blank=True)
    photo_cuisine = models.ImageField(upload_to='media/cuisines/', null=True, blank=True)
    photo_salon = models.ImageField(upload_to='media/salons/', null=True, blank=True)
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='libre')
    preciser_la_localisation_de_votre_maison = models.CharField(max_length=255,null= True, blank=True)
    is_deleted = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Maison à {self.localisation}"

    class Meta:
        permissions = [
            ("can_create_maison", "Peut créer des maisons"),
            ("can_modify_maison", "Peut modifier des maisons"),
            ("can_publish_maison", "Peut publier des maisons"),
        ]


class Profile(models.Model):
    user = models.OneToOneField(Proprietaire, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images', blank=True, null=True)
    username = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.user.username

from django.db import models

class Commentaire(models.Model):
    nom = models.CharField(max_length=100)
    commentaire = models.TextField()

    def __str__(self):
        return f"Commentaire de {self.nom}"


from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from django.urls import reverse
from django.utils.html import format_html


class Facture(models.Model):
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE)
    date_debut = models.DateField(default=timezone.now)
    date_fin = models.DateField()
    prix_paye = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation = models.DateTimeField(auto_now_add=True)

    @property
    def temps_restant(self):
        if self.date_fin and timezone.now().date():
            jours_restants = (self.date_fin - timezone.now().date()).days
            return f"{jours_restants} jour(s)"
        return "Date non définie"

    def afficher_status(self):
        if self.date_fin and timezone.now().date():
            jours_restants = (self.date_fin - timezone.now().date()).days
            if jours_restants > 3:
                couleur = 'green'
            elif 1 <= jours_restants <= 3:
                couleur = 'yellow'
            else:
                couleur = 'red'
            return format_html('<span style="color: {};">●</span>', couleur)
        return format_html('<span style="color: grey;">●</span>')

    def aller_au_proprietaire(self):
        url = reverse('admin:home_proprietaire_change', args=[self.proprietaire.pk])  # Assurez-vous que 'home' est le nom de votre application
        return format_html('<a href="{}">Aller</a>', url)

    aller_au_proprietaire.short_description = 'Aller au propriétaire'

    def __str__(self):
        return f"Facture de {self.proprietaire.nom} du {self.date_debut} au {self.date_fin}"

from django.contrib.auth.models import User
from .models import Proprietaire, Maison

def set_default_proprietaire(sender, instance, **kwargs):
    if not instance.proprietaire:
        # Récupérer ou créer l'instance de Proprietaire correspondant à l'utilisateur par défaut
        user = User.objects.get(username='default_user')  # Assurez-vous que cet utilisateur existe
        default_proprietaire, created = Proprietaire.objects.get_or_create(
            nom=user.username,
            defaults={'sexe': 'homme', 'ville': 'Douala', 'mot_de_passe': user.password}
        )
        instance.proprietaire = default_proprietaire

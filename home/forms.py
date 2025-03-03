from django import forms
from .models import Maison, Profile
from django.contrib.auth.forms import UserCreationForm

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'photo']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'required': False})
        }

from django import forms
from .models import Maison
# ce ci est reservé pour la maison
class MaisonForm(forms.ModelForm):
    class Meta:
        model = Maison
        fields = ('type_maison', 'prix', 'localisation', 'photo', 'photo_douche', 'photo_chambre', 'photo_cuisine', 'photo_salon', 'nombre_de_chambre', 'nombre_de_douche', 'nombre_de_cuisine','status','preciser_la_localisation_de_votre_maison')

    def __init__(self, *args, **kwargs):
        super(MaisonForm, self).__init__(*args, **kwargs)
        self.fields['prix'].initial = 0
        self.fields['localisation'].initial = ''
        self.fields['nombre_de_chambre'].initial = 0
        self.fields['nombre_de_douche'].initial = 0
        self.fields['nombre_de_cuisine'].initial = 0

    def __init__(self, *args, **kwargs):
        super(MaisonForm, self).__init__(*args, **kwargs)
        self.fields['prix'].initial = 0
        self.fields['localisation'].initial = ''
        self.fields['nombre_de_chambre'].initial = 0
        self.fields['nombre_de_douche'].initial = 0
        self.fields['nombre_de_cuisine'].initial = 0



from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from .models import Proprietaire

class ProprietaireForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}), label="Mot de passe", required=False)
    mot_de_passe_confirme = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe'}), label="Confirmer le mot de passe", required=False)
    magic_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe magique'}), label="Mot de passe magique", required=True)

    class Meta:
        model = Proprietaire
        fields = ("nom", "sexe", "ville", "mot_de_passe", "mot_de_passe_confirme", "image", "telephone", "whatsapp", "magic_password")
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom'}),
            'sexe': forms.Select(attrs={'placeholder': 'Sexe'}),
            'ville': forms.TextInput(attrs={'placeholder': 'Ville'}),
            'image': forms.ClearableFileInput(),
            'telephone': forms.TextInput(),
            'whatsapp': forms.TextInput(attrs={'placeholder': 'Lien WhatsApp'})
        }

    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get("mot_de_passe")
        mot_de_passe_confirme = cleaned_data.get("mot_de_passe_confirme")

        if mot_de_passe and mot_de_passe_confirme:
            if mot_de_passe != mot_de_passe_confirme:
                raise ValidationError("Les mots de passe ne correspondent pas.")

            # Vérifiez si un autre propriétaire utilise le même mot de passe
            for proprietaire in Proprietaire.objects.all():
                if check_password(mot_de_passe, proprietaire.mot_de_passe):
                    raise ValidationError("Ce mot de passe est déjà utilisé. Veuillez en choisir un autre.")
        
            # Hash the password before returning the cleaned data
            cleaned_data['mot_de_passe'] = make_password(mot_de_passe)
        else:
            # Ne pas modifier le mot de passe s'il n'est pas renseigné
            cleaned_data.pop('mot_de_passe', None)
            cleaned_data.pop('mot_de_passe_confirme', None)

        return cleaned_data



from django import forms
from django.contrib.auth.hashers import check_password
from .models import Proprietaire

from django import forms
from django.contrib.auth.hashers import check_password
from .models import Proprietaire

class RecuperationForm(forms.Form):
    nom = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nom'}))
    mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))

    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get("nom")
        mot_de_passe = cleaned_data.get("mot_de_passe")

        if not Proprietaire.objects.filter(nom=nom).exists():
            raise forms.ValidationError("Ce nom n'est pas inscrit dans notre plateforme.")

        utilisateurs = Proprietaire.objects.filter(nom=nom)
        mot_de_passe_correct = False
        for utilisateur in utilisateurs:
            if check_password(mot_de_passe, utilisateur.mot_de_passe):
                mot_de_passe_correct = True
                break

        if not mot_de_passe_correct:
            raise forms.ValidationError("Le mot de passe est incorrect.")

        return cleaned_data

from django import forms
from .models import Maison

class MaisonUpdateForm(forms.ModelForm):
    class Meta:
        model = Maison
        fields = ('type_maison', 'prix', 'localisation', 'photo', 'photo_douche', 'photo_chambre', 'photo_cuisine', 'photo_salon', 'nombre_de_chambre', 'nombre_de_douche', 'nombre_de_cuisine', 'status')

from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control border-0 py-3', 'placeholder': 'Rechercher'}))
    type_maison = forms.ChoiceField(choices=[
        ('', 'Type de propriété'),
        ('VILLA', 'Villa'),
        ('APPARTEMENT', 'Appartement'),
        ('MAISON SIMPLE', 'Maison simple'),
        ('MAISON DE LUXE', 'Maison de luxe'),
        ('MAISON DE CAMPAGNE', 'Maison de campagne'),
        ('STUDIO', 'Studio'),
        ('CHAMBRE MODERNE','Chambre moderne'),
        ('CHAMBRE','Chambre'),


    ], required=False, widget=forms.Select(attrs={'class': 'form-select border-0 py-3'}))
    localisation = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control border-0 py-3', 'placeholder': 'Localisation'}))
    prix_min = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control border-0 py-3', 'placeholder': 'Prix minimum'}))
    prix_max = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control border-0 py-3', 'placeholder': 'Prix maximum'}))

from django import forms
from .models import Commentaire

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['nom', 'commentaire']

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MaisonForm, ProfileUpdateForm, ProprietaireForm, RecuperationForm
from .models import Maison, Profile, Proprietaire
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

MAGIC_PASSWORD = 'admin123'  # Mot de passe magique prédéfini

def register(request):
    submitted = False
    if request.method == 'POST':
        form = ProprietaireForm(request.POST, request.FILES)
        if form.is_valid():
            magic_password = form.cleaned_data.get('magic_password')
            if magic_password == MAGIC_PASSWORD:
                form.save()
                messages.success(request, "Votre compte a été créé avec succès!")
                return redirect('register')
            else:
                messages.error(request, "Mot de passe magique incorrect, veuillez contacter les administrateurs.")
                return redirect('register')
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer.")
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ProprietaireForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'register.html', {'form': form, 'submitted': submitted})



def home(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirige vers la page d'accueil après la déconnexion

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Proprietaire
from .forms import ProprietaireForm

def proprietaire_edit(request, proprietaire_id):
    proprietaire = get_object_or_404(Proprietaire, pk=proprietaire_id)
    if request.method == 'POST':
        form = ProprietaireForm(request.POST, request.FILES, instance=proprietaire)
        if form.is_valid():
            form.save()
            messages.success(request, "Informations mises à jour avec succès !")
            return redirect('proprietaire_detail', proprietaire_id=proprietaire.id)
    else:
        form = ProprietaireForm(instance=proprietaire)
    return render(request, 'proprietaire_edit.html', {'form': form, 'proprietaire': proprietaire})


@login_required
def maison_edit(request, maison_id):
    maison = get_object_or_404(Maison, id=maison_id, proprietaire=request.user)
    if request.method == 'POST':
        form = MaisonForm(request.POST, request.FILES, instance=maison)
        if form.is_valid():
            form.save()
            return redirect('maison_list')
    else:
        form = MaisonForm(instance=maison)
    return render(request, 'maison_form.html', {'form': form})

@login_required
def maison_create(request):
    if request.method == 'POST':
        form = MaisonForm(request.POST, request.FILES)
        if form.is_valid():
            maison = form.save(commit=False)
            maison.proprietaire = request.user  # Assigner le propriétaire actuel
            maison.save()
            return redirect('maison_list')
    else:
        form = MaisonForm()
    return render(request, 'maison_form.html', {'form': form})

@login_required
def maison_delete(request, maison_id):
    maison = get_object_or_404(Maison, id=maison_id, proprietaire=request.user)
    if request.method == 'POST':
        maison.delete()
        return redirect('maison_list')
    return render(request, 'maison_confirm_delete.html', {'maison': maison})

def about(request):
    return render(request, 'about.html')

def guide(request):
    return render(request, 'guide.html')

def property_list(request):
    maisons = Maison.objects.all()
    return render(request, 'maison_list.html', {'maisons': maisons})

def contact(request):
    return render(request, 'contact.html')

def profile(request):
    return render(request, 'profile.html')

def connexion(request):
    return render(request, 'connexion.html')

def create_missing_profiles(request):
    for user in User.objects.all():
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)
    return redirect('home')  # Redirige vers la page d'accueil après la création des profils
from django.shortcuts import render
from .models import Maison

def index(request):
    maisons = Maison.objects.filter(is_published=True, proprietaire__is_deleted=False)[:9]  # Filtrer les maisons par les propriétaires non masqués
    return render(request, 'index.html', {'maisons': maisons})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Proprietaire
from .forms import RecuperationForm

def recuperation_view(request):
    if request.method == 'POST':
        form = RecuperationForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            mot_de_passe = form.cleaned_data['mot_de_passe']

            # Authentification de l'utilisateur
            utilisateurs = Proprietaire.objects.filter(nom=nom)
            utilisateur_authentifie = None
            for utilisateur in utilisateurs:
                if check_password(mot_de_passe, utilisateur.mot_de_passe):
                    utilisateur_authentifie = utilisateur
                    break

            if utilisateur_authentifie:
                # Vérifiez si le propriétaire est masqué
                if utilisateur_authentifie.is_deleted:
                    messages.error(request, "Cher proprietaire, votre compte a été suspendu, merci de bien vouloir contacter un adminnistrateur!.")
                    return redirect('recuperation')

                # Connexion de l'utilisateur manuelle
                request.session['proprietaire_id'] = utilisateur_authentifie.id
                messages.success(request, "Connexion réussie !")
                return redirect('maison_list')  # Redirection vers maison_list après connexion
            else:
                messages.error(request, "Le mot de passe est incorrect.")
        else:
            messages.error(request, "Les informations saisies sont incorrectes. Veuillez réessayer.")
    else:
        form = RecuperationForm()
    return render(request, 'recuperation.html', {'form': form})





from django.shortcuts import render
from .models import Maison

def maison_list(request):
    if request.user.is_authenticated:
        proprietaire = request.user.proprietaire
    else:
        proprietaire = None
    maisons = Maison.objects.filter(proprietaire=request.user)  # Filtrer les maisons par le propriétaire connecté
    return render(request, 'maison_list.html', {'maisons': maisons, 'proprietaire': proprietaire})


# views.py
from django.shortcuts import render, redirect
from .forms import MaisonForm
from .models import Maison
from django.contrib.auth.decorators import login_required

def publier_maison(request):
    #if request.method == 'POST':
       # form = MaisonForm(request.POST, request.FILES)
       # if form.is_valid():
          #  maison = form.save(commit=False)
            if request.user.is_authenticated:
               form = MaisonForm(request.POST or None, request.FILES or None)
               if request.method == 'POST'and form.is_valid():
                   maison = form.save(commit=False)
                   maison.proprietaire = request.user.proprietaire
                   maison.save()
                   return redirect('maison_list')
               return render(request, 'maison_form.html', {'form': form})
            else:
                    return redirect('index')



from django.shortcuts import render
from .models import Maison

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Maison, Proprietaire

def maison_list(request):
    try:
        proprietaire_id = request.session.get('proprietaire_id')
        if proprietaire_id:
            maisons = Maison.objects.filter(proprietaire_id=proprietaire_id, is_deleted=False)  # Filtrer les maisons par le propriétaire connecté et vérifier s'ils ne sont pas supprimés
            proprietaire = Proprietaire.objects.get(id=proprietaire_id)
            published_properties_count = maisons.filter(is_published=True).count()
            context = {
                'maisons': maisons,
                'proprietaire': proprietaire,
                'published_properties_count': published_properties_count,
            }
            return render(request, 'maison_list.html', context)
        else:
            messages.error(request, "Vous devez être connecté pour accéder à cette page.")
            return redirect('login')  # Redirige vers la page de connexion
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('recuperation')


from django.shortcuts import get_object_or_404
from .models import Maison, Proprietaire

def publier_maison(request, maison_id):
    maison = get_object_or_404(Maison, id=maison_id)
    if not maison.proprietaire.is_deleted:
        maison.is_published = True
        maison.save()
        messages.success(request, "Maison publiée avec succès !")
    else:
        messages.error(request, "Le propriétaire de cette maison est masqué. La maison ne peut pas être publiée.")
    return redirect('maison_list')





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MaisonForm
from .models import Proprietaire


def maison_form(request):
    if request.method == 'POST':
        form = MaisonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('maison_list')  # Redirige vers une page de liste ou de succès
    else:
        form = MaisonForm()
    return render(request, 'maison_form.html', {'form': form})

from django.http import JsonResponse

def debug_user_info(request):
    user_info = {
        "is_authenticated": request.user.is_authenticated,
        "username": request.user.username,
        "proprietaire_id": getattr(request.user, 'proprietaire', None).id if request.user.is_authenticated else None
    }
    return JsonResponse(user_info)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Maison, Proprietaire
from .forms import MaisonForm

def maison_create(request):
    try:
        proprietaire_id = request.session.get('proprietaire_id')
        proprietaire = get_object_or_404(Proprietaire, id=proprietaire_id)

        # Vérifiez si le propriétaire est masqué
        if proprietaire.is_deleted:
            messages.error(request, "Vous ne pouvez pas créer une maison car votre compte est masqué.")
            return redirect('maison_list')

        if request.method == 'POST':
            form = MaisonForm(request.POST, request.FILES)
            if form.is_valid():
                maison = form.save(commit=False)
                maison.proprietaire = proprietaire
                maison.save()
                messages.success(request, "Maison créée avec succès !")
                return redirect('maison_list')
        else:
            form = MaisonForm()
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('recuperation')

    return render(request, 'maison_form.html', {'form': form})


from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Proprietaire

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                proprietaire = Proprietaire.objects.get(user=user)
                if proprietaire.is_deleted:
                    messages.error(request, "Votre compte est masqué. Veuillez contacter l'administrateur.")
                    return render(request, 'login.html', {'error': 'Votre compte est masqué. Veuillez contacter l\'administrateur.'})

                login(request, user)
                next_url = request.POST.get('next', 'maison_list')
                print(f"Redirecting to: {next_url}")  # Debugging
                return redirect(next_url)
            except Proprietaire.DoesNotExist:
                messages.error(request, "Propriétaire non trouvé.")
                return render(request, 'login.html', {'error': 'Propriétaire non trouvé'})
        else:
            print("Authentication failed")  # Debugging
            return render(request, 'login.html', {'error': 'Nom d\'utilisateur ou mot de passe incorrect'})
    else:
        next_url = request.GET.get('next', '')
        print(f"Next URL: {next_url}")  # Debugging
        return render(request, 'login.html', {'next': next_url})





from django.shortcuts import render, get_object_or_404
from .models import Maison
from .forms import MaisonUpdateForm
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from .forms import MaisonUpdateForm
from .models import Maison

def maison_update(request, maison_id):
    maison = get_object_or_404(Maison, id=maison_id)
    if request.method == 'POST':
        form = MaisonUpdateForm(request.POST, request.FILES, instance=maison)
        if form.is_valid():
            form.save()
            messages.success(request, "Maison mise à jour avec succès !")
            return redirect('maison_list')
    else:
        form = MaisonUpdateForm(instance=maison)
    return render(request, 'maison_update.html', {'form': form, 'maison': maison})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Maison

def maison_delete(request, maison_id):
    maison = get_object_or_404(Maison, id=maison_id)
    if request.method == 'POST':
        maison.delete()
        messages.success(request, "Maison supprimée avec succès !")
    return redirect('maison_list')



def debug_user_info(request):
    user_info = {
        "is_authenticated": request.user.is_authenticated,
        "username": request.user.username,
        "proprietaire_id": getattr(request.user, 'proprietaire', None).id if request.user.is_authenticated else None
    }
    return JsonResponse(user_info)

from django.shortcuts import render
from .models import Maison

def maison_affiche(request):
    maisons = Maison.objects.filter(is_published=True,is_deleted=False, proprietaire__is_deleted=False)
    return render(request, 'maison_affiche.html', {'maisons': maisons})

from django.shortcuts import render, get_object_or_404
from .models import Maison

def maison_detail(request, maison_id):
    maison = get_object_or_404(Maison, id=maison_id)
    return render(request, 'maison_detail.html', {'maison': maison})

from django.shortcuts import render
from .models import Maison

def maison_search(request):
    query = request.GET.get('q')
    type_propriete = request.GET.get('type')
    location = request.GET.get('location')
    
    maisons = Maison.objects.filter(is_deleted=False, proprietaire__is_deleted=False)
    
    if query:
        maisons = maisons.filter(description__icontains=query)
    if type_propriete:
        maisons = maisons.filter(type_maison=type_propriete)
    if location:
        maisons = maisons.filter(localisation__icontains=location)
    
    return render(request, 'maison_search.html', {'maisons': maisons})

from django.shortcuts import render
from .models import Maison
from .forms import SearchForm

def search(request):
    form = SearchForm(request.GET or None)    
    maisons = Maison.objects.filter(is_deleted=False, proprietaire__is_deleted=False)

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        type_maison = form.cleaned_data.get('type_maison')
        localisation = form.cleaned_data.get('localisation')
        prix_min = form.cleaned_data.get('prix_min')
        prix_max = form.cleaned_data.get('prix_max')

        if keyword:
            maisons = maisons.filter(localisation__icontains=keyword)
        if type_maison:
            maisons = maisons.filter(type_maison=type_maison)
        if localisation:
            maisons = maisons.filter(localisation__icontains=localisation)
        if prix_min is not None:
            maisons = maisons.filter(prix__gte=prix_min)
        if prix_max is not None:
            maisons = maisons.filter(prix__lte=prix_max)

    return render(request, 'search_results.html', {'form': form, 'maisons': maisons})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Commentaire
from .forms import CommentaireForm

def laisser_commentaire(request):
    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Merci pour votre commentaire !")
            return redirect('laisser_commentaire')
    else:
        form = CommentaireForm()
    return render(request, 'commentaire.html', {'form': form})

from django.shortcuts import render
from .models import Commentaire

def afficher_commentaires(request):
    commentaires = Commentaire.objects.all()
    return render(request, 'afficher_commentaires.html', {'commentaires': commentaires})


from django.shortcuts import render
from .models import Proprietaire

def proprietaires_connectes(request):
    proprietaires = Proprietaire.objects.filter(is_active=True).order_by('-last_login')
    return render(request, 'proprietaire.html', {'proprietaires': proprietaires})

from django.shortcuts import render, get_object_or_404
from .models import Proprietaire

def proprietaire_detail(request, proprietaire_id):
    proprietaire = get_object_or_404(Proprietaire, pk=proprietaire_id)
    context = {
        'proprietaire': proprietaire,
    }
    return render(request, 'proprietaire_detail.html', context)


def politique(request):
    return render(request, 'politique.html')
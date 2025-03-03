from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('proprietaire/<int:proprietaire_id>/', views.proprietaire_detail, name='proprietaire_detail'),
    path('proprietaires-connectes/', views.proprietaires_connectes, name='proprietaires_connectes'),
    path('laisser_commentaire/', views.laisser_commentaire, name='laisser_commentaire'),
    path('afficher_commentaires/', views.afficher_commentaires, name='afficher_commentaires'),
    path('search/', views.search, name='search'),
    path('maison/search/', views.maison_search, name='maison_search'),
    path('maison/<int:maison_id>/', views.maison_detail, name='maison_detail'),  # URL pour les détails de la maison
    path('maison_affiche/', views.maison_affiche, name='maison_affiche'),
    path('maisons/<int:maison_id>/update/', views.maison_update, name='maison_update'),
    path('maisons/<int:maison_id>/publier/', views.publier_maison, name='publier_maison'),
    path('maison_form', views.maison_form, name='maison_form'),
    path('recuperation/', views.recuperation_view, name='recuperation'),
    path('maison_list/', views.maison_list, name='maison_list'),
    path('maison/<int:maison_id>/delete/', views.maison_delete, name='maison_delete'),  # URL pour la suppression
    path('', views.index, name='index'),
    path('maison/create/', views.maison_create, name='ajouter_maison'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('proprietaire/<int:proprietaire_id>/edit/', views.proprietaire_edit, name='proprietaire_edit'),
    path('create_profiles/', views.create_missing_profiles, name='create_profiles'),
    path('about/', views.about, name='about'),
    path('property_list/', views.property_list, name='property_list'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('maison/edit/<int:maison_id>/', views.maison_edit, name='maison_edit'),
    path('maison/delete/<int:maison_id>/', views.maison_delete, name='maison_delete'),
    path('debug_user/', views.debug_user_info, name='debug_user'),
    path('login/', views.login_view, name='login'), 
    path('guide/', views.guide, name='guide'),
    path('politique/', views.politique, name='politique')
    # autres URL...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

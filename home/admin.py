from django.contrib import admin
from django.contrib.auth.models import User
from .models import Proprietaire, Maison

def masquer_proprietaires(modeladmin, request, queryset):
    queryset.update(is_deleted=True)
    Maison.objects.filter(proprietaire__in=queryset).update(is_deleted=True)
    for proprietaire in queryset:
        if proprietaire.user:
            proprietaire.user.is_active = False
            proprietaire.user.save()

def restaurer_proprietaires(modeladmin, request, queryset):
    queryset.update(is_deleted=False)
    Maison.objects.filter(proprietaire__in=queryset).update(is_deleted=False)
    for proprietaire in queryset:
        if proprietaire.user:
            proprietaire.user.is_active = True
            proprietaire.user.save()

masquer_proprietaires.short_description = "Masquer les propriétaires sélectionnés"
restaurer_proprietaires.short_description = "Restaurer les propriétaires sélectionnés"

class ProprietaireAdmin(admin.ModelAdmin):
    list_display = ['nom', 'is_deleted']
    actions = [masquer_proprietaires, restaurer_proprietaires]

admin.site.register(Proprietaire, ProprietaireAdmin)
admin.site.register(Maison)

from .models import Facture
from django.utils.html import format_html

class FactureAdmin(admin.ModelAdmin):
    list_display = ['proprietaire', 'date_debut', 'date_fin', 'temps_restant', 'prix_paye', 'afficher_status', 'aller_au_proprietaire']
    search_fields = ['proprietaire__nom', 'date_debut', 'date_fin']
    list_filter = ['date_debut', 'date_fin']
    readonly_fields = ['afficher_status']

admin.site.register(Facture, FactureAdmin)


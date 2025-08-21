from django.contrib import admin
from .models import User, Gateau, Commande, ArticleEvenement, ParametresLivraison

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_patron', 'is_collaborateur', 'is_staff', 'is_superuser')

@admin.register(Gateau)
class GateauAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'prix', 'disponible')
    search_fields = ('nom',)
    list_filter = ('type',)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('client_nom', 'gateau', 'date_livraison', 'status', 'livraison', 'prix_total')
    search_fields = ('client_nom', 'client_telephone')
    list_filter = ('status', 'livraison', 'date_livraison')

@admin.register(ArticleEvenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_publication')
    search_fields = ('titre',)

@admin.register(ParametresLivraison)
class ParametreLivraisonAdmin(admin.ModelAdmin):
    list_display = ('prix_livraison',)

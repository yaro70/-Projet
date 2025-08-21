"""
URL configuration for patisserie_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from boutique.views import (
    login_view, logout_view, create_commande, public_gateaux, 
    test_permissions, mark_whatsapp_sent, send_whatsapp_validation, 
    mark_commande_terminee, create_collaborateur, get_statistiques, 
    create_article, get_notifications, mark_notification_read, 
    mark_all_notifications_read, galerie_photos, ajouter_photo_galerie,
    modifier_photo_galerie, supprimer_photo_galerie
)
from rest_framework.routers import DefaultRouter
from boutique.views import *
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('gateaux', GateauViewSet)
router.register('commandes', CommandeViewSet)
router.register('evenements', ArticleEvenementViewSet)
router.register('parametres', ParametresLivraisonViewSet)
router.register('utilisateurs', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('api/', include(router.urls)),
    path('api/login/', login_view),
    path('api/logout/', logout_view),
    path('api/create-commande/', create_commande),
    path('api/public/gateaux/', public_gateaux),
    path('api/test-permissions/', test_permissions),
    path('api/commandes/<int:commande_id>/mark-whatsapp/', mark_whatsapp_sent),
    path('api/commandes/<int:commande_id>/send-whatsapp-validation/', send_whatsapp_validation),
    path('api/commandes/<int:commande_id>/mark-terminee/', mark_commande_terminee),
    path('api/create-collaborateur/', create_collaborateur),
    path('api/statistiques/', get_statistiques),
    path('api/create-article/', create_article),
    # URLs pour les notifications
    path('api/notifications/', get_notifications),
    path('api/notifications/mark-read/', mark_notification_read),
    path('api/notifications/mark-all-read/', mark_all_notifications_read),
    # URLs pour la galerie photos
    path('api/galerie/', galerie_photos),
    path('api/galerie/ajouter/', ajouter_photo_galerie),
    path('api/galerie/<int:photo_id>/modifier/', modifier_photo_galerie),
    path('api/galerie/<int:photo_id>/supprimer/', supprimer_photo_galerie),
]

# Ajouter les URLs pour les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from rest_framework import viewsets, permissions
from .models import Gateau, Commande, ArticleEvenement, ParametresLivraison, User, Notification, GaleriePhoto
from .serializers import GateauSerializer, CommandeSerializer, ArticleEvenementSerializer, ParametresLivraisonSerializer, UserSerializer, GaleriePhotoSerializer
from .qr_service import QRCodeService

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

from django.core.cache import cache

class GateauViewSet(viewsets.ModelViewSet):
    queryset = Gateau.objects.all()
    serializer_class = GateauSerializer
    permission_classes = [permissions.AllowAny]

class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.select_related('gateau').all()
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Pour les collaborateurs, afficher seulement les commandes non terminées
        if self.request.user.is_collaborateur:
            return Commande.objects.select_related('gateau').exclude(status='terminee')
        # Pour les patrons, afficher toutes les commandes
        elif self.request.user.is_patron:
            return Commande.objects.select_related('gateau').all()
        # Pour les autres utilisateurs, afficher seulement leurs commandes
        else:
            return Commande.objects.select_related('gateau').filter(client_nom=self.request.user.username)
    
    def update(self, request, *args, **kwargs):
        """Override update pour générer automatiquement le QR code"""
        instance = self.get_object()
        old_status = instance.status
        
        print(f"🔍 CommandeViewSet.update - Commande {instance.id}")
        print(f"🔍 Ancien statut: {old_status}")
        print(f"🔍 Nouveau statut: {request.data.get('status', 'non spécifié')}")
        
        # Appeler la méthode parent
        response = super().update(request, *args, **kwargs)
        
        # Rafraîchir l'instance depuis la base de données
        instance.refresh_from_db()
        
        print(f"🔍 Statut après update: {instance.status}")
        print(f"🔍 QR code déjà généré: {instance.qr_code_generated}")
        
        # Si le statut est passé à 'validee' et qu'aucun QR code n'a été généré
        if (instance.status == 'validee' and 
            old_status != 'validee' and 
            not instance.qr_code_generated):
            
            print("🔍 Génération automatique du QR code...")
            
            # Générer le QR code
            qr_code = QRCodeService.generate_qr_code(instance)
            if qr_code:
                instance.qr_code = qr_code
                instance.qr_code_generated = True
                instance.save()
                
                print(f"✅ QR code généré avec succès pour la commande {instance.id}")
                
                # Envoyer notification WebSocket
                self.send_qr_code_notification(instance)
            else:
                print("❌ Erreur lors de la génération du QR code")
        else:
            print("🔍 QR code non généré - conditions non remplies")
        
        return response
    
    def send_qr_code_notification(self, commande):
        """Envoyer une notification WebSocket pour le QR code généré"""
        try:
            channel_layer = get_channel_layer()
            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    'patron_notifications',
                    {
                        'type': 'qr_code_generated',
                        'message': f'QR code généré pour la commande #{commande.id}',
                        'commande_id': commande.id,
                        'client_nom': commande.client_nom,
                        'qr_code_url': QRCodeService.get_qr_code_image_url(commande.qr_code)
                    }
                )
        except Exception as e:
            print(f"Erreur lors de l'envoi de la notification QR code: {e}")

class ArticleEvenementViewSet(viewsets.ModelViewSet):
    queryset = ArticleEvenement.objects.all()
    serializer_class = ArticleEvenementSerializer
    permission_classes = [permissions.AllowAny]

class ParametresLivraisonViewSet(viewsets.ModelViewSet):
    queryset = ParametresLivraison.objects.all()
    serializer_class = ParametresLivraisonSerializer
    permission_classes = [permissions.AllowAny]
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': f'Erreur lors de la mise à jour: {str(e)}'}, status=400)
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': f'Erreur lors de la création: {str(e)}'}, status=400)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class GaleriePhotoViewSet(viewsets.ModelViewSet):
    """ViewSet pour la galerie photos"""
    queryset = GaleriePhoto.objects.filter(visible=True)
    serializer_class = GaleriePhotoSerializer
    permission_classes = [permissions.AllowAny]  # Public pour la consultation
    
    def get_queryset(self):
        """Filtrer par catégorie si spécifiée"""
        queryset = GaleriePhoto.objects.filter(visible=True)
        categorie = self.request.query_params.get('categorie', None)
        if categorie:
            queryset = queryset.filter(categorie=categorie)
        return queryset.order_by('-ordre_affichage', '-date_realisation')


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Nouvelle vue de login simplifiée"""
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Nom d\'utilisateur et mot de passe requis'}, status=400)

        # Authentification simple
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)

        if user and user.is_active:
            # Créer ou récupérer le token
            from rest_framework.authtoken.models import Token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'is_patron': getattr(user, 'is_patron', False),
                'is_collaborateur': getattr(user, 'is_collaborateur', False)
            })
        else:
            return Response({'error': 'Identifiants invalides'}, status=401)
            
    except Exception as e:
        return Response({'error': f'Erreur serveur: {str(e)}'}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    try:
        # Supprimer le token de l'utilisateur
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
        return Response({'message': 'Déconnexion réussie'})
    except Exception as e:
        return Response({'error': 'Erreur lors de la déconnexion'}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def test_permissions(request):
    """Vue de test pour diagnostiquer les permissions"""
    print(f"🔍 test_permissions appelée")
    print(f"🔍 Méthode: {request.method}")
    print(f"🔍 Utilisateur: {request.user}")
    print(f"🔍 Authentifié: {request.user.is_authenticated}")
    print(f"🔍 Headers: {dict(request.headers)}")
    
    return Response({
        'message': 'Test permissions OK',
        'user': str(request.user),
        'authenticated': request.user.is_authenticated,
        'method': request.method
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def create_commande(request):
    """Créer une nouvelle commande"""
    print(f"🔍 create_commande appelée - Méthode: {request.method}")
    print(f"🔍 Utilisateur authentifié: {request.user.is_authenticated}")
    print(f"🔍 Permissions: {request.user.get_all_permissions()}")
    print(f"🔍 Headers: {dict(request.headers)}")
    
    # Forcer l'authentification anonyme
    from django.contrib.auth.models import AnonymousUser
    if isinstance(request.user, AnonymousUser):
        print("🔍 Utilisateur anonyme détecté - OK pour les commandes publiques")
    
    try:
        data = request.data
        print(f"🔍 Données reçues: {data}")
        
        gateau_id = data.get('gateau') or data.get('gateau_id')
        client_nom = data.get('client_nom')
        client_telephone = data.get('client_telephone')
        texte_sur_gateau = data.get('texte_sur_gateau', '')
        date_livraison = data.get('date_livraison')
        livraison = data.get('livraison', False)
        
        # Récupérer le gâteau
        gateau = Gateau.objects.get(id=gateau_id)
        
        # Calculer le prix total (addition correcte)
        from decimal import Decimal
        prix_total = Decimal(str(gateau.prix))
        if livraison:
            try:
                parametres = ParametresLivraison.objects.first()
                if parametres:
                    prix_total += Decimal(str(parametres.prix_livraison))
                    print(f"Calcul: {gateau.prix} + {parametres.prix_livraison} = {prix_total}")
            except Exception as e:
                print(f"Erreur lors du calcul des frais de livraison: {e}")
        
        # Créer la commande
        commande = Commande.objects.create(
            gateau=gateau,
            client_nom=client_nom,
            client_telephone=client_telephone,
            texte_sur_gateau=texte_sur_gateau,
            date_livraison=date_livraison,
            livraison=livraison,
            prix_total=prix_total
        )
        
        # Envoyer notification aux patrons
        order_data = {
            'id': commande.id,
            'client_nom': commande.client_nom,
            'gateau_nom': commande.gateau.nom,
            'prix_total': str(commande.prix_total),
            'date_livraison': str(commande.date_livraison)
        }
        
        send_patron_notification(
            'new_order',
            '🎂 Nouvelle commande reçue',
            f'Nouvelle commande de {client_nom} pour {gateau.nom} - {prix_total} FCFA',
            order_data
        )
        
        return Response({
            'message': 'Commande créée avec succès',
            'commande_id': commande.id,
            'prix_total': str(prix_total)
        }, status=201)
        
    except Gateau.DoesNotExist:
        return Response({'error': 'Gâteau non trouvé'}, status=404)
    except Exception as e:
        return Response({'error': f'Erreur lors de la création de la commande: {str(e)}'}, status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_gateaux(request):
    """Vue publique pour récupérer les gâteaux avec cache"""
    try:
        # Cache simple pour 10 minutes
        cache_key = 'public_gateaux'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        gateaux = Gateau.objects.all()
        data = []
        for gateau in gateaux:
            # Construire l'URL complète de l'image
            image_url = None
            if gateau.image:
                image_url = f"http://localhost:8000{gateau.image.url}"
            
            data.append({
                'id': gateau.id,
                'nom': gateau.nom,
                'description': gateau.description,
                'prix': str(gateau.prix),
                'type': gateau.type,
                'image': image_url
            })
        
        response_data = {'gateaux': data}
        
        # Mettre en cache pour 10 minutes
        cache.set(cache_key, response_data, 600)
        
        return Response(response_data)
        
    except Exception as e:
        return Response({'error': f'Erreur lors de la récupération des gâteaux: {str(e)}'}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_whatsapp_sent(request, commande_id):
    """Marquer le message WhatsApp comme envoyé pour une commande"""
    try:
        commande = Commande.objects.get(id=commande_id)
        commande.mark_whatsapp_sent()
        return Response({
            'message': 'Message WhatsApp marqué comme envoyé',
            'commande_id': commande.id,
            'whatsapp_envoye': commande.whatsapp_envoye,
            'date_whatsapp': commande.date_whatsapp
        })
    except Commande.DoesNotExist:
        return Response({'error': 'Commande non trouvée'}, status=404)
    except Exception as e:
        return Response({'error': f'Erreur: {str(e)}'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_whatsapp_validation(request, commande_id):
    """Envoyer automatiquement un message WhatsApp de validation au client"""
    try:
        commande = Commande.objects.get(id=commande_id)
        
        # Générer le message de validation
        message = f"""🎉 Bonjour {commande.client_nom}!

Votre commande a été validée avec succès!

📋 Détails de votre commande:
🎂 Gâteau: {commande.gateau.nom}
💰 Prix: {commande.gateau.prix} FCFA
{commande.livraison and f'🚚 Livraison: {commande.prix_total - commande.gateau.prix} FCFA' or ''}
💰 Total: {commande.prix_total} FCFA
📅 Date de {'livraison' if commande.livraison else 'récupération'}: {commande.date_livraison.strftime('%d/%m/%Y à %H:%M')}
{commande.texte_sur_gateau and f'📝 Texte: {commande.texte_sur_gateau}' or ''}

✅ Votre commande est en cours de préparation.
{'📞 Nous vous contacterons bientôt pour confirmer la livraison.' if commande.livraison else '🏪 Vous pourrez venir le récupérer à notre boutique.'}

Merci de votre confiance! 🎂"""
        
        # Créer le lien WhatsApp avec le numéro du client
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        whatsapp_link = f"https://wa.me/{commande.client_telephone}?text={encoded_message}"
        
        # Marquer comme envoyé
        commande.mark_whatsapp_sent()
        
        return Response({
            'message': 'Message WhatsApp de validation envoyé',
            'commande_id': commande.id,
            'whatsapp_link': whatsapp_link,
            'client_telephone': commande.client_telephone,
            'whatsapp_envoye': commande.whatsapp_envoye,
            'date_whatsapp': commande.date_whatsapp
        })
        
    except Commande.DoesNotExist:
        return Response({'error': 'Commande non trouvée'}, status=404)
    except Exception as e:
        return Response({'error': f'Erreur: {str(e)}'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_commande_terminee(request, commande_id):
    """Marquer une commande comme terminée et envoyer un message WhatsApp approprié"""
    try:
        commande = Commande.objects.get(id=commande_id)
        
        # Marquer comme terminée
        commande.mark_commande_terminee()
        
        # Générer le lien WhatsApp approprié
        whatsapp_link = commande.get_terminaison_whatsapp_link()
        
        return Response({
            'message': 'Commande marquée comme terminée',
            'commande_id': commande.id,
            'whatsapp_link': whatsapp_link,
            'client_telephone': commande.client_telephone,
            'livraison': commande.livraison,
            'whatsapp_envoye': commande.whatsapp_envoye,
            'date_whatsapp': commande.date_whatsapp
        })
        
    except Commande.DoesNotExist:
        return Response({'error': 'Commande non trouvée'}, status=404)
    except Exception as e:
        return Response({'error': f'Erreur: {str(e)}'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_collaborateur(request):
    """Créer un nouveau collaborateur (seulement pour les patrons)"""
    try:
        # Vérifier que l'utilisateur est un patron
        if not request.user.is_patron:
            return Response({'error': 'Accès refusé. Seuls les patrons peuvent créer des collaborateurs.'}, status=403)
        
        # Récupérer les données du formulaire
        nom = request.data.get('nom')
        prenom = request.data.get('prenom')
        telephone = request.data.get('telephone')
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Validation des données
        if not all([nom, prenom, telephone, username, password]):
            return Response({'error': 'Tous les champs sont requis'}, status=400)
        
        # Vérifier si le username existe déjà
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Ce nom d\'utilisateur existe déjà'}, status=400)
        
        # Créer l'utilisateur collaborateur
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=prenom,
            last_name=nom,
            is_collaborateur=True,
            is_patron=False
        )
        
        # Créer un token pour le nouvel utilisateur
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Collaborateur créé avec succès',
            'collaborateur': {
                'id': user.id,
                'username': user.username,
                'nom': user.last_name,
                'prenom': user.first_name,
                'telephone': telephone,
                'is_collaborateur': user.is_collaborateur,
                'token': token.key
            }
        })
        
    except Exception as e:
        return Response({'error': f'Erreur lors de la création du collaborateur: {str(e)}'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_statistiques(request):
    """Récupérer les statistiques des commandes et chiffres d'affaires (seulement pour les patrons)"""
    try:
        # Vérifier que l'utilisateur est un patron
        if not request.user.is_patron:
            return Response({'error': 'Accès refusé. Seuls les patrons peuvent voir les statistiques.'}, status=403)
        
        from datetime import datetime, timedelta
        from django.db.models import Sum, Count
        from django.utils import timezone
        
        now = timezone.now()
        
        # Calculer les dates pour chaque période
        def get_period_stats(days_ago):
            start_date = now - timedelta(days=days_ago)
            return Commande.objects.filter(
                date_commande__gte=start_date,
                date_commande__lte=now
            )
        
        # Statistiques par période
        stats = {
            'semaine': {
                'commandes': get_period_stats(7).count(),
                'chiffre_affaires': float(get_period_stats(7).aggregate(total=Sum('prix_total'))['total'] or 0)
            },
            'mois': {
                'commandes': get_period_stats(30).count(),
                'chiffre_affaires': float(get_period_stats(30).aggregate(total=Sum('prix_total'))['total'] or 0)
            },
            'trimestre': {
                'commandes': get_period_stats(90).count(),
                'chiffre_affaires': float(get_period_stats(90).aggregate(total=Sum('prix_total'))['total'] or 0)
            },
            'annee': {
                'commandes': get_period_stats(365).count(),
                'chiffre_affaires': float(get_period_stats(365).aggregate(total=Sum('prix_total'))['total'] or 0)
            }
        }
        
        # Statistiques par statut
        status_stats = {
            'en_attente': Commande.objects.filter(status='en_attente').count(),
            'validee': Commande.objects.filter(status='validee').count(),
            'refusee': Commande.objects.filter(status='refusee').count(),
            'terminee': Commande.objects.filter(status='terminee').count()
        }
        
        # Top 5 des gâteaux les plus commandés
        top_gateaux = Commande.objects.values('gateau__nom').annotate(
            total_commandes=Count('id')
        ).order_by('-total_commandes')[:5]
        
        return Response({
            'statistiques_periode': stats,
            'statistiques_status': status_stats,
            'top_gateaux': list(top_gateaux),
            'periode_calcul': {
                'semaine': '7 derniers jours',
                'mois': '30 derniers jours',
                'trimestre': '90 derniers jours',
                'annee': '365 derniers jours'
            }
        })
        
    except Exception as e:
        return Response({'error': f'Erreur lors du calcul des statistiques: {str(e)}'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_article(request):
    """Créer un nouvel article d'événement (seulement pour les patrons)"""
    try:
        # Vérifier que l'utilisateur est un patron
        if not request.user.is_patron:
            return Response({'error': 'Accès refusé. Seuls les patrons peuvent créer des articles.'}, status=403)
        
        # Récupérer les données du formulaire
        titre = request.data.get('titre')
        description = request.data.get('description')
        image = request.FILES.get('image')
        
        # Validation des données
        if not titre or not description:
            return Response({'error': 'Titre et description sont requis'}, status=400)
        
        # Créer l'article
        article = ArticleEvenement.objects.create(
            titre=titre,
            description=description,
            image=image
        )
        
        return Response({
            'message': 'Article créé avec succès',
            'article': {
                'id': article.id,
                'titre': article.titre,
                'description': article.description,
                'image': article.image.url if article.image else None,
                'date_publication': article.date_publication
            }
        })
        
    except Exception as e:
        return Response({'error': f'Erreur lors de la création de l\'article: {str(e)}'}, status=400)

def send_notification(recipient, notification_type, title, message, data=None):
    """Envoyer une notification à un utilisateur"""
    try:
        # Créer la notification en base
        notification = Notification.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            data=data or {}
        )
        
        # Envoyer via WebSocket si l'utilisateur est connecté
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{recipient.id}",
            {
                'type': 'notification_message',
                'notification': notification.to_dict()
            }
        )
        
        return notification
    except Exception as e:
        print(f"Erreur lors de l'envoi de notification: {e}")
        return None

def send_patron_notification(notification_type, title, message, data=None):
    """Envoyer une notification à tous les patrons"""
    try:
        patrons = User.objects.filter(is_patron=True)
        
        for patron in patrons:
            send_notification(patron, notification_type, title, message, data)
        
        # Notification WebSocket pour les patrons connectés
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "patron_notifications",
            {
                'type': 'new_order_message',
                'order': data
            }
        )
        
    except Exception as e:
        print(f"Erreur lors de l'envoi de notification patron: {e}")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    """Récupérer les notifications de l'utilisateur"""
    try:
        notifications = Notification.objects.filter(
            recipient=request.user
        ).order_by('-created_at')[:20]
        
        return Response({
            'notifications': [notification.to_dict() for notification in notifications],
            'unread_count': Notification.objects.filter(
                recipient=request.user,
                is_read=False
            ).count()
        })
        
    except Exception as e:
        return Response({'error': f'Erreur lors de la récupération des notifications: {str(e)}'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request):
    """Marquer une notification comme lue"""
    try:
        notification_id = request.data.get('notification_id')
        
        if not notification_id:
            return Response({'error': 'ID de notification requis'}, status=400)
        
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        notification.mark_as_read()
        
        return Response({'message': 'Notification marquée comme lue'})
        
    except Notification.DoesNotExist:
        return Response({'error': 'Notification non trouvée'}, status=404)
    except Exception as e:
        return Response({'error': f'Erreur: {str(e)}'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_notifications_read(request):
    """Marquer toutes les notifications comme lues"""
    try:
        Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)
        
        return Response({'message': 'Toutes les notifications marquées comme lues'})
        
    except Exception as e:
        return Response({'error': f'Erreur: {str(e)}'}, status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def galerie_photos(request):
    """Vue publique pour récupérer toutes les photos de galerie avec cache"""
    try:
        # Cache simple pour 5 minutes
        cache_key = 'galerie_photos'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        categorie = request.GET.get('categorie')
        queryset = GaleriePhoto.objects.filter(visible=True)
        
        if categorie:
            queryset = queryset.filter(categorie=categorie)
        
        # Optimisation : limiter le nombre de photos
        photos = queryset.order_by('-ordre_affichage', '-date_realisation')[:50]
        data = [photo.to_dict() for photo in photos]
        
        response_data = {
            'photos': data,
            'total': len(data),
            'categories': dict(GaleriePhoto.CATEGORIE_CHOICES)
        }
        
        # Mettre en cache pour 5 minutes
        cache.set(cache_key, response_data, 300)
        
        return Response(response_data)
        
    except Exception as e:
        return Response({'error': f'Erreur lors de la récupération de la galerie: {str(e)}'}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ajouter_photo_galerie(request):
    """Ajouter une nouvelle photo à la galerie (seulement pour les patrons)"""
    try:
        if not request.user.is_patron:
            return Response({'error': 'Accès refusé. Seuls les patrons peuvent ajouter des photos.'}, status=403)
        
        titre = request.data.get('titre')
        description = request.data.get('description', '')
        categorie = request.data.get('categorie', 'autre')
        date_realisation = request.data.get('date_realisation')
        image = request.FILES.get('image')
        ordre_affichage = request.data.get('ordre_affichage', 0)
        
        if not all([titre, date_realisation, image]):
            return Response({'error': 'Titre, date de réalisation et image sont requis'}, status=400)
        
        photo = GaleriePhoto.objects.create(
            titre=titre,
            description=description,
            categorie=categorie,
            date_realisation=date_realisation,
            image=image,
            ordre_affichage=ordre_affichage
        )
        
        return Response({
            'message': 'Photo ajoutée avec succès',
            'photo': photo.to_dict()
        })
        
    except Exception as e:
        return Response({'error': f'Erreur lors de l\'ajout de la photo: {str(e)}'}, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifier_photo_galerie(request, photo_id):
    """Modifier une photo de galerie (seulement pour les patrons)"""
    try:
        if not request.user.is_patron:
            return Response({'error': 'Accès refusé. Seuls les patrons peuvent modifier les photos.'}, status=403)
        
        photo = GaleriePhoto.objects.get(id=photo_id)
        
        # Mettre à jour les champs
        if 'titre' in request.data:
            photo.titre = request.data['titre']
        if 'description' in request.data:
            photo.description = request.data['description']
        if 'categorie' in request.data:
            photo.categorie = request.data['categorie']
        if 'date_realisation' in request.data:
            photo.date_realisation = request.data['date_realisation']
        if 'ordre_affichage' in request.data:
            photo.ordre_affichage = request.data['ordre_affichage']
        if 'visible' in request.data:
            photo.visible = request.data['visible']
        if 'image' in request.FILES:
            photo.image = request.FILES['image']
        
        photo.save()
        
        return Response({
            'message': 'Photo modifiée avec succès',
            'photo': photo.to_dict()
        })
        
    except GaleriePhoto.DoesNotExist:
        return Response({'error': 'Photo non trouvée'}, status=404)
    except Exception as e:
        return Response({'error': f'Erreur lors de la modification: {str(e)}'}, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def supprimer_photo_galerie(request, photo_id):
    """Supprimer une photo de galerie (seulement pour les patrons)"""
    try:
        if not request.user.is_patron:
            return Response({'error': 'Accès refusé. Seuls les patrons peuvent supprimer les photos.'}, status=403)
        
        photo = GaleriePhoto.objects.get(id=photo_id)
        photo.delete()
        
        return Response({'message': 'Photo supprimée avec succès'})
        
    except GaleriePhoto.DoesNotExist:
        return Response({'error': 'Photo non trouvée'}, status=404)
    except Exception as e:
        return Response({'error': f'Erreur lors de la suppression: {str(e)}'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def scan_qr_code(request):
    """Scanner un QR code et retourner les informations de la commande"""
    try:
        qr_data = request.data.get('qr_data')
        if not qr_data:
            return Response({'error': 'Données QR code manquantes'}, status=400)
        
        # Décoder les données du QR code
        decoded_data = QRCodeService.decode_qr_code(qr_data)
        if not decoded_data:
            return Response({'error': 'QR code invalide'}, status=400)
        
        # Vérifier que c'est bien une commande de pâtisserie
        if decoded_data.get('type') != 'commande_patisserie':
            return Response({'error': 'QR code non reconnu'}, status=400)
        
        # Récupérer la commande
        commande_id = decoded_data.get('commande_id')
        try:
            commande = Commande.objects.select_related('gateau').get(id=commande_id)
        except Commande.DoesNotExist:
            return Response({'error': 'Commande non trouvée'}, status=404)
        
        # Vérifier que la commande est validée
        if commande.status != 'validee':
            return Response({'error': 'Commande non validée'}, status=400)
        
        # Retourner les informations de la commande
        return Response({
            'success': True,
            'commande': {
                'id': commande.id,
                'client_nom': commande.client_nom,
                'client_telephone': commande.client_telephone,
                'gateau_nom': commande.gateau.nom,
                'gateau_description': commande.gateau.description,
                'prix_total': str(commande.prix_total),
                'date_livraison': commande.date_livraison.isoformat(),
                'livraison': commande.livraison,
                'texte_sur_gateau': commande.texte_sur_gateau,
                'status': commande.status,
                'date_commande': commande.date_commande.isoformat(),
                'qr_code_generated': commande.qr_code_generated
            },
            'qr_data': decoded_data
        })
        
    except Exception as e:
        return Response({'error': f'Erreur lors du scan: {str(e)}'}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_qr_code(request, commande_id):
    """Récupérer le QR code d'une commande"""
    try:
        commande = Commande.objects.get(id=commande_id)
        
        # Vérifier que l'utilisateur a le droit de voir cette commande
        if not (request.user.is_patron or request.user.is_collaborateur):
            return Response({'error': 'Accès refusé'}, status=403)
        
        if not commande.qr_code_generated:
            return Response({'error': 'QR code non généré'}, status=404)
        
        return Response({
            'qr_code_url': QRCodeService.get_qr_code_image_url(commande.qr_code),
            'commande_id': commande.id,
            'client_nom': commande.client_nom
        })
        
    except Commande.DoesNotExist:
        return Response({'error': 'Commande non trouvée'}, status=404)
    except Exception as e:
        return Response({'error': f'Erreur: {str(e)}'}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_qr_code(request, commande_id):
    """Générer manuellement le QR code pour une commande"""
    try:
        commande = Commande.objects.get(id=commande_id)
        
        # Vérifier que l'utilisateur a le droit de générer le QR code
        if not (request.user.is_patron or request.user.is_collaborateur):
            return Response({'error': 'Accès refusé'}, status=403)
        
        # Vérifier que la commande est validée
        if commande.status != 'validee':
            return Response({'error': 'La commande doit être validée pour générer un QR code'}, status=400)
        
        # Générer le QR code
        qr_code = QRCodeService.generate_qr_code(commande)
        if qr_code:
            commande.qr_code = qr_code
            commande.qr_code_generated = True
            commande.save()
            
            return Response({
                'message': 'QR code généré avec succès',
                'qr_code_url': QRCodeService.get_qr_code_image_url(commande.qr_code),
                'commande_id': commande.id,
                'client_nom': commande.client_nom
            })
        else:
            return Response({'error': 'Erreur lors de la génération du QR code'}, status=500)
        
    except Commande.DoesNotExist:
        return Response({'error': 'Commande non trouvée'}, status=404)
    except Exception as e:
        return Response({'error': f'Erreur: {str(e)}'}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_qr_code_to_client(request, commande_id):
    """Envoyer le QR code au client par WhatsApp"""
    try:
        commande = Commande.objects.get(id=commande_id)
        
        # Vérifier que l'utilisateur a le droit d'envoyer le QR code
        if not (request.user.is_patron or request.user.is_collaborateur):
            return Response({'error': 'Accès refusé'}, status=403)
        
        if not commande.qr_code_generated:
            return Response({'error': 'QR code non généré'}, status=404)
        
        # Générer le message WhatsApp avec le QR code
        message = f"""🎉 Bonjour {commande.client_nom}!

Votre commande a été validée avec succès!

📋 Détails de votre commande:
🎂 Gâteau: {commande.gateau.nom}
💰 Prix: {commande.prix_total} FCFA
📅 Date de {'livraison' if commande.livraison else 'récupération'}: {commande.date_livraison.strftime('%d/%m/%Y à %H:%M')}

📱 Votre QR code de récupération:
Présentez ce QR code lors de la récupération de votre commande.

Merci pour votre confiance! 🍰"""
        
        # Générer le lien WhatsApp
        whatsapp_link = f"https://wa.me/{commande.client_telephone.replace('+', '').replace(' ', '')}?text={message}"
        
        # Marquer comme envoyé
        commande.qr_code_sent = True
        commande.save()
        
        return Response({
            'message': 'QR code envoyé au client',
            'whatsapp_link': whatsapp_link,
            'client_telephone': commande.client_telephone,
            'qr_code_sent': commande.qr_code_sent
        })
        
    except Commande.DoesNotExist:
        return Response({'error': 'Commande non trouvée'}, status=404)
    except Exception as e:
        return Response({'error': f'Erreur: {str(e)}'}, status=500)


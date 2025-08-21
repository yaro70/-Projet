from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_patron = models.BooleanField(default=False)
    is_collaborateur = models.BooleanField(default=False)

    #Ajoutez ces lignes pour résoudre les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="boutique_user_groups",  # Nom personnalisé pour la relation inverse
        related_query_name="boutique_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="boutique_user_permissions",  # Nom personnalisé pour la relation inverse
        related_query_name="boutique_user",
    )

    def __str__(self):
        return self.username

# Rendre Pillow optionnel
try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

class Gateau(models.Model):
    TYPE_CHOICES = [
        ('anniversaire', 'Anniversaire'),
        ('mariage', 'Mariage'),
        ('autre', 'Autre'),
    ]
    
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='gateaux/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        # Vérifier si Pillow est disponible avant de traiter l'image
        if self.image and HAS_PILLOW:
            try:
                img = Image.open(self.image)
                # Redimensionner l'image si nécessaire
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except Exception as e:
                print(f"Erreur lors du traitement de l'image: {e}")
        super().save(*args, **kwargs)

class Commande(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('validee', 'Validée'),
        ('refusee', 'Refusée'),
        ('terminee', 'Terminée'),
    ]
    
    client_nom = models.CharField(max_length=100)
    client_telephone = models.CharField(max_length=20)
    gateau = models.ForeignKey(Gateau, on_delete=models.CASCADE)
    texte_sur_gateau = models.CharField(max_length=100, blank=True)
    date_livraison = models.DateTimeField()
    livraison = models.BooleanField(default=False)
    prix_total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    date_commande = models.DateTimeField(auto_now_add=True)
    whatsapp_envoye = models.BooleanField(default=False)
    date_whatsapp = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Commande #{self.id} - {self.client_nom}"
    
    def get_whatsapp_link(self):
        """Génère le lien WhatsApp pour cette commande"""
        message = f"""Bonjour! J'ai passé une commande de gâteau:

🎂 Gâteau: {self.gateau.nom}
💰 Prix: {self.gateau.prix} FCFA
{self.livraison and f'🚚 Livraison: {self.prix_total - self.gateau.prix} FCFA' or ''}
💰 Total: {self.prix_total} FCFA

👤 Nom: {self.client_nom}
📞 Téléphone: {self.client_telephone}
📅 Date de livraison: {self.date_livraison.strftime('%d/%m/%Y à %H:%M')}
{self.texte_sur_gateau and f'📝 Texte: {self.texte_sur_gateau}' or ''}

J'ai effectué le dépôt et je souhaite envoyer la capture d'écran."""
        
        # Encoder le message pour l'URL
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        return f"https://wa.me/2250123456789?text={encoded_message}"
    
    def mark_whatsapp_sent(self):
        """Marque le message WhatsApp comme envoyé"""
        from django.utils import timezone
        self.whatsapp_envoye = True
        self.date_whatsapp = timezone.now()
        self.save()
    
    def mark_commande_terminee(self):
        """Marque la commande comme terminée et envoie un message WhatsApp approprié"""
        from django.utils import timezone
        self.status = 'terminee'
        self.whatsapp_envoye = True
        self.date_whatsapp = timezone.now()
        self.save()
    
    def get_terminaison_whatsapp_link(self):
        """Génère le lien WhatsApp pour annoncer la fin de préparation"""
        if self.livraison:
            message = f"""🎉 Bonjour {self.client_nom}!

Votre gâteau est maintenant terminé et sera bientôt livré!

📋 Détails de votre commande:
🎂 Gâteau: {self.gateau.nom}
💰 Prix: {self.gateau.prix} FCFA
🚚 Livraison: {self.prix_total - self.gateau.prix} FCFA
💰 Total: {self.prix_total} FCFA
📅 Date de livraison: {self.date_livraison.strftime('%d/%m/%Y à %H:%M')}
{self.texte_sur_gateau and f'📝 Texte: {self.texte_sur_gateau}' or ''}

🚚 Notre livreur vous contactera bientôt pour la livraison.
⏰ Merci de rester disponible pour la réception.

Bon appétit! 🎂"""
        else:
            message = f"""🎉 Bonjour {self.client_nom}!

Votre gâteau est maintenant terminé et prêt à être récupéré!

📋 Détails de votre commande:
🎂 Gâteau: {self.gateau.nom}
💰 Prix: {self.gateau.prix} FCFA
💰 Total: {self.prix_total} FCFA
📅 Date de livraison: {self.date_livraison.strftime('%d/%m/%Y à %H:%M')}
{self.texte_sur_gateau and f'📝 Texte: {self.texte_sur_gateau}' or ''}

🏪 Vous pouvez maintenant passer le récupérer à notre boutique.
⏰ Merci de venir dans les plus brefs délais.

Bon appétit! 🎂"""
        
        # Encoder le message pour l'URL
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        return f"https://wa.me/{self.client_telephone}?text={encoded_message}"

class ArticleEvenement(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_evenement = models.DateTimeField()
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        # Vérifier si Pillow est disponible avant de traiter l'image
        if self.image and HAS_PILLOW:
            try:
                img = Image.open(self.image)
                # Redimensionner l'image si nécessaire
                if img.height > 400 or img.width > 400:
                    output_size = (400, 400)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except Exception as e:
                print(f"Erreur lors du traitement de l'image: {e}")
        super().save(*args, **kwargs)

class ParametresLivraison(models.Model):
    prix_livraison = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"Prix livraison: {self.prix_livraison}€"

class Notification(models.Model):
    """Modèle pour les notifications en temps réel"""
    NOTIFICATION_TYPES = [
        ('new_order', 'Nouvelle commande'),
        ('order_validated', 'Commande validée'),
        ('order_finished', 'Commande terminée'),
        ('system_message', 'Message système'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)  # Données supplémentaires (ID commande, etc.)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} - {self.recipient.username} - {self.title}"
    
    def mark_as_read(self):
        """Marquer la notification comme lue"""
        self.is_read = True
        self.save()
    
    def to_dict(self):
        """Convertir en dictionnaire pour l'API"""
        return {
            'id': self.id,
            'type': self.notification_type,
            'title': self.title,
            'message': self.message,
            'data': self.data,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat(),
        }

class GaleriePhoto(models.Model):
    """Modèle pour la galerie photos des réalisations"""
    CATEGORIE_CHOICES = [
        ('gateaux', 'Gâteaux'),
        ('evenements', 'Événements'),
        ('ateliers', 'Ateliers'),
        ('autres', 'Autres'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='galerie/')
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default='gateaux')
    date_realisation = models.DateField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    ordre_affichage = models.IntegerField(default=0)  # Pour l'ordre d'affichage
    visible = models.BooleanField(default=True)  # Pour masquer certaines photos
    
    class Meta:
        ordering = ['-ordre_affichage', '-date_realisation']
        verbose_name = "Photo de galerie"
        verbose_name_plural = "Photos de galerie"
    
    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        # Vérifier si Pillow est disponible avant de traiter l'image
        if self.image and HAS_PILLOW:
            try:
                img = Image.open(self.image)
                # Redimensionner l'image si nécessaire
                if img.height > 500 or img.width > 500:
                    output_size = (500, 500)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except Exception as e:
                print(f"Erreur lors du traitement de l'image: {e}")
        super().save(*args, **kwargs)

    def to_dict(self):
        """Convertir en dictionnaire pour l'API"""
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'image_url': self.image.url if self.image else None,
            'categorie': self.categorie,
            'categorie_display': self.get_categorie_display(),
            'date_realisation': self.date_realisation.isoformat(),
            'date_ajout': self.date_ajout.isoformat(),
            'ordre_affichage': self.ordre_affichage,
            'visible': self.visible,
        }
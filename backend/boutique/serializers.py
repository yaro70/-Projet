from rest_framework import serializers
from .models import Gateau, Commande, ArticleEvenement, ParametresLivraison, User, GaleriePhoto

class GateauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateau
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    gateau_nom = serializers.CharField(source='gateau.nom', read_only=True)
    whatsapp_link = serializers.SerializerMethodField()
    
    class Meta:
        model = Commande
        fields = '__all__'
    
    def get_whatsapp_link(self, obj):
        return obj.get_whatsapp_link()

class ArticleEvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleEvenement
        fields = '__all__'

class ParametresLivraisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametresLivraison
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_patron', 'is_collaborateur']

class GaleriePhotoSerializer(serializers.ModelSerializer):
    """Serializer pour les photos de galerie"""
    categorie_display = serializers.CharField(source='get_categorie_display', read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = GaleriePhoto
        fields = [
            'id', 'titre', 'description', 'image', 'image_url',
            'categorie', 'categorie_display', 'date_realisation',
            'date_ajout', 'ordre_affichage', 'visible'
        ]
    
    def get_image_url(self, obj):
        """Retourner l'URL de l'image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                # Utiliser notre nouvelle route /api/images/ au lieu de /media/
                return request.build_absolute_uri(f'/api/images{obj.image.url}')
            return f'/api/images{obj.image.url}'
        return None
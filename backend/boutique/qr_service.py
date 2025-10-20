import qrcode
import io
import base64
from django.conf import settings
import json

class QRCodeService:
    """Service pour la génération et gestion des QR codes"""
    
    @staticmethod
    def generate_qr_code(commande):
        """Génère un QR code pour une commande"""
        try:
            # Données à encoder dans le QR code
            qr_data = {
                'commande_id': commande.id,
                'client_nom': commande.client_nom,
                'client_telephone': commande.client_telephone,
                'gateau_nom': commande.gateau.nom,
                'prix_total': str(commande.prix_total),
                'date_livraison': commande.date_livraison.isoformat(),
                'status': commande.status,
                'type': 'commande_patisserie'
            }
            
            # Convertir en JSON
            qr_json = json.dumps(qr_data, ensure_ascii=False)
            
            # Générer le QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_json)
            qr.make(fit=True)
            
            # Créer l'image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convertir en base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return qr_base64
            
        except Exception as e:
            print(f"Erreur lors de la génération du QR code: {e}")
            return None
    
    @staticmethod
    def decode_qr_code(qr_data):
        """Décode les données d'un QR code"""
        try:
            if isinstance(qr_data, str):
                # Si c'est déjà du JSON
                if qr_data.startswith('{'):
                    return json.loads(qr_data)
                else:
                    # Si c'est du base64, décoder d'abord
                    decoded = base64.b64decode(qr_data).decode('utf-8')
                    return json.loads(decoded)
            return None
        except Exception as e:
            print(f"Erreur lors du décodage du QR code: {e}")
            return None
    
    @staticmethod
    def get_qr_code_image_url(qr_base64):
        """Retourne l'URL de l'image QR code pour l'affichage"""
        if qr_base64:
            return f"data:image/png;base64,{qr_base64}"
        return None

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import User, Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    """Consumer pour les notifications en temps réel"""
    
    async def connect(self):
        """Connexion WebSocket"""
        self.user = self.scope["user"]
        
        if self.user.is_anonymous:
            await self.close()
            return
        
        # Groupe spécifique à l'utilisateur
        self.room_group_name = f"notifications_{self.user.id}"
        
        # Rejoindre le groupe
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Envoyer les notifications non lues existantes
        unread_notifications = await self.get_unread_notifications()
        if unread_notifications:
            await self.send(text_data=json.dumps({
                'type': 'initial_notifications',
                'notifications': unread_notifications
            }))
    
    async def disconnect(self, close_code):
        """Déconnexion WebSocket"""
        # Quitter le groupe
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Réception de messages du client"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'mark_read':
                notification_id = data.get('notification_id')
                await self.mark_notification_read(notification_id)
                
            elif message_type == 'mark_all_read':
                await self.mark_all_notifications_read()
                
        except json.JSONDecodeError:
            pass
    
    async def notification_message(self, event):
        """Envoyer une notification au client"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': event['notification']
        }))
    
    async def notification_update(self, event):
        """Mettre à jour les notifications (marquer comme lues)"""
        await self.send(text_data=json.dumps({
            'type': 'notification_update',
            'notification_id': event['notification_id'],
            'is_read': event['is_read']
        }))
    
    @database_sync_to_async
    def get_unread_notifications(self):
        """Récupérer les notifications non lues"""
        notifications = Notification.objects.filter(
            recipient=self.user,
            is_read=False
        )[:10]  # Limiter à 10 notifications
        
        return [notification.to_dict() for notification in notifications]
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Marquer une notification comme lue"""
        try:
            notification = Notification.objects.get(
                id=notification_id,
                recipient=self.user
            )
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False
    
    @database_sync_to_async
    def mark_all_notifications_read(self):
        """Marquer toutes les notifications comme lues"""
        Notification.objects.filter(
            recipient=self.user,
            is_read=False
        ).update(is_read=True)
        return True

class PatronConsumer(AsyncWebsocketConsumer):
    """Consumer spécifique pour les patrons (nouvelles commandes)"""
    
    async def connect(self):
        """Connexion WebSocket pour patrons"""
        self.user = self.scope["user"]
        
        if self.user.is_anonymous or not self.user.is_patron:
            await self.close()
            return
        
        # Groupe pour tous les patrons
        self.room_group_name = "patron_notifications"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """Déconnexion WebSocket"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def new_order_message(self, event):
        """Nouvelle commande reçue"""
        await self.send(text_data=json.dumps({
            'type': 'new_order',
            'order': event['order']
        }))
    
    async def order_status_update(self, event):
        """Mise à jour du statut d'une commande"""
        await self.send(text_data=json.dumps({
            'type': 'order_status_update',
            'order_id': event['order_id'],
            'status': event['status'],
            'message': event['message']
        })) 
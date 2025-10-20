// Configuration pour l'API et WebSocket
const config = {
  // URL de l'API backend - Force l'URL Render en production
  API_URL: process.env.NODE_ENV === 'production' 
    ? 'https://patisserie-backend.onrender.com'
    : (process.env.REACT_APP_API_URL || 'http://localhost:8000'),
  
  // URL WebSocket pour les notifications en temps réel
  WS_URL: process.env.NODE_ENV === 'production'
    ? 'wss://patisserie-backend.onrender.com'
    : (process.env.REACT_APP_WS_URL || 'ws://localhost:8000'),
  
  // Configuration des endpoints
  ENDPOINTS: {
    LOGIN: '/api/login/',
    LOGOUT: '/api/logout/',
    GATEAUX: '/api/gateaux/',
    PUBLIC_GATEAUX: '/api/public/gateaux/',
    COMMANDES: '/api/commandes/',
    CREATE_COMMANDE: '/api/create-commande/',
    PARAMETRES: '/api/parametres/',
    NOTIFICATIONS: '/api/notifications/',
    GALERIE: '/api/galerie/',
    CREATE_COLLABORATEUR: '/api/create-collaborateur/',
    STATISTIQUES: '/api/statistiques/',
    CREATE_ARTICLE: '/api/create-article/',
    MARK_TERMINEE: '/api/commandes/{id}/mark-terminee/',
  },
  
  // Configuration WhatsApp
  WHATSAPP: {
    DEFAULT_NUMBER: '2250123456789', // À remplacer par le vrai numéro
  },
  
  // Configuration des notifications
  NOTIFICATIONS: {
    TYPES: {
      NEW_ORDER: 'new_order',
      ORDER_VALIDATED: 'order_validated',
      ORDER_FINISHED: 'order_finished',
      SYSTEM_MESSAGE: 'system_message',
    },
  },
};

export default config;





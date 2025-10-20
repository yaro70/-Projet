import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Box, Typography, Button, Grid, Card, CardContent,
  TextField, Dialog, DialogTitle, DialogContent, DialogActions,
  Drawer, List, ListItem, ListItemText, Toolbar, Alert,
  Chip
} from '@mui/material';
import { useAuth } from './AuthContext';
import NotificationSystem from './NotificationSystem';
import Galerie from './Galerie';
import QRCodeScanner from './QRCodeScanner';

const drawerWidth = 240;

const DashboardPatron = () => {
  const { logout } = useAuth();
  const [section, setSection] = useState('commandes'); // 👈 section active
  const [gateaux, setGateaux] = useState([]);
  const [commandes, setCommandes] = useState([]);
  const [livraisonPrix, setLivraisonPrix] = useState('');
  const [numeroPatron, setNumeroPatron] = useState('');
  const [newGateau, setNewGateau] = useState({ nom: '', description: '', prix: '', type: '', image: null });
  const [dialogOpen, setDialogOpen] = useState(false);
  
  // États pour la création de collaborateurs
  const [newCollaborateur, setNewCollaborateur] = useState({
    nom: '',
    prenom: '',
    telephone: '',
    username: '',
    password: ''
  });
  const [collaborateurDialogOpen, setCollaborateurDialogOpen] = useState(false);
  
  // États pour les statistiques
  const [statistiques, setStatistiques] = useState(null);
  const [loadingStats, setLoadingStats] = useState(false);
  
  // États pour les articles
  const [articles, setArticles] = useState([]);
  const [newArticle, setNewArticle] = useState({
    titre: '',
    description: '',
    image: null
  });
  const [articleDialogOpen, setArticleDialogOpen] = useState(false);
  
  // État pour le scanner QR code
  const [qrScannerOpen, setQrScannerOpen] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    if (section === 'statistiques') {
      fetchStatistiques();
    }
  }, [section]);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { 'Authorization': `Token ${token}` } : {};
      
      const gRes = await axios.get('https://patisserie-backend.onrender.com/api/gateaux/');
      const cRes = await axios.get('https://patisserie-backend.onrender.com/api/commandes/', { headers });
      const lRes = await axios.get('https://patisserie-backend.onrender.com/api/parametres/');
      const aRes = await axios.get('https://patisserie-backend.onrender.com/api/evenements/');
      
      setGateaux(gRes.data);
      setCommandes(cRes.data);
      setArticles(aRes.data);
      if (lRes.data.length) {
        setLivraisonPrix(lRes.data[0].prix_livraison);
        setNumeroPatron(lRes.data[0].numero_patron || '');
      }
    } catch (err) {
      console.error('Erreur lors du chargement des données:', err);
    }
  };

  const fetchStatistiques = async () => {
    try {
      setLoadingStats(true);
      const token = localStorage.getItem('token');
      const headers = token ? { 'Authorization': `Token ${token}` } : {};
      
      const response = await axios.get('https://patisserie-backend.onrender.com/api/statistiques/', { headers });
      setStatistiques(response.data);
    } catch (err) {
      console.error('Erreur lors du chargement des statistiques:', err);
      alert('Erreur lors du chargement des statistiques');
    } finally {
      setLoadingStats(false);
    }
  };

  const updateCommandeStatus = async (id, status) => {
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { 'Authorization': `Token ${token}` } : {};
      
      await axios.patch(`https://patisserie-backend.onrender.com/api/commandes/${id}/`, { status }, { headers });
      
      // Si la commande est validée, envoyer automatiquement le message WhatsApp
      if (status === 'validee') {
        try {
          const whatsappResponse = await axios.post(
            `https://patisserie-backend.onrender.com/api/commandes/${id}/send-whatsapp-validation/`, 
            {}, 
            { headers }
          );
          
          if (whatsappResponse.data.whatsapp_link) {
            // Ouvrir automatiquement WhatsApp
            window.open(whatsappResponse.data.whatsapp_link, '_blank');
            alert(`Commande validée! Message WhatsApp envoyé au client ${whatsappResponse.data.client_telephone}`);
          }
        } catch (whatsappErr) {
          console.error('Erreur lors de l\'envoi WhatsApp:', whatsappErr);
          alert('Commande validée mais erreur lors de l\'envoi WhatsApp');
        }
      } else {
        alert(`Commande ${status === 'refusee' ? 'refusée' : 'terminée'} avec succès!`);
      }
      
      fetchData();
    } catch (err) {
      console.error('Erreur lors de la mise à jour du statut:', err);
      alert('Erreur lors de la mise à jour du statut');
    }
  };

  const generateAndSendQRCode = async (commandeId) => {
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { 'Authorization': `Token ${token}` } : {};
      
      // 1. Générer le QR code
      const generateResponse = await axios.post(
        `https://patisserie-backend.onrender.com/api/qr-code/${commandeId}/generate/`,
        {},
        { headers }
      );
      
      if (generateResponse.data.qr_code_url) {
        console.log(`✅ QR code généré pour la commande ${commandeId}`);
        
        // 2. Envoyer le QR code sur WhatsApp
        const sendResponse = await axios.post(
          `https://patisserie-backend.onrender.com/api/qr-code/${commandeId}/send/`,
          {},
          { headers }
        );
        
        if (sendResponse.data.whatsapp_link) {
          // Ouvrir automatiquement WhatsApp
          window.open(sendResponse.data.whatsapp_link, '_blank');
          alert(`QR code généré et envoyé sur WhatsApp au client ${sendResponse.data.client_telephone}!`);
        } else {
          alert(`QR code généré mais erreur lors de l'envoi WhatsApp`);
        }
        
        fetchData(); // Rafraîchir les données
      }
    } catch (error) {
      console.error('Erreur génération/envoi QR code:', error);
      alert(`Erreur: ${error.response?.data?.error || error.message}`);
    }
  };

  const handleGâteauChange = (e) => {
    const { name, value, files } = e.target;
    setNewGateau((prev) => ({ ...prev, [name]: files ? files[0] : value }));
  };

  const createGâteau = async () => {
    const formData = new FormData();
    for (let key in newGateau) {
      formData.append(key, newGateau[key]);
    }
    try {
      await axios.post('https://patisserie-backend.onrender.com/api/gateaux/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setDialogOpen(false);
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const saveLivraisonPrix = async () => {
    try {
      // Convertir le prix en nombre
      const prix = parseFloat(livraisonPrix);
      if (isNaN(prix) || prix < 0) {
        alert('Veuillez entrer un prix valide');
        return;
      }

      // Valider le numéro de téléphone
      if (!numeroPatron || numeroPatron.trim() === '') {
        alert('Veuillez entrer un numéro de téléphone valide');
        return;
      }

      const res = await axios.get('https://patisserie-backend.onrender.com/api/parametres/');
      if (res.data.length) {
        await axios.patch(`https://patisserie-backend.onrender.com/api/parametres/${res.data[0].id}/`, { 
          prix_livraison: prix.toString(),
          numero_patron: numeroPatron.trim()
        });
      } else {
        await axios.post(`https://patisserie-backend.onrender.com/api/parametres/`, { 
          prix_livraison: prix.toString(),
          numero_patron: numeroPatron.trim()
        });
      }
      // Rafraîchir les données après sauvegarde
      fetchData();
      alert('Paramètres enregistrés avec succès!');
    } catch (err) {
      console.error('Erreur détaillée:', err.response?.data || err.message);
      alert('Erreur lors de l\'enregistrement des paramètres');
    }
  };

  const handleCollaborateurChange = (e) => {
    const { name, value } = e.target;
    setNewCollaborateur(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const createCollaborateur = async () => {
    try {
      // Validation des champs
      if (!newCollaborateur.nom || !newCollaborateur.prenom || !newCollaborateur.telephone || 
          !newCollaborateur.username || !newCollaborateur.password) {
        alert('Veuillez remplir tous les champs');
        return;
      }

      const token = localStorage.getItem('token');
      const headers = token ? { 'Authorization': `Token ${token}` } : {};

      await axios.post('https://patisserie-backend.onrender.com/api/create-collaborateur/', newCollaborateur, { headers });
      
      alert('Collaborateur créé avec succès!');
      setCollaborateurDialogOpen(false);
      setNewCollaborateur({
        nom: '',
        prenom: '',
        telephone: '',
        username: '',
        password: ''
      });
    } catch (err) {
      console.error('Erreur lors de la création du collaborateur:', err);
      const errorMessage = err.response?.data?.error || 'Erreur lors de la création du collaborateur';
      alert(errorMessage);
    }
  };

  const handleArticleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === 'image' && files) {
      setNewArticle(prev => ({
        ...prev,
        image: files[0]
      }));
    } else {
      setNewArticle(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const createArticle = async () => {
    try {
      // Validation des champs
      if (!newArticle.titre || !newArticle.description) {
        alert('Veuillez remplir le titre et la description');
        return;
      }

      const token = localStorage.getItem('token');
      const headers = token ? { 'Authorization': `Token ${token}` } : {};

      const formData = new FormData();
      formData.append('titre', newArticle.titre);
      formData.append('description', newArticle.description);
      if (newArticle.image) {
        formData.append('image', newArticle.image);
      }

      await axios.post('https://patisserie-backend.onrender.com/api/create-article/', formData, { 
        headers: {
          ...headers,
          'Content-Type': 'multipart/form-data'
        }
      });
      
      alert('Article créé avec succès!');
      setArticleDialogOpen(false);
      setNewArticle({
        titre: '',
        description: '',
        image: null
      });
      fetchData(); // Recharger les données
    } catch (err) {
      console.error('Erreur lors de la création de l\'article:', err);
      const errorMessage = err.response?.data?.error || 'Erreur lors de la création de l\'article';
      alert(errorMessage);
    }
  };

  return (
    <Box sx={{ display: 'flex' }}>
      {/* Drawer avec responsive minimal */}
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
          // Responsive simple
          '@media (max-width: 768px)': {
            width: '100%',
            '& .MuiDrawer-paper': {
              width: '100%',
              position: 'relative',
            },
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            <ListItem onClick={() => setSection('commandes')} sx={{ cursor: 'pointer' }}>
              <ListItemText primary="📦 Commandes" />
            </ListItem>
            <ListItem onClick={() => setQrScannerOpen(true)} sx={{ cursor: 'pointer', backgroundColor: '#e3f2fd' }}>
              <ListItemText primary="📱 Scanner QR Code" />
            </ListItem>
            <ListItem onClick={() => setSection('gateaux')} sx={{ cursor: 'pointer' }}>
              <ListItemText primary="🎂 Gâteaux" />
            </ListItem>
            <ListItem onClick={() => setSection('galerie')} sx={{ cursor: 'pointer' }}>
              <ListItemText primary="🖼️ Galerie" />
            </ListItem>
            <ListItem onClick={() => setSection('parametres')} sx={{ cursor: 'pointer' }}>
              <ListItemText primary="⚙️ Paramètres" />
            </ListItem>
            <ListItem onClick={() => setSection('statistiques')} sx={{ cursor: 'pointer' }}>
              <ListItemText primary="📊 Statistiques" />
            </ListItem>
            <ListItem onClick={() => setSection('articles')} sx={{ cursor: 'pointer' }}>
              <ListItemText primary="📰 Articles" />
            </ListItem>
          </List>
        </Box>
      </Drawer>

      {/* Contenu principal */}
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        {/* Header simple */}
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center', 
          mb: 3,
          flexWrap: 'wrap',
          gap: 1
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <NotificationSystem />
            <Typography variant="h4">
              Dashboard Patron
            </Typography>
          </Box>
          <Button
            variant="outlined"
            onClick={logout}
          >
            Déconnexion
          </Button>
        </Box>

        {/* Contenu des sections */}
        <Box>
          {/* === SECTION : Commandes === */}
          {section === 'commandes' && (
            <Box>
              <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
                📦 Gestion des Commandes
              </Typography>
              
              {/* Grille responsive simple */}
              <Grid container spacing={3}>
                {/* Commandes en attente */}
                <Grid size={{ xs: 12, lg: 6 }}>
                  <Box sx={{ 
                    border: '2px solid #ff9800', 
                    borderRadius: 2, 
                    p: 2,
                    mb: 2
                  }}>
                    <Typography variant="h6" sx={{ color: '#ff9800', mb: 2 }}>
                      ⏳ Commandes en attente
                    </Typography>
                    {commandes.filter(cmd => cmd.status === 'en_attente').length === 0 ? (
                      <Alert severity="info">Aucune commande en attente</Alert>
                    ) : (
                      <Grid container spacing={2}>
                        {commandes.filter(cmd => cmd.status === 'en_attente').map((cmd) => (
                          <Grid size={{ xs: 12, sm: 6 }} key={cmd.id}>
                            <Card sx={{ height: '100%' }}>
                              <CardContent>
                                <Typography variant="h6" gutterBottom>
                                  {cmd.client_nom}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  📞 {cmd.client_telephone}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  🎂 {cmd.gateau.nom}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  💰 {cmd.prix_total} FCFA
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  📅 {new Date(cmd.date_livraison).toLocaleDateString('fr-FR')}
                                </Typography>
                                <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                                  <Button
                                    size="small"
                                    variant="contained"
                                    color="success"
                                    onClick={() => updateCommandeStatus(cmd.id, 'validee')}
                                  >
                                    ✅ Valider
                                  </Button>
                                  <Button
                                    size="small"
                                    variant="contained"
                                    color="error"
                                    onClick={() => updateCommandeStatus(cmd.id, 'refusee')}
                                  >
                                    ❌ Refuser
                                  </Button>
                                </Box>
                              </CardContent>
                            </Card>
                          </Grid>
                        ))}
                      </Grid>
                    )}
                  </Box>
                </Grid>

                {/* Commandes validées */}
                <Grid size={{ xs: 12, lg: 6 }}>
                  <Box sx={{ 
                    border: '2px solid #4caf50', 
                    borderRadius: 2, 
                    p: 2,
                    mb: 2
                  }}>
                    <Typography variant="h6" sx={{ color: '#4caf50', mb: 2 }}>
                      ✅ Commandes validées
                    </Typography>
                    {commandes.filter(cmd => cmd.status === 'validee').length === 0 ? (
                      <Alert severity="info">Aucune commande validée</Alert>
                    ) : (
                      <Grid container spacing={2}>
                        {commandes.filter(cmd => cmd.status === 'validee').map((cmd) => (
                          <Grid size={{ xs: 12, sm: 6 }} key={cmd.id}>
                            <Card sx={{ height: '100%' }}>
                              <CardContent>
                                <Typography variant="h6" gutterBottom>
                                  {cmd.client_nom}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  📞 {cmd.client_telephone}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  🎂 {cmd.gateau.nom}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  💰 {cmd.prix_total} FCFA
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  📅 {new Date(cmd.date_livraison).toLocaleDateString('fr-FR')}
                                </Typography>
                                <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                                  <Button
                                    size="small"
                                    variant="contained"
                                    color="primary"
                                    onClick={() => updateCommandeStatus(cmd.id, 'terminee')}
                                  >
                                    🎂 Terminer
                                  </Button>
                                  <Button
                                    size="small"
                                    variant="outlined"
                                    color="secondary"
                                    onClick={() => generateAndSendQRCode(cmd.id)}
                                    disabled={cmd.qr_code_sent}
                                  >
                                    {cmd.qr_code_sent ? '✅ QR Code envoyé' : '📱 Générer & Envoyer QR Code'}
                                  </Button>
                                </Box>
                              </CardContent>
                            </Card>
                          </Grid>
                        ))}
                      </Grid>
                    )}
                  </Box>
                </Grid>

                {/* Commandes terminées */}
                <Grid size={{ xs: 12, lg: 6 }}>
                  <Box sx={{ 
                    border: '2px solid #2196f3', 
                    borderRadius: 2, 
                    p: 2,
                    mb: 2
                  }}>
                    <Typography variant="h6" sx={{ color: '#2196f3', mb: 2 }}>
                      🎂 Commandes terminées
                    </Typography>
                    {commandes.filter(cmd => cmd.status === 'terminee').length === 0 ? (
                      <Alert severity="info">Aucune commande terminée</Alert>
                    ) : (
                      <Grid container spacing={2}>
                        {commandes.filter(cmd => cmd.status === 'terminee').map((cmd) => (
                          <Grid size={{ xs: 12, sm: 6 }} key={cmd.id}>
                            <Card sx={{ height: '100%' }}>
                              <CardContent>
                                <Typography variant="h6" gutterBottom>
                                  {cmd.client_nom}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  📞 {cmd.client_telephone}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  🎂 {cmd.gateau.nom}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  💰 {cmd.prix_total} FCFA
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  📅 {new Date(cmd.date_livraison).toLocaleDateString('fr-FR')}
                                </Typography>
                                <Chip 
                                  label="Terminée" 
                                  color="success" 
                                  size="small"
                                  sx={{ mt: 1 }}
                                />
                              </CardContent>
                            </Card>
                          </Grid>
                        ))}
                      </Grid>
                    )}
                  </Box>
                </Grid>

                {/* Commandes refusées */}
                <Grid size={{ xs: 12, lg: 6 }}>
                  <Box sx={{ 
                    border: '2px solid #f44336', 
                    borderRadius: 2, 
                    p: 2,
                    mb: 2
                  }}>
                    <Typography variant="h6" sx={{ color: '#f44336', mb: 2 }}>
                      ❌ Commandes refusées
                    </Typography>
                    {commandes.filter(cmd => cmd.status === 'refusee').length === 0 ? (
                      <Alert severity="info">Aucune commande refusée</Alert>
                    ) : (
                      <Grid container spacing={2}>
                        {commandes.filter(cmd => cmd.status === 'refusee').map((cmd) => (
                          <Grid size={{ xs: 12, sm: 6 }} key={cmd.id}>
                            <Card sx={{ height: '100%' }}>
                              <CardContent>
                                <Typography variant="h6" gutterBottom>
                                  {cmd.client_nom}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  📞 {cmd.client_telephone}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  🎂 {cmd.gateau.nom}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  💰 {cmd.prix_total} FCFA
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  📅 {new Date(cmd.date_livraison).toLocaleDateString('fr-FR')}
                                </Typography>
                                <Chip 
                                  label="Refusée" 
                                  color="error" 
                                  size="small"
                                  sx={{ mt: 1 }}
                                />
                              </CardContent>
                            </Card>
                          </Grid>
                        ))}
                      </Grid>
                    )}
                  </Box>
                </Grid>
              </Grid>
            </Box>
          )}

          {/* === SECTION : Statistiques === */}
          {section === 'statistiques' && (
            <>
              <Typography variant="h4" gutterBottom>📊 Statistiques</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Vue d'ensemble de l'activité de votre pâtisserie
              </Typography>
              
              {loadingStats ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                  <Typography>Chargement des statistiques...</Typography>
                </Box>
              ) : statistiques ? (
                <Grid container spacing={3}>
                  {/* Statistiques par période */}
                  <Grid size={{ xs: 12 }}>
                    <Typography variant="h6" gutterBottom>📈 Statistiques par période</Typography>
                    <Grid container spacing={2}>
                      {Object.entries(statistiques.statistiques_periode).map(([periode, data]) => (
                        <Grid size={{ xs: 12, sm: 6, md: 3 }} key={periode}>
                          <Card sx={{ 
                            bgcolor: periode === 'semaine' ? '#e3f2fd' : 
                                     periode === 'mois' ? '#f3e5f5' : 
                                     periode === 'trimestre' ? '#e8f5e8' : '#fff3e0',
                            border: '2px solid',
                            borderColor: periode === 'semaine' ? '#2196f3' : 
                                       periode === 'mois' ? '#9c27b0' : 
                                       periode === 'trimestre' ? '#4caf50' : '#ff9800'
                          }}>
                            <CardContent>
                              <Typography variant="h6" sx={{ textTransform: 'capitalize', fontWeight: 'bold' }}>
                                {periode === 'semaine' ? '📅 Semaine' :
                                 periode === 'mois' ? '📅 Mois' :
                                 periode === 'trimestre' ? '📅 Trimestre' : '📅 Année'}
                              </Typography>
                              <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                                {data.commandes}
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                Commandes
                              </Typography>
                              <Typography variant="h5" sx={{ fontWeight: 'bold', color: 'success.main', mt: 1 }}>
                                {data.chiffre_affaires.toLocaleString()} FCFA
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                Chiffre d'affaires
                              </Typography>
                              <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
                                {statistiques.periode_calcul[periode]}
                              </Typography>
                            </CardContent>
                          </Card>
                        </Grid>
                      ))}
                    </Grid>
                  </Grid>

                  {/* Statistiques par statut */}
                  <Grid size={{ xs: 12, md: 6 }}>
                    <Typography variant="h6" gutterBottom>📊 Répartition par statut</Typography>
                    <Card>
                      <CardContent>
                        <Grid container spacing={2}>
                          {Object.entries(statistiques.statistiques_status).map(([status, count]) => (
                            <Grid size={{ xs: 6 }} key={status}>
                              <Box sx={{ 
                                p: 2, 
                                borderRadius: 1,
                                bgcolor: status === 'en_attente' ? '#fff3e0' :
                                         status === 'validee' ? '#e8f5e8' :
                                         status === 'refusee' ? '#ffebee' : '#e3f2fd',
                                border: '1px solid',
                                borderColor: status === 'en_attente' ? '#ff9800' :
                                            status === 'validee' ? '#4caf50' :
                                            status === 'refusee' ? '#f44336' : '#2196f3'
                              }}>
                                <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                  {count}
                                </Typography>
                                <Typography variant="body2" sx={{ textTransform: 'capitalize' }}>
                                  {status === 'en_attente' ? '⏳ En attente' :
                                   status === 'validee' ? '✅ Validées' :
                                   status === 'refusee' ? '❌ Refusées' : '🎂 Terminées'}
                                </Typography>
                              </Box>
                            </Grid>
                          ))}
                        </Grid>
                      </CardContent>
                    </Card>
                  </Grid>

                  {/* Top gâteaux */}
                  <Grid size={{ xs: 12, md: 6 }}>
                    <Typography variant="h6" gutterBottom>🏆 Top gâteaux</Typography>
                    <Card>
                      <CardContent>
                        {statistiques.top_gateaux.length > 0 ? (
                          <Grid container spacing={2}>
                            {statistiques.top_gateaux.map((gateau, index) => (
                              <Grid size={{ xs: 12 }} key={index}>
                                <Box sx={{ 
                                  display: 'flex', 
                                  justifyContent: 'space-between', 
                                  alignItems: 'center',
                                  p: 1,
                                  borderRadius: 1,
                                  bgcolor: index === 0 ? '#fff3e0' : 
                                           index === 1 ? '#f3e5f5' : 
                                           index === 2 ? '#e8f5e8' : '#f5f5f5'
                                }}>
                                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                    <Typography variant="h6" sx={{ 
                                      color: index < 3 ? 'primary.main' : 'text.secondary',
                                      fontWeight: 'bold'
                                    }}>
                                      #{index + 1}
                                    </Typography>
                                    <Typography variant="body1">
                                      {gateau.gateau__nom || 'Gâteau inconnu'}
                                    </Typography>
                                  </Box>
                                  <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'success.main' }}>
                                    {gateau.total_commandes}
                                  </Typography>
                                </Box>
                              </Grid>
                            ))}
                          </Grid>
                        ) : (
                          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
                            Aucune commande pour le moment
                          </Typography>
                        )}
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              ) : (
                <Typography variant="h6" color="text.secondary" sx={{ textAlign: 'center', mt: 4 }}>
                  Erreur lors du chargement des statistiques
                </Typography>
              )}
            </>
          )}

          {/* === SECTION : Articles === */}
          {section === 'articles' && (
            <>
              <Typography variant="h4" gutterBottom>📰 Gestion des Articles</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Publiez des articles pour la page d'accueil
              </Typography>
              
              <Button 
                variant="contained" 
                onClick={() => setArticleDialogOpen(true)}
                startIcon={<span>➕</span>}
                sx={{ mb: 3 }}
              >
                Ajouter un article
              </Button>
              
              <Grid container spacing={3}>
                {articles.map((article) => (
                  <Grid size={{ xs: 12, md: 6, lg: 4 }} key={article.id}>
                    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                      {article.image && (
                        <Box sx={{ 
                          height: 200, 
                          backgroundImage: `url(https://patisserie-backend.onrender.com${article.image})`,
                          backgroundSize: 'cover',
                          backgroundPosition: 'center',
                          backgroundRepeat: 'no-repeat'
                        }} />
                      )}
                      <CardContent sx={{ flexGrow: 1 }}>
                        <Typography variant="h6" gutterBottom>
                          {article.titre}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                          {article.description.length > 150 
                            ? `${article.description.substring(0, 150)}...` 
                            : article.description
                          }
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          📅 Publié le {new Date(article.date_publication).toLocaleDateString('fr-FR')}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </>
          )}

          {/* === SECTION : Gâteaux === */}
          {section === 'gateaux' && (
            <>
              <Typography variant="h4" gutterBottom>Gâteaux</Typography>
              <Button variant="contained" onClick={() => setDialogOpen(true)}>➕ Ajouter un gâteau</Button>
              <Grid container spacing={2} mt={2}>
                {gateaux.map((g) => (
                  <Grid size={{ xs: 12, md: 4 }} key={g.id}>
                    <Card>
                      <CardContent>
                        <Typography><strong>{g.nom}</strong> ({g.type})</Typography>
                        <Typography>{g.description}</Typography>
                        <Typography>{g.prix} FCFA</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
              <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
                <DialogTitle>Ajouter un gâteau</DialogTitle>
                <DialogContent>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
                    <TextField name="nom" label="Nom" fullWidth onChange={handleGâteauChange} />
                    <TextField name="description" label="Description" fullWidth onChange={handleGâteauChange} />
                    <TextField name="prix" label="Prix" type="number" fullWidth onChange={handleGâteauChange} />
                    <TextField name="type" label="Type (anniversaire, mariage, etc.)" fullWidth onChange={handleGâteauChange} />
                    <Box>
                      <input type="file" name="image" onChange={handleGâteauChange} />
                    </Box>
                  </Box>
                </DialogContent>
                <DialogActions>
                  <Button onClick={() => setDialogOpen(false)}>
                    Annuler
                  </Button>
                  <Button onClick={createGâteau} variant="contained">Créer</Button>
                </DialogActions>
              </Dialog>
            </>
          )}

          {/* === SECTION : Galerie === */}
          {section === 'galerie' && (
            <Galerie />
          )}

          {/* === SECTION : Paramètres === */}
          {section === 'parametres' && (
            <>
              <Typography variant="h4" gutterBottom>⚙️ Paramètres</Typography>
              
              {/* Prix de livraison */}
              <Box sx={{ mb: 4 }}>
                <Typography variant="h6" gutterBottom>💰 Prix de livraison (FCFA)</Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <TextField 
                    value={livraisonPrix} 
                    onChange={(e) => setLivraisonPrix(e.target.value)}
                    type="number"
                    placeholder="2000"
                    sx={{ width: 200 }}
                  />
                  <Button onClick={saveLivraisonPrix} variant="outlined">
                    💾 Enregistrer
                  </Button>
                </Box>
              </Box>

              {/* Numéro du patron */}
              <Box sx={{ mb: 4 }}>
                <Typography variant="h6" gutterBottom>📞 Numéro de téléphone pour les dépôts</Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Ce numéro sera utilisé dans les messages WhatsApp pour les dépôts des clients
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <TextField 
                    value={numeroPatron} 
                    onChange={(e) => setNumeroPatron(e.target.value)}
                    placeholder="2250123456789"
                    sx={{ width: 300 }}
                    helperText="Format: 2250123456789 (avec indicatif pays)"
                  />
                  <Button onClick={saveLivraisonPrix} variant="outlined">
                    💾 Enregistrer
                  </Button>
                </Box>
              </Box>

              {/* Gestion des collaborateurs */}
              <Box sx={{ mb: 4 }}>
                <Typography variant="h6" gutterBottom>👥 Gestion des Collaborateurs</Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Créez de nouveaux collaborateurs pour vous aider dans la gestion
                </Typography>
                <Button 
                  variant="contained" 
                  onClick={() => setCollaborateurDialogOpen(true)}
                  startIcon={<span>➕</span>}
                >
                  Ajouter un collaborateur
                </Button>
              </Box>
            </>
          )}
        </Box>
      </Box>

      {/* Dialog pour créer un collaborateur */}
      <Dialog open={collaborateurDialogOpen} onClose={() => setCollaborateurDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>👥 Ajouter un Collaborateur</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <TextField
              name="nom"
              label="Nom de famille"
              fullWidth
              value={newCollaborateur.nom}
              onChange={handleCollaborateurChange}
              required
            />
            <TextField
              name="prenom"
              label="Prénom"
              fullWidth
              value={newCollaborateur.prenom}
              onChange={handleCollaborateurChange}
              required
            />
            <TextField
              name="telephone"
              label="Numéro de téléphone"
              fullWidth
              value={newCollaborateur.telephone}
              onChange={handleCollaborateurChange}
              required
            />
            <TextField
              name="username"
              label="Nom d'utilisateur"
              fullWidth
              value={newCollaborateur.username}
              onChange={handleCollaborateurChange}
              required
            />
            <TextField
              name="password"
              label="Mot de passe"
              type="password"
              fullWidth
              value={newCollaborateur.password}
              onChange={handleCollaborateurChange}
              required
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCollaborateurDialogOpen(false)}>
            Annuler
          </Button>
          <Button onClick={createCollaborateur} variant="contained">
            👥 Créer le collaborateur
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog pour créer un article */}
      <Dialog open={articleDialogOpen} onClose={() => setArticleDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>📰 Ajouter un Article</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <TextField
              name="titre"
              label="Titre de l'article"
              fullWidth
              value={newArticle.titre}
              onChange={handleArticleChange}
              required
            />
            <TextField
              name="description"
              label="Description de l'article"
              fullWidth
              multiline
              rows={4}
              value={newArticle.description}
              onChange={handleArticleChange}
              required
            />
            <input type="file" name="image" onChange={handleArticleChange} />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setArticleDialogOpen(false)}>
            Annuler
          </Button>
          <Button onClick={createArticle} variant="contained">
            📰 Créer l'article
          </Button>
        </DialogActions>
      </Dialog>

      {/* Scanner QR Code */}
      <QRCodeScanner 
        open={qrScannerOpen} 
        onClose={() => setQrScannerOpen(false)} 
      />
    </Box>
  );
};

export default DashboardPatron;

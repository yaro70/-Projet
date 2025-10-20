import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Box, Typography, Button, Grid, Card, CardContent, CardActions,
  Drawer, List, ListItem, ListItemText, Divider, Toolbar,
  Alert, Chip
} from '@mui/material';
import { useAuth } from './AuthContext';
import QRCodeScanner from './QRCodeScanner';

const drawerWidth = 240;

const DashboardCollaborateur = () => {
  const { logout } = useAuth();
  const [commandes, setCommandes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [qrScannerOpen, setQrScannerOpen] = useState(false);

  useEffect(() => {
    fetchCommandes();
  }, []);

  const fetchCommandes = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('token');
      const headers = token ? { 'Authorization': `Token ${token}` } : {};
      
      const response = await axios.get('https://patisserie-backend.onrender.com/api/commandes/', { headers });
      
      // Filtrer pour ne montrer que les commandes validées
      const commandesValidees = response.data.filter(cmd => cmd.status === 'validee');
      setCommandes(commandesValidees);
      
    } catch (err) {
      console.error("Erreur de récupération des commandes :", err);
      setError('Erreur lors du chargement des commandes');
    } finally {
      setLoading(false);
    }
  };

  const terminerCommande = async (id) => {
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { 'Authorization': `Token ${token}` } : {};
      
      // Utiliser la même API que le patron pour marquer comme terminée
      const response = await axios.post(
        `https://patisserie-backend.onrender.com/api/commandes/${id}/mark-terminee/`, 
        {}, 
        { headers }
      );
      
      // Ouvrir automatiquement WhatsApp si le lien est disponible
      if (response.data.whatsapp_link) {
        window.open(response.data.whatsapp_link, '_blank');
      }
      
      alert('Commande marquée comme terminée! WhatsApp ouvert automatiquement.');
      fetchCommandes(); // Recharger les commandes
      
    } catch (err) {
      console.error("Erreur lors de la mise à jour de la commande :", err);
      alert('Erreur lors de la mise à jour de la commande');
    }
  };

  return (
    <Box sx={{ display: 'flex' }}>
      {/* === Sidebar === */}
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' }
        }}
      >
        <Toolbar />
        <List>
          <ListItem><Typography variant="h6">👨‍🍳 Collaborateur</Typography></ListItem>
          <Divider />
          <ListItem>
            <ListItemText primary="📦 Commandes validées" />
          </ListItem>
          <ListItem onClick={() => setQrScannerOpen(true)} sx={{ cursor: 'pointer', backgroundColor: '#e3f2fd' }}>
            <ListItemText primary="📱 Scanner QR Code" />
          </ListItem>
          <Divider />
          <ListItem button onClick={logout}>
            <ListItemText primary="🚪 Déconnexion" />
          </ListItem>
        </List>
      </Drawer>

      {/* === Main Content === */}
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        
        <Typography variant="h4" gutterBottom>📦 Commandes à traiter</Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Commandes validées par le patron - Préparez les gâteaux et marquez-les comme terminés
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {loading ? (
          <Typography variant="h6" color="text.secondary" sx={{ textAlign: 'center', mt: 4 }}>
            Chargement des commandes...
          </Typography>
        ) : commandes.length === 0 ? (
          <Box sx={{ textAlign: 'center', mt: 4 }}>
            <Typography variant="h6" color="text.secondary" gutterBottom>
              🎉 Aucune commande validée à traiter
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Toutes les commandes validées ont été traitées ou aucune commande n'est en attente
            </Typography>
          </Box>
        ) : (
          <>
            {/* === SECTION : Commandes validées (à traiter) === */}
            <Box sx={{ mb: 4 }}>
              <Typography variant="h5" gutterBottom sx={{ 
                color: '#4caf50', 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1 
              }}>
                ✅ Commandes validées à traiter
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Commandes validées par le patron - Préparez les gâteaux et marquez-les comme terminés
              </Typography>
              
              {commandes.filter(cmd => cmd.status === 'validee').length === 0 ? (
                <Alert severity="info" sx={{ mb: 2 }}>
                  Aucune commande validée à traiter
                </Alert>
              ) : (
                <Grid container spacing={3}>
                  {commandes.filter(cmd => cmd.status === 'validee').map((cmd) => (
                    <Grid size={{ xs: 12, md: 6, lg: 4 }} key={cmd.id}>
                      <Card sx={{ 
                        border: '2px solid #4caf50',
                        bgcolor: '#e8f5e8',
                        height: '100%',
                        display: 'flex',
                        flexDirection: 'column'
                      }}>
                        <CardContent sx={{ flexGrow: 1 }}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                            <Typography variant="h6" gutterBottom>
                              Commande #{cmd.id}
                            </Typography>
                            <Chip 
                              label="✅ Validée"
                              sx={{ 
                                bgcolor: '#4caf50',
                                color: 'white',
                                fontWeight: 'bold'
                              }}
                            />
                          </Box>
                          
                          <Typography><strong>👤 Client:</strong> {cmd.client_nom}</Typography>
                          <Typography><strong>📞 Téléphone:</strong> {cmd.client_telephone}</Typography>
                          <Typography><strong>🎂 Gâteau:</strong> {cmd.gateau_nom || cmd.gateau}</Typography>
                          <Typography><strong>📝 Texte:</strong> {cmd.texte_sur_gateau || 'Aucun'}</Typography>
                          <Typography><strong>📅 Livraison:</strong> {new Date(cmd.date_livraison).toLocaleString('fr-FR')}</Typography>
                          <Typography><strong>🚚 Livraison:</strong> {cmd.livraison ? 'Oui' : 'Non'}</Typography>
                          <Typography><strong>💰 Prix total:</strong> {parseFloat(cmd.prix_total).toLocaleString()} FCFA</Typography>
                          
                          {/* Statut WhatsApp */}
                          <Box sx={{ mt: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="body2" sx={{ 
                              color: cmd.whatsapp_envoye ? '#4caf50' : '#ff9800',
                              fontWeight: 'bold'
                            }}>
                              📱 WhatsApp: {cmd.whatsapp_envoye ? 'Envoyé' : 'Non envoyé'}
                            </Typography>
                            {cmd.whatsapp_envoye && cmd.date_whatsapp && (
                              <Typography variant="caption" color="text.secondary">
                                ({new Date(cmd.date_whatsapp).toLocaleString('fr-FR')})
                              </Typography>
                            )}
                          </Box>
                        </CardContent>
                        
                        <CardActions sx={{ justifyContent: 'center', p: 2 }}>
                          <Button
                            variant="contained"
                            color="success"
                            size="large"
                            onClick={() => terminerCommande(cmd.id)}
                            startIcon={<span>🎂</span>}
                            fullWidth
                          >
                            🎂 Marquer comme terminé
                          </Button>
                        </CardActions>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              )}
            </Box>

            {/* === SECTION : Commandes terminées === */}
            <Box sx={{ mb: 4 }}>
              <Typography variant="h5" gutterBottom sx={{ 
                color: '#2196f3', 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1 
              }}>
                🎂 Commandes terminées
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Commandes que vous avez terminées
              </Typography>
              
              {commandes.filter(cmd => cmd.status === 'terminee').length === 0 ? (
                <Alert severity="info" sx={{ mb: 2 }}>
                  Aucune commande terminée
                </Alert>
              ) : (
                <Grid container spacing={3}>
                  {commandes.filter(cmd => cmd.status === 'terminee').map((cmd) => (
                    <Grid size={{ xs: 12, md: 6, lg: 4 }} key={cmd.id}>
                      <Card sx={{ 
                        border: '2px solid #2196f3',
                        bgcolor: '#e3f2fd',
                        height: '100%',
                        display: 'flex',
                        flexDirection: 'column'
                      }}>
                        <CardContent sx={{ flexGrow: 1 }}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                            <Typography variant="h6" gutterBottom>
                              Commande #{cmd.id}
                            </Typography>
                            <Chip 
                              label="🎂 Terminée"
                              sx={{ 
                                bgcolor: '#2196f3',
                                color: 'white',
                                fontWeight: 'bold'
                              }}
                            />
                          </Box>
                          
                          <Typography><strong>👤 Client:</strong> {cmd.client_nom}</Typography>
                          <Typography><strong>📞 Téléphone:</strong> {cmd.client_telephone}</Typography>
                          <Typography><strong>🎂 Gâteau:</strong> {cmd.gateau_nom || cmd.gateau}</Typography>
                          <Typography><strong>📝 Texte:</strong> {cmd.texte_sur_gateau || 'Aucun'}</Typography>
                          <Typography><strong>📅 Livraison:</strong> {new Date(cmd.date_livraison).toLocaleString('fr-FR')}</Typography>
                          <Typography><strong>🚚 Livraison:</strong> {cmd.livraison ? 'Oui' : 'Non'}</Typography>
                          <Typography><strong>💰 Prix total:</strong> {parseFloat(cmd.prix_total).toLocaleString()} FCFA</Typography>
                          
                          {/* Statut WhatsApp */}
                          <Box sx={{ mt: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="body2" sx={{ 
                              color: cmd.whatsapp_envoye ? '#4caf50' : '#ff9800',
                              fontWeight: 'bold'
                            }}>
                              📱 WhatsApp: {cmd.whatsapp_envoye ? 'Envoyé' : 'Non envoyé'}
                            </Typography>
                            {cmd.whatsapp_envoye && cmd.date_whatsapp && (
                              <Typography variant="caption" color="text.secondary">
                                ({new Date(cmd.date_whatsapp).toLocaleString('fr-FR')})
                              </Typography>
                            )}
                          </Box>
                        </CardContent>
                        
                        <CardActions sx={{ justifyContent: 'center', p: 2 }}>
                          <Button
                            variant="outlined"
                            color="success"
                            size="small"
                            onClick={() => window.open(cmd.whatsapp_link, '_blank')}
                            startIcon={<span>📱</span>}
                            fullWidth
                          >
                            WhatsApp
                          </Button>
                        </CardActions>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              )}
            </Box>
          </>
        )}
      </Box>

      {/* Scanner QR Code */}
      <QRCodeScanner 
        open={qrScannerOpen} 
        onClose={() => setQrScannerOpen(false)} 
      />
    </Box>
  );
};

export default DashboardCollaborateur;

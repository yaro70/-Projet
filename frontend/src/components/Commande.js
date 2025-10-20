import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { 
  TextField, Button, FormControlLabel, Checkbox, Typography, Container,
  Card, CardContent, CardMedia, Box, Grid, Paper, Divider
} from '@mui/material';

const Commande = () => {
  const { gateauId } = useParams();
  const navigate = useNavigate();
  const [gateau, setGateau] = useState(null);
  const [prixLivraison, setPrixLivraison] = useState(0);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [commandeData, setCommandeData] = useState(null);
  const [formData, setFormData] = useState({
    client_nom: '',
    client_telephone: '',
    texte_sur_gateau: '',
    date_livraison: '',
    livraison: false,
  });
  
  useEffect(() => {
    axios.get(`http://localhost:8000/api/gateaux/${gateauId}/`)
      .then(res => setGateau(res.data))
      .catch(err => console.log(err));
    
    axios.get('http://localhost:8000/api/parametres/')
      .then(res => {
        if (res.data.length > 0) {
          setPrixLivraison(parseFloat(res.data[0].prix_livraison));
        }
      })
      .catch(err => console.log(err));
  }, [gateauId]);
  
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    const maintenant = new Date();
    const dateLivraison = new Date(formData.date_livraison);
    const diffHeures = (dateLivraison - maintenant) / (1000 * 60 * 60);
    
    if (diffHeures < 12) {
      alert('La commande doit être passée au moins 12 heures avant la livraison');
      return;
    }
    
    // Calculer le prix total
    const prixTotal = parseFloat(gateau.prix) + (formData.livraison ? parseFloat(prixLivraison) : 0);
    
    // Sauvegarder les données de commande pour l'étape de confirmation
    setCommandeData({
      ...formData,
      gateau_id: gateau.id,
      prix_total: prixTotal,
      gateau_nom: gateau.nom,
      gateau_prix: gateau.prix
    });
    
    // Afficher l'étape de confirmation
    setShowConfirmation(true);
  };

  const handleConfirmCommande = async () => {
    try {
      console.log('Envoi de la commande:', commandeData);
      
      const res = await axios.post('http://localhost:8000/api/create-commande/', commandeData);
      console.log('Réponse de l\'API:', res.data);
      
      // Afficher le message de succès avec les instructions
      setShowConfirmation(false);
      setCommandeData(null);
      
      // Naviguer vers la page de succès ou afficher le message
      alert('Commande passée avec succès! Veuillez suivre les instructions pour le paiement.');
    } catch (err) {
      console.error('Erreur détaillée:', err);
      console.error('Réponse d\'erreur:', err.response?.data);
      console.error('Statut:', err.response?.status);
      alert(`Erreur lors de la commande: ${err.response?.data?.error || err.message}`);
    }
  };

  const handleWhatsAppClick = async () => {
    if (!commandeData) return;
    
    try {
      // Récupérer le numéro du patron depuis les paramètres
      const response = await axios.get('http://localhost:8000/api/parametres/');
      const numeroPatron = response.data.length > 0 ? response.data[0].numero_patron : "2250123456789";
      
      const message = `Bonjour! J'ai passé une commande de gâteau:

🎂 Gâteau: ${commandeData.gateau_nom}
💰 Prix: ${commandeData.gateau_prix.toLocaleString()} FCFA
${commandeData.livraison ? `🚚 Livraison: ${prixLivraison.toLocaleString()} FCFA` : ''}
💰 Total: ${commandeData.prix_total.toLocaleString()} FCFA

👤 Nom: ${commandeData.client_nom}
📞 Téléphone: ${commandeData.client_telephone}
📅 Date de ${commandeData.livraison ? 'livraison' : 'récupération'}: ${new Date(commandeData.date_livraison).toLocaleString('fr-FR')}
${commandeData.texte_sur_gateau ? `📝 Texte: ${commandeData.texte_sur_gateau}` : ''}

J'ai effectué le dépôt et je souhaite envoyer la capture d'écran.`;

      const whatsappUrl = `https://wa.me/${numeroPatron}?text=${encodeURIComponent(message)}`;
      window.open(whatsappUrl, '_blank');
    } catch (error) {
      console.error('Erreur lors de la récupération du numéro patron:', error);
      // Fallback vers le numéro par défaut
      const message = `Bonjour! J'ai passé une commande de gâteau:

🎂 Gâteau: ${commandeData.gateau_nom}
💰 Prix: ${commandeData.gateau_prix.toLocaleString()} FCFA
${commandeData.livraison ? `🚚 Livraison: ${prixLivraison.toLocaleString()} FCFA` : ''}
💰 Total: ${commandeData.prix_total.toLocaleString()} FCFA

👤 Nom: ${commandeData.client_nom}
📞 Téléphone: ${commandeData.client_telephone}
📅 Date de ${commandeData.livraison ? 'livraison' : 'récupération'}: ${new Date(commandeData.date_livraison).toLocaleString('fr-FR')}
${commandeData.texte_sur_gateau ? `📝 Texte: ${commandeData.texte_sur_gateau}` : ''}

J'ai effectué le dépôt et je souhaite envoyer la capture d'écran.`;

      const whatsappUrl = `https://wa.me/2250123456789?text=${encodeURIComponent(message)}`;
      window.open(whatsappUrl, '_blank');
    }
  };
  
  if (!gateau) return <div>Chargement...</div>;

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h3" gutterBottom sx={{ textAlign: 'center', color: '#8B4513', mb: 4 }}>
        🎂 Commander votre gâteau
      </Typography>

      <Grid container spacing={4}>
        {/* Gâteau sélectionné */}
        <Grid item xs={12} md={4}>
          <Card sx={{ height: 'fit-content', borderRadius: 3, overflow: 'hidden' }}>
            <CardMedia
              component="img"
              height="240"
              image={gateau.image ? `http://localhost:8000${gateau.image}` : '/default-cake.jpg'}
              alt={gateau.nom}
              sx={{ objectFit: 'cover', width: '100%' }}
            />
            <CardContent>
              <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                {gateau.nom}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                {gateau.description}
              </Typography>
              <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                {gateau.prix.toLocaleString()} FCFA
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Formulaire de commande */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: { xs: 2, sm: 3 } }}>
            <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
              📝 Informations de commande
            </Typography>
            
            <form onSubmit={handleSubmit}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Votre nom complet"
                    name="client_nom"
                    value={formData.client_nom}
                    onChange={handleChange}
                    fullWidth
                    required
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Votre numéro de téléphone"
                    name="client_telephone"
                    value={formData.client_telephone}
                    onChange={handleChange}
                    fullWidth
                    required
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    label="Texte personnalisé sur le gâteau (optionnel)"
                    name="texte_sur_gateau"
                    value={formData.texte_sur_gateau}
                    onChange={handleChange}
                    fullWidth
                    margin="normal"
                    multiline
                    rows={2}
                    helperText="Ex: 'Joyeux Anniversaire Marie'"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    label="Date et heure de livraison souhaitée"
                    type="datetime-local"
                    name="date_livraison"
                    value={formData.date_livraison}
                    onChange={handleChange}
                    fullWidth
                    required
                    margin="normal"
                    InputLabelProps={{ shrink: true }}
                    helperText="Commande minimum 12h à l'avance"
                  />
                </Grid>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        name="livraison"
                        checked={formData.livraison}
                        onChange={handleChange}
                        color="primary"
                      />
                    }
                    label={`Livraison à domicile (+${prixLivraison.toLocaleString()} FCFA)`}
                  />
                </Grid>
              </Grid>

              {/* Résumé de la commande */}
              <Box sx={{ mt: 3, p: 2, borderRadius: 2, background: 'linear-gradient(135deg, #F7F9FC, #FFFFFF)' }}>
                <Typography variant="h6" gutterBottom sx={{ color: '#8B4513' }}>
                  💰 Résumé de votre commande
                </Typography>
                <Grid container spacing={1}>
                  <Grid item xs={6}>
                    <Typography>Prix du gâteau:</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography sx={{ fontWeight: 'bold' }}>
                      {gateau.prix.toLocaleString()} FCFA
                    </Typography>
                  </Grid>
                  {formData.livraison && (
                    <>
                      <Grid item xs={6}>
                        <Typography>Livraison:</Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography sx={{ fontWeight: 'bold' }}>
                          {prixLivraison.toLocaleString()} FCFA
                        </Typography>
                      </Grid>
                    </>
                  )}
                  <Grid item xs={12}>
                    <Divider sx={{ my: 1 }} />
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="h6" sx={{ color: '#8B4513', fontWeight: 'bold' }}>
                      Total:
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="h6" sx={{ color: '#8B4513', fontWeight: 'bold' }}>
                      {(parseFloat(gateau.prix) + (formData.livraison ? parseFloat(prixLivraison) : 0)).toLocaleString()} FCFA
                    </Typography>
                  </Grid>
                </Grid>
              </Box>

              <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                <Button 
                  variant="outlined" 
                  onClick={() => navigate('/')}
                  sx={{ color: '#8B4513', borderColor: '#8B4513' }}
                >
                  ← Retour au catalogue
                </Button>
                <Button 
                  type="submit" 
                  variant="contained" 
                  size="large"
                  sx={{ 
                    backgroundColor: '#8B4513',
                    '&:hover': { backgroundColor: '#A0522D' }
                  }}
                >
                  ✅ Confirmer la commande
                </Button>
              </Box>
            </form>
          </Paper>
        </Grid>
      </Grid>

      {/* Étape de confirmation */}
      {showConfirmation && commandeData && (
        <Box sx={{ 
          position: 'fixed', 
          top: 0, 
          left: 0, 
          right: 0, 
          bottom: 0, 
          backgroundColor: 'rgba(0,0,0,0.8)', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <Paper sx={{ 
            p: 4, 
            maxWidth: 600, 
            width: '90%', 
            maxHeight: '90vh', 
            overflow: 'auto',
            backgroundColor: '#FFF8DC'
          }}>
            <Typography variant="h4" gutterBottom sx={{ color: '#8B4513', textAlign: 'center' }}>
              🎉 Commande confirmée !
            </Typography>
            
            <Box sx={{ mt: 3, p: 3, backgroundColor: '#FFFFFF', borderRadius: 2, mb: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ color: '#8B4513' }}>
                📋 Détails de votre commande
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography><strong>Gâteau:</strong></Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography>{commandeData.gateau_nom}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography><strong>Prix:</strong></Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography>{commandeData.gateau_prix.toLocaleString()} FCFA</Typography>
                </Grid>
                {commandeData.livraison && (
                  <>
                    <Grid item xs={6}>
                      <Typography><strong>Livraison:</strong></Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography>{prixLivraison.toLocaleString()} FCFA</Typography>
                    </Grid>
                  </>
                )}
                <Grid item xs={6}>
                  <Typography><strong>Total:</strong></Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography sx={{ fontWeight: 'bold', color: '#8B4513' }}>
                    {commandeData.prix_total.toLocaleString()} FCFA
                  </Typography>
                </Grid>
              </Grid>
            </Box>

            <Box sx={{ p: 3, backgroundColor: '#E8F5E8', borderRadius: 2, mb: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ color: '#2E7D32' }}>
                💳 Instructions de paiement
              </Typography>
              <Typography variant="body1" sx={{ mb: 2 }}>
                Après avoir confirmé la commande, faites le dépôt au numéro suivant :
              </Typography>
              <Typography variant="h5" sx={{ 
                color: '#2E7D32', 
                fontWeight: 'bold', 
                textAlign: 'center',
                p: 2,
                backgroundColor: '#FFFFFF',
                borderRadius: 1,
                mb: 2
              }}>
                📱 +225 01 23 45 67 89
              </Typography>
              <Typography variant="body1" sx={{ mb: 3 }}>
                Puis cliquez sur le bouton ci-dessous pour envoyer la capture du dépôt avec les frais de retrait.
              </Typography>
            </Box>

            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
              <Button 
                variant="outlined" 
                onClick={() => {
                  setShowConfirmation(false);
                  setCommandeData(null);
                }}
                sx={{ color: '#8B4513', borderColor: '#8B4513' }}
              >
                ❌ Annuler
              </Button>
              <Button 
                variant="contained" 
                onClick={handleConfirmCommande}
                sx={{ 
                  backgroundColor: '#8B4513',
                  '&:hover': { backgroundColor: '#A0522D' }
                }}
              >
                ✅ Confirmer la commande
              </Button>
              <Button 
                variant="contained" 
                onClick={handleWhatsAppClick}
                sx={{ 
                  backgroundColor: '#25D366',
                  '&:hover': { backgroundColor: '#128C7E' }
                }}
                startIcon={<span>📱</span>}
              >
                WhatsApp
              </Button>
            </Box>
          </Paper>
        </Box>
      )}
    </Container>
  );
};

export default Commande;
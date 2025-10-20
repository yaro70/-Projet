import React, { useEffect, useState } from 'react';
import { 
  AppBar, Toolbar, Typography, Container, Box, Button, 
  Grid, Divider, Card, CardContent, CardMedia
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Catalogue from './Catalogue';
import { useAuth } from './AuthContext';
import axios from 'axios';

const Home = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [username, setUsername] = useState('');
  const [articles, setArticles] = useState([]);
  const [galeriePhotos, setGaleriePhotos] = useState([]);

  useEffect(() => {
    const storedName = localStorage.getItem('username');
    if (storedName) {
      setUsername(storedName);
    }
    
    // Charger les articles et la galerie
    fetchArticles();
    fetchGalerie();
  }, []);

  const fetchArticles = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/evenements/');
      setArticles(response.data || []);
    } catch (err) {
      console.error('Erreur lors du chargement des articles:', err);
      setArticles([]);
    }
  };

  const fetchGalerie = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/galerie/');
      const photos = response.data?.photos || [];
      setGaleriePhotos(photos.slice(0, 6)); // Afficher seulement 6 photos
    } catch (err) {
      console.error('Erreur lors du chargement de la galerie:', err);
      setGaleriePhotos([]);
    }
  };

  return (
    <div>
      <AppBar position="static" color="primary">
        <Toolbar sx={{ display: 'flex', justifyContent: 'space-between' }}>
          <Typography variant="h6" sx={{ fontWeight: 800 }}>
            🎂 Pâtisserie Royale
          </Typography>

          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <Typography variant="body1">Bonjour, {username}</Typography>
              <Button variant="contained" color="secondary" onClick={logout} sx={{ borderRadius: 2 }}>
                Déconnexion
              </Button>
            </div>
          ) : (
            <Button variant="contained" color="secondary" onClick={() => navigate('/login')} sx={{ borderRadius: 2 }}>
              Connexion
            </Button>
          )}
        </Toolbar>
      </AppBar>

      {/* Hero Section */}
      <Box sx={{ 
        background: 'linear-gradient(135deg, #F7F9FC, #FFFFFF)',
        py: 8, 
        textAlign: 'center'
      }}>
        <Container maxWidth="md">
          <Typography variant="h2" gutterBottom sx={{ fontWeight: 800 }}>
            🎂 Nos Délicieuses Créations
          </Typography>
          <Typography variant="h5" sx={{ color: 'text.secondary', mb: 4 }}>
            Découvrez notre sélection de gâteaux artisanaux faits avec amour
          </Typography>
          <Button 
            variant="contained" 
            size="large"
            sx={{ borderRadius: 2, mr: 2 }}
            onClick={() => document.getElementById('catalogue').scrollIntoView({ behavior: 'smooth' })}
          >
            Voir le Catalogue
          </Button>
          <Button variant="outlined" size="large" href="#evenements" sx={{ borderRadius: 2 }}>Nos événements</Button>
        </Container>
      </Box>

      {/* Articles Section */}
      {articles.length > 0 && (
        <Container maxWidth="lg" sx={{ py: 4 }}>
          <Typography variant="h3" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
            📰 Actualités & Événements
          </Typography>
          <Grid container spacing={3}>
            {articles.map((article) => (
              <Grid size={{ xs: 12, md: 6, lg: 4 }} key={article.id}>
                <Card sx={{ 
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  borderRadius: 3,
                  boxShadow: '0 8px 24px rgba(31,42,55,0.08)',
                  transition: 'transform .15s ease, box-shadow .15s ease',
                  '&:hover': {
                    transform: 'translateY(-3px)',
                    boxShadow: '0 12px 28px rgba(31,42,55,0.14)'
                  }
                }}>
                  {article.image && (
                    <CardMedia
                      component="img"
                      height="200"
                      image={`http://localhost:8000${article.image}`}
                      alt={article.titre}
                      sx={{ objectFit: 'cover' }}
                    />
                  )}
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 700 }}>
                      {article.titre}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {article.description && article.description.length > 150 
                        ? `${article.description.substring(0, 150)}...` 
                        : article.description || 'Aucune description disponible'
                      }
                    </Typography>
                    <Typography variant="caption" color="text.secondary" sx={{ 
                      display: 'block',
                      fontStyle: 'italic'
                    }}>
                      📅 Publié le {article.date_publication ? new Date(article.date_publication).toLocaleDateString('fr-FR') : 'Date non disponible'}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      )}

      {/* Galerie Section */}
      {galeriePhotos.length > 0 && (
        <Container maxWidth="lg" sx={{ py: 4 }}>
          <Typography variant="h3" gutterBottom sx={{ textAlign: 'center', color: '#8B4513', mb: 4 }}>
            📸 Galerie
          </Typography>
          <Grid container spacing={2}>
            {galeriePhotos.map((photo, index) => (
              <Grid size={{ xs: 12, sm: 6, md: 4 }} key={index}>
                <Card sx={{ height: '100%', boxShadow: 3 }}>
                  <CardMedia
                    component="img"
                    height="200"
                    image={`http://localhost:8000${photo.image}`}
                    alt={`Photo ${index + 1}`}
                    sx={{ objectFit: 'cover' }}
                  />
                  <CardContent>
                    <Typography variant="body2" color="text.secondary">
                      {photo.titre || 'Sans titre'}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      )}

      {/* Catalogue Section */}
      <Container maxWidth="lg" sx={{ py: 4 }} id="catalogue">
        <Typography variant="h3" gutterBottom sx={{ textAlign: 'center', color: '#8B4513', mb: 4 }}>
          🍰 Notre Catalogue
        </Typography>
        <Catalogue />
      </Container>

      {/* Footer */}
      <Box component="footer" sx={{ 
        py: 4, 
        textAlign: 'center',
        backgroundColor: '#EDF2FF',
        color: 'text.primary',
        borderTop: '1px solid rgba(31,42,55,0.08)'
      }}>
        <Container maxWidth="lg">
          <Grid container spacing={3}>
            <Grid size={{ xs: 12, md: 4 }}>
              <Typography variant="h6" gutterBottom>
                🎂 Pâtisserie Royale
              </Typography>
              <Typography variant="body2">
                Créations faites avec passion et des ingrédients de qualité.
              </Typography>
            </Grid>
            <Grid size={{ xs: 12, md: 4 }}>
              <Typography variant="h6" gutterBottom>
                📞 Contact
              </Typography>
              <Typography variant="body2">
                Téléphone: +226 72 86 07 68<br />
                Email: contact@patisserie.com
              </Typography>
            </Grid>
            <Grid size={{ xs: 12, md: 4 }}>
              <Typography variant="h6" gutterBottom>
                🕒 Horaires
              </Typography>
              <Typography variant="body2">
                Lundi - Samedi: 8h - 20h<br />
                Dimanche: 9h - 18h
              </Typography>
            </Grid>
          </Grid>
          <Divider sx={{ my: 2, backgroundColor: 'rgba(255,255,255,0.3)' }} />
          <Typography variant="body2">
            © {new Date().getFullYear()} Pâtisserie Royale - Tous droits réservés
          </Typography>
        </Container>
      </Box>
    </div>
  );
};

export default Home;

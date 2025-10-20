import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardMedia,
  CardContent,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  Tooltip,
  Alert,
  Skeleton,
  Fab,
  CircularProgress
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Close as CloseIcon
} from '@mui/icons-material';
import axios from 'axios';
import { useAuth } from './AuthContext';

const Galerie = () => {
  const { user } = useAuth();
  const [photos, setPhotos] = useState([]);
  const [categories, setCategories] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedCategorie, setSelectedCategorie] = useState('toutes');
  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [loadingImages, setLoadingImages] = useState({});
  const [formData, setFormData] = useState({
    titre: '',
    description: '',
    categorie: 'autre',
    date_realisation: '',
    ordre_affichage: 0,
    image: null
  });

  // Optimisation : useCallback pour éviter les re-renders inutiles
  const fetchPhotos = useCallback(async () => {
    try {
      setLoading(true);
      const response = await axios.get('https://patisserie-backend.onrender.com/api/galerie/');
      setPhotos(response.data.photos);
      setCategories(response.data.categories);
    } catch (error) {
      console.error('Erreur lors du chargement de la galerie:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPhotos();
  }, [fetchPhotos]);

  // Optimisation : Gestion du chargement des images
  const handleImageLoad = (photoId) => {
    setLoadingImages(prev => ({ ...prev, [photoId]: false }));
  };

  const handleImageError = (photoId) => {
    setLoadingImages(prev => ({ ...prev, [photoId]: false }));
  };

  // Optimisation : Debounce pour le filtrage
  const handleCategorieChange = useCallback((categorie) => {
    setSelectedCategorie(categorie);
  }, []);

  const handlePhotoClick = (photo) => {
    setSelectedPhoto(photo);
  };

  const handleAddPhoto = () => {
    setEditMode(false);
    setFormData({
      titre: '',
      description: '',
      categorie: 'autre',
      date_realisation: '',
      ordre_affichage: 0,
      image: null
    });
    setDialogOpen(true);
  };

  const handleEditPhoto = (photo) => {
    setEditMode(true);
    setFormData({
      titre: photo.titre,
      description: photo.description,
      categorie: photo.categorie,
      date_realisation: photo.date_realisation,
      ordre_affichage: photo.ordre_affichage,
      image: null
    });
    setSelectedPhoto(photo);
    setDialogOpen(true);
  };

  const handleDeletePhoto = async (photoId) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cette photo ?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.delete(`https://patisserie-backend.onrender.com/api/galerie/${photoId}/supprimer/`, {
        headers: { Authorization: `Token ${token}` }
      });
      
      setPhotos(photos.filter(photo => photo.id !== photoId));
      alert('Photo supprimée avec succès');
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
      alert('Erreur lors de la suppression');
    }
  };

  const handleSubmit = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Token ${token}` };
      
      const submitData = new FormData();
      submitData.append('titre', formData.titre);
      submitData.append('description', formData.description);
      submitData.append('categorie', formData.categorie);
      submitData.append('date_realisation', formData.date_realisation);
      submitData.append('ordre_affichage', formData.ordre_affichage);
      if (formData.image) {
        submitData.append('image', formData.image);
      }

      if (editMode) {
        await axios.put(`https://patisserie-backend.onrender.com/api/galerie/${selectedPhoto.id}/modifier/`, submitData, { headers });
        alert('Photo modifiée avec succès');
      } else {
        await axios.post('https://patisserie-backend.onrender.com/api/galerie/ajouter/', submitData, { headers });
        alert('Photo ajoutée avec succès');
      }
      
      setDialogOpen(false);
      fetchPhotos();
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error);
      alert('Erreur lors de la sauvegarde');
    }
  };

  const handleFileChange = (event) => {
    setFormData({ ...formData, image: event.target.files[0] });
  };

  const filteredPhotos = selectedCategorie === 'toutes' 
    ? photos 
    : photos.filter(photo => photo.categorie === selectedCategorie);

  const getCategorieColor = (categorie) => {
    const colors = {
      'anniversaire': 'primary',
      'mariage': 'secondary',
      'bapteme': 'success',
      'communion': 'info',
      'autre': 'default'
    };
    return colors[categorie] || 'default';
  };

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>📸 Galerie Photos</Typography>
        <Grid container spacing={3}>
          {[...Array(6)].map((_, index) => (
            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={index}>
              <Card>
                <Skeleton variant="rectangular" height={200} />
                <CardContent>
                  <Skeleton variant="text" height={24} />
                  <Skeleton variant="text" height={20} />
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" gutterBottom>📸 Galerie Photos</Typography>
        
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          {/* Filtre par catégorie */}
          <FormControl sx={{ minWidth: 150 }}>
            <InputLabel>Catégorie</InputLabel>
            <Select
              value={selectedCategorie}
              onChange={(e) => handleCategorieChange(e.target.value)}
              label="Catégorie"
            >
              <MenuItem value="toutes">Toutes les catégories</MenuItem>
              {Object.entries(categories).map(([key, value]) => (
                <MenuItem key={key} value={key}>{value}</MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Bouton d'ajout (patrons seulement) */}
          {user && user.is_patron && (
            <Fab
              color="primary"
              aria-label="ajouter"
              onClick={handleAddPhoto}
              sx={{ ml: 2 }}
            >
              <AddIcon />
            </Fab>
          )}
        </Box>
      </Box>

      {filteredPhotos.length === 0 ? (
        <Alert severity="info" sx={{ mt: 2 }}>
          Aucune photo disponible dans cette catégorie
        </Alert>
      ) : (
        <Grid container spacing={3}>
          {filteredPhotos.map((photo) => (
            <Grid size={{ xs: 12, sm: 6, md: 4, lg: 3 }} key={photo.id}>
              <Card 
                sx={{ 
                  height: '100%',
                  cursor: 'pointer',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'scale(1.02)',
                    boxShadow: 3
                  }
                }}
                onClick={() => handlePhotoClick(photo)}
              >
                <Box sx={{ position: 'relative', height: 200 }}>
                  {loadingImages[photo.id] !== false && (
                    <Box sx={{ 
                      position: 'absolute', 
                      top: '50%', 
                      left: '50%', 
                      transform: 'translate(-50%, -50%)',
                      zIndex: 1
                    }}>
                      <CircularProgress size={40} />
                    </Box>
                  )}
                  <CardMedia
                    component="img"
                    height="200"
                    image={photo.image_url || photo.image}
                    alt={photo.titre}
                    sx={{ 
                      objectFit: 'cover',
                      opacity: loadingImages[photo.id] !== false ? 0.3 : 1,
                      transition: 'opacity 0.3s'
                    }}
                    onLoad={() => handleImageLoad(photo.id)}
                    onError={() => handleImageError(photo.id)}
                    loading="lazy"
                  />
                </Box>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {photo.titre}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    {photo.description}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Chip 
                      label={photo.categorie_display} 
                      color={getCategorieColor(photo.categorie)}
                      size="small"
                    />
                    <Typography variant="caption" color="text.secondary">
                      {new Date(photo.date_realisation).toLocaleDateString('fr-FR')}
                    </Typography>
                  </Box>
                  
                  {/* Actions pour les patrons */}
                  {user && user.is_patron && (
                    <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                      <Tooltip title="Modifier">
                        <IconButton 
                          size="small" 
                          onClick={(e) => {
                            e.stopPropagation();
                            handleEditPhoto(photo);
                          }}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Supprimer">
                        <IconButton 
                          size="small" 
                          color="error"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDeletePhoto(photo.id);
                          }}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Dialog pour ajouter/modifier une photo */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editMode ? 'Modifier la photo' : 'Ajouter une photo'}
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Titre"
            value={formData.titre}
            onChange={(e) => setFormData({ ...formData, titre: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            margin="normal"
            multiline
            rows={3}
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Catégorie</InputLabel>
            <Select
              value={formData.categorie}
              onChange={(e) => setFormData({ ...formData, categorie: e.target.value })}
              label="Catégorie"
            >
              {Object.entries(categories).map(([key, value]) => (
                <MenuItem key={key} value={key}>{value}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            fullWidth
            label="Date de réalisation"
            type="date"
            value={formData.date_realisation}
            onChange={(e) => setFormData({ ...formData, date_realisation: e.target.value })}
            margin="normal"
            required
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            fullWidth
            label="Ordre d'affichage"
            type="number"
            value={formData.ordre_affichage}
            onChange={(e) => setFormData({ ...formData, ordre_affichage: parseInt(e.target.value) })}
            margin="normal"
          />
          <input
            accept="image/*"
            type="file"
            onChange={handleFileChange}
            style={{ marginTop: 16 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Annuler</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editMode ? 'Modifier' : 'Ajouter'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog pour afficher une photo en grand */}
      {selectedPhoto && (
        <Dialog 
          open={!!selectedPhoto} 
          onClose={() => setSelectedPhoto(null)}
          maxWidth="md"
          fullWidth
        >
          <DialogTitle>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              {selectedPhoto.titre}
              <IconButton onClick={() => setSelectedPhoto(null)}>
                <CloseIcon />
              </IconButton>
            </Box>
          </DialogTitle>
          <DialogContent>
            <img 
              src={selectedPhoto.image_url || selectedPhoto.image} 
              alt={selectedPhoto.titre}
              style={{ width: '100%', height: 'auto', maxHeight: '70vh', objectFit: 'contain' }}
            />
            <Typography variant="body1" sx={{ mt: 2 }}>
              {selectedPhoto.description}
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
              <Chip 
                label={selectedPhoto.categorie_display} 
                color={getCategorieColor(selectedPhoto.categorie)}
              />
              <Typography variant="body2" color="text.secondary">
                Réalisé le {new Date(selectedPhoto.date_realisation).toLocaleDateString('fr-FR')}
              </Typography>
            </Box>
          </DialogContent>
        </Dialog>
      )}
    </Box>
  );
};

export default Galerie; 
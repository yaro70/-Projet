import React, { useState, useEffect } from 'react';
import {
  Grid, Card, CardContent, CardMedia, Typography, 
  Chip, Skeleton, Box, Button
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Catalogue = () => {
  const navigate = useNavigate();
  const [gateaux, setGateaux] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingImages, setLoadingImages] = useState({});

  useEffect(() => {
    fetchGateaux();
  }, []);

  const fetchGateaux = async () => {
    try {
      setLoading(true);
      const response = await axios.get('https://patisserie-backend.onrender.com/api/public/gateaux/');
      setGateaux(response.data.gateaux || response.data);
    } catch (error) {
      console.error('Erreur lors du chargement du catalogue:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleImageLoad = (gateauId) => {
    setLoadingImages(prev => ({ ...prev, [gateauId]: false }));
  };

  const handleImageError = (gateauId) => {
    setLoadingImages(prev => ({ ...prev, [gateauId]: false }));
  };

  const getTypeColor = (type) => {
    const colors = {
      'anniversaire': 'primary',
      'mariage': 'secondary',
      'bapteme': 'success',
      'communion': 'info',
      'autre': 'default'
    };
    return colors[type] || 'default';
  };

  const handleCommander = (gateauId) => {
    navigate(`/commander/${gateauId}`);
  };

  if (loading) {
    return (
      <Grid container spacing={3}>
        {[...Array(6)].map((_, index) => (
          <Grid size={{ xs: 12, sm: 6, md: 4 }} key={index}>
            <Card>
              <Skeleton variant="rectangular" height={200} />
              <CardContent>
                <Skeleton variant="text" height={24} />
                <Skeleton variant="text" height={20} />
                <Skeleton variant="text" height={20} />
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    );
  }

  return (
    <Grid container spacing={3}>
      {gateaux.map((gateau) => (
        <Grid size={{ xs: 12, sm: 6, md: 4 }} key={gateau.id}>
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
            <Box sx={{ position: 'relative' }}>
              {loadingImages[gateau.id] !== false && (
                <Skeleton 
                  variant="rectangular" 
                  height={200} 
                  sx={{ position: 'absolute', top: 0, left: 0, right: 0, zIndex: 1 }}
                />
              )}
              <CardMedia
                component="img"
                height="200"
                image={gateau.image || '/images/gateau-placeholder.svg'}
                alt={gateau.nom}
                sx={{ 
                  objectFit: 'cover',
                  opacity: loadingImages[gateau.id] !== false ? 0.3 : 1,
                  transition: 'opacity 0.3s'
                }}
                onLoad={() => handleImageLoad(gateau.id)}
                onError={(e) => {
                  handleImageError(gateau.id);
                  e.target.src = '/images/gateau-placeholder.svg';
                }}
                loading="lazy"
              />
            </Box>
            <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
              <Typography variant="h6" gutterBottom>
                {gateau.nom}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2, flexGrow: 1 }}>
                {gateau.description}
              </Typography>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Chip 
                  label={gateau.type} 
                  color={getTypeColor(gateau.type)}
                  size="small"
                />
                <Typography variant="h6" color="primary" sx={{ fontWeight: 'bold' }}>
                  {parseFloat(gateau.prix).toLocaleString()} FCFA
                </Typography>
              </Box>
              <Button 
                variant="contained" 
                fullWidth
                onClick={() => handleCommander(gateau.id)}
                sx={{ 
                  borderRadius: 2,
                  py: 1.2
                }}
              >
                🛒 Commander
              </Button>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default Catalogue;

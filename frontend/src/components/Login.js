import React, { useState } from 'react';
import {
  Container,
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  Alert,
  CircularProgress
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

const Login = () => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login, updateUser } = useAuth();

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      console.log('🔍 Tentative de connexion avec:', credentials);
      
      // URL directe sans config
      const url = 'https://patisserie-backend.onrender.com/api/login/';
      console.log('🔍 URL:', url);
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials)
      });

      console.log('🔍 Status de la réponse:', response.status);
      console.log('🔍 Headers de la réponse:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        const errorData = await response.text();
        console.log('🔍 Erreur reçue:', errorData);
        setError(`Erreur ${response.status}: ${errorData}`);
        return;
      }

      const data = await response.json();
      console.log('🔍 Données reçues:', data);

      if (data.token) {
        // Mise à jour du contexte d'authentification
        const userData = {
          token: data.token,
          user_id: data.user_id,
          username: data.username,
          is_patron: data.is_patron,
          is_collaborateur: data.is_collaborateur
        };
        
        console.log('🔍 Données utilisateur:', userData);
        
        login(data.token, userData);
        updateUser(userData);
        
        // Redirection selon le rôle
        if (data.is_patron) {
          navigate('/patron/dashboard');
        } else if (data.is_collaborateur) {
          navigate('/collaborateur/dashboard');
        } else {
          navigate('/');
        }
      } else {
        setError('Token manquant dans la réponse');
      }
    } catch (err) {
      console.error('🔍 Erreur de connexion:', err);
      setError(`Erreur de connexion: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ px: { xs: 2, sm: 3 } }}>
      <Box
        sx={{
          mt: { xs: 4, sm: 8 },
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper elevation={3} sx={{ p: { xs: 3, sm: 4 }, width: '100%' }}>
          <Typography component="h1" variant="h4" align="center" gutterBottom>
            🎂 Pâtisserie
          </Typography>
          <Typography component="h2" variant="h6" align="center" color="textSecondary" gutterBottom>
            Connexion
          </Typography>
          
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Nom d'utilisateur"
              name="username"
              autoComplete="username"
              autoFocus
              value={credentials.username}
              onChange={handleChange}
              disabled={loading}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Mot de passe"
              type="password"
              id="password"
              autoComplete="current-password"
              value={credentials.password}
              onChange={handleChange}
              disabled={loading}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 1, mb: 1, py: 1.2, borderRadius: 2 }}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Se connecter'}
            </Button>
          </Box>
          
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Typography variant="body2" color="textSecondary">
              Identifiants de test:
            </Typography>
            <Typography variant="body2" color="textSecondary">
              admin / admin123
            </Typography>
            <Typography variant="body2" color="textSecondary">
              patron / patron123
            </Typography>
            <Typography variant="body2" color="textSecondary">
              collaborateur / collaborateur123
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default Login;

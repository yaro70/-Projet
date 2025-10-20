import React, { useState, useRef, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Card,
  CardContent,
  Alert,
  CircularProgress,
  IconButton,
  Chip
} from '@mui/material';
import {
  QrCodeScanner as QrCodeScannerIcon,
  Close as CloseIcon,
  Person as PersonIcon,
  Cake as CakeIcon,
  Phone as PhoneIcon,
  CalendarToday as CalendarIcon,
  AttachMoney as MoneyIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material';
import axios from 'axios';
import QrScanner from 'qr-scanner';

const QRCodeScanner = ({ open, onClose }) => {
  const [scanning, setScanning] = useState(false);
  const [scannedData, setScannedData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const videoRef = useRef(null);
  const qrScannerRef = useRef(null);

  useEffect(() => {
    if (open) {
      // Ne pas démarrer automatiquement, attendre le clic
    } else {
      stopScanning();
      setScannedData(null);
      setError(null);
    }
  }, [open]);

  const startScanning = async () => {
    try {
      setScanning(true);
      setError(null);
      
      if (!videoRef.current) {
        setError('Élément vidéo non trouvé');
        return;
      }

      // Créer le scanner QR
      qrScannerRef.current = new QrScanner(
        videoRef.current,
        (result) => {
          console.log('QR Code détecté:', result);
          handleScan(result.data);
        },
        {
          onDecodeError: (error) => {
            // Ignorer les erreurs de décodage (trop fréquentes)
            console.log('Erreur décodage QR:', error);
          },
          highlightScanRegion: true,
          highlightCodeOutline: true,
        }
      );

      await qrScannerRef.current.start();
    } catch (err) {
      console.error('Erreur démarrage scanner:', err);
      setError('Impossible d\'accéder à la caméra. Vérifiez les permissions.');
      setScanning(false);
    }
  };

  const stopScanning = () => {
    if (qrScannerRef.current) {
      qrScannerRef.current.stop();
      qrScannerRef.current.destroy();
      qrScannerRef.current = null;
    }
    setScanning(false);
  };

  const handleScan = async (qrData) => {
    try {
      setLoading(true);
      setError(null);
      
      // Envoyer les données du QR code au backend
      const response = await axios.post('https://patisserie-backend.onrender.com/api/qr-code/scan/', {
        qr_data: qrData
      }, {
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`
        }
      });
      
      if (response.data.success) {
        setScannedData(response.data.commande);
        stopScanning();
      } else {
        setError(response.data.error || 'QR code invalide');
      }
    } catch (err) {
      console.error('Erreur scan QR code:', err);
      setError(err.response?.data?.error || 'Erreur lors du scan du QR code');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    stopScanning();
    onClose();
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusColor = (status) => {
    const colors = {
      'en_attente': 'warning',
      'validee': 'success',
      'refusee': 'error',
      'terminee': 'info'
    };
    return colors[status] || 'default';
  };

  const getStatusText = (status) => {
    const texts = {
      'en_attente': 'En attente',
      'validee': 'Validée',
      'refusee': 'Refusée',
      'terminee': 'Terminée'
    };
    return texts[status] || status;
  };

  return (
    <Dialog 
      open={open} 
      onClose={handleClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: { minHeight: { xs: '100vh', sm: '500px' }, m: { xs: 0, sm: 2 }, borderRadius: { xs: 0, sm: 2 } }
      }}
    >
      <DialogTitle sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <QrCodeScannerIcon sx={{ mr: 1 }} />
          Scanner QR Code
        </Box>
        <IconButton onClick={handleClose}>
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent sx={{ p: { xs: 2, sm: 3 } }}>
        {!scannedData ? (
          <Box>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
            
            {scanning ? (
              <Box sx={{ textAlign: 'center' }}>
                <Box
                  sx={{
                    position: 'relative',
                    width: '100%',
                    maxWidth: '400px',
                    margin: '0 auto',
                    borderRadius: 2,
                    overflow: 'hidden',
                    border: '2px solid #1976d2'
                  }}
                >
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    style={{
                      width: '100%',
                      height: '300px',
                      objectFit: 'cover'
                    }}
                  />
                  {loading && (
                    <Box
                      sx={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        backgroundColor: 'rgba(0,0,0,0.5)'
                      }}
                    >
                      <CircularProgress color="primary" />
                    </Box>
                  )}
                </Box>
                
                <Typography variant="body2" sx={{ mt: 2, color: 'text.secondary' }}>
                  Pointez la caméra vers le QR code du client
                </Typography>
              </Box>
            ) : (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <QrCodeScannerIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Scanner QR Code
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  Cliquez sur "Démarrer le scan" pour scanner le QR code du client
                </Typography>
                <Button
                  variant="contained"
                  onClick={startScanning}
                  startIcon={<QrCodeScannerIcon />}
                  sx={{ backgroundColor: '#8B4513', '&:hover': { backgroundColor: '#A0522D' } }}
                >
                  Démarrer le scan
                </Button>
              </Box>
            )}
          </Box>
        ) : (
          <Box>
            <Alert severity="success" sx={{ mb: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <CheckIcon sx={{ mr: 1 }} />
                QR code scanné avec succès !
              </Box>
            </Alert>

            <Card sx={{ backgroundColor: '#f8f9fa' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <CakeIcon sx={{ mr: 1, color: '#8B4513' }} />
                  Informations de la commande
                </Typography>

                <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2, mb: 3 }}>
                  <Box>
                    <Typography variant="subtitle2" color="text.secondary">
                      ID Commande
                    </Typography>
                    <Typography variant="h6" color="primary">
                      #{scannedData.id}
                    </Typography>
                  </Box>
                  
                  <Box>
                    <Typography variant="subtitle2" color="text.secondary">
                      Statut
                    </Typography>
                    <Chip 
                      label={getStatusText(scannedData.status)}
                      color={getStatusColor(scannedData.status)}
                      size="small"
                    />
                  </Box>
                </Box>

                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Informations client
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <PersonIcon sx={{ mr: 1, fontSize: 20, color: 'text.secondary' }} />
                    <Typography variant="body1">{scannedData.client_nom}</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <PhoneIcon sx={{ mr: 1, fontSize: 20, color: 'text.secondary' }} />
                    <Typography variant="body1">{scannedData.client_telephone}</Typography>
                  </Box>
                </Box>

                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Détails du gâteau
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 1 }}>
                    <strong>{scannedData.gateau_nom}</strong>
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {scannedData.gateau_description}
                  </Typography>
                  {scannedData.texte_sur_gateau && (
                    <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
                      Texte sur gâteau: "{scannedData.texte_sur_gateau}"
                    </Typography>
                  )}
                </Box>

                <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2, mb: 3 }}>
                  <Box>
                    <Typography variant="subtitle2" color="text.secondary">
                      Date de livraison
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <CalendarIcon sx={{ mr: 1, fontSize: 20, color: 'text.secondary' }} />
                      <Typography variant="body1">
                        {formatDate(scannedData.date_livraison)}
                      </Typography>
                    </Box>
                  </Box>
                  
                  <Box>
                    <Typography variant="subtitle2" color="text.secondary">
                      Prix total
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <MoneyIcon sx={{ mr: 1, fontSize: 20, color: 'text.secondary' }} />
                      <Typography variant="h6" color="primary">
                        {parseFloat(scannedData.prix_total).toLocaleString()} FCFA
                      </Typography>
                    </Box>
                  </Box>
                </Box>

                {scannedData.livraison && (
                  <Alert severity="info" sx={{ mb: 2 }}>
                    🚚 Livraison à domicile incluse
                  </Alert>
                )}
              </CardContent>
            </Card>
          </Box>
        )}
      </DialogContent>

      <DialogActions>
        {scannedData ? (
          <Button onClick={() => setScannedData(null)}>
            Scanner un autre QR code
          </Button>
        ) : (
          <Button onClick={handleClose}>
            Fermer
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default QRCodeScanner;

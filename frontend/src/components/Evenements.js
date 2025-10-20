import React from 'react';
import { Container, Grid, Card, CardContent, Typography, Box } from '@mui/material';

const Evenements = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h3" gutterBottom>
          🗓️ Événements
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Découvrez nos dernières actualités et événements spéciaux
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {[...Array(6)].map((_, idx) => (
          <Grid key={idx} size={{ xs: 12, sm: 6, md: 4 }}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Événement à venir #{idx + 1}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Détails à venir...
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Evenements;
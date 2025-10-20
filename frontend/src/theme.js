import { createTheme } from '@mui/material/styles';

// Thème clair, couleurs douces et composants plus arrondis
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#7BA7FF', // bleu doux
      light: '#A9C5FF',
      dark: '#4D7ED6'
    },
    secondary: {
      main: '#FFAD66', // orange pastel
      light: '#FFC896',
      dark: '#D98C47'
    },
    background: {
      default: '#F7F9FC',
      paper: '#FFFFFF'
    },
    text: {
      primary: '#1F2A37',
      secondary: '#4B5563'
    },
    success: { main: '#72D39D' },
    warning: { main: '#F6C667' },
    info: { main: '#69C0FF' },
    error: { main: '#F28B82' }
  },
  shape: {
    borderRadius: 14
  },
  typography: {
    fontFamily: 'Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif',
    h4: { fontWeight: 700 },
    h5: { fontWeight: 600 },
    button: { textTransform: 'none', fontWeight: 600 }
  },
  components: {
    MuiButton: {
      defaultProps: { disableElevation: true },
      styleOverrides: {
        root: {
          borderRadius: 12,
          paddingInline: 18,
        },
        containedPrimary: {
          background: 'linear-gradient(135deg, #7BA7FF 0%, #69C0FF 100%)'
        },
        containedSecondary: {
          background: 'linear-gradient(135deg, #FFAD66 0%, #FFC896 100%)',
          color: '#1F2A37'
        }
      }
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 8px 24px rgba(31, 42, 55, 0.08)',
          transition: 'transform .15s ease, box-shadow .15s ease',
          ':hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 12px 28px rgba(31, 42, 55, 0.12)'
          }
        }
      }
    },
    MuiPaper: {
      styleOverrides: {
        rounded: { borderRadius: 16 }
      }
    },
    MuiTextField: {
      defaultProps: { size: 'medium' }
    },
    MuiChip: {
      styleOverrides: {
        root: { borderRadius: 10, fontWeight: 600 }
      }
    },
    MuiAppBar: {
      styleOverrides: {
        colorPrimary: {
          background: 'linear-gradient(135deg, #FFFFFF 0%, #F7F9FC 100%)',
          color: '#1F2A37',
          boxShadow: '0 4px 12px rgba(31, 42, 55, 0.06)'
        }
      }
    },
    MuiContainer: {
      defaultProps: { maxWidth: 'lg' }
    }
  }
});

export default theme;



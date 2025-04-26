import { createTheme } from "@mui/material/styles";

// Palette de couleurs moderne
const theme = createTheme({
  palette: {
    primary: {
      main: '#2563eb', // Bleu plus moderne et vibrant
      light: '#60a5fa',
      dark: '#1e40af',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#f97316', // Orange pour les accents et CTA
      light: '#fdba74',
      dark: '#c2410c',
      contrastText: '#ffffff',
    },
    error: {
      main: '#ef4444',
    },
    warning: {
      main: '#f59e0b',
    },
    info: {
      main: '#3b82f6',
    },
    success: {
      main: '#10b981',
    },
    background: {
      default: '#f8fafc',
      paper: '#ffffff',
    },
    text: {
      primary: '#1e293b',
      secondary: '#64748b',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
      lineHeight: 1.2,
    },
    h2: {
      fontWeight: 700,
      fontSize: '2rem',
      lineHeight: 1.2,
    },
    h3: {
      fontWeight: 600,
      fontSize: '1.75rem',
      lineHeight: 1.3,
    },
    h4: {
      fontWeight: 600,
      fontSize: '1.5rem',
      lineHeight: 1.3,
    },
    h5: {
      fontWeight: 600,
      fontSize: '1.25rem',
      lineHeight: 1.4,
    },
    h6: {
      fontWeight: 600,
      fontSize: '1rem',
      lineHeight: 1.4,
    },
    subtitle1: {
      fontSize: '1rem',
      lineHeight: 1.5,
      fontWeight: 500,
    },
    subtitle2: {
      fontSize: '0.875rem',
      lineHeight: 1.5,
      fontWeight: 500,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.5,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.5,
    },
    button: {
      fontWeight: 600,
      textTransform: 'none',
    },
  },
  shape: {
    borderRadius: 12,
  },
  shadows: [
    'none',
    '0px 2px 4px rgba(0, 0, 0, 0.05)',
    '0px 4px 6px rgba(0, 0, 0, 0.05)',
    '0px 6px 8px rgba(0, 0, 0, 0.05)',
    '0px 8px 12px rgba(0, 0, 0, 0.05)',
    '0px 10px 14px rgba(0, 0, 0, 0.05)',
    '0px 12px 16px rgba(0, 0, 0, 0.05)',
    '0px 14px 18px rgba(0, 0, 0, 0.05)',
    '0px 16px 20px rgba(0, 0, 0, 0.05)',
    '0px 18px 22px rgba(0, 0, 0, 0.05)',
    '0px 20px 24px rgba(0, 0, 0, 0.05)',
    '0px 22px 26px rgba(0, 0, 0, 0.05)',
    '0px 24px 28px rgba(0, 0, 0, 0.05)',
    '0px 26px 30px rgba(0, 0, 0, 0.05)',
    '0px 28px 32px rgba(0, 0, 0, 0.05)',
    '0px 30px 34px rgba(0, 0, 0, 0.05)',
    '0px 32px 36px rgba(0, 0, 0, 0.05)',
    '0px 34px 38px rgba(0, 0, 0, 0.05)',
    '0px 36px 40px rgba(0, 0, 0, 0.05)',
    '0px 38px 42px rgba(0, 0, 0, 0.05)',
    '0px 40px 44px rgba(0, 0, 0, 0.05)',
    '0px 42px 46px rgba(0, 0, 0, 0.05)',
    '0px 44px 48px rgba(0, 0, 0, 0.05)',
    '0px 46px 50px rgba(0, 0, 0, 0.05)',
    '0px 48px 52px rgba(0, 0, 0, 0.05)',
  ],
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          padding: '10px 24px',
          boxShadow: '0px 4px 14px rgba(0, 0, 0, 0.1)',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0px 6px 20px rgba(0, 0, 0, 0.15)',
          },
        },
        contained: {
          '&:hover': {
            backgroundColor: '#1e40af',
          },
        },
        outlined: {
          borderWidth: 2,
          '&:hover': {
            borderWidth: 2,
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.08)',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-5px)',
            boxShadow: '0px 8px 30px rgba(0, 0, 0, 0.12)',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 12,
            transition: 'all 0.3s ease',
            '&.Mui-focused': {
              boxShadow: '0px 0px 0px 3px rgba(37, 99, 235, 0.1)',
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: '0px 2px 10px rgba(0, 0, 0, 0.08)',
        },
      },
    },
  },
});

export default theme;

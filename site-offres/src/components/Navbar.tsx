import React, { useState, useEffect } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container,
  IconButton,
  Menu,
  MenuItem,
  useMediaQuery,
  useTheme,
  Badge,
  Slide,
  Snackbar,
  Alert
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import NotificationsIcon from "@mui/icons-material/Notifications";
import WorkIcon from "@mui/icons-material/Work";
import PersonIcon from "@mui/icons-material/Person";
import BookmarkIcon from "@mui/icons-material/Bookmark";

interface NavbarProps {
  onFeatureNotAvailable?: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ onFeatureNotAvailable }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [scrolled, setScrolled] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");

  // Gestion du défilement pour l'effet de transparence
  useEffect(() => {
    const handleScroll = () => {
      const offset = window.scrollY;
      if (offset > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  // Gestion du menu mobile
  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  // Gestionnaire pour les fonctionnalités non disponibles
  const handleFeatureNotAvailable = (featureName: string) => {
    // Si un gestionnaire externe est fourni, l'utiliser
    if (onFeatureNotAvailable) {
      onFeatureNotAvailable();
    } else {
      // Sinon, utiliser le Snackbar local
      setSnackbarMessage(`La fonctionnalité "${featureName}" sera disponible prochainement`);
      setSnackbarOpen(true);
    }
    // Fermer le menu mobile si ouvert
    if (anchorEl) {
      handleClose();
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  return (
    <>
      <Slide appear={false} direction="down" in={!scrolled}>
        <AppBar
          position="sticky"
          elevation={scrolled ? 4 : 0}
          sx={{
            backgroundColor: scrolled ? theme.palette.primary.main : "rgba(37, 99, 235, 0.95)",
            backdropFilter: "blur(8px)",
            transition: "all 0.3s ease",
          }}
        >
          <Container maxWidth="xl">
            <Toolbar
              sx={{
                display: "flex",
                justifyContent: "space-between",
                py: 1,
              }}
            >
              {/* Logo et titre */}
              <Box sx={{ display: "flex", alignItems: "center" }}>
                <Box
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    background: "rgba(255, 255, 255, 0.15)",
                    borderRadius: "12px",
                    p: 0.8,
                    mr: 1.5,
                  }}
                >
                  <WorkIcon sx={{ fontSize: 28, color: "#fff" }} />
                </Box>
                <Typography
                  variant="h6"
                  sx={{
                    fontWeight: 700,
                    letterSpacing: "0.5px",
                    background: "linear-gradient(90deg, #ffffff, #e0e7ff)",
                    backgroundClip: "text",
                    WebkitBackgroundClip: "text",
                    WebkitTextFillColor: "transparent",
                    textShadow: "0px 2px 4px rgba(0, 0, 0, 0.1)",
                  }}
                >
                  Offres d'emploi
                </Typography>
              </Box>

              {/* Navigation desktop */}
              {!isMobile && (
                <Box sx={{ display: "flex", alignItems: "center", gap: 3 }}>
                  <Button
                    color="inherit"
                    sx={{
                      fontWeight: 600,
                      opacity: 0.9,
                      "&:hover": { opacity: 1, transform: "translateY(-2px)" },
                    }}
                    onClick={() => handleFeatureNotAvailable("Accueil")}
                  >
                    Accueil
                  </Button>
                  <Button
                    color="inherit"
                    sx={{
                      fontWeight: 600,
                      opacity: 0.9,
                      "&:hover": { opacity: 1, transform: "translateY(-2px)" },
                    }}
                    onClick={() => handleFeatureNotAvailable("Entreprises")}
                  >
                    Entreprises
                  </Button>
                  <Button
                    color="inherit"
                    sx={{
                      fontWeight: 600,
                      opacity: 0.9,
                      "&:hover": { opacity: 1, transform: "translateY(-2px)" },
                    }}
                    onClick={() => handleFeatureNotAvailable("Conseils")}
                  >
                    Conseils
                  </Button>
                </Box>
              )}

              {/* Boutons d'action */}
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                {!isMobile && (
                  <>
                    <IconButton
                      color="inherit"
                      sx={{
                        backgroundColor: "rgba(255, 255, 255, 0.1)",
                        "&:hover": {
                          backgroundColor: "rgba(255, 255, 255, 0.2)",
                        },
                      }}
                      onClick={() => handleFeatureNotAvailable("Favoris")}
                    >
                      <BookmarkIcon />
                    </IconButton>
                    <IconButton
                      color="inherit"
                      sx={{
                        backgroundColor: "rgba(255, 255, 255, 0.1)",
                        "&:hover": {
                          backgroundColor: "rgba(255, 255, 255, 0.2)",
                        },
                      }}
                      onClick={() => handleFeatureNotAvailable("Notifications")}
                    >
                      <Badge badgeContent={3} color="secondary">
                        <NotificationsIcon />
                      </Badge>
                    </IconButton>
                  </>
                )}

                {!isMobile ? (
                  <Button
                    variant="contained"
                    color="secondary"
                    startIcon={<PersonIcon />}
                    onClick={() => handleFeatureNotAvailable("Connexion")}
                    sx={{
                      ml: 1,
                      fontWeight: 600,
                      backgroundColor: theme.palette.secondary.main,
                      "&:hover": {
                        backgroundColor: theme.palette.secondary.dark,
                      },
                    }}
                  >
                    Connexion
                  </Button>
                ) : (
                  <IconButton
                    edge="end"
                    color="inherit"
                    aria-label="menu"
                    onClick={handleMenu}
                    sx={{
                      backgroundColor: "rgba(255, 255, 255, 0.1)",
                      "&:hover": {
                        backgroundColor: "rgba(255, 255, 255, 0.2)",
                      },
                    }}
                  >
                    <MenuIcon />
                  </IconButton>
                )}

                {/* Menu mobile */}
                <Menu
                  id="menu-appbar"
                  anchorEl={anchorEl}
                  anchorOrigin={{
                    vertical: "bottom",
                    horizontal: "right",
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: "top",
                    horizontal: "right",
                  }}
                  open={Boolean(anchorEl)}
                  onClose={handleClose}
                >
                  <MenuItem onClick={() => handleFeatureNotAvailable("Accueil")}>Accueil</MenuItem>
                  <MenuItem onClick={() => handleFeatureNotAvailable("Entreprises")}>Entreprises</MenuItem>
                  <MenuItem onClick={() => handleFeatureNotAvailable("Conseils")}>Conseils</MenuItem>
                  <MenuItem onClick={() => handleFeatureNotAvailable("Favoris")}>Favoris</MenuItem>
                  <MenuItem onClick={() => handleFeatureNotAvailable("Notifications")}>Notifications</MenuItem>
                  <MenuItem onClick={() => handleFeatureNotAvailable("Connexion")}>Connexion</MenuItem>
                </Menu>
              </Box>
            </Toolbar>
          </Container>
        </AppBar>
      </Slide>

      {/* Snackbar pour les notifications de fonctionnalités non disponibles */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={4000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity="info" sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </>
  );
};

export default Navbar;

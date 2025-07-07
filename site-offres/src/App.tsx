import React, { useEffect, useState } from "react";
import { ThemeProvider, CssBaseline, Typography, Box } from "@mui/material";
import { Routes, Route, useLocation, Link } from "react-router-dom";
import theme from "./theme";
import OffreList from "./components/OffreList";
import Navbar from "./components/Navbar";
import Confidentialite from "./pages/Confidentialite";
import Conditions from "./pages/Conditions";
import Aide from "./pages/Aide";
import Contact from "./pages/Contact";

const App: React.FC = () => {
  const [, setScrolled] = useState(false);
  const location = useLocation();

  // Gestion du défilement pour les effets visuels
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

  // Remonter en haut de la page lors des changements de route
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location.pathname]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          position: "relative",
          minHeight: "100vh",
          width: "100%",
          maxWidth: "100vw", // Limite la largeur à la largeur de la fenêtre
          overflowX: "hidden",
          bgcolor: "#f8fafc",
          margin: "0 auto", // Centre le contenu
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* Éléments décoratifs de fond */}
        <Box
          sx={{
            position: "absolute",
            top: 0,
            right: 0,
            width: "50%",
            height: "500px",
            background: "radial-gradient(circle, rgba(37, 99, 235, 0.05) 0%, rgba(37, 99, 235, 0) 70%)",
            zIndex: 0,
            pointerEvents: "none",
          }}
        />
        <Box
          sx={{
            position: "absolute",
            bottom: "20%",
            left: 0,
            width: "30%",
            height: "300px",
            background: "radial-gradient(circle, rgba(249, 115, 22, 0.03) 0%, rgba(249, 115, 22, 0) 70%)",
            zIndex: 0,
            pointerEvents: "none",
          }}
        />

        {/* Navbar - pleine largeur */}
        <Navbar />
        
        {/* Contenu principal avec routes */}
        <Box 
          sx={{ 
            width: "100%",
            maxWidth: "1200px", // Largeur fixe maximale
            margin: "0 auto", // Centre le contenu
            px: { xs: 2, sm: 3, md: 4 },
            pb: 8,
            position: "relative",
            zIndex: 1,
            flex: 1,
          }}
        >
          <Routes>
            <Route path="/" element={<OffreList />} />
            <Route path="/confidentialite" element={<Confidentialite />} />
            <Route path="/conditions" element={<Conditions />} />
            <Route path="/aide" element={<Aide />} />
            <Route path="/contact" element={<Contact />} />
          </Routes>
        </Box>

        {/* Footer */}
        <Box
          component="footer"
          sx={{
            py: 4,
            px: { xs: 2, sm: 3, md: 4 },
            mt: "auto",
            backgroundColor: "#1e293b",
            color: "white",
            width: "100%",
          }}
        >
          <Box
            sx={{
              maxWidth: "1200px", // Largeur fixe maximale
              margin: "0 auto", // Centre le contenu
              width: "100%",
            }}
          >
            <Box
              sx={{
                display: "flex",
                flexDirection: { xs: "column", md: "row" },
                justifyContent: "space-between",
                alignItems: { xs: "flex-start", md: "center" },
                gap: 2,
              }}
            >
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                © {new Date().getFullYear()} HorsESN.fr - Tous droits réservés
              </Typography>
              <Box
                sx={{
                  display: "flex",
                  gap: { xs: 2, md: 4 },
                  flexWrap: "wrap",
                }}
              >
                <Typography 
                  variant="body2" 
                  component={Link} 
                  to="/confidentialite"
                  sx={{ 
                    opacity: 0.8, 
                    "&:hover": { opacity: 1 },
                    color: "inherit",
                    textDecoration: "none"
                  }}
                >
                  Confidentialité
                </Typography>
                <Typography 
                  variant="body2" 
                  component={Link} 
                  to="/conditions"
                  sx={{ 
                    opacity: 0.8, 
                    "&:hover": { opacity: 1 },
                    color: "inherit",
                    textDecoration: "none"
                  }}
                >
                  Conditions d'utilisation
                </Typography>
                <Typography 
                  variant="body2" 
                  component={Link} 
                  to="/aide"
                  sx={{ 
                    opacity: 0.8, 
                    "&:hover": { opacity: 1 },
                    color: "inherit",
                    textDecoration: "none"
                  }}
                >
                  Aide
                </Typography>
                <Typography 
                  variant="body2" 
                  component={Link} 
                  to="/contact"
                  sx={{ 
                    opacity: 0.8, 
                    "&:hover": { opacity: 1 },
                    color: "inherit",
                    textDecoration: "none"
                  }}
                >
                  Contact
                </Typography>
              </Box>
            </Box>
          </Box>
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default App;

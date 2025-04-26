import React, { useEffect, useState } from "react";
import { ThemeProvider, CssBaseline, Typography, Box, Container, useMediaQuery } from "@mui/material";
import theme from "./theme";
import OffreList from "./components/OffreList";
import Navbar from "./components/Navbar";

const App: React.FC = () => {
  const [scrolled, setScrolled] = useState(false);
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

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

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          position: "relative",
          minHeight: "100vh",
          width: "100%",
          overflowX: "hidden",
          bgcolor: "#f8fafc",
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

        {/* Contenu principal */}
        <Navbar />
        
        <Container 
          maxWidth="xl" 
          sx={{ 
            position: "relative", 
            zIndex: 1,
            px: { xs: 2, sm: 3, md: 4 },
            pb: 8,
          }}
        >
          <OffreList />
        </Container>

        {/* Footer */}
        <Box
          component="footer"
          sx={{
            py: 4,
            px: { xs: 2, sm: 3, md: 4 },
            mt: "auto",
            backgroundColor: "#1e293b",
            color: "white",
          }}
        >
          <Container maxWidth="xl">
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
                © {new Date().getFullYear()} Offres d'emploi - Tous droits réservés
              </Typography>
              <Box
                sx={{
                  display: "flex",
                  gap: { xs: 2, md: 4 },
                  flexWrap: "wrap",
                }}
              >
                <Typography variant="body2" sx={{ opacity: 0.8, "&:hover": { opacity: 1 } }}>
                  Confidentialité
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8, "&:hover": { opacity: 1 } }}>
                  Conditions d'utilisation
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8, "&:hover": { opacity: 1 } }}>
                  Aide
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8, "&:hover": { opacity: 1 } }}>
                  Contact
                </Typography>
              </Box>
            </Box>
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default App;

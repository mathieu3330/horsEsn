import React from "react";
import { ThemeProvider, CssBaseline, Typography, Box } from "@mui/material";
import theme from "./theme";
import OffreList from "./components/OffreList";
import Navbar from "./components/Navbar";

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Navbar />

      <Box
        sx={{
          bgcolor: "#f4f4f4",
          minHeight: "100vh",
          width: "100vw", // ← utilise 100% viewport réel
          overflowX: "hidden", // ← évite débordement horizontal
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          px: { xs: 2, sm: 4, md: 6 },
          pb: 4,
        }}
      >
        <Typography
          variant="h4"
          sx={{
            fontWeight: "bold",
            textAlign: "center",
            mt: 4,
            mb: 3,
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
          }}
        >
          <span style={{ color: "#1976d2" }}>Votre nouvel emploi,</span>&nbsp;
          <span style={{ color: "#333", fontWeight: 600 }}>
            offres disponibles dans toute la France
          </span>
        </Typography>

        <OffreList />
      </Box>
    </ThemeProvider>
  );
};

export default App;

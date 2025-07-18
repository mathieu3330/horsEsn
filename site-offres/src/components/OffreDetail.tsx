import React, { useState } from "react";
import {
  Dialog,
  DialogContent,
  Button,
  Typography,
  Box,
  Grid,
  Divider,
  Chip,
  Avatar,
  useTheme,
  useMediaQuery,
  IconButton,
  Snackbar,
  Alert,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import WorkIcon from "@mui/icons-material/Work";
import BusinessIcon from "@mui/icons-material/Business";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import CalendarTodayIcon from "@mui/icons-material/CalendarToday";
import ShareIcon from "@mui/icons-material/Share";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import BookmarkBorderIcon from "@mui/icons-material/BookmarkBorder";

            
const TITRES_SECTIONS = [
  "Description du poste",
  "Vos missions au quotidien",
  "Profil souhaité",
  "Concrètement, vous serez amené à",
  "Ce que nous recherchons",
  "Ce que vous apporterez",
  "Ce que nous offrons",
  "Les technologies utilisées",
  "Description de l'offre",
  "Avantages :",
  "Le saviez vous ?",
  "Plus précisément vous êtes en charge :",
  "De missions de terrain  :",
  "Vos missions :",
  "Vos principales missions :",
  "Vos missions",
  "VOTRE PROFIL :",
  "À propos de nous",
  "Rejoignez-nous"

];


interface OffreDetailProps {
  id?: number;
  titre?: string;
  contrat?: string;
  ville?: string;
  description?: string;
  dateoffre?: string;
  logo?: string;
  lien?: string; // Ajout du lien vers l'offre officielle
  open: boolean;
  onClose: () => void;
}

const OffreDetail: React.FC<OffreDetailProps> = ({
  titre = "Titre de l'offre",
  contrat = "CDI",
  ville = "Paris",
  description = "Description de l'offre d'emploi...",
  dateoffre = new Date().toISOString(),
  logo = "",
  lien = "",
  open,
  onClose,
}) => {
  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down("md"));
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");

  const handleApply = () => {
    // Rediriger vers le site officiel de l'offre
    if (lien) {
      window.open(lien, "_blank");
    } else {
      setSnackbarMessage("Lien vers l'offre non disponible");
      setSnackbarOpen(true);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullScreen={fullScreen}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: { xs: 0, sm: "20px" },
          overflow: "hidden",
        },
      }}
    >
      {/* En-tête */}
      <Box
        sx={{
          position: "relative",
          bgcolor: theme.palette.primary.main,
          color: "white",
          py: 4,
          px: 3,
        }}
      >
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{
            position: "absolute",
            right: 16,
            top: 16,
            color: "white",
            bgcolor: "rgba(255, 255, 255, 0.1)",
            "&:hover": {
              bgcolor: "rgba(255, 255, 255, 0.2)",
            },
          }}
        >
          <CloseIcon />
        </IconButton>

        <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
          {logo ? (
            <Avatar
              src={logo}
              alt="Logo entreprise"
              variant="rounded"
              sx={{
                width: 70,
                height: 70,
                mr: 2,
                bgcolor: "white",
                p: 1,
                borderRadius: "12px",
                boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)",
              }}
            />
          ) : (
            <Avatar
              variant="rounded"
              sx={{
                width: 70,
                height: 70,
                mr: 2,
                bgcolor: "rgba(255, 255, 255, 0.2)",
                borderRadius: "12px",
              }}
            >
              <BusinessIcon fontSize="large" />
            </Avatar>
          )}
          <Box>
            <Typography variant="h5" fontWeight="bold" gutterBottom>
              {titre}
            </Typography>
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
              <Chip
                icon={<WorkIcon style={{ color: "white" }} />}
                label={contrat}
                sx={{
                  bgcolor: "rgba(255, 255, 255, 0.15)",
                  color: "white",
                  fontWeight: 600,
                  borderRadius: "8px",
                }}
              />
              <Chip
                icon={<LocationOnIcon style={{ color: "white" }} />}
                label={ville}
                sx={{
                  bgcolor: "rgba(255, 255, 255, 0.15)",
                  color: "white",
                  fontWeight: 600,
                  borderRadius: "8px",
                }}
              />
            </Box>
          </Box>
        </Box>
      </Box>

      <DialogContent sx={{ px: { xs: 2, sm: 3 }, py: 3 }}>
        <Grid container spacing={4}>
          {/* Colonne principale */}
          <Grid item xs={12} md={8}>
            {/* Section Description */}
            <Box sx={{ mb: 4 }}>
              <Typography
                variant="h6"
                fontWeight="bold"
                sx={{
                  mb: 2,
                  pb: 1,
                  borderBottom: `2px solid ${theme.palette.primary.main}`,
                  display: "inline-block",
                }}
              >
                Description du poste
              </Typography>
            

<Box sx={{ color: "#334155", fontSize: "16px", lineHeight: 1.7 }}>
  {description.split("\n").map((line, idx) => {
    const trimmed = line.trim();
    const isTitle = TITRES_SECTIONS.some(title =>
      trimmed.toLowerCase().startsWith(title.toLowerCase())
    );

    return (
      <Typography
        key={idx}
        variant="body1"
        sx={{
          mb: trimmed === "" ? 2 : 1,
          fontWeight: isTitle ? "bold" : "normal"
        }}
      >
        {trimmed}
      </Typography>
    );
  })}
</Box>



            </Box>
          </Grid>

          {/* Colonne latérale */}
          <Grid item xs={12} md={4}>
            <Box
              sx={{
                bgcolor: "#f8fafc",
                borderRadius: "16px",
                p: 3,
                mb: 3,
                border: "1px solid #e2e8f0",
              }}
            >
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Détails de l'offre
              </Typography>
              <Divider sx={{ my: 2 }} />

              <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
                <Box sx={{ display: "flex", alignItems: "center" }}>
                  <Box
                    sx={{
                      mr: 2,
                      bgcolor: `${theme.palette.primary.main}15`,
                      borderRadius: "8px",
                      p: 1,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <WorkIcon color="primary" fontSize="small" />
                  </Box>
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Type de contrat
                    </Typography>
                    <Typography variant="body1" fontWeight="medium">
                      {contrat}
                    </Typography>
                  </Box>
                </Box>

                <Box sx={{ display: "flex", alignItems: "center" }}>
                  <Box
                    sx={{
                      mr: 2,
                      bgcolor: `${theme.palette.primary.main}15`,
                      borderRadius: "8px",
                      p: 1,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <LocationOnIcon color="primary" fontSize="small" />
                  </Box>
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Localisation
                    </Typography>
                    <Typography variant="body1" fontWeight="medium">
                      {ville}
                    </Typography>
                  </Box>
                </Box>

                <Box sx={{ display: "flex", alignItems: "center" }}>
                  <Box
                    sx={{
                      mr: 2,
                      bgcolor: `${theme.palette.primary.main}15`,
                      borderRadius: "8px",
                      p: 1,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <AttachMoneyIcon color="primary" fontSize="small" />
                  </Box>
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Salaire
                    </Typography>
                    <Typography variant="body1" fontWeight="medium">
                      Selon profil
                    </Typography>
                  </Box>
                </Box>

                <Box sx={{ display: "flex", alignItems: "center" }}>
                  <Box
                    sx={{
                      mr: 2,
                      bgcolor: `${theme.palette.primary.main}15`,
                      borderRadius: "8px",
                      p: 1,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <CalendarTodayIcon color="primary" fontSize="small" />
                  </Box>
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Date de publication
                    </Typography>
                    <Typography variant="body1" fontWeight="medium">
                      {new Date(dateoffre).toLocaleDateString("fr-FR", {
                        day: "numeric",
                        month: "long",
                        year: "numeric",
                      })}
                    </Typography>
                  </Box>
                </Box>
              </Box>

              <Divider sx={{ my: 2 }} />

              {/* Boutons d'action - Correction du bouton Sauvegarder selon la capture d'écran */}
              <Box sx={{ display: "flex", gap: 0.5 }}>
                <Button
                  variant="outlined"
                  startIcon={<BookmarkBorderIcon />}
                  size="small"
                  fullWidth
                  sx={{
                    borderRadius: "8px",
                    textTransform: "none",
                    fontWeight: 600,
                    borderWidth: "1.5px",
                  }}
                >
                  Sauvegarder
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<ShareIcon />}
                  size="small"
                  fullWidth
                  sx={{
                    borderRadius: "8px",
                    textTransform: "none",
                    fontWeight: 600,
                    borderWidth: "1.5px",
                  }}
                >
                  Partager
                </Button>
              </Box>
            </Box>

            {/* Bouton de candidature - Remplacé par un bouton qui redirige vers le site officiel */}
            <Box
              sx={{
                bgcolor: "#fff",
                borderRadius: "16px",
                p: 3,
                border: "1px solid #e2e8f0",
                boxShadow: "0 4px 20px rgba(0, 0, 0, 0.05)",
              }}
            >
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Postuler rapidement
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Cliquez sur le bouton ci-dessous pour postuler directement sur le site de l'entreprise.
              </Typography>

              <Button
                variant="contained"
                color="primary"
                fullWidth
                startIcon={<OpenInNewIcon />}
                onClick={handleApply}
                sx={{
                  py: 1.5,
                  borderRadius: "10px",
                  textTransform: "none",
                  fontWeight: 600,
                  boxShadow: "0 4px 14px rgba(37, 99, 235, 0.2)",
                }}
              >
                Postuler sur le site officiel
              </Button>
            </Box>
          </Grid>
        </Grid>
      </DialogContent>

      {/* Snackbar pour les notifications */}
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
    </Dialog>
  );
};

export default OffreDetail;

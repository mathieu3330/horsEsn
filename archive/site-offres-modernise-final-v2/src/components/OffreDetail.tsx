import React, { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  TextField,
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
import SendIcon from "@mui/icons-material/Send";
import BookmarkIcon from "@mui/icons-material/Bookmark";
import ShareIcon from "@mui/icons-material/Share";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";

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
  id,
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

  // Déterminer la couleur du badge de contrat
  const getContractColor = (type: string) => {
    switch (type.toLowerCase()) {
      case "cdi":
        return {
          bg: "#ecfdf5",
          color: "#059669",
          borderColor: "#a7f3d0",
        };
      case "cdd":
        return {
          bg: "#eff6ff",
          color: "#3b82f6",
          borderColor: "#bfdbfe",
        };
      case "stage":
        return {
          bg: "#fef3c7",
          color: "#d97706",
          borderColor: "#fde68a",
        };
      case "alternance":
        return {
          bg: "#f3e8ff",
          color: "#9333ea",
          borderColor: "#e9d5ff",
        };
      default:
        return {
          bg: "#f1f5f9",
          color: "#64748b",
          borderColor: "#cbd5e1",
        };
    }
  };

  const contractStyle = getContractColor(contrat);

  const handleSaveOffer = () => {
    setSnackbarMessage("Offre sauvegardée avec succès");
    setSnackbarOpen(true);
  };

  const handleShareOffer = () => {
    setSnackbarMessage("Fonctionnalité de partage sera disponible prochainement");
    setSnackbarOpen(true);
  };

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
              <Typography variant="body1" sx={{ whiteSpace: "pre-line", color: "#334155" }}>
                {description}
              </Typography>
            </Box>

            {/* Section Responsabilités */}
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
                Responsabilités
              </Typography>
              <ul style={{ paddingLeft: "20px", color: "#334155" }}>
                <li>Développer et maintenir des applications web modernes</li>
                <li>Collaborer avec les équipes produit et design</li>
                <li>Participer aux revues de code et aux sessions de pair programming</li>
                <li>Optimiser les performances des applications</li>
                <li>Rester à jour sur les nouvelles technologies et les meilleures pratiques</li>
              </ul>
            </Box>

            {/* Section Compétences */}
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
                Compétences requises
              </Typography>
              <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
                <Chip label="React" sx={{ bgcolor: "#f1f5f9", fontWeight: 500 }} />
                <Chip label="TypeScript" sx={{ bgcolor: "#f1f5f9", fontWeight: 500 }} />
                <Chip label="Material-UI" sx={{ bgcolor: "#f1f5f9", fontWeight: 500 }} />
                <Chip label="Node.js" sx={{ bgcolor: "#f1f5f9", fontWeight: 500 }} />
                <Chip label="Git" sx={{ bgcolor: "#f1f5f9", fontWeight: 500 }} />
                <Chip label="Agile/Scrum" sx={{ bgcolor: "#f1f5f9", fontWeight: 500 }} />
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
              <Box sx={{ display: "flex", gap: 1 }}>
                <Button
                  variant="outlined"
                  startIcon={<BookmarkIcon />}
                  size="large"
                  fullWidth
                  onClick={handleSaveOffer}
                  sx={{
                    borderRadius: "50px",
                    textTransform: "none",
                    fontWeight: 600,
                    borderWidth: "1.5px",
                    py: 1.2,
                    color: theme.palette.primary.main,
                    borderColor: theme.palette.primary.main,
                    backgroundColor: "transparent",
                    "&:hover": {
                      backgroundColor: `${theme.palette.primary.main}10`,
                      borderColor: theme.palette.primary.main,
                    }
                  }}
                >
                  Sauvegarder
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<ShareIcon />}
                  size="large"
                  fullWidth
                  onClick={handleShareOffer}
                  sx={{
                    borderRadius: "50px",
                    textTransform: "none",
                    fontWeight: 600,
                    borderWidth: "1.5px",
                    py: 1.2,
                    color: theme.palette.primary.main,
                    borderColor: theme.palette.primary.main,
                    backgroundColor: "transparent",
                    "&:hover": {
                      backgroundColor: `${theme.palette.primary.main}10`,
                      borderColor: theme.palette.primary.main,
                    }
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

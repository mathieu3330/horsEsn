import React from "react";
import {
  Card,
  CardContent,
  Typography,
  Box,
  Stack,
  useMediaQuery,
  useTheme,
  Chip,
  Button,
  Avatar,
  Divider,
  Fade,
} from "@mui/material";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import WorkIcon from "@mui/icons-material/Work";
import BookmarkBorderIcon from "@mui/icons-material/BookmarkBorder";
import SendIcon from "@mui/icons-material/Send";

interface OffreProps {
  titre: string;
  contrat: string;
  ville: string;
  description: string;
  dateoffre: string;
  logo?: string;
}

const OffreCard: React.FC<OffreProps> = ({
  titre,
  contrat,
  ville,
  description,
  dateoffre,
  logo,
}) => {
  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));

  const getNbJoursDepuis = (dateString: string): number => {
    const date = new Date(dateString);
    const today = new Date();
    const diffTime = today.getTime() - date.getTime();
    return Math.floor(diffTime / (1000 * 60 * 60 * 24));
  };

  const joursDepuis = getNbJoursDepuis(dateoffre);
  const isNew = joursDepuis <= 3;

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

  return (
    <Fade in={true} timeout={500}>
      <Card
        sx={{
          width: "100%",
          mb: 3,
          borderRadius: "16px",
          boxShadow: "0 10px 30px rgba(0, 0, 0, 0.05)",
          transition: "all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
          "&:hover": {
            boxShadow: "0 15px 35px rgba(0, 0, 0, 0.1)",
            transform: "translateY(-8px)",
          },
          border: "1px solid rgba(0, 0, 0, 0.05)",
          overflow: "hidden",
          position: "relative",
        }}
      >
        {/* Badge "Nouveau" si l'offre a moins de 3 jours */}
        {isNew && (
          <Box
            sx={{
              position: "absolute",
              top: 0,
              right: 0,
              backgroundColor: theme.palette.secondary.main,
              color: "white",
              py: 0.5,
              px: 2,
              borderBottomLeftRadius: "12px",
              fontWeight: "bold",
              fontSize: "0.75rem",
              zIndex: 1,
              boxShadow: "0 2px 8px rgba(249, 115, 22, 0.3)",
            }}
          >
            NOUVEAU
          </Box>
        )}

        <CardContent sx={{ p: { xs: 2, md: 3 } }}>
          <Stack
            direction={isSmallScreen ? "column" : "row"}
            justifyContent="space-between"
            alignItems={isSmallScreen ? "flex-start" : "center"}
            spacing={2}
          >
            <Box flex={1}>
              {/* En-tête avec logo */}
              <Box
                sx={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  mb: 2,
                  flexWrap: "wrap",
                  gap: 1,
                }}
              >
                <Box sx={{ flex: 1, minWidth: 0 }}>
                  <Typography
                    variant="h5"
                    color="primary"
                    fontWeight={700}
                    sx={{
                      wordBreak: "break-word",
                      lineHeight: 1.3,
                      mb: 0.5,
                    }}
                  >
                    {titre}
                  </Typography>
                </Box>

                {logo && (
                  <Avatar
                    src={logo}
                    alt="Logo entreprise"
                    variant="rounded"
                    sx={{
                      height: 60,
                      width: 60,
                      ml: 2,
                      boxShadow: "0 4px 12px rgba(0, 0, 0, 0.08)",
                      p: 1,
                      bgcolor: "white",
                      borderRadius: "12px",
                    }}
                  />
                )}
              </Box>

              {/* Informations principales */}
              <Box
                sx={{
                  display: "flex",
                  alignItems: "center",
                  flexWrap: "wrap",
                  gap: 1.5,
                  mb: 2,
                }}
              >
                {/* Type de contrat */}
                <Chip
                  icon={<WorkIcon style={{ color: contractStyle.color }} />}
                  label={contrat}
                  sx={{
                    bgcolor: contractStyle.bg,
                    color: contractStyle.color,
                    fontWeight: 600,
                    px: 1,
                    py: 2.5,
                    borderRadius: "8px",
                    border: `1px solid ${contractStyle.borderColor}`,
                    "& .MuiChip-label": {
                      px: 1,
                    },
                  }}
                />

                {/* Localisation */}
                <Box
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    bgcolor: "#f8fafc",
                    px: 1.5,
                    py: 0.75,
                    borderRadius: "8px",
                    border: "1px solid #e2e8f0",
                  }}
                >
                  <LocationOnIcon
                    sx={{ fontSize: 18, color: "#64748b", mr: 0.5 }}
                  />
                  <Typography
                    variant="body2"
                    sx={{ fontWeight: 500, color: "#334155" }}
                  >
                    {ville}
                  </Typography>
                </Box>

                {/* Date de publication */}
                <Box
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    bgcolor: "#f8fafc",
                    px: 1.5,
                    py: 0.75,
                    borderRadius: "8px",
                    border: "1px solid #e2e8f0",
                  }}
                >
                  <AccessTimeIcon
                    sx={{ fontSize: 18, color: "#64748b", mr: 0.5 }}
                  />
                  <Typography
                    variant="body2"
                    sx={{
                      fontWeight: 500,
                      color: isNew ? theme.palette.secondary.main : "#334155",
                    }}
                  >
                    il y a {joursDepuis} jours
                  </Typography>
                </Box>
              </Box>

              {/* Description */}
              <Typography
                variant="body2"
                color="text.secondary"
                sx={{
                  mb: 2.5,
                  lineHeight: 1.6,
                  color: "#475569",
                  display: "-webkit-box",
                  WebkitLineClamp: 3,
                  WebkitBoxOrient: "vertical",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                }}
              >
                {description}
              </Typography>

              {/* Boutons d'action */}
              <Divider sx={{ mb: 2 }} />
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  flexWrap: "wrap",
                  gap: 1,
                }}
              >
                <Button
                  variant="outlined"
                  color="primary"
                  startIcon={<BookmarkBorderIcon />}
                  size="small"
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
                  variant="contained"
                  color="primary"
                  endIcon={<SendIcon />}
                  size="small"
                  sx={{
                    borderRadius: "8px",
                    textTransform: "none",
                    fontWeight: 600,
                    boxShadow: "0 4px 14px rgba(37, 99, 235, 0.2)",
                  }}
                >
                  Postuler maintenant
                </Button>
              </Box>
            </Box>
          </Stack>
        </CardContent>
      </Card>
    </Fade>
  );
};

export default OffreCard;

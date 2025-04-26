import React from "react";
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  Stack,
  useMediaQuery,
  useTheme,
  Chip,
} from "@mui/material";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import WorkIcon from "@mui/icons-material/Work";

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

  return (
    <Card
      sx={{
        width: "100%",
        mb: 3,
        borderRadius: "16px",
        boxShadow: 3,
        transition: "all 0.3s ease",
        "&:hover": {
          boxShadow: 6,
          transform: "translateY(-3px)",
        },
        bgcolor: "#fff",
      }}
    >
      <CardContent>
        <Stack
          direction={isSmallScreen ? "column" : "row"}
          justifyContent="space-between"
          alignItems={isSmallScreen ? "flex-start" : "center"}
          spacing={2}
        >
          <Box flex={1}>
            {/* Titre avec logo à droite */}
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                mb: 1,
                flexWrap: "wrap",
                gap: 1,
              }}
            >
              <Typography
                variant="h6"
                color="primary"
                fontWeight={700}
                sx={{ flex: 1, minWidth: 0, wordBreak: "break-word" }}
              >
                {titre}
              </Typography>

              {logo && (
                <Box
                  component="img"
                  src={logo}
                  alt="Logo entreprise"
                  sx={{
                    height: 60,
                    width: "auto",
                    ml: 2,
                    objectFit: "contain",
                    maxWidth: 100,
                  }}
                />
              )}
            </Box>

            {/* Contrat + Ville */}
            <Box sx={{ display: "flex", alignItems: "center", flexWrap: "wrap", gap: 1 }}>
              <Chip
                icon={<WorkIcon />}
                label={contrat}
                variant="outlined"
                sx={{
                  bgcolor: "#f5f5f5",
                  fontWeight: 500,
                  px: 1,
                  py: 0.5,
                  borderRadius: "24px",
                }}
              />

              <Box sx={{ display: "flex", alignItems: "center", ml: 1 }}>
                <LocationOnIcon sx={{ fontSize: 18, color: "#1976d2", mr: 0.5 }} />
                <Typography variant="body2" color="text.primary">
                  {ville}
                </Typography>
              </Box>
            </Box>

            {/* Date */}
            <Box sx={{ display: "flex", alignItems: "center", mt: 1, color: "gray" }}>
              <AccessTimeIcon sx={{ fontSize: 18, mr: 1 }} />
              <Typography variant="body2" sx={{ color: "gray" }}>
                il y a {joursDepuis} jours{" "}
                {joursDepuis <= 3 && (
                  <Typography component="span" sx={{ color: "orange", fontWeight: 600 }}>
                    Nouvelle
                  </Typography>
                )}
              </Typography>
            </Box>

            {/* Description */}
            <Typography variant="body2" color="text.primary" mt={1}>
              {description.length > 160
                ? `${description.substring(0, 160)}...`
                : description}
            </Typography>
          </Box>

        </Stack>
      </CardContent>
    </Card>
  );
};

export default OffreCard;

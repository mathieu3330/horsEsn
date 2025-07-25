import React from "react";
import {
  Box,
  Typography,
  Button,
  Grid,
  useTheme,
  useMediaQuery,
  Paper,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import StarIcon from "@mui/icons-material/Star";

interface HeroSectionProps {
  onFeatureNotAvailable?: () => void;
  onExploreOffers?: () => void;
}

const HeroSection: React.FC<HeroSectionProps> = ({onExploreOffers }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));

  const handleExploreOffers = () => {
    if (onExploreOffers) {
      onExploreOffers();
    }
  };

  return (
    <Box
      sx={{
        position: "relative",
        overflow: "hidden",
        borderRadius: "16px",
        mb: 3,
        mt: 2,
        background: `linear-gradient(135deg, ${theme.palette.primary.dark} 0%, ${theme.palette.primary.main} 100%)`,
        boxShadow: "0 20px 40px rgba(37, 99, 235, 0.15)",
        width: "100%", // Assure que la section prend toute la largeur disponible
        maxWidth: "100%", // Empêche tout débordement
      }}
    >
      {/* Cercles décoratifs */}
      <Box
        sx={{
          position: "absolute",
          width: "300px",
          height: "300px",
          borderRadius: "50%",
          background: "rgba(255, 255, 255, 0.05)",
          top: "-150px",
          right: "-50px",
        }}
      />
      <Box
        sx={{
          position: "absolute",
          width: "200px",
          height: "200px",
          borderRadius: "50%",
          background: "rgba(255, 255, 255, 0.05)",
          bottom: "-100px",
          left: "10%",
        }}
      />

      <Box 
        sx={{
          margin: "0 auto", // Centre le contenu horizontalement
          width: "100%",
          maxWidth: "100%",
          px: { xs: 2, sm: 3, md: 4 },
        }}
      >
        <Grid container spacing={4} alignItems="center">
          <Grid item xs={12} md={7}>
            <Box sx={{ py: { xs: 3, md: 4 } }}>
              <Typography
                variant="h4"
                component="h1"
                sx={{
                  fontWeight: 800,
                  color: "white",
                  mb: 1.5,
                  textShadow: "0 2px 10px rgba(0, 0, 0, 0.1)",
                  fontSize: { xs: "1.5rem", sm: "1.8rem", md: "2.2rem" },
                  lineHeight: 1.2,
                }}
              >
                 En 1 clic, rejoignez l'élite des entreprises françaises et internationales, des postes 100% internes et hors ESN.
              </Typography>

              <Typography
                variant="body1"
                sx={{
                  color: "rgba(255, 255, 255, 0.9)",
                  mb: 2.5,
                  maxWidth: "600px",
                  lineHeight: 1.4,
                  fontSize: { xs: "0.9rem", sm: "1rem", md: "1.1rem" },
                }}
              >
                Des postes que vous ne verrez nulle part ailleurs.
              </Typography>

              <Box
                sx={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: 2,
                  mb: 2.5,
                }}
              >
                <Button
                  variant="contained"
                  color="secondary"
                  size="large"
                  startIcon={<SearchIcon />}
                  onClick={handleExploreOffers}
                  sx={{
                    py: 1.5,
                    px: 3,
                    fontWeight: 600,
                    fontSize: "1rem",
                    boxShadow: "0 8px 20px rgba(249, 115, 22, 0.3)",
                    "&:hover": {
                      transform: "translateY(-3px)",
                      boxShadow: "0 12px 25px rgba(249, 115, 22, 0.4)",
                    },
                  }}
                >
                  Explorer les offres
                </Button>
        
              </Box>



              {/* Badges statistiques */}
{/* Badges statistiques */}
{!isMobile && (
  <Box
    sx={{
      display: "flex",
      flexWrap: "nowrap",
      gap: { xs: 2, sm: 3 },
      mt: 1,
    }}
  >
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 1,
        minWidth: 160,
      }}
    >
      <Box
        sx={{
          bgcolor: "rgba(255, 255, 255, 0.2)",
          borderRadius: "50%",
          width: 40,
          height: 40,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <TrendingUpIcon sx={{ color: "white" }} />
      </Box>
      <Box>
        <Typography
          variant="h6"
          sx={{ color: "white", fontWeight: 700, lineHeight: 1.2 }}
        >
          +150000
        </Typography>
        <Typography
          variant="body2"
          sx={{ color: "rgba(255, 255, 255, 0.8)" }}
        >
          Offres disponibles
        </Typography>
      </Box>
    </Box>

    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 1,
        minWidth: 160,
      }}
    >
      <Box
        sx={{
          bgcolor: "rgba(255, 255, 255, 0.2)",
          borderRadius: "50%",
          width: 40,
          height: 40,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <StarIcon sx={{ color: "white" }} />
      </Box>
      <Box>
        <Typography
          variant="h6"
          sx={{ color: "white", fontWeight: 700, lineHeight: 1.2 }}
        >
          4.8/5
        </Typography>
        <Typography
          variant="body2"
          sx={{ color: "rgba(255, 255, 255, 0.8)" }}
        >
          Satisfaction candidats
        </Typography>
      </Box>
    </Box>
  </Box>
)}






            </Box>
          </Grid>

          {/* Image ou illustration */}
          {!isMobile && (
            <Grid item xs={12} md={5}>
              <Box
                sx={{
                  position: "relative",
                  height: "100%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <Paper
                  elevation={24}
                  sx={{
                    borderRadius: "20px",
                    overflow: "hidden",
                    transform: "rotate(3deg)",
                    width: "90%",
                    height: "auto",
                    position: "relative",
                    boxShadow: "0 20px 40px rgba(0, 0, 0, 0.2)",
                    border: "5px solid white",
                  }}
                >
                  {/* Simuler une interface d'application */}
                  <Box
                    sx={{
                      bgcolor: "#f8fafc",
                      p: 2,
                      borderTopLeftRadius: "16px",
                      borderTopRightRadius: "16px",
                      borderBottom: "1px solid #e2e8f0",
                      display: "flex",
                      alignItems: "center",
                      gap: 1,
                    }}
                  >
                    <Box
                      sx={{
                        width: 12,
                        height: 12,
                        borderRadius: "50%",
                        bgcolor: "#f87171",
                      }}
                    />
                    <Box
                      sx={{
                        width: 12,
                        height: 12,
                        borderRadius: "50%",
                        bgcolor: "#fbbf24",
                      }}
                    />
                    <Box
                      sx={{
                        width: 12,
                        height: 12,
                        borderRadius: "50%",
                        bgcolor: "#34d399",
                      }}
                    />
                    <Typography
                      variant="caption"
                      sx={{ ml: 1, color: "#64748b", fontWeight: 500 }}
                    >
                      Offres d'emploi - Tableau de bord
                    </Typography>
                  </Box>

                  <Box sx={{ p: 2, bgcolor: "white" }}>
                    {/* Simuler des cartes d'offres */}
                    {[1, 2, 3].map((item) => (
                      <Box
                        key={item}
                        sx={{
                          p: 2,
                          mb: 2,
                          borderRadius: "12px",
                          border: "1px solid #e2e8f0",
                          bgcolor: item === 1 ? "#f0f9ff" : "white",
                          boxShadow:
                            item === 1
                              ? "0 4px 12px rgba(0, 0, 0, 0.05)"
                              : "none",
                        }}
                      >
                        <Box
                          sx={{
                            display: "flex",
                            justifyContent: "space-between",
                            mb: 1,
                          }}
                        >
                          <Typography
                            variant="subtitle2"
                            sx={{ fontWeight: 600, color: "#334155" }}
                          >
                            {item === 1
                              ? "Ingénieur Développement"
                              : item === 2
                              ? "Chef de Projet Marketing"
                              : "Analyste Financier"}
                          </Typography>
                          <Box
                            sx={{
                              width: 30,
                              height: 30,
                              borderRadius: "8px",
                              bgcolor: "#f1f5f9",
                            }}
                          />
                        </Box>
                        <Box
                          sx={{
                            display: "flex",
                            gap: 1,
                            alignItems: "center",
                          }}
                        >
                          <Box
                            sx={{
                              px: 1,
                              py: 0.5,
                              borderRadius: "4px",
                              bgcolor: "#f1f5f9",
                              fontSize: "0.7rem",
                              color: "#64748b",
                            }}
                          >
                            {item === 1 ? "CDI" : item === 2 ? "CDD" : "Stage"}
                          </Box>
                          <Typography
                            variant="caption"
                            sx={{ color: "#64748b" }}
                          >
                            {item === 1
                              ? "Paris"
                              : item === 2
                              ? "Lyon"
                              : "Bordeaux"}
                          </Typography>
                        </Box>
                      </Box>
                    ))}
                  </Box>
                </Paper>
              </Box>
            </Grid>
          )}
        </Grid>
      </Box>
    </Box>
  );
};

export default HeroSection;

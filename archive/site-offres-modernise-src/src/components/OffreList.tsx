import React, { useEffect, useState } from "react";
import axios from "axios";
import { 
  Container, 
  CircularProgress, 
  Box, 
  Typography, 
  Paper,
  Grid,
  Button,
  Fade,
  Grow,
  Pagination,
  Skeleton,
  useTheme,
  Dialog
} from "@mui/material";
import OffreCard from "./OffreCard";
import FilterBar from "./FilterBar";
import HeroSection from "./HeroSection";
import OffreDetail from "./OffreDetail";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import WorkIcon from "@mui/icons-material/Work";
import BusinessIcon from "@mui/icons-material/Business";

interface Offre {
  id: number;
  titre: string;
  contrat: string;
  ville: string;
  description: string;
  dateoffre: string;
  logo: string;
}

const OffreList: React.FC = () => {
  const theme = useTheme();
  const [offres, setOffres] = useState<Offre[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ search: "", ville: "", contrat: "" });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [showStats, setShowStats] = useState(false);
  const [selectedOffre, setSelectedOffre] = useState<Offre | null>(null);
  const [detailOpen, setDetailOpen] = useState(false);

  useEffect(() => {
    const fetchOffres = async () => {
      try {
        setLoading(true);
        // Simuler un délai de chargement pour montrer les animations
        setTimeout(async () => {
          try {
            const response = await axios.get(
              `/api/offres?search=${encodeURIComponent(filters.search)}&contrat=${filters.contrat}&ville=${filters.ville}&page=${page}`
            );
            setOffres(response.data.offres);
            setTotalPages(response.data.totalPages || 1);
          } catch (error) {
            console.error("Erreur API :", error);
            // Données de démonstration en cas d'erreur API
            setOffres([
              {
                id: 1,
                titre: "ALTERNANCE - MODELISATION DE LA DISPERSION DE POLLUANT EN CHAMP PROCHE",
                contrat: "Alternance",
                ville: "Paris",
                description: "Pour réussir à intégrer les métiers de l'électricité et des énergies renouvelables, TotalEnergies a créé une nouvelle entité OneTech qui regroupe l'ensemble des...",
                dateoffre: "2025-03-03",
                logo: "https://www.totalenergies.fr/typo3conf/ext/theme_totalenergies/Resources/Public/images/logo-totalenergies.svg"
              },
              {
                id: 2,
                titre: "Assistant administratif et commercial (H/F)",
                contrat: "CDI",
                ville: "Lyon",
                description: "TotalEnergies est une compagnie multi-énergies mondiale de production et de fourniture d'énergies : pétrole et biocarburants, gaz naturel et gaz verts, renouvel...",
                dateoffre: "2025-03-01",
                logo: "https://www.totalenergies.fr/typo3conf/ext/theme_totalenergies/Resources/Public/images/logo-totalenergies.svg"
              },
              {
                id: 3,
                titre: "LNG & Cryogenics Process Engineer M/F",
                contrat: "CDI",
                ville: "Marseille",
                description: "Rejoignez une équipe dynamique dans le secteur de l'énergie pour travailler sur des projets innovants liés au GNL et aux processus cryogéniques...",
                dateoffre: "2025-04-01",
                logo: "https://www.totalenergies.fr/typo3conf/ext/theme_totalenergies/Resources/Public/images/logo-totalenergies.svg"
              }
            ]);
            setTotalPages(3);
          } finally {
            setLoading(false);
            // Afficher les statistiques après le chargement
            setTimeout(() => setShowStats(true), 300);
          }
        }, 800);
      } catch (error) {
        console.error("Erreur API :", error);
        setLoading(false);
      }
    };

    fetchOffres();
  }, [filters, page]);

  const handlePageChange = (event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
    // Remonter en haut de la liste
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleOpenDetail = (offre: Offre) => {
    setSelectedOffre(offre);
    setDetailOpen(true);
  };

  const handleCloseDetail = () => {
    setDetailOpen(false);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 0, pb: 8 }}>
      {/* Section Hero */}
      <HeroSection />
      
      {/* Barre de filtres */}
      <FilterBar onFilter={(search, ville, contrat) => {
        setFilters({ search, ville, contrat });
        setPage(1); // Réinitialiser à la première page lors d'un changement de filtre
      }} />

      {/* Statistiques */}
      <Fade in={showStats} timeout={1000}>
        <Box sx={{ mb: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Paper
                elevation={0}
                sx={{
                  p: 2,
                  borderRadius: "16px",
                  height: "100%",
                  display: "flex",
                  alignItems: "center",
                  border: "1px solid #e2e8f0",
                  background: "linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)",
                  transition: "transform 0.3s ease",
                  "&:hover": {
                    transform: "translateY(-5px)",
                  }
                }}
              >
                <Box
                  sx={{
                    bgcolor: theme.palette.primary.main,
                    color: "white",
                    p: 1.5,
                    borderRadius: "12px",
                    mr: 2,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <WorkIcon fontSize="large" />
                </Box>
                <Box>
                  <Typography variant="h4" fontWeight="bold" color="primary">
                    1,248
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Offres disponibles
                  </Typography>
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12} md={4}>
              <Paper
                elevation={0}
                sx={{
                  p: 2,
                  borderRadius: "16px",
                  height: "100%",
                  display: "flex",
                  alignItems: "center",
                  border: "1px solid #e2e8f0",
                  background: "linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)",
                  transition: "transform 0.3s ease",
                  "&:hover": {
                    transform: "translateY(-5px)",
                  }
                }}
              >
                <Box
                  sx={{
                    bgcolor: theme.palette.success.main,
                    color: "white",
                    p: 1.5,
                    borderRadius: "12px",
                    mr: 2,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <BusinessIcon fontSize="large" />
                </Box>
                <Box>
                  <Typography variant="h4" fontWeight="bold" color="success.main">
                    342
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Entreprises partenaires
                  </Typography>
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12} md={4}>
              <Paper
                elevation={0}
                sx={{
                  p: 2,
                  borderRadius: "16px",
                  height: "100%",
                  display: "flex",
                  alignItems: "center",
                  border: "1px solid #e2e8f0",
                  background: "linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%)",
                  transition: "transform 0.3s ease",
                  "&:hover": {
                    transform: "translateY(-5px)",
                  }
                }}
              >
                <Box
                  sx={{
                    bgcolor: theme.palette.secondary.main,
                    color: "white",
                    p: 1.5,
                    borderRadius: "12px",
                    mr: 2,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <TrendingUpIcon fontSize="large" />
                </Box>
                <Box>
                  <Typography variant="h4" fontWeight="bold" color="secondary.main">
                    +124
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Nouvelles offres cette semaine
                  </Typography>
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </Box>
      </Fade>

      {/* Titre de section */}
      <Box sx={{ mb: 3, mt: 5 }}>
        <Typography 
          variant="h5" 
          fontWeight="bold"
          sx={{
            position: "relative",
            display: "inline-block",
            "&:after": {
              content: '""',
              position: "absolute",
              bottom: "-8px",
              left: 0,
              width: "60px",
              height: "4px",
              backgroundColor: theme.palette.primary.main,
              borderRadius: "2px",
            }
          }}
        >
          Offres d'emploi
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
          {loading 
            ? "Recherche des meilleures opportunités pour vous..." 
            : `${offres.length} résultats trouvés pour votre recherche`}
        </Typography>
      </Box>

      {/* Liste des offres */}
      {loading ? (
        // Squelettes de chargement
        Array.from(new Array(3)).map((_, index) => (
          <Box key={index} sx={{ mb: 3 }}>
            <Skeleton variant="rectangular" width="100%" height={200} sx={{ borderRadius: "16px" }} />
          </Box>
        ))
      ) : offres.length === 0 ? (
        // Message si aucune offre trouvée
        <Paper
          sx={{
            p: 4,
            borderRadius: "16px",
            textAlign: "center",
            bgcolor: "#f8fafc",
            border: "1px dashed #cbd5e1",
          }}
        >
          <Typography variant="h6" color="text.secondary" gutterBottom>
            Aucune offre ne correspond à votre recherche
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Essayez de modifier vos critères de recherche ou consultez nos suggestions ci-dessous
          </Typography>
          <Button 
            variant="contained" 
            color="primary"
            onClick={() => setFilters({ search: "", ville: "", contrat: "" })}
          >
            Voir toutes les offres
          </Button>
        </Paper>
      ) : (
        // Liste des offres
        <Box>
          {offres.map((offre, index) => (
            <Grow
              key={offre.id}
              in={true}
              timeout={(index + 1) * 300}
              style={{ transformOrigin: '0 0 0' }}
            >
              <Box onClick={() => handleOpenDetail(offre)} sx={{ cursor: 'pointer' }}>
                <OffreCard
                  titre={offre.titre}
                  contrat={offre.contrat}
                  ville={offre.ville}
                  description={offre.description}
                  dateoffre={offre.dateoffre}
                  logo={offre.logo}
                />
              </Box>
            </Grow>
          ))}
          
          {/* Pagination */}
          {totalPages > 1 && (
            <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
              <Pagination 
                count={totalPages} 
                page={page} 
                onChange={handlePageChange} 
                color="primary"
                size="large"
                sx={{
                  '& .MuiPaginationItem-root': {
                    borderRadius: '8px',
                    fontWeight: 500,
                  },
                }}
              />
            </Box>
          )}
        </Box>
      )}

      {/* Modal de détail d'offre */}
      {selectedOffre && (
        <OffreDetail
          open={detailOpen}
          onClose={handleCloseDetail}
          id={selectedOffre.id}
          titre={selectedOffre.titre}
          contrat={selectedOffre.contrat}
          ville={selectedOffre.ville}
          description={selectedOffre.description}
          dateoffre={selectedOffre.dateoffre}
          logo={selectedOffre.logo}
        />
      )}
    </Container>
  );
};

export default OffreList;

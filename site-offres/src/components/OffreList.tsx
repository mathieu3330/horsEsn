import React, { useEffect, useState, useRef, useCallback } from "react";
import axios from "axios";
import { 
  Box, 
  CircularProgress, 
  Typography, 
  Paper,
  Grid,
  Button,
  Skeleton,
  useTheme,
  Snackbar,
  Alert
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
  nomclient: string;
  contrat: string;
  ville: string;
  description: string;
  dateoffre: string;
  logo: string;
  lien?: string; // Ajout du champ lien pour rediriger vers le site officiel
}

const OffreList: React.FC = () => {
  const theme = useTheme();
  const [offres, setOffres] = useState<Offre[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [filters, setFilters] = useState({ search: "", ville: "", contrat: "", secteur: "", teletravail: "" });
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [showStats, setShowStats] = useState(false);
  const [selectedOffre, setSelectedOffre] = useState<Offre | null>(null);
  const [detailOpen, setDetailOpen] = useState(false);
  const [featureNotAvailableOpen, setFeatureNotAvailableOpen] = useState(false);
  const [filtersApplied, setFiltersApplied] = useState(false);
  
  // Référence pour éviter les appels API redondants pendant le défilement
  const isLoadingRef = useRef(false);
  
  // Observer pour détecter quand l'utilisateur atteint le dernier élément
  const observer = useRef<IntersectionObserver | null>(null);
  const lastOffreElementRef = useCallback((node: HTMLDivElement | null) => {
    if (loading || loadingMore || !hasMore) return;
    if (observer.current) observer.current.disconnect();
    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && hasMore && !isLoadingRef.current) {
        setPage(prevPage => prevPage + 1);
      }
    }, { 
      threshold: 0.1,  // Déclencher plus tôt pour une expérience plus fluide
      rootMargin: '200px' // Précharger avant d'atteindre le bas
    });
    if (node) observer.current.observe(node);
  }, [loading, loadingMore, hasMore]);

  // Fonction pour récupérer les offres avec debounce
  useEffect(() => {
    // Ne pas charger les offres si aucun filtre n'est appliqué
    if (!filtersApplied) {
      setOffres([]);
      setLoading(false);
      return;
    }
    
    const fetchOffres = async () => {
      try {
        // Éviter les appels redondants
        if (isLoadingRef.current) return;
        isLoadingRef.current = true;
        
        if (page === 1) {
          setLoading(true);
          setOffres([]);
        } else {
          setLoadingMore(true);
        }
        
        // Construire l'URL avec les paramètres
        const searchParams = new URLSearchParams();
        if (filters.search) searchParams.append('search', filters.search);
        if (filters.contrat) searchParams.append('contrat', filters.contrat);
        if (filters.ville) searchParams.append('ville', filters.ville);
        if (filters.secteur) searchParams.append('secteur', filters.secteur);
        if (filters.teletravail) searchParams.append('teletravail', filters.teletravail);
        searchParams.append('page', page.toString());
        searchParams.append('limit', '20');
        
        const apiUrl = `https://api-offres-145837535580.us-central1.run.app/offres?${searchParams.toString()}`;
        
        try {
          const response = await axios.get(apiUrl);
          
          if (page === 1) {
            setOffres(response.data.offres || []);
          } else {
            // Éviter les doublons en vérifiant les IDs
            const newOffres = response.data.offres || [];
            const existingIds = new Set(offres.map(o => o.id));
            const uniqueNewOffres = newOffres.filter((o: Offre) => !existingIds.has(o.id));
            
            setOffres(prevOffres => [...prevOffres, ...uniqueNewOffres]);
          }
          
          // Vérifier s'il y a plus de résultats à charger
          const receivedCount = response.data.offres ? response.data.offres.length : 0;
          setHasMore(receivedCount === 20);
        } catch (error) {
          console.error("Erreur API :", error);
          // Données de démonstration en cas d'erreur API
          const demoOffres = [
            {
              id: 3,
              titre: "LNG & Cryogenics Process Engineer M/F",
              nomclient: "EDF",
              contrat: "CDI",
              ville: "Marseille",
              description: "Rejoignez une équipe dynamique dans le secteur de l'énergie pour travailler sur des projets innovants liés au GNL et aux processus cryogéniques...",
              dateoffre: "2025-04-01",
              logo: "https://www.totalenergies.fr/typo3conf/ext/theme_totalenergies/Resources/Public/images/logo-totalenergies.svg",
              lien: "https://www.totalenergies.fr/carrieres/nos-offres"
            }
          ];
          
          if (page === 1) {
            setOffres(demoOffres);
          } else if (page <= 3) {
            // Simuler plus de données pour les tests
            const newDemoOffres = demoOffres.map((offre, index) => ({
              ...offre,
              id: offre.id + (page - 1) * 3 + index * 100
            }));
            setOffres(prevOffres => [...prevOffres, ...newDemoOffres]);
          }
          
          // Simuler qu'il n'y a plus de données après la page 3
          setHasMore(page < 3);
        } finally {
          if (page === 1) {
            setLoading(false);
          } else {
            setLoadingMore(false);
          }
          // Afficher les statistiques immédiatement pour éviter l'effet de disparition
          setShowStats(true);
          
          // Réinitialiser le flag de chargement
          setTimeout(() => {
            isLoadingRef.current = false;
          }, 300); // Petit délai pour éviter les appels trop rapprochés
        }
      } catch (error) {
        console.error("Erreur API :", error);
        if (page === 1) {
          setLoading(false);
        } else {
          setLoadingMore(false);
        }
        isLoadingRef.current = false;
      }
    };

    fetchOffres();
  }, [filters, page, filtersApplied]);

  const handleOpenDetail = (offre: Offre) => {
    setSelectedOffre(offre);
    setDetailOpen(true);
  };

  const handleCloseDetail = () => {
    setDetailOpen(false);
  };

  const handleFeatureNotAvailable = () => {
    setFeatureNotAvailableOpen(true);
  };

  const handleCloseFeatureNotAvailable = () => {
    setFeatureNotAvailableOpen(false);
  };

  const resetFilters = () => {
    setFilters({ search: "", ville: "", contrat: "", secteur: "", teletravail: "" });
    setPage(1);
    setHasMore(true);
    setFiltersApplied(false);
  };

  return (
    <Box sx={{ width: "100%", maxWidth: "100%" }}>
      {/* Section Hero */}
      <HeroSection 
        onFeatureNotAvailable={handleFeatureNotAvailable}
        onExploreOffers={() => {
          // Déclencher l'affichage de toutes les offres (recherche vide)
          setFilters({ search: "", ville: "", contrat: "", secteur: "", teletravail: "" });
          setPage(1);
          setHasMore(true);
          setFiltersApplied(true);
          
          // Scroll automatique vers les offres après un petit délai
          setTimeout(() => {
            const offresSection = document.querySelector('[data-section="offres"]');
            if (offresSection) {
              offresSection.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
              });
            }
          }, 300);
        }}
      />
      
      {/* Barre de filtres */}
      <Box sx={{ width: "100%", maxWidth: "100%" }}>
        <FilterBar onFilter={(search, ville, contrat, secteur, teletravail) => {
          setFilters({ search, ville, contrat, secteur, teletravail });
          setPage(1); // Réinitialiser à la première page lors d'un changement de filtre
          setHasMore(true); // Réinitialiser hasMore
          setFiltersApplied(true); // Marquer que les filtres ont été appliqués
        }} />
      </Box>

      {/* Statistiques - Suppression de l'effet Fade pour éviter la disparition */}
      <Box sx={{ mb: 2, width: "100%", display: showStats && filtersApplied ? 'block' : 'none' }}>
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
                  +150000
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
                  899
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
                  +2364
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Nouvelles offres cette semaine
                </Typography>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Box>

      {/* Titre de section */}
      <Box sx={{ mb: 2, mt: 3, width: "100%" }} data-section="offres">
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
            : filtersApplied 
              ? `Découvrez davantage d'offres en parcourant la page vers le bas`
              : "Utilisez les filtres ci-dessus pour trouver des offres d'emploi"}
        </Typography>
      </Box>

      {/* Message initial quand aucun filtre n'est appliqué */}
      {!filtersApplied && (
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
            Bienvenue sur notre plateforme de recherche d'emploi
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Utilisez les filtres ci-dessus et cliquez sur "Trouver" pour découvrir les offres qui correspondent à vos critères
          </Typography>
        </Paper>
      )}

      {/* Liste des offres - Suppression des effets Grow pour éviter la disparition progressive */}
      {filtersApplied && (
        <Box sx={{ width: "100%" }}>
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
                onClick={resetFilters}
              >
                Voir toutes les offres
              </Button>
            </Paper>
          ) : (
            // Liste des offres - sans animation Grow
            <Box>
              {offres.map((offre, index) => {
                // Si c'est le dernier élément et qu'il y a potentiellement plus d'offres à charger
                if (index === offres.length - 1 && hasMore) {
                  return (
                    <Box 
                      key={offre.id} 
                      ref={lastOffreElementRef}
                      onClick={() => handleOpenDetail(offre)} 
                      sx={{ cursor: 'pointer', mb: 3 }}
                    >
                      <OffreCard
                        titre={offre.titre}
                        nomclient={offre.nomclient}
                        contrat={offre.contrat}
                        ville={offre.ville}
                        description={offre.description}
                        dateoffre={offre.dateoffre}
                        logo={offre.logo}
                      />
                    </Box>
                  );
                } else {
                  return (
                    <Box 
                      key={offre.id} 
                      onClick={() => handleOpenDetail(offre)} 
                      sx={{ cursor: 'pointer', mb: 3 }}
                    >
                      <OffreCard
                        titre={offre.titre}
                        nomclient={offre.nomclient}
                        contrat={offre.contrat}
                        ville={offre.ville}
                        description={offre.description}
                        dateoffre={offre.dateoffre}
                        logo={offre.logo}
                      />
                    </Box>
                  );
                }
              })}
            </Box>
          )}
        </Box>
      )}

      {/* Indicateur de chargement pour "charger plus" */}
      {loadingMore && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress color="primary" />
        </Box>
      )}

      {/* Détail de l'offre */}
      {selectedOffre && (
        <OffreDetail
          id={selectedOffre.id}
          titre={selectedOffre.titre}
          contrat={selectedOffre.contrat}
          ville={selectedOffre.ville}
          description={selectedOffre.description}
          dateoffre={selectedOffre.dateoffre}
          logo={selectedOffre.logo}
          lien={selectedOffre.lien}
          open={detailOpen}
          onClose={handleCloseDetail}
        />
      )}

      {/* Snackbar pour les fonctionnalités non disponibles */}
      <Snackbar
        open={featureNotAvailableOpen}
        autoHideDuration={4000}
        onClose={handleCloseFeatureNotAvailable}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseFeatureNotAvailable} severity="info" sx={{ width: '100%' }}>
          Cette fonctionnalité sera disponible prochainement
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default OffreList;

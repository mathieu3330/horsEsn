import React, { useState, useEffect } from "react";
import {
  Button,
  MenuItem,
  Select,
  InputAdornment,
  Box,
  Paper,
  Chip,
  Typography,
  Collapse,
  FormControl,
  InputLabel,
  useTheme,
  Snackbar,
  Alert
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ExpandLessIcon from "@mui/icons-material/ExpandLess";
import WorkIcon from "@mui/icons-material/Work";
import BusinessIcon from "@mui/icons-material/Business";
import LaptopIcon from "@mui/icons-material/Laptop";
import ClearIcon from "@mui/icons-material/Clear";
import Autocomplete from "./Autocomplete";
import { fetchEmploiSuggestions, fetchRegionSuggestions, fetchPopularSuggestions } from "../api";

interface FilterBarProps {
  onFilter: (search: string, ville: string, contrat: string, secteur: string, teletravail: string) => void;
}

const FilterBar: React.FC<FilterBarProps> = ({ onFilter }) => {
  const theme = useTheme();
  const [search, setSearch] = useState("");
  const [ville, setVille] = useState("");
  const [contrat, setContrat] = useState("");
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [secteur, setSecteur] = useState("");
  const [teletravail, setTeletravail] = useState("");
  const [activeFilters, setActiveFilters] = useState<string[]>([]);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [popularEmplois, setPopularEmplois] = useState<string[]>([]);
  const [popularRegions, setPopularRegions] = useState<string[]>([]);

  // Charger les suggestions populaires au chargement du composant
  useEffect(() => {
    const loadPopularSuggestions = async () => {
      try {
        const suggestions = await fetchPopularSuggestions();
        setPopularEmplois(suggestions.emplois);
        setPopularRegions(suggestions.regions);
      } catch (error) {
        console.error("Erreur lors du chargement des suggestions populaires:", error);
      }
    };

    loadPopularSuggestions();
  }, []);

  const handleSearch = (event?: React.FormEvent) => {
    // Empêcher le comportement par défaut du formulaire qui pourrait causer un défilement
    if (event) {
      event.preventDefault();
    }
    
    onFilter(search, ville, contrat, secteur, teletravail);
    
    // Mise à jour des filtres actifs
    const newFilters = [];
    if (search) newFilters.push(`Recherche: ${search}`);
    if (ville) newFilters.push(`Lieu: ${ville}`);
    if (contrat) newFilters.push(`Contrat: ${contrat}`);
    if (secteur) newFilters.push(`Secteur: ${secteur}`);
    if (teletravail) newFilters.push(`Télétravail: ${teletravail}`);
    
    setActiveFilters(newFilters);
    
    // Afficher une notification de confirmation
    setOpenSnackbar(true);
    
    // Scroll automatique vers les offres après un petit délai pour laisser le temps aux filtres de s'appliquer
    setTimeout(() => {
      const offresSection = document.querySelector('[data-section="offres"]');
      if (offresSection) {
        offresSection.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'start' 
        });
      }
    }, 300);
  };

  const handleRemoveFilter = (filter: string) => {
    setActiveFilters(activeFilters.filter(f => f !== filter));
    
    // Réinitialiser le filtre correspondant
    if (filter.startsWith("Recherche:")) setSearch("");
    if (filter.startsWith("Lieu:")) setVille("");
    if (filter.startsWith("Contrat:")) setContrat("");
    if (filter.startsWith("Secteur:")) setSecteur("");
    if (filter.startsWith("Télétravail:")) setTeletravail("");
    
    // Appliquer les filtres mis à jour sans faire défiler la page
    window.scrollTo({ top: 0, behavior: 'auto' });
    
    onFilter(
      filter.startsWith("Recherche:") ? "" : search,
      filter.startsWith("Lieu:") ? "" : ville,
      filter.startsWith("Contrat:") ? "" : contrat,
      filter.startsWith("Secteur:") ? "" : secteur,
      filter.startsWith("Télétravail:") ? "" : teletravail
    );
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  const handleClearAllFilters = () => {
    // Réinitialiser tous les filtres
    setSearch("");
    setVille("");
    setContrat("");
    setSecteur("");
    setTeletravail("");
    setActiveFilters([]);
    
    // Appliquer les filtres vides
    onFilter("", "", "", "", "");
    
    // Notification
    setOpenSnackbar(true);
  };

  const inputStyle = {
    width: "100%",
    backgroundColor: "#fff",
    borderRadius: "12px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
    "& .MuiOutlinedInput-root": {
      borderRadius: "12px",
      "& fieldset": {
        borderColor: "#e2e8f0",
        borderWidth: "1.5px",
      },
      "&:hover fieldset": {
        borderColor: theme.palette.primary.light,
      },
      "&.Mui-focused fieldset": {
        borderColor: theme.palette.primary.main,
        boxShadow: `0 0 0 3px ${theme.palette.primary.main}15`,
      },
    },
    "& .MuiInputBase-input": {
      padding: "14px 16px",
    },
  };

  return (
    <Paper
      elevation={3}
      sx={{
        width: "100%",
        borderRadius: "20px",
        overflow: "visible",
        mb: 4,
        background: "linear-gradient(145deg, #ffffff, #f8fafc)",
        boxShadow: "0 10px 25px rgba(0,0,0,0.05)",
      }}
    >
      <Box sx={{ p: { xs: 2, md: 3 } }}>
        {/* Formulaire avec preventDefault pour empêcher le comportement par défaut */}
        <form onSubmit={handleSearch}>
          {/* Barre de recherche principale */}
          <Box
            sx={{
              display: "flex",
              flexDirection: { xs: "column", md: "row" },
              gap: 2,
              mb: 2,
            }}
          >
            {/* Recherche avec autocomplétion */}
            <Box sx={{ flex: 2 }}>
              <Autocomplete
                placeholder="Je cherche un emploi..."
                value={search}
                onChange={setSearch}
                onSelect={setSearch}
                fetchSuggestions={fetchEmploiSuggestions}
                icon="search"
                showMic={true}
                initialSuggestions={popularEmplois}
              />
            </Box>

            {/* Localisation avec autocomplétion */}
            <Box sx={{ flex: 1 }}>
              <Autocomplete
                placeholder="Dans la région..."
                value={ville}
                onChange={setVille}
                onSelect={setVille}
                fetchSuggestions={fetchRegionSuggestions}
                icon="location"
                initialSuggestions={popularRegions}
              />
            </Box>

            {/* Contrat */}
            <FormControl variant="outlined" sx={{ ...inputStyle, flex: 1 }}>
              <InputLabel id="contrat-label">Type de contrat</InputLabel>
              <Select
                labelId="contrat-label"
                id="contrat-select"
                value={contrat}
                onChange={(e) => setContrat(e.target.value)}
                label="Type de contrat"
                startAdornment={
                  <InputAdornment position="start">
                    <WorkIcon color="primary" />
                  </InputAdornment>
                }
              >
                <MenuItem value="">Tous les contrats</MenuItem>
                <MenuItem value="CDI">CDI</MenuItem>
                <MenuItem value="CDD">CDD</MenuItem>
                <MenuItem value="Stage">Stage</MenuItem>
                <MenuItem value="Alternance">Alternance</MenuItem>
              </Select>
            </FormControl>

            {/* Bouton de recherche */}
            <Button
              variant="contained"
              color="primary"
              type="submit"
              sx={{
                height: { xs: 56, md: "auto" },
                px: 3,
                borderRadius: "12px",
                boxShadow: "0 4px 14px rgba(37, 99, 235, 0.2)",
                fontSize: "1rem",
                minWidth: { xs: "100%", md: "120px" },
              }}
              startIcon={<SearchIcon />}
            >
              Trouver
            </Button>
          </Box>
        </form>

        {/* Filtres avancés toggle */}
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <Button
            color="primary"
            startIcon={showAdvanced ? <ExpandLessIcon /> : <ExpandMoreIcon />}
            onClick={() => setShowAdvanced(!showAdvanced)}
            sx={{ textTransform: "none", fontWeight: 500 }}
          >
            Filtres avancés
          </Button>
          
          <Button
            color="primary"
            startIcon={<ClearIcon />}
            variant="text"
            onClick={handleClearAllFilters}
            sx={{ textTransform: "none", fontWeight: 500 }}
          >
            Supprimer les filtres
          </Button>
        </Box>

        {/* Filtres avancés */}
        <Collapse in={showAdvanced}>
          <Box
            sx={{
              mt: 2,
              p: 2,
              borderRadius: "12px",
              backgroundColor: "rgba(241, 245, 249, 0.7)",
              display: "flex",
              flexDirection: { xs: "column", md: "row" },
              gap: 2,
            }}
          >
            {/* Secteur */}
            <FormControl variant="outlined" sx={{ ...inputStyle, flex: 1 }}>
              <InputLabel id="secteur-label">Secteur</InputLabel>
              <Select
                labelId="secteur-label"
                value={secteur}
                onChange={(e) => setSecteur(e.target.value)}
                label="Secteur"
                startAdornment={
                  <InputAdornment position="start">
                    <BusinessIcon color="primary" />
                  </InputAdornment>
                }
              >
                <MenuItem value="">Tous les secteurs</MenuItem>
                <MenuItem value="public">Public</MenuItem>
                <MenuItem value="prive">Privé</MenuItem>
              </Select>
            </FormControl>

            {/* Télétravail */}
            <FormControl variant="outlined" sx={{ ...inputStyle, flex: 1 }}>
              <InputLabel id="teletravail-label">Télétravail</InputLabel>
              <Select
                labelId="teletravail-label"
                value={teletravail}
                onChange={(e) => setTeletravail(e.target.value)}
                label="Télétravail"
                startAdornment={
                  <InputAdornment position="start">
                    <LaptopIcon color="primary" />
                  </InputAdornment>
                }
              >
                <MenuItem value="">Toutes options</MenuItem>
                <MenuItem value="Oui">Oui</MenuItem>
                <MenuItem value="Non">Non</MenuItem>
                <MenuItem value="Non précisé">Non précisé</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </Collapse>

        {/* Filtres actifs */}
        {activeFilters.length > 0 && (
          <Box sx={{ mt: 2, display: "flex", flexWrap: "wrap", gap: 1 }}>
            <Typography variant="body2" color="text.secondary" sx={{ mr: 1, display: "flex", alignItems: "center" }}>
              Filtres actifs:
            </Typography>
            {activeFilters.map((filter) => (
              <Chip
                key={filter}
                label={filter}
                onDelete={() => handleRemoveFilter(filter)}
                color="primary"
                variant="outlined"
                size="small"
                sx={{ 
                  borderRadius: "8px", 
                  fontWeight: 500,
                  backgroundColor: `${theme.palette.primary.main}10`,
                }}
              />
            ))}
          </Box>
        )}
      </Box>
      
      {/* Notification de confirmation */}
      <Snackbar
        open={openSnackbar}
        autoHideDuration={3000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity="success" sx={{ width: '100%' }}>
          {activeFilters.length > 0 ? "Filtres appliqués avec succès" : "Filtres supprimés avec succès"}
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default FilterBar;


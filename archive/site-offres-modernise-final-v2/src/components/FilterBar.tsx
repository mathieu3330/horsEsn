import React, { useState } from "react";
import {
  TextField,
  Button,
  MenuItem,
  Select,
  InputAdornment,
  Box,
  Paper,
  Chip,
  Typography,
  IconButton,
  Collapse,
  FormControl,
  InputLabel,
  Tooltip,
  useTheme,
  useMediaQuery,
  Snackbar,
  Alert
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import MicIcon from "@mui/icons-material/Mic";
import TuneIcon from "@mui/icons-material/Tune";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ExpandLessIcon from "@mui/icons-material/ExpandLess";
import WorkIcon from "@mui/icons-material/Work";
import EuroIcon from "@mui/icons-material/Euro";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import FilterAltIcon from "@mui/icons-material/FilterAlt";

interface FilterBarProps {
  onFilter: (search: string, ville: string, contrat: string) => void;
}

const FilterBar: React.FC<FilterBarProps> = ({ onFilter }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  const [search, setSearch] = useState("");
  const [ville, setVille] = useState("");
  const [contrat, setContrat] = useState("");
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [salaryRange, setSalaryRange] = useState("");
  const [experience, setExperience] = useState("");
  const [activeFilters, setActiveFilters] = useState<string[]>([]);
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const handleSearch = (event?: React.FormEvent) => {
    // Empêcher le comportement par défaut du formulaire qui pourrait causer un défilement
    if (event) {
      event.preventDefault();
    }
    
    // Maintenir la position de défilement en haut de la page
    window.scrollTo({ top: 0, behavior: 'auto' });
    
    onFilter(search, ville, contrat);
    
    // Mise à jour des filtres actifs
    const newFilters = [];
    if (search) newFilters.push(`Recherche: ${search}`);
    if (ville) newFilters.push(`Lieu: ${ville}`);
    if (contrat) newFilters.push(`Contrat: ${contrat}`);
    if (salaryRange) newFilters.push(`Salaire: ${salaryRange}`);
    if (experience) newFilters.push(`Expérience: ${experience}`);
    
    setActiveFilters(newFilters);
    
    // Afficher une notification de confirmation
    setOpenSnackbar(true);
  };

  const handleRemoveFilter = (filter: string) => {
    setActiveFilters(activeFilters.filter(f => f !== filter));
    
    // Réinitialiser le filtre correspondant
    if (filter.startsWith("Recherche:")) setSearch("");
    if (filter.startsWith("Lieu:")) setVille("");
    if (filter.startsWith("Contrat:")) setContrat("");
    if (filter.startsWith("Salaire:")) setSalaryRange("");
    if (filter.startsWith("Expérience:")) setExperience("");
    
    // Appliquer les filtres mis à jour sans faire défiler la page
    window.scrollTo({ top: 0, behavior: 'auto' });
    
    onFilter(
      filter.startsWith("Recherche:") ? "" : search,
      filter.startsWith("Lieu:") ? "" : ville,
      filter.startsWith("Contrat:") ? "" : contrat
    );
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
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
        overflow: "hidden",
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
            {/* Recherche */}
            <TextField
              variant="outlined"
              placeholder="Je cherche un emploi..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              sx={{ ...inputStyle, flex: 2 }}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon color="primary" />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <Tooltip title="Recherche vocale">
                      <IconButton color="primary" size="small">
                        <MicIcon />
                      </IconButton>
                    </Tooltip>
                  </InputAdornment>
                ),
              }}
            />

            {/* Localisation */}
            <TextField
              variant="outlined"
              placeholder="Dans la région..."
              value={ville}
              onChange={(e) => setVille(e.target.value)}
              sx={{ ...inputStyle, flex: 1 }}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <LocationOnIcon color="primary" />
                  </InputAdornment>
                ),
              }}
            />

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
                <MenuItem value="Freelance">Freelance</MenuItem>
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
            startIcon={<TuneIcon />}
            variant="text"
            sx={{ textTransform: "none", fontWeight: 500 }}
          >
            Trier par pertinence
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
            {/* Salaire */}
            <FormControl variant="outlined" sx={{ ...inputStyle, flex: 1 }}>
              <InputLabel id="salary-label">Salaire</InputLabel>
              <Select
                labelId="salary-label"
                value={salaryRange}
                onChange={(e) => setSalaryRange(e.target.value)}
                label="Salaire"
                startAdornment={
                  <InputAdornment position="start">
                    <EuroIcon color="primary" />
                  </InputAdornment>
                }
              >
                <MenuItem value="">Tous les salaires</MenuItem>
                <MenuItem value="20-30k">20 000 € - 30 000 €</MenuItem>
                <MenuItem value="30-40k">30 000 € - 40 000 €</MenuItem>
                <MenuItem value="40-50k">40 000 € - 50 000 €</MenuItem>
                <MenuItem value="50-70k">50 000 € - 70 000 €</MenuItem>
                <MenuItem value="70k+">Plus de 70 000 €</MenuItem>
              </Select>
            </FormControl>

            {/* Expérience */}
            <FormControl variant="outlined" sx={{ ...inputStyle, flex: 1 }}>
              <InputLabel id="experience-label">Expérience</InputLabel>
              <Select
                labelId="experience-label"
                value={experience}
                onChange={(e) => setExperience(e.target.value)}
                label="Expérience"
                startAdornment={
                  <InputAdornment position="start">
                    <AccessTimeIcon color="primary" />
                  </InputAdornment>
                }
              >
                <MenuItem value="">Toute expérience</MenuItem>
                <MenuItem value="debutant">Débutant</MenuItem>
                <MenuItem value="1-3">1 à 3 ans</MenuItem>
                <MenuItem value="3-5">3 à 5 ans</MenuItem>
                <MenuItem value="5-10">5 à 10 ans</MenuItem>
                <MenuItem value="10+">Plus de 10 ans</MenuItem>
              </Select>
            </FormControl>

            {/* Autres filtres possibles */}
            <Button
              variant="outlined"
              color="primary"
              onClick={() => handleSearch()}
              sx={{
                height: 56,
                borderRadius: "12px",
                borderWidth: "1.5px",
                fontWeight: 600,
                flex: 1,
              }}
              startIcon={<FilterAltIcon />}
            >
              Appliquer les filtres
            </Button>
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
          Filtres appliqués avec succès
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default FilterBar;

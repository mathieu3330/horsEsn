import React, { useState, useEffect, useRef } from 'react';
import { 
  Box, 
  TextField, 
  List, 
  ListItemText, 
  Paper, 
  InputAdornment,
  CircularProgress,
  Typography,
  useTheme
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import MicIcon from '@mui/icons-material/Mic';
import { debounce } from 'lodash';
import ListItemButton from '@mui/material/ListItemButton';

interface AutocompleteProps {
  placeholder: string;
  value: string;
  onChange: (value: string) => void;
  onSelect: (value: string) => void;
  fetchSuggestions: (query: string) => Promise<string[]>;
  icon?: 'search' | 'location';
  showMic?: boolean;
  initialSuggestions?: string[];
}

const Autocomplete: React.FC<AutocompleteProps> = ({
  placeholder,
  value,
  onChange,
  onSelect,
  fetchSuggestions,
  icon = 'search',
  showMic = false,
  initialSuggestions = []
}) => {
  const theme = useTheme();
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [loading, setLoading] = useState(false);
  const [focused, setFocused] = useState(false);
  const inputRef = useRef<HTMLDivElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);

  // Fonction pour récupérer les suggestions avec debounce
  const debouncedFetchSuggestions = useRef(
    debounce(async (query: string) => {
      if (query.length < 2) {
        if (initialSuggestions.length > 0 && focused) {
          setSuggestions(initialSuggestions);
          setShowSuggestions(true);
        } else {
          setSuggestions([]);
          setShowSuggestions(false);
        }
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const results = await fetchSuggestions(query);
        setSuggestions(results);
        setShowSuggestions(results.length > 0);
      } catch (error) {
        console.error('Erreur lors de la récupération des suggestions:', error);
        setSuggestions([]);
        setShowSuggestions(false);
      } finally {
        setLoading(false);
      }
    }, 300)
  ).current;

  // Effet pour gérer les clics en dehors du composant
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        inputRef.current && 
        !inputRef.current.contains(event.target as Node) &&
        suggestionsRef.current && 
        !suggestionsRef.current.contains(event.target as Node)
      ) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Effet pour récupérer les suggestions quand la valeur change
  useEffect(() => {
    debouncedFetchSuggestions(value);
    
    return () => {
      debouncedFetchSuggestions.cancel();
    };
  }, [value, debouncedFetchSuggestions]);

  // Afficher les suggestions initiales au focus si la valeur est vide
  const handleFocus = () => {
    setFocused(true);
    if (value.length < 2 && initialSuggestions.length > 0) {
      setSuggestions(initialSuggestions);
      setShowSuggestions(true);
    }
  };

  const handleBlur = () => {
    setFocused(false);
    // Ne pas fermer immédiatement pour permettre la sélection
    setTimeout(() => {
      if (!document.activeElement?.contains(suggestionsRef.current)) {
        setShowSuggestions(false);
      }
    }, 200);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    onChange(newValue);
  };

  const handleSuggestionClick = (suggestion: string) => {
    onSelect(suggestion);
    setShowSuggestions(false);
  };

  const getStartIcon = () => {
    if (icon === 'search') {
      return <SearchIcon color="primary" />;
    } else if (icon === 'location') {
      return <LocationOnIcon color="primary" />;
    }
    return null;
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
    <Box sx={{ position: 'relative', width: '100%' }} ref={inputRef}>
      <TextField
        variant="outlined"
        placeholder={placeholder}
        value={value}
        onChange={handleChange}
        onFocus={handleFocus}
        onBlur={handleBlur}
        fullWidth
        sx={inputStyle}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              {getStartIcon()}
            </InputAdornment>
          ),
          endAdornment: (
            <InputAdornment position="end">
              {loading ? (
                <CircularProgress size={20} color="primary" />
              ) : (
                showMic && (
                  <MicIcon color="primary" />
                )
              )}
            </InputAdornment>
          ),
        }}
      />
      
      {showSuggestions && (
        <Paper
          ref={suggestionsRef}
          elevation={3}
          sx={{
            position: 'absolute',
            width: '100%',
            maxHeight: '300px',
            overflowY: 'auto',
            mt: 0.5,
            zIndex: 1500,
            borderRadius: '12px',
            boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
          }}
        >
          {suggestions.length > 0 ? (
            <List disablePadding>
              {suggestions.map((suggestion, index) => (
                
              
<ListItemButton
  key={index}
  onClick={() => handleSuggestionClick(suggestion)}
  sx={{
    py: 1.5,
    borderBottom: index < suggestions.length - 1 ? '1px solid #f0f0f0' : 'none',
    '&:hover': {
      backgroundColor: 'rgba(25, 118, 210, 0.04)',
    },
  }}
>
  <ListItemText 
    primary={
      <Typography variant="body1" sx={{ fontWeight: 400 }}>
        {suggestion}
      </Typography>
    } 
  />
</ListItemButton>







              ))}
            </List>
          ) : (
            <Box sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">
                Aucune suggestion trouvée
              </Typography>
            </Box>
          )}
        </Paper>
      )}
    </Box>
  );
};

export default Autocomplete;


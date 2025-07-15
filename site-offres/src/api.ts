// Définition de l'URL de base de l'API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://api-offres-145837535580.us-central1.run.app';

// Interface pour les paramètres de recherche d'offres
interface OffresParams {
  contrat?: string;
  ville?: string;
  secteur?: string;
  teletravail?: string;
  search?: string;
  page?: number;
  limit?: number;
}

// Interface pour les suggestions populaires
interface PopularSuggestions {
  emplois: string[];
  regions: string[];
}

// Fonction pour récupérer les offres
export const fetchOffres = async (params: OffresParams) => {
  const queryParams = new URLSearchParams();
  
  // Ajouter les paramètres non vides à l'URL
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      queryParams.append(key, value.toString());
    }
  });
  
  const response = await fetch(`${API_BASE_URL}/offres?${queryParams.toString()}`);
  
  if (!response.ok) {
    throw new Error(`Erreur lors de la récupération des offres: ${response.statusText}`);
  }
  
  return await response.json();
};

// Fonction pour récupérer une offre spécifique
export const fetchOffre = async (id: number) => {
  const response = await fetch(`${API_BASE_URL}/offres/${id}`);
  
  if (!response.ok) {
    throw new Error(`Erreur lors de la récupération de l'offre: ${response.statusText}`);
  }
  
  return await response.json();
};

// Fonction pour récupérer les suggestions d'emplois
export const fetchEmploiSuggestions = async (query: string): Promise<string[]> => {
  if (!query || query.length < 2) return [];
  
  try {
    const response = await fetch(`${API_BASE_URL}/autocomplete/emplois?q=${encodeURIComponent(query)}`);
    
    if (!response.ok) {
      throw new Error(`Erreur lors de la récupération des suggestions d'emplois: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Erreur API suggestions emplois:', error);
    return [];
  }
};

// Fonction pour récupérer les suggestions de régions
export const fetchRegionSuggestions = async (query: string): Promise<string[]> => {
  if (!query || query.length < 2) return [];
  
  try {
    const response = await fetch(`${API_BASE_URL}/autocomplete/regions?q=${encodeURIComponent(query)}`);
    
    if (!response.ok) {
      throw new Error(`Erreur lors de la récupération des suggestions de régions: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Erreur API suggestions régions:', error);
    return [];
  }
};

// Fonction pour récupérer les suggestions populaires
export const fetchPopularSuggestions = async (): Promise<PopularSuggestions> => {
  try {
    const response = await fetch(`${API_BASE_URL}/suggestions/populaires`);
    
    if (!response.ok) {
      throw new Error(`Erreur lors de la récupération des suggestions populaires: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Erreur API suggestions populaires:', error);
    return { emplois: [], regions: [] };
  }
};


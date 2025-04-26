import React, { useEffect, useState } from "react";
import axios from "axios";
import { Container, CircularProgress } from "@mui/material";
import OffreCard from "./OffreCard";
import FilterBar from "./FilterBar";

interface Offre {
  id: number;
  titre: string;
  contrat: string;
  ville: string;
  description: string;
  dateoffre: string;
  logo: string; // ✅ ici
}


const OffreList: React.FC = () => {
  const [offres, setOffres] = useState<Offre[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ search: "", ville: "", contrat: "" });

  useEffect(() => {
    const fetchOffres = async () => {
      try {
        setLoading(true);
        const response = await axios.get(
          `/api/offres?search=${encodeURIComponent(filters.search)}&contrat=${filters.contrat}&ville=${filters.ville}`
        );
        setOffres(response.data.offres);
      } catch (error) {
        console.error("Erreur API :", error);
      } finally {
        setLoading(false);
      }
    };

    fetchOffres();
  }, [filters]);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <FilterBar onFilter={(search, ville, contrat) => setFilters({ search, ville, contrat })} />

      {loading ? (
        <CircularProgress sx={{ display: "block", mx: "auto", mt: 5 }} />
      ) : (
        offres.map((offre) => (
      <OffreCard
        key={offre.id}
        titre={offre.titre}
        contrat={offre.contrat}
        ville={offre.ville}
        description={offre.description}
        dateoffre={offre.dateoffre}
        logo={offre.logo} // ✅ passer ici
        
      />

        ))
      )}
    </Container>
  );
};

export default OffreList;

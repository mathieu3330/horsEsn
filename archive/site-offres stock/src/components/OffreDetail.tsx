import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { Container, Typography, Button, CircularProgress } from "@mui/material";
import { Link } from "react-router-dom";

interface Offre {
  id: number;
  titre: string;
  contrat: string;
  ville: string;
  description: string;
}

const OffreDetail: React.FC = () => {
  const { id } = useParams();
  const [offre, setOffre] = useState<Offre | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get(`/api/offres/${id}`)
      .then((response) => {
        setOffre(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Erreur API :", error);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return <CircularProgress />;
  }

  if (!offre) {
    return <Typography variant="h6">Offre non trouvée</Typography>;
  }

  return (
    <Container 
      maxWidth="md" 
      sx={{ 
        display: "flex", 
        flexDirection: "column", 
        alignItems: "center", 
        justifyContent: "center",
        px: 2, 
        py: 3,
        width: "100%",
        margin: "0 auto" // Centre le conteneur
      }}
    >
      <Typography variant="h4" fontWeight="bold" mb={2}>
        {offre.titre}
      </Typography>
      <Typography variant="subtitle1">
        {offre.contrat} - {offre.ville}
      </Typography>
      <Typography variant="body1" mt={2}>
        {offre.description}
      </Typography>
      <Button variant="contained" color="secondary" component={Link} to="/">
        Retour aux offres
      </Button>
    </Container>
  );
};

export default OffreDetail;
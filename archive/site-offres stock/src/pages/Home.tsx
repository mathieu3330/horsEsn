import React from "react";
import { Container, Typography } from "@mui/material";
import OffreList from "../components/OffreList";

const Home: React.FC = () => {
  return (
    <Container>
      <Typography variant="h3" textAlign="center" sx={{ marginBottom: 4 }}>
        📢 Offres d'emploi
      </Typography>
      <OffreList />
    </Container>
  );
};

export default Home;

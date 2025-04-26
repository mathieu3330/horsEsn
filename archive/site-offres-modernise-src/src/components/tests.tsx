// Ce fichier contient des tests pour vérifier que les composants modernisés fonctionnent correctement
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { ThemeProvider } from "@mui/material";
import theme from "../theme";
import Navbar from "./Navbar";
import FilterBar from "./FilterBar";
import OffreCard from "./OffreCard";
import HeroSection from "./HeroSection";
import OffreDetail from "./OffreDetail";
import OffreList from "./OffreList";

// Mock des fonctions et props
const mockFilterFunction = jest.fn();
const mockCloseFunction = jest.fn();

// Données de test
const testOffre = {
  id: 1,
  titre: "Développeur Frontend React",
  contrat: "CDI",
  ville: "Paris",
  description: "Nous recherchons un développeur frontend expérimenté pour rejoindre notre équipe...",
  dateoffre: "2025-03-15",
  logo: "https://example.com/logo.png",
};

describe("Tests des composants UI modernisés", () => {
  // Test du composant Navbar
  test("Navbar s'affiche correctement", () => {
    render(
      <ThemeProvider theme={theme}>
        <Navbar />
      </ThemeProvider>
    );
    
    expect(screen.getByText("Offres d'emploi")).toBeInTheDocument();
  });

  // Test du composant FilterBar
  test("FilterBar s'affiche correctement", () => {
    render(
      <ThemeProvider theme={theme}>
        <FilterBar onFilter={mockFilterFunction} />
      </ThemeProvider>
    );
    
    expect(screen.getByPlaceholderText("Je cherche un emploi...")).toBeInTheDocument();
    expect(screen.getByText("Trouver")).toBeInTheDocument();
    expect(screen.getByText("Filtres avancés")).toBeInTheDocument();
  });

  // Test du composant OffreCard
  test("OffreCard affiche correctement les informations de l'offre", () => {
    render(
      <ThemeProvider theme={theme}>
        <OffreCard
          titre={testOffre.titre}
          contrat={testOffre.contrat}
          ville={testOffre.ville}
          description={testOffre.description}
          dateoffre={testOffre.dateoffre}
          logo={testOffre.logo}
        />
      </ThemeProvider>
    );
    
    expect(screen.getByText(testOffre.titre)).toBeInTheDocument();
    expect(screen.getByText(testOffre.contrat)).toBeInTheDocument();
    expect(screen.getByText(testOffre.ville)).toBeInTheDocument();
    expect(screen.getByText("Postuler maintenant")).toBeInTheDocument();
  });

  // Test du composant HeroSection
  test("HeroSection s'affiche correctement", () => {
    render(
      <ThemeProvider theme={theme}>
        <HeroSection />
      </ThemeProvider>
    );
    
    expect(screen.getByText("Trouvez votre prochain emploi dans les meilleures entreprises")).toBeInTheDocument();
    expect(screen.getByText("Explorer les offres")).toBeInTheDocument();
  });

  // Test du composant OffreDetail
  test("OffreDetail s'affiche correctement", () => {
    render(
      <ThemeProvider theme={theme}>
        <OffreDetail
          open={true}
          onClose={mockCloseFunction}
          titre={testOffre.titre}
          contrat={testOffre.contrat}
          ville={testOffre.ville}
          description={testOffre.description}
          dateoffre={testOffre.dateoffre}
          logo={testOffre.logo}
        />
      </ThemeProvider>
    );
    
    expect(screen.getByText(testOffre.titre)).toBeInTheDocument();
    expect(screen.getByText("Description du poste")).toBeInTheDocument();
    expect(screen.getByText("Postuler rapidement")).toBeInTheDocument();
  });
});

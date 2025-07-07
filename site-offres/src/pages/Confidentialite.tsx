import React from "react";
import { Box, Typography, Container, Paper, Divider } from "@mui/material";

const Confidentialite: React.FC = () => {
  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Paper elevation={2} sx={{ p: 4, borderRadius: "16px" }}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight="bold" color="primary">
          Politique de Confidentialité – HorsESN.fr
        </Typography>
        
        <Divider sx={{ my: 3 }} />
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            1. Responsable du traitement
          </Typography>
          <Typography variant="body1" paragraph>
            Les données personnelles collectées sur le site sont traitées par :
          </Typography>
          <Typography variant="body1" paragraph>
            HorsESN.fr
          </Typography>
          <Typography variant="body1" paragraph>
            Email : hello@horsesn.fr
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            2. Données collectées
          </Typography>
          <Typography variant="body1" paragraph>
            HorsESN.fr collecte uniquement les données nécessaires à l'utilisation de ses fonctionnalités :
          </Typography>
          <Typography variant="body1" component="ul" sx={{ pl: 4 }}>
            <li>Adresse email</li>
            <li>Préférences d'alerte emploi</li>
            <li>Historique de navigation (via cookies analytiques)</li>
          </Typography>
          <Typography variant="body1" paragraph sx={{ mt: 2 }}>
            Aucun CV, lettre de motivation ou document personnel n'est collecté ni stocké.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            3. Finalités
          </Typography>
          <Typography variant="body1" paragraph>
            Les données sont utilisées pour :
          </Typography>
          <Typography variant="body1" component="ul" sx={{ pl: 4 }}>
            <li>Envoyer des alertes emploi personnalisées</li>
            <li>Permettre l'accès à l'espace utilisateur</li>
            <li>Mesurer la fréquentation du site (statistiques anonymisées)</li>
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            4. Base légale
          </Typography>
          <Typography variant="body1" paragraph>
            Le traitement des données repose sur le consentement de l'utilisateur, obtenu lors de l'inscription ou de l'acceptation des cookies.
          </Typography>
          <Typography variant="body1" paragraph>
            Conformément à l'article 6.1.a du Règlement Général sur la Protection des Données (RGPD), ce consentement est libre, spécifique, éclairé et univoque.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            5. Durée de conservation
          </Typography>
          <Typography variant="body1" component="ul" sx={{ pl: 4 }}>
            <li>Données de compte : 2 ans après la dernière activité</li>
            <li>Données analytiques : 12 mois</li>
          </Typography>
          <Typography variant="body1" paragraph sx={{ mt: 2 }}>
            À l'issue de ces périodes, les données sont soit supprimées, soit anonymisées pour des fins statistiques.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            6. Destinataires
          </Typography>
          <Typography variant="body1" paragraph>
            Les données sont uniquement accessibles par l'équipe HorsESN.fr.
          </Typography>
          <Typography variant="body1" paragraph>
            Elles ne sont jamais partagées, vendues ou cédées à des tiers ou à des recruteurs.
          </Typography>
          <Typography variant="body1" paragraph>
            Nous pouvons faire appel à des sous-traitants techniques (hébergement, maintenance) qui n'ont accès aux données que pour exécuter les services nécessaires au fonctionnement du site.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            7. Vos droits
          </Typography>
          <Typography variant="body1" paragraph>
            Conformément au RGPD, vous pouvez à tout moment :
          </Typography>
          <Typography variant="body1" component="ul" sx={{ pl: 4 }}>
            <li>Accéder à vos données</li>
            <li>Demander leur rectification ou leur suppression</li>
            <li>Retirer votre consentement</li>
            <li>Exercer votre droit à la portabilité ou à l'opposition</li>
            <li>Définir des directives relatives au sort de vos données après votre décès</li>
          </Typography>
          <Typography variant="body1" paragraph sx={{ mt: 2 }}>
            Envoyez votre demande à : hello@horsesn.fr
          </Typography>
          <Typography variant="body1" paragraph>
            Nous nous engageons à y répondre dans un délai maximum d'un mois. Vous disposez également du droit d'introduire une réclamation auprès de la CNIL.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            8. Cookies
          </Typography>
          <Typography variant="body1" paragraph>
            Le site utilise des cookies pour :
          </Typography>
          <Typography variant="body1" component="ul" sx={{ pl: 4 }}>
            <li>Assurer le bon fonctionnement du site</li>
            <li>Analyser le trafic (Google Analytics ou outil équivalent)</li>
          </Typography>
          <Typography variant="body1" paragraph sx={{ mt: 2 }}>
            Vous pouvez gérer votre consentement via le bandeau prévu à cet effet lors de votre première visite.
          </Typography>
          <Typography variant="body1" paragraph>
            Vous pouvez également configurer votre navigateur pour refuser les cookies ou les supprimer à tout moment.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            9. Sécurité des données
          </Typography>
          <Typography variant="body1" paragraph>
            Nous mettons en œuvre des mesures techniques et organisationnelles appropriées pour protéger vos données contre toute perte, altération ou accès non autorisé.
          </Typography>
          <Typography variant="body1" paragraph>
            En cas de violation de données susceptible d'engendrer un risque pour vos droits et libertés, nous nous engageons à vous en informer dans les meilleurs délais.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            10. Mise à jour de la politique
          </Typography>
          <Typography variant="body1" paragraph>
            Cette politique de confidentialité peut être mise à jour périodiquement. La date de dernière mise à jour figure en bas de page.
          </Typography>
          <Typography variant="body1" paragraph>
            En cas de modifications substantielles, nous vous en informerons par email ou via une notification sur notre site.
          </Typography>
        </Box>
        
        <Box sx={{ mt: 6, textAlign: "center" }}>
          <Typography variant="body2" color="text.secondary">
            Dernière mise à jour : Mai 2025
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default Confidentialite;

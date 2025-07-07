import React from "react";
import { Box, Typography, Container, Paper, Divider } from "@mui/material";

const Conditions: React.FC = () => {
  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Paper elevation={2} sx={{ p: 4, borderRadius: "16px" }}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight="bold" color="primary">
          Conditions Générales d'Utilisation (CGU) – HorsESN.fr
        </Typography>
        
        <Divider sx={{ my: 3 }} />
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            1. Objet du site
          </Typography>
          <Typography variant="body1" paragraph>
            HorsESN.fr est une plateforme qui centralise des offres d'emploi publiées directement par
            les entreprises, à l'exclusion des offres issues d'ESN (Entreprises de Services du
            Numérique). Le site redirige les utilisateurs vers les plateformes de recrutement officielles
            des entreprises concernées.
          </Typography>
          <Typography variant="body1" paragraph>
            Ces conditions générales d'utilisation définissent les modalités d'accès et d'utilisation des services proposés sur notre plateforme.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            2. Accès au service
          </Typography>
          <Typography variant="body1" paragraph>
            L'accès au site est gratuit. Les utilisateurs peuvent créer un compte pour :
          </Typography>
          <Typography variant="body1" component="ul" sx={{ pl: 4 }}>
            <li>Recevoir des alertes personnalisées</li>
            <li>Enregistrer des offres en favoris</li>
            <li>Gérer leurs préférences</li>
          </Typography>
          <Typography variant="body1" paragraph sx={{ mt: 2 }}>
            Aucune candidature ne se fait directement via HorsESN.fr. Le site agit comme un
            agrégateur d'annonces externes.
          </Typography>
          <Typography variant="body1" paragraph>
            L'utilisation du site est soumise à l'acceptation pleine et entière des présentes conditions générales d'utilisation.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            3. Compte utilisateur
          </Typography>
          <Typography variant="body1" paragraph>
            L'utilisateur s'engage à :
          </Typography>
          <Typography variant="body1" component="ul" sx={{ pl: 4 }}>
            <li>Fournir des informations exactes lors de la création de son compte</li>
            <li>Ne pas usurper l'identité d'un tiers</li>
            <li>Ne pas perturber le bon fonctionnement du site</li>
            <li>Maintenir la confidentialité de ses identifiants de connexion</li>
            <li>Informer immédiatement HorsESN.fr en cas d'utilisation non autorisée de son compte</li>
          </Typography>
          <Typography variant="body1" paragraph sx={{ mt: 2 }}>
            L'utilisateur peut supprimer son compte à tout moment. L'équipe de HorsESN se réserve
            également le droit de suspendre ou supprimer un compte en cas d'utilisation abusive ou non conforme aux présentes conditions.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            4. Propriété intellectuelle
          </Typography>
          <Typography variant="body1" component="ul" sx={{ pl: 4 }}>
            <li>Les logos, noms, contenus et extraits d'annonces appartiennent aux entreprises
            respectives.</li>
            <li>HorsESN.fr ne revendique aucune propriété sur les contenus issus des sites
            d'origine.</li>
            <li>Toute reproduction ou réutilisation du site sans autorisation est interdite.</li>
          </Typography>
          <Typography variant="body1" paragraph sx={{ mt: 2 }}>
            La structure générale du site, les graphismes, et la marque HorsESN.fr sont la propriété exclusive de HorsESN.fr et sont protégés par les lois relatives à la propriété intellectuelle.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            5. Responsabilité
          </Typography>
          <Typography variant="body1" paragraph>
            HorsESN.fr ne garantit pas :
          </Typography>
          <Typography variant="body1" component="ul" sx={{ pl: 4 }}>
            <li>L'exactitude ou l'actualité des offres référencées</li>
            <li>La disponibilité des sites tiers vers lesquels les utilisateurs sont redirigés</li>
            <li>L'absence d'interruption ou d'erreur dans le fonctionnement du site</li>
          </Typography>
          <Typography variant="body1" paragraph sx={{ mt: 2 }}>
            Le site n'intervient ni dans le processus de candidature, ni dans le recrutement.
          </Typography>
          <Typography variant="body1" paragraph>
            HorsESN.fr ne pourra être tenu responsable des dommages directs ou indirects résultant de l'utilisation du site ou de l'impossibilité d'y accéder.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            6. Évolution des conditions
          </Typography>
          <Typography variant="body1" paragraph>
            Ces conditions peuvent être modifiées à tout moment. Les utilisateurs seront informés de
            toute mise à jour significative par email ou via une notification sur le site.
          </Typography>
          <Typography variant="body1" paragraph>
            La poursuite de l'utilisation du site après modification des CGU vaut acceptation des nouvelles conditions.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            7. Protection des données personnelles
          </Typography>
          <Typography variant="body1" paragraph>
            Les informations recueillies sur le site font l'objet d'un traitement informatique destiné à permettre l'accès aux services proposés.
          </Typography>
          <Typography variant="body1" paragraph>
            Pour plus d'informations sur la gestion de vos données et l'exercice de vos droits, veuillez consulter notre Politique de Confidentialité.
          </Typography>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            8. Droit applicable
          </Typography>
          <Typography variant="body1" paragraph>
            Les présentes CGU sont régies par le droit français. En cas de litige, les tribunaux
            compétents seront ceux du ressort du siège social de l'éditeur du site.
          </Typography>
          <Typography variant="body1" paragraph>
            En cas de litige, une solution amiable sera recherchée avant toute action judiciaire.
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

export default Conditions;

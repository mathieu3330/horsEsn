import React from "react";
import { Box, Typography, Container, Paper, Divider, Accordion, AccordionSummary, AccordionDetails } from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

const Aide: React.FC = () => {
  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Paper elevation={2} sx={{ p: 4, borderRadius: "16px" }}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight="bold" color="primary">
          Centre d'aide – HorsESN.fr
        </Typography>
        
        <Typography variant="body1" paragraph sx={{ mb: 4 }}>
          Bienvenue dans notre centre d'aide. Vous trouverez ci-dessous les réponses aux questions les plus fréquemment posées.
          Si vous ne trouvez pas la réponse à votre question, n'hésitez pas à nous contacter via notre page de contact.
        </Typography>
        
        <Divider sx={{ my: 3 }} />
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            Questions fréquentes
          </Typography>
          
          <Accordion sx={{ mb: 2, borderRadius: "8px", overflow: "hidden" }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle1" fontWeight="bold">Qu'est-ce que HorsESN.fr ?</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body1">
                HorsESN.fr est une plateforme qui centralise des offres d'emploi publiées directement par les entreprises, 
                à l'exclusion des offres issues d'ESN (Entreprises de Services du Numérique). Notre objectif est de faciliter 
                la recherche d'emploi en entreprise pour les professionnels qui souhaitent travailler directement chez le client final.
              </Typography>
            </AccordionDetails>
          </Accordion>
          
          <Accordion sx={{ mb: 2, borderRadius: "8px", overflow: "hidden" }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle1" fontWeight="bold">Comment utiliser les filtres de recherche ?</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body1">
                Pour rechercher des offres, utilisez les filtres disponibles en haut de la page d'accueil :
                <ul>
                  <li>Saisissez des mots-clés dans le champ de recherche</li>
                  <li>Sélectionnez une région ou une ville</li>
                  <li>Choisissez un type de contrat</li>
                  <li>Cliquez sur "Trouver" pour afficher les résultats</li>
                </ul>
                Vous pouvez également utiliser les filtres avancés pour affiner votre recherche selon le secteur et les options de télétravail.
              </Typography>
            </AccordionDetails>
          </Accordion>
          
          <Accordion sx={{ mb: 2, borderRadius: "8px", overflow: "hidden" }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle1" fontWeight="bold">Comment postuler à une offre ?</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body1">
                HorsESN.fr ne gère pas directement les candidatures. Lorsque vous cliquez sur une offre qui vous intéresse, 
                vous êtes redirigé vers le site de recrutement officiel de l'entreprise concernée. C'est sur ce site que vous 
                pourrez soumettre votre candidature selon le processus défini par l'entreprise.
              </Typography>
            </AccordionDetails>
          </Accordion>
          
          <Accordion sx={{ mb: 2, borderRadius: "8px", overflow: "hidden" }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle1" fontWeight="bold">Comment créer un compte ?</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body1">
                Pour créer un compte, cliquez sur "Connexion" en haut à droite de la page, puis sur "Créer un compte". 
                Remplissez le formulaire avec votre adresse email et choisissez un mot de passe. Vous recevrez un email 
                de confirmation pour activer votre compte. Une fois votre compte créé, vous pourrez configurer des alertes 
                personnalisées et enregistrer des offres en favoris.
              </Typography>
            </AccordionDetails>
          </Accordion>
          
          <Accordion sx={{ mb: 2, borderRadius: "8px", overflow: "hidden" }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle1" fontWeight="bold">Comment configurer des alertes emploi ?</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body1">
                Une fois connecté à votre compte, vous pouvez configurer des alertes emploi en fonction de vos critères de recherche.
                Rendez-vous dans votre espace personnel, cliquez sur "Mes alertes" et définissez les critères souhaités (mots-clés, 
                localisation, type de contrat, etc.). Vous recevrez alors des notifications par email lorsque de nouvelles offres 
                correspondant à vos critères seront publiées.
              </Typography>
            </AccordionDetails>
          </Accordion>
          
          <Accordion sx={{ mb: 2, borderRadius: "8px", overflow: "hidden" }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle1" fontWeight="bold">Comment supprimer mon compte ?</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body1">
                Pour supprimer votre compte, connectez-vous et accédez à votre espace personnel. Dans les paramètres du compte, 
                vous trouverez l'option "Supprimer mon compte". Après confirmation, toutes vos données personnelles seront 
                supprimées de notre base de données conformément à notre politique de confidentialité.
              </Typography>
            </AccordionDetails>
          </Accordion>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
            Problèmes techniques
          </Typography>
          
          <Accordion sx={{ mb: 2, borderRadius: "8px", overflow: "hidden" }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle1" fontWeight="bold">Je ne reçois pas les emails d'alerte</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body1">
                Si vous ne recevez pas nos emails d'alerte, vérifiez d'abord votre dossier de spam ou de courrier indésirable. 
                Assurez-vous également que votre adresse email est correctement renseignée dans votre profil. Si le problème 
                persiste, contactez-nous à hello@HorsESN.fr.
              </Typography>
            </AccordionDetails>
          </Accordion>
          
          <Accordion sx={{ mb: 2, borderRadius: "8px", overflow: "hidden" }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle1" fontWeight="bold">Le site ne fonctionne pas correctement</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body1">
                Si vous rencontrez des problèmes techniques sur notre site, essayez d'abord de vider le cache de votre navigateur 
                ou d'utiliser un autre navigateur. Si le problème persiste, décrivez-nous précisément le dysfonctionnement 
                rencontré via notre page de contact, en précisant le navigateur et l'appareil utilisés.
              </Typography>
            </AccordionDetails>
          </Accordion>
        </Box>
        
        <Box sx={{ mt: 6, textAlign: "center" }}>
          <Typography variant="h6" gutterBottom>
            Vous n'avez pas trouvé la réponse à votre question ?
          </Typography>
          <Typography variant="body1">
            N'hésitez pas à nous contacter directement à hello@HorsESN.fr ou via notre page de contact.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default Aide;

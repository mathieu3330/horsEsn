import React, { useState } from "react";
import { 
  Box, 
  Typography, 
  Container, 
  Paper, 
  Grid, 
  Divider,
  Snackbar,
  Alert
} from "@mui/material";
import EmailIcon from "@mui/icons-material/Email";

const Contact: React.FC = () => {
  const [] = useState({
    nom: "",
    email: "",
    sujet: "",
    message: ""
  });
  
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [formError, setFormError] = useState(false);
  

  
  const handleCloseSnackbar = () => {
    setFormSubmitted(false);
    setFormError(false);
  };
  


  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Paper elevation={2} sx={{ p: 4, borderRadius: "16px" }}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight="bold" color="primary">
          Contactez-nous
        </Typography>
        
        <Typography variant="body1" paragraph sx={{ mb: 4 }}>
          Vous avez une question, une suggestion ou besoin d'assistance ? N'hésitez pas à nous contacter.
          Notre équipe vous répondra dans les meilleurs délais.
        </Typography>
        
        <Divider sx={{ my: 3 }} />
        
        <Grid container spacing={4}>
          <Grid item xs={12} md={5}>
            <Box sx={{ mb: 4 }}>
              <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
                Nos coordonnées
              </Typography>
              
              <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                <EmailIcon color="primary" sx={{ mr: 2 }} />
                <Typography variant="body1">
                  <strong>Email :</strong> hello@HorsESN.fr
                </Typography>
              </Box>
              
              <Typography variant="body1" paragraph sx={{ mt: 4 }}>
                Nous vous répondrons dans un délai de 48 heures ouvrées.
              </Typography>
            </Box>
            
            <Box sx={{ mt: 6 }}>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Horaires de disponibilité
              </Typography>
              <Typography variant="body2">
                Du lundi au vendredi<br />
                De 9h à 18h
              </Typography>
            </Box>
          </Grid>
          
 
        </Grid>
        
        <Box sx={{ mt: 6, textAlign: "center" }}>
          <Typography variant="body2" color="text.secondary">
            En nous contactant, vous acceptez notre politique de confidentialité concernant le traitement de vos données.
          </Typography>
        </Box>
      </Paper>
      
      {/* Notifications */}
      <Snackbar open={formSubmitted} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity="success" sx={{ width: '100%' }}>
          Votre message a bien été envoyé ! Nous vous répondrons dans les meilleurs délais.
        </Alert>
      </Snackbar>
      
      <Snackbar open={formError} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity="error" sx={{ width: '100%' }}>
          Veuillez remplir tous les champs obligatoires.
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Contact;

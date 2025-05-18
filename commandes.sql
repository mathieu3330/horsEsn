
DELETE FROM
  "public"."offres" WHERE dateoffre> CURRENT_DATE;
UPDATE "public"."offres" SET teletravail='non précisé' WHERE teletravail='Non renseigné';
UPDATE "public"."offres" SET contrat='CDD' WHERE contrat like '%CDD%';
UPDATE "public"."offres" SET contrat='Alternance' WHERE contrat like 'Contrat de professionnalisation Temps plein';
UPDATE "public"."offres" SET contrat='Alternance' WHERE contrat like '%Alternance%';
UPDATE "public"."offres" SET contrat='non précisé' WHERE contrat like 'Non renseigné';
UPDATE "public"."offres" SET contrat='CDD' WHERE contrat like '%Contrat A Duree Determinee%';
UPDATE "public"."offres" SET contrat='Alternance' WHERE contrat='Apprentissage';
UPDATE "public"."offres" SET contrat='Alternance' WHERE contrat='ALTERNANCE';
UPDATE "public"."offres" SET contrat='Alternance' WHERE contrat='Apprenti';
UPDATE "public"."offres" SET contrat='CDD' WHERE contrat='Contrat à durée déterminée';
UPDATE "public"."offres" SET contrat='CDI' WHERE contrat='Contrat à durée indéterminée';
UPDATE "public"."offres" SET contrat='Alternance' WHERE contrat like '%alternance%';
UPDATE "public"."offres" SET contrat='Stage' WHERE contrat like '%Stagiaire%';
UPDATE "public"."offres" SET teletravail='Oui' WHERE teletravail = 'oui';

# Acomytha — Avis sur le paquet prioritaire réécrit

Version examinée : commit `88534bed28a80274dba7f5622529485c2dc1a5b0` du 4 septembre 2026. Dépôt consulté à nouveau sur GitHub, puis lecture des fichiers de cette version. Aucune modification des histoires.

## Périmètre exact

Le fichier [PRIORITE.md](https://github.com/klaghmari-github/acomytha/blob/88534bed28a80274dba7f5622529485c2dc1a5b0/stories/PRIORITE.md) désigne deux arbres pour le chantier :

- `TREE-AUT-001`, « Le sac d’Amir sur le tapis rayé », N1, 3–4 ans, seul arbre ramifié dans `stories/arbres/`.
- `TREE-COL-001`, « La casserole et les pommes de Raphaël », N2, 4–5 ans, réécrit mais conservé dans `stories/archive/arbres/`.

Les 685 histoires atomiques restent dans le dossier actif. Elles ne font pas partie de cette relecture ciblée. L’expression « paquet prioritaire » désigne ici les deux histoires explicitement sélectionnées dans PRIORITE.md, pas tous les fichiers hors archives.

**Lecture effectuée : les 172 passages complets, avec les rôles vocaux, les 6 questions pédagogiques et leurs réponses/relances, les 26 nœuds de choix et les 54 fins.** Les passages communs ont été lus une fois ; je ne présente pas cela comme 54 lectures séparées du même début. Les 54 chemins ont été reconstruits avec l’algorithme de graphe du dépôt et contrôlés structurellement. Les enchaînements ont également servi à vérifier les continuités signalées ci-dessous.

Les textes `merged.json` et les textes Excel concordent pour tous les passages des deux histoires. Pas d’écoute des nouveaux audios ni de test du moteur en conditions réelles.

## Avis général

**La réécriture progresse nettement dans la suppression des slogans et la synchronisation des questions. Elle n’atteint pas encore le niveau narratif qui justifierait de prendre ces deux arbres comme modèles pour le reste du catalogue.**

Le point restant n’est pas principalement le nombre de descriptions : les deux histoires en ont. Il faut rendre plus nécessaire ce que les personnages font, donner du poids à leurs initiatives et conduire les choix vers une résolution préparée.

Mon appréciation éditoriale : Raphaël offre davantage de potentiel de jeu et de complicité ; Amir demande une reprise plus profonde de sa raison de préparer le sac et de ses fins. Ce sont des jugements fondés sur cette lecture, pas des résultats d’essais auprès d’enfants.

## Ce qui s’est réellement amélioré

| Élément | Résultat vérifié | Portée |
|---|---|---|
| Questions et réponses principales | Les six questions sont désormais cohérentes avec leur contexte et leur réponse principale | Alignement éditorial ; reconnaissance vocale non testée |
| Félicitations « Bravo » | Ancienne version : 69 occurrences pour AUT et 70 pour COL ; nouvelle version : zéro dans les deux textes | Occurrences sur tous les passages de chaque arbre, pas par écoute |
| Personnages | Amir/papa/maman et Raphaël/Mila/papa/maman cohérents dans les textes et la fiche `characters` examinés | Les anciennes colonnes de synthèse restent à traiter |
| Texte et script vocal | Aucune divergence de contenu après normalisation des espaces | Les attributions de voix ont aussi été lues |
| Graphe | 27 chemins par arbre ; aucun lien vers un identifiant absent, cycle, passage inaccessible ou chemin sans `passage_fin` dans le contrôle exécuté | Une fin techniquement atteinte n’est pas une conclusion littérairement satisfaisante |
| Petites actions | Pomme rattrapée, manche qui dépasse, couvercle déplacé, vitre essuyée | Le récit montre davantage de gestes concrets |
| Jeu et humour | « La soupe de yaourt, c’est nouveau », « Ticket pomme », « On ne réveille pas les pommes » | Des idées liées aux objets et à la scène, à développer plutôt qu’à multiplier artificiellement |

## TREE-AUT-001 — Le sac d’Amir sur le tapis rayé

Source lisible : [merged.json](https://github.com/klaghmari-github/acomytha/blob/88534bed28a80274dba7f5622529485c2dc1a5b0/stories/rewrites/TREE-AUT-001/merged.json).

### 1. Il manque la raison concrète de préparer ce sac

L’ouverture annonce : « Amir veut aller jouer », puis maman impose « On prépare ton sac d’abord ». Aucun projet de sortie ou de jeu nécessitant le sac n’est clairement installé. Plusieurs fins le font fermer puis ressortir immédiatement un objet pour jouer au même endroit.

Exemple : pomme → chambre → cubes, fin `CHK_T0001_P0001_T0002_P0003_T0003_P0001_F0001` : Amir ferme le sac au pied du lit, demande à jouer, puis sort deux cubes et les pose sur le tapis.

Ce n’est pas physiquement impossible. C’est un défaut de motivation narrative : le sac semble une étape imposée pour démontrer la leçon. Le désir « jouer » reste trop large pour donner une direction aux préparatifs.

**Correction proposée :** préciser dès le début une destination ou un projet qui nécessite ces objets. Le sac sert à transporter ce qu’Amir utilisera réellement. Faire vivre à la fin le jeu promis, avec les objets et conséquences du chemin choisi.

### 2. Les objets changent, mais leur utilité n’est pas toujours racontée

La cuillère après le yaourt et la boîte pour le pain sont des associations concrètes. En revanche, le petit gant près du yaourt ou les chaussons ajoutés au sac ne répondent à aucun besoin annoncé. Le personnage suit une nouvelle instruction, puis la suivante.

Passages : `CHK_T0001_P0002_T0002_P0002` et `CHK_T0001_P0002_T0002_P0003`.

L’objectif actuel du référentiel est bien de mettre dans le sac ce que papa ou maman a dit : la conduite est montrée. Mais sa mise en récit demeure trop proche d’une succession de consignes.

**Correction proposée :** montrer pourquoi un objet est utile au projet ou faire découvrir un petit manque au héros. Conserver les instructions parentales lorsqu’elles sont naturelles, sans leur confier toute la progression.

### 3. Certaines fins promettent encore ce qu’elles devraient montrer

- Pomme → chambre → dînette : « On va vraiment jouer, maintenant », puis une couverture retombe et l’histoire finit (`…P0001_T0002_P0003_T0003_P0003_F0001`).
- Pain → jardin → livre : Amir touche le livre « juste un peu », puis la fin arrive (`…P0003_T0002_P0002_T0003_P0002_F0001`).
- Pomme → cuisine → cubes : maman répond « Oui. Les cubes, après », mais Amir sort aussitôt un cube (`…P0001_T0002_P0001_T0003_P0001_F0001`). Le sens d’« après » devient peu clair.

**Correction proposée :** terminer par une action accomplie ou un petit moment de jeu développé, plutôt que par l’annonce du jeu ou un contact symbolique avec l’objet.

### 4. Une continuité d’objet est réellement cassée

Pain → jardin : `CHK_T0001_P0003_T0002_P0002` place le chapeau dans le sac, près du pain. Si le choix suivant est le livre, `CHK_T0001_P0003_T0002_P0002_T0003_P0002` commence : « Le livre est sous le chapeau, sur le banc. » Aucun retour du chapeau sur le banc n’a été raconté.

**Correction nécessaire :** laisser le chapeau sur le banc jusqu’à la découverte, ou situer le livre ailleurs. Recontrôler ensuite l’ordre des objets dans le sac.

### 5. Plusieurs images ou phrases restent maladroites

- « Amir le souffle » à propos du livre : préférer « Amir souffle dessus » (`…P0002_T0002_P0002_T0003_P0002`).
- « Le tapis rayé est calme » : image peu informative après un jeu de cubes (`…P0001_T0002_P0003_T0003_P0001_F0001`). Ce n’est pas une faute grammaticale, mais une faiblesse stylistique.
- Dans « Les cubes aussi, à côté », après « Le pain est dans la boîte », le mot « aussi » brouille la position des cubes (`…P0003_T0002_P0001_T0003_P0001_F0001`). Le passage précédent précisait pourtant qu’ils étaient à côté de la boîte.

L’ouverture possède 142 mots et retarde le désir derrière plusieurs détails successifs. Certains peuvent être conservés ; d’autres gagneraient à être répartis dans l’action. Plus de détails ne signifie pas automatiquement plus d’immersion.

### Direction éditoriale proposée

Un projet possible serait un petit goûter-jeu à transporter jusqu’à un lieu choisi. Les trois décisions pourraient concerner ce que l’on emporte, la façon de résoudre un petit problème de préparation et le jeu à réaliser à destination. La fin montrerait la réalisation. C’est une piste créative ; il faut la travailler sans imposer artificiellement 27 variations du même dernier geste.

## TREE-COL-001 — La casserole et les pommes de Raphaël

Source lisible : [merged.json](https://github.com/klaghmari-github/acomytha/blob/88534bed28a80274dba7f5622529485c2dc1a5b0/stories/rewrites/TREE-COL-001/merged.json).

### 1. Une meilleure base de jeu partagé

Raphaël veut donner des pommes à Mila. Le train, le bus et la voiture permettent de transformer le goûter en petit voyage. « Terminus, les pommes », « Ticket pomme » et « Terminus sieste » sont des éléments prometteurs : ils se comprennent dans la scène et créent une complicité.

L’arrivée de Mila et les réponses bonjour/s’il te plaît/merci sont mieux situées. La leçon principale est identifiable sans être annoncée comme un cours.

### 2. Le développement reste dominé par le service des pommes

Beaucoup de passages suivent encore le même mouvement : un adulte propose une rondelle, un enfant dit s’il te plaît, puis merci. Sur un chemin complet, on compte de 4 à 5 occurrences de « s’il te plaît » et de 4 à 8 de « merci », selon la branche. Ces comptes incluent le texte des questions et confirmations lorsqu’il contient la formule, sans inclure les variantes techniques ni une éventuelle relance.

La fréquence seule n’est pas une erreur : la politesse est le sujet. Mon objection est la faible évolution entre plusieurs de ces échanges. Raphaël a un souhait, mais peu de difficulté ou de découverte fait durer ce souhait. Papa et maman continuent souvent à distribuer.

**Correction proposée :** faire du voyage des pommes une action menée par les deux enfants, avec un petit problème concret de préparation ou d’installation. La politesse accompagne quelques échanges utiles ; les autres passages développent le jeu.

### 3. Le choix temporel arrive trop tard et manque de cadre

Les neuf nœuds de troisième choix demandent : « C’est quel moment ? Le matin, après la sieste, ou le soir. » L’arrivée de Mila, la lumière et le jeu sont déjà racontés. Rien n’explique si l’on choisit rétrospectivement l’heure de la scène, si le temps vient de passer ou si c’est une question de compréhension.

Ce n’est pas une contradiction temporelle certaine pour toutes les branches. C’est une ambiguïté de narration et d’interaction sur les 27 chemins.

**Correction proposée :** fixer le moment au début, le demander avant l’ouverture, ou remplacer ce choix par une décision que les personnages peuvent prendre maintenant. Un saut temporel choisi demanderait une transition explicite et adaptée à la scène.

### 4. Les mots de politesse restent parfois forcés

- Maman : « Donne-moi ton manteau ? » ; Mila : « S’il te plaît, tu peux le prendre » (`CHK_T0001_P0003`). Une réponse telle que « Oui, merci » serait naturelle ; si l’on veut une demande, Mila peut demander elle-même qu’on accroche son manteau.
- Raphaël : « Je peux le tabouret, après ? » ; Mila : « S’il te plaît, tu attends » (`CHK_T0001_P0001_T0002_P0003`). Reformuler la demande et la réponse pour qu’elles ressemblent à une conversation.
- « Une rondelle calme ? » apparaît dans deux variantes. Cela peut viser une fantaisie tendre, mais ne devient pas un gag compréhensible simplement parce que le personnage a sommeil.

**Correction proposée :** écrire d’abord le dialogue naturel qui sert la scène, puis vérifier la politesse ; ne pas faire entrer une formule dans chaque échange à tout prix.

### 5. Erreurs et ambiguïtés locales à corriger

- « Un rond de soleil pose sur le carrelage » dans l’ouverture : « se pose » ou « éclaire » selon l’image voulue.
- Près de la fenêtre, Mila dessine une route dans la buée ; Raphaël essuie et « la buée part » ; une suite le fait suivre « la route sur la vitre » (`…P0003_T0002_P0002`, puis `…P0003_T0002_P0002_T0003_P0001`). Préciser qu’une partie de la route reste, ou la redessiner.
- « Vous avez bien attendu le bol » dans une fin bus/tabouret/matin (`…P0002_T0002_P0003_T0003_P0001_F0001`) félicite une attente qui n’a pas été mise en scène. C’est un résidu de validation pédagogique automatique.

### Direction éditoriale proposée

Le « petit voyage des pommes » semble une meilleure promesse que la casserole du titre, qui sert surtout d’ambiance. Raphaël et Mila pourraient préparer une livraison imaginaire autour de la table, construire un arrêt ou décider comment partager leur cargaison. La fin accomplirait le voyage annoncé. Inutile d’ajouter une difficulté grave ou un conflit pour rendre cette petite aventure intéressante.

## Points communs à régler avant une validation du paquet

1. **Questions placées après le modèle.** Les six questions interviennent après la parole ou le geste demandé. Elles sont désormais cohérentes comme questions de rappel, mais ne font pas participer l’enfant avant la résolution. Leur position ne doit pas être décrite comme une anticipation lorsque ce n’est pas le cas.
2. **Relances prescriptives.** Les six relances sont de type « Dis : … ». Elles sont alignées mais invitent à répéter. Décider si l’objectif est le rappel, l’aide graduée ou la simple poursuite de l’histoire.
3. **N1 à trois options.** AUT propose trois options à chacun des 13 nœuds de choix, alors que REGLES.md fixe deux options maximum pour N1 et impose ailleurs trois options aux arbres. C’est une contradiction du cahier, pas une preuve que trois choix seraient toujours inadaptés. Elle doit être tranchée.
4. **Leçons secondaires obsolètes.** AUT déclare AUT.AFF.002, « Prendre son manteau », sans ce scénario ; COL déclare COL.ECO.001, « Écouter la maîtresse, en parler à la maison », absent de ce récit. Retirer ces déclarations ou justifier leur présence par un contenu réel. Ne pas ajouter une leçon pour sauver la métadonnée.
5. **Anciennes colonnes vocales.** L’ouverture SSML d’AUT parle encore de Lina, celle de COL de Sami. Les notes de relecture le signalent déjà. Ne pas conclure que l’audio utilise ces champs sans vérifier le pipeline ; les rendre inexploitables ou les synchroniser avant un usage ultérieur.
6. **Durée non mesurée.** AUT contient 393–437 mots par chemin ; COL 319–357. Avec les `rate_wpm` renseignés, le texte seul donne environ 205–228 s pour AUT et 148–166 s pour COL. Ce calcul exclut pauses, attente et relances et ne mesure pas la synthèse vocale. COL mérite une vérification particulière vis-à-vis du minimum de trois minutes ; aucun échec de durée réelle ne peut être affirmé sans audio.

## Priorités pour la prochaine passe

1. Pour Amir, écrire une phrase expliquant pourquoi le sac est nécessaire et une fin où ce projet se réalise. Réorganiser ensuite les branches autour de ce fil.
2. Pour Raphaël, développer le voyage imaginaire des pommes et remplacer ou déplacer le choix temporel. Garder les meilleures idées comiques.
3. Corriger les continuités, dialogues et erreurs de langue cités ; mettre à jour les métadonnées et dépendances.
4. Relire les chemins complets corrigés, puis écouter les nouveaux audios. Ne pas étendre la méthode au catalogue avant cette vérification.

**Décision éditoriale proposée : poursuivre le travail sur ces deux prototypes. Les progrès sont réels, mais le paquet n’est pas encore une référence de haute qualité à reproduire.**

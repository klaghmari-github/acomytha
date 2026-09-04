# Acomytha — compréhension du projet et trajectoire vers la commercialisation

Audit du dépôt au 4 septembre 2026 • commit `5e403fd1d4d205536d17053305a6573c84507ee8` • branche `main`.

## 1. Conclusion

Acomytha dispose d’un atelier de contenus important, d’un référentiel pédagogique structuré et d’un prototype web comportant catalogue, rôles parent/enfant/admin, lecteur et commerce. Ce dépôt ne permet pas de conclure à un produit prêt à être commercialisé. Les principaux obstacles sont la cohérence éditoriale, la disponibilité réelle des audios, la fidélité des interactions aux promesses et la sécurisation du parcours commercial.

Le cœur du produit est précis : le parent choisit ce qu’il souhaite faire découvrir à son enfant ; l’enfant vit une histoire audio où ces apprentissages prennent sens. La génération se fait avant publication. Le lecteur enfant ne sollicite pas de modèle génératif en direct.

La cible que tu fixes aujourd’hui est la maternelle et le début du primaire, puis tout le primaire. Le dépôt actuel décrit et étiquette exclusivement N1 (3–4 ans), N2 (4–5 ans), N3 (5–6 ans). L’extension au primaire est donc une direction produit, pas une couverture déjà démontrée.

## 2. Méthode et limites de preuve

Ordre suivi : documents Markdown/TXT, code Python et shell, puis résultats et Excel. Les composants JavaScript ont aussi été examinés car les interactions et la vitrine y sont implémentées.

- Dépôt identifié via GitHub, cloné et figé au commit ci-dessus.
- Inventaire : 20 Markdown, 3 TXT, 35 Python, 1 shell, 14 JavaScript ; aucun Word `.doc` ou `.docx` dans cet état de `main`. Les documents indiquent que les anciens Word ont été fusionnés dans la spécification. L’historique complet n’a pas été audité.
- Lecture des spécifications, décisions, stratégies, backlog, règles, processus de réécriture, documentation des outils et rapport de validation.
- Extraction de tous les 1 449 classeurs de `stories/arbres/`, des deux référentiels et comparaison aux réécritures.
- Contrôle structurel de tous les chemins avec l’algorithme `StoryGraph` du dépôt ; comparaison `text`/`script`, inventaire des audios et mesure des durées WAV.
- Reproduction isolée du comportement du moteur JavaScript pour une transition `auto_default`, jour et nuit.
- Lecture éditoriale d’exemples couvrant les 13 domaines et de chemins ramifiés. Ce n’est pas une relecture humaine exhaustive des 21 313 chemins.
- Pas d’écoute perceptive complète des audios, de transcription ASR, de tests avec enfants, de parcours navigateur réel ou de validation d’un site déployé. La qualité des voix n’est donc pas notée.
- La suite API n’a pas été exécutée : FastAPI, SQLAlchemy, lameenc, pytest et httpx étaient absents ; la tentative d’installation a été bloquée par l’accès réseau. Les constats API sont issus de lecture de code, et non de tests d’intégration réussis.
- Aucun changement du produit, des textes ou du dépôt distant. Les contrôles locaux ont été séparés des sources.

Convention : **constat** = fichier ou mesure ; **analyse** = interprétation motivée ; **proposition** = choix à envisager. Aucun résultat d’apprentissage ni intérêt commercial n’est présumé.

## 3. Ce qu’est réellement le produit

### La proposition pédagogique

Le référentiel compte 85 leçons, chacune avec un objectif observable, des messages attendus, des conduites sûres, des idées erronées à éviter, des intentions de réponse et des compatibilités. Il s’agit largement d’apprentissages du quotidien : émotions, relations, autonomie, sécurité, vie collective, hygiène, monde vivant, langage et premiers nombres.

Cette base n’est pas à elle seule un programme complet de maternelle ou de primaire. Elle contient notamment « Compter jusqu’à cinq ou dix », « Reconnaître un son », « Préparer son sac », « Respirer et faire une pause ». Une promesse scolaire globale demanderait une cartographie supplémentaire et une validation pédagogique.

Les règles recherchent un langage concret et positif, sans humiliation, sans menace affective, sans description imitable d’un danger. Les choix narratifs sont supposés neutres : l’enfant choisit un objet ou un lieu ; la sécurité n’est pas mise en jeu dans une mauvaise branche.

L’univers familial et les thèmes absents sont explicitement définis dans les règles. Il s’agit d’un choix éditorial du projet, pas d’un résultat scientifique ou d’une universalité démontrée. La troupe récente comprend Amir, Aniss, Sarah, Chouchou, Mila, Nino, Nina, Raphaël, Victorino, Victorina ; cette règle n’est pas encore appliquée à tout le corpus.

### Le parent et l’enfant n’achètent pas la même valeur

**Pour le parent**, la valeur visée est de choisir un contenu pertinent, de savoir ce qu’il contient, d’avoir confiance et de pouvoir l’utiliser facilement dans la vie familiale.

**Pour l’enfant**, la valeur visée est l’envie d’écouter : un personnage reconnaissable, une envie ou un petit problème, une aventure compréhensible, des choix qui ont un effet et une fin satisfaisante.

Mon analyse : le catalogue de leçons est un actif de conception. Ce qui devra déclencher l’achat est une expérience immédiatement convaincante, et non le seul nombre de fichiers disponibles.

### Les trois sens à séparer

| Notion | Sens constaté |
|---|---|
| Leçon | Objectif pédagogique identifié, réutilisé dans plusieurs récits. |
| Histoire atomique | Un chemin de lecture, avec passages, question et conclusion. |
| Arbre ramifié | Un fichier comprenant 27 chemins possibles ; une écoute n’en parcourt qu’un. |
| Histoires liées dans la vitrine | Autres fichiers partageant la même leçon principale. |

La vitrine dit « ramifications vers d’autres histoires », mais le moteur branche entre des passages d’un même `story_id`. Les liens de catalogue sont calculés séparément par leçon commune. Ces deux mécanismes ne doivent pas être présentés comme identiques.

## 4. Inventaire mesuré

| Indicateur | État observé |
|---|---:|
| Classeurs d’histoires | 1 449 |
| Atomiques | 685 |
| Ramifiés | 764 |
| Passages | 69 131 |
| Leçons principales distinctes | 85 |
| Domaines | 13 |
| Histoires N1 / N2 / N3 | 404 / 567 / 478 |
| Chemins structurels | 21 313 |
| Classeurs avec `fil_rouge` renseigné | 629 |
| Réécritures `merged.json` | 629 |
| Ensembles audio d’histoires présents | 2 |
| MP3 d’histoires présents | 91 |

Un fichier de test sonore ajoute un MP3 et un WAV hors histoires. Les 629 `fil_rouge` se répartissent en 537 atomiques et 92 ramifiés ; la présence de ce champ n’est pas une certification éditoriale.

Le rapport historique annonce 1 445 histoires et 68 787 chunks. Les quatre fichiers supplémentaires sont `TREE-AUT-045` à `TREE-AUT-048`. Ils sont absents du référentiel de liaisons. Ce dernier comporte 2 211 associations histoire/leçon et 28 580 lignes de passages pédagogiques ; 716 lignes d’association ont un titre différent du classeur actuel.

| Domaine | Fichiers |
|---|---:|
| AUT | 84 |
| COL | 70 |
| DIF | 133 |
| EMO | 203 |
| FAM | 76 |
| JEU | 73 |
| LAN | 50 |
| REL | 169 |
| SAN | 152 |
| SEC | 168 |
| SOC | 104 |
| TMP | 90 |
| VIV | 77 |

Les 13 domaines sont Autonomie, Vie collective, Différences, Émotions, Famille, Jeux, Langage, Relations, Santé et quotidien, Sécurité, Société, Temps et Vivant. Les codes restent des identifiants d’atelier.

### Résultats des contrôles structurels

Sur tous les fichiers : aucune cible explicite inexistante, aucun cycle détecté, aucun passage inaccessible selon `StoryGraph`, aucune terminaison inattendue détectée. Les 685 atomiques ont un chemin ; les 764 ramifiés en ont chacun 27. Les 69 131 textes correspondent à la concaténation de leurs scripts vocaux après normalisation des espaces.

C’est un point positif réel : la structure est exploitable. Cela ne prouve ni la cohérence d’une scène, ni l’exactitude pédagogique, ni la qualité sonore.

### Audio : ce qui existe, ce que cela prouve

| Ensemble | Couverture | Durée WAV cumulée d’un chemin, hors attentes |
|---|---|---:|
| ATOM-SAN.ALI.001-01 | 5/5 passages | 133,50 s, soit 2 min 13,5 s |
| TREE-SEC-001 | 86/86 passages | 101,11 à 119,00 s ; défaut 116,70 s |

Les deux ensembles couvrent tous leurs passages mais ne satisfont pas le minimum documentaire de trois minutes dans les fichiers audio mesurés. Les autres histoires ne disposent pas d’audio versionné ici. Des sorties peuvent exister sur la machine du fondateur ; le dépôt ne permet pas de le vérifier.

Les WAV et MP3 témoignent de fichiers audio, pas d’un `APPROVED_PACKAGE` validé. La correspondance sémantique entre audio ancien et texte réécrit reste à vérifier par transcription et écoute.

## 5. Architecture et chaîne de production

La chaîne actuelle est : référentiel Excel → histoires Excel → scripts de rôles et effets → synthèse locale Piper ou eSpeak → WAV/MP3 → chiffrement serveur à la demande → lecteur web.

Le backend utilise FastAPI, SQLAlchemy et SQLite. Le frontend utilise des modules JavaScript et des Custom Elements. Les rôles parent, enfant et admin sont contrôlés côté API. Les mots de passe et PIN sont hachés par scrypt. Les sessions sont des cookies HttpOnly ; le flag Secure dépend de la configuration.

Les histoires sont importées au démarrage si la table est vide. Le runtime n’utilise pas directement le référentiel `lecon_histoires.xlsx` comme table relationnelle complète : il importe une leçon principale et une chaîne de leçons secondaires dans `Story`. Les associations fines aux passages sont conservées dans l’atelier, pas exposées comme un moteur pédagogique complet.

Le chiffrement AES-GCM est implémenté ; la clé d’histoire est dérivée du secret maître et transmise au navigateur. Le navigateur déchiffre le passage et révoque son URL Blob après lecture. Ce n’est pas la gestion native Keystore/Keychain décrite dans la cible.

La synthèse vocale est réalisée hors écoute. L’orientation sans génération en direct est bien présente. En revanche, l’usage hors connexion reste à construire : le lecteur récupère graphes et passages sur le réseau et aucun service worker/cache de paquets n’a été trouvé dans le dépôt.

### Rôle des principaux scripts

| Script | Rôle et constat |
|---|---|
| `json_to_xlsx.py` | Conversion historique des anciens JSON vers les classeurs, options, rythme et questions. Les dossiers sources JSON ont été supprimés. |
| `make_ramifiee.py`, `batch_ramifiees.py` | Génération structurée d’arbres, combinaisons de scènes et de choix. Une structure combinatoire n’assure pas la cohérence du récit. |
| `validate.py` | Validation des anciens JSON, puis écriture de leur statut et du rapport. Ne parcourt pas les Excel actuels. |
| `build_referentiel_xlsx.py` | Construction des référentiels ; son point d’entrée lit encore un JSON de leçons retiré. |
| `rewrite_story.py` | Extraction, fusion et application des réécritures. Le merge automatique classe encore par longueur et présence de script, alors que les décisions demandent une fusion éditoriale. |
| `voice_cast.py` | Distribution de répliques par rôle et détection d’effets via lexique. |
| `xlsx_to_audio.py` | Synthèse, assemblage, traitement du signal, export WAV/MP3. Cache fondé sur l’existence/validité des fichiers, sans empreinte du texte pour invalider un ancien audio. |
| `gitpush.sh` | Synchronisation GitLab/GitHub, ajout de tout le dossier et commits. Peut créer un merge en cas de divergence, contrairement à la consigne de graphe linéaire. Ne pas l’utiliser comme outil d’audit. |

## 6. Écarts à traiter avant toute vente

### A. Commerce et accès — priorité bloquante

**1. Recharge : validation démo non isolée.** `confirm_demo` remplit la recharge après recherche par parent et référence sans vérifier un mode démo ou un paiement Stripe. La route de confirmation reste disponible. De plus, une exception Stripe retourne un parcours démo. Il faut rendre le mode production explicite, interdire le crédit sans événement de paiement vérifié et ne jamais basculer automatiquement d’un échec réel vers un crédit démo.

Critère : un utilisateur ne peut pas créditer une recharge réelle sans paiement ; un événement répété ne crédite qu’une fois, y compris en concurrence. Le garde-fou actuel sur `status == paid` ne constitue pas à lui seul une preuve d’atomicité concurrente.

**2. Contenu sans audio achetable.** `/shop/buy` vérifie l’existence et le solde, pas la disponibilité audio ni une publication validée. L’espace parent affiche le bouton d’achat même sans audio. Critère : seuls les produits dont tous les passages et chemins ont passé le contrôle de publication sont vendables.

**3. Option voix facturée sans enregistrement.** Le formulaire envoie un rôle, sans capture micro ni fichier. Le serveur accepte le fichier absent et débite le solde ; `apply-all` pose un booléen, sans pipeline de transformation connecté. Critère : retirer cette offre de la vente tant qu’une prestation livrable ne fonctionne pas de bout en bout.

**4. Commandes personnalisées incomplètes.** Le code débite, crée une commande et la liste ; aucun processus de production/livraison n’a été trouvé. Un service manuel reste possible, mais il faut définir délai, livraison, validation et traitement des échecs avant de le proposer.

**5. Upload vocal à durcir.** Le chemin combine des entrées utilisateur (`role`, nom de fichier), sans confinement explicite ni limite de taille/type visible. Utiliser des noms générés, vérifier le chemin résolu et contrôler taille et contenu. Aucun test offensif n’a été lancé.

**6. Démonstration et production à séparer.** Les comptes démo sont créés au bootstrap. Il faut une configuration de production sans ces comptes par défaut et des contrôles d’authentification adaptés. Les routes observées ne montrent pas de limitation des tentatives de PIN ou mot de passe, ni vérification d’e-mail/récupération de mot de passe.

### B. Expérience enfant — priorité bloquante

**7. Les choix sont court-circuités en journée.** Toutes les 9 932 transitions portent `night_policy=auto_default`. Le JavaScript teste `this.night || policy === "auto_default"` : la condition est vraie même le jour. La reproduction isolée joue la question puis la fin sans appeler le choix utilisateur. Critère : chaque choix diurne est proposé ; le silence suit une option définie ; les trois branches sont testables.

**8. Mode nuit incomplet.** La même branche de code joue la question de transition au lieu de la sauter. Aucun ajustement volume/vitesse n’est appliqué par le réglage nuit observé. Critère : nuit sans sollicitations, avec traitement sonore réellement vérifié, y compris des effets intégrés aux passages.

**9. Les réponses orales ne sont pas reconnues.** Une question d’écoute joue, attend, continue. Les options sont des boutons textuels. Aucun ASR ou reconnaissance d’intentions n’est branché. Une réponse correcte ne peut donc pas être enregistrée comme une compétence acquise. Pour des non-lecteurs, les boutons textuels ne suffisent pas à garantir l’autonomie.

**10. Arrêt, erreurs et mémoire.** La Map de préchargement conserve les passages chargés pendant toute la session ; elle n’est pas limitée à N+1. Certains échecs audio sont masqués tandis que les échecs de chargement peuvent remonter. Les attentes ne sont pas annulées lors de l’arrêt. Critère : erreur récupérable, aucun son après arrêt, pas de retour d’une ancienne session qui perturbe la nouvelle, mémoire bornée et test en réseau interrompu.

**11. Sélection familiale limitée.** Un profil enfant est créé par parent ; la sélection est attachée au parent. La liste proposée n’est pas un véritable plan de progression ou une file qui enchaîne automatiquement. Critère : décider ce que le MVP promet : sélection simple ou parcours organisé, puis l’implémenter exactement.

### C. Production et cohérence — priorité bloquante

**12. `APPROVED_AUDIO` trop faible.** L’import le déduit de la seule présence du MP3 racine. Critère : vérification de tous les passages, versions, empreintes, durées, décodage, validation éditoriale et package ; la présence d’un fichier ne doit pas créer une approbation.

**13. Rapport de validation historique.** Le validateur vise les JSON disparus. Le rapport « 1 445 approuvés » ne certifie pas les classeurs réécrits. Critère : validation de la source actuelle et rapport attaché à sa version ; échouer si le corpus attendu est vide.

**14. Sources dérivées désynchronisées.** 716 titres de liaisons sont obsolètes ; 13 réécritures diffèrent du texte des classeurs ; 6 titres de réécriture diffèrent. Exemple : Sarah est le personnage du texte de `ATOM-SAN.ALI.001-01`, mais `characters`, certains exports SSML et la relance mentionnent encore Lina. Critère : une publication met à jour tous les champs dérivés, pas seulement `text` et `script`.

**15. Audio non invalidé après réécriture.** Le bake saute un WAV/MP3 existant s’il semble valide, sans comparer le texte. L’import n’est pas relancé automatiquement sur une base déjà peuplée. Critère : versionner texte, script, voix, FX et configuration ; invalider les sorties dépendantes à chaque modification.

**16. Effets absents.** 3 821 passages ont `sons` renseigné mais `outils/fx/` ne contient que le lexique, aucun WAV. Un effet absent devient 1,15 seconde de silence. Les effets d’un passage sont tous insérés après la première réplique narrative, pas à leur position exacte dans la scène. Critère : chaque effet référencé existe et son placement narratif est vérifié.

**17. Durées affichées estimées de façon fragile.** `fill_durations` divise les mots d’un ramifié par neuf ; pour les atomiques audio il utilise la taille du MP3 avec un débit supposé de 64 kb/s, alors que le générateur exporte à 128 kb/s. Il borne ensuite entre 45 et 720 secondes. Critère : calculer la durée des chemins avec les métadonnées réelles, en distinguant attente, jour et nuit.

**18. Déploiement reproductible absent du dépôt examiné.** Pas de manifeste de dépendances Python trouvé, ni workflow CI de livraison ou procédure complète de restauration. Cela n’établit pas leur absence ailleurs. Critère : installation reproductible, environnement isolé, sauvegarde/restauration testée, journalisation et monitoring minimal.

## 7. Qualité éditoriale : diagnostic concret

Le backlog pose déjà le bon problème : certains textes ressemblent à des scénarios de leçon. Les réécritures ajoutent du décor et des dialogues, mais cela ne suffit pas toujours à produire un récit.

- Dans `TREE-SEC-001`, « jaune, le seau, ou blanc » mélange catégories et objets dans un même choix. Un graphe peut être valide avec des options narrativement incohérentes.
- Dans `TREE-EMO-001`, le décor passe de l’école à la cuisine avec du sable, de la terre et une tasse sans transitions suffisamment établies ; les descriptions émotionnelles se répètent.
- Dans `ATOM-LAN.NOM.001-01`, le premier passage compte cinq pommes puis deux tomates. La question revient aux pommes et la confirmation répond cinq ; ce n’est pas automatiquement faux, mais la multiplication des ensembles peut rendre l’attention et la référence de la question plus difficiles.
- `ATOM-TMP.JOU.001-01` associe systématiquement soleil/jour et lune/nuit. Il faut vérifier que la simplification n’enseigne pas une règle exclusive inexacte. C’est un point de revue éditoriale, pas une conclusion que tous les récits du domaine seraient incorrects.
- Les textes réécrits répètent souvent « Bravo » et « bon travail ». La félicitation n’est pas un problème en soi ; sa fréquence peut faire entendre l’exercice davantage que l’aventure.

**Proposition de grille éditoriale** : envie concrète du héros ; petit obstacle ; action qui évolue ; choix ayant une conséquence perceptible ; continuité lieu/temps/objets/personnages ; question compréhensible sans indice visuel ; apprentissage vécu ; fin qui résout l’envie initiale. Une décoration sensorielle sans progression ne satisfait pas cette grille.

## 8. Produit de lancement proposé

### Positionnement à tester

Des histoires audio pour grandir au quotidien, avec des aventures que l’enfant peut faire évoluer et des apprentissages choisis par ses parents.

Il s’agit d’une proposition de positionnement, pas d’une promesse déjà tenue par le build actuel. Ne pas annoncer de reconnaissance vocale, de hors-ligne, de résultats pédagogiques ou de programme primaire complet avant validation.

### Une première collection terminée

Je recommande de choisir un petit nombre de récits représentatifs à rendre excellents : par exemple 12 histoires linéaires et 3 ramifiées, réparties entre émotions, autonomie et relations. Ce nombre est une proposition de périmètre, pas une estimation de demande. Les contenus de sécurité demandent leur propre validation avant exposition.

La version commercialisée devrait avoir : une sélection adaptée à l’âge, un essai réellement représentatif, une lecture fiable, des choix accessibles, un mode calme fonctionnel, des contenus publiés versionnés, un prix explicite et une assistance joignable.

Reporter les voix personnalisées et commandes payantes tant que leur livraison n’est pas opérationnelle. Maintenir un chantier primaire séparé : objectifs, vocabulaire, durée, complexité narrative et modalités d’interaction propres au CP/CE1 puis aux niveaux suivants. Ne pas simplement changer l’étiquette d’âge.

### Trois pistes créatives compatibles avec le socle

1. **Les petits défis d’un personnage.** Un héros revient avec des envies reconnaissables ; les apprentissages apparaissent dans les actions. Construire des préférences et petits traits cohérents, pas uniquement une liste de prénoms.
2. **Une aventure, plusieurs façons de la vivre.** Le choix change réellement la suite : construire un pont avec des cubes ou chercher une autre route pour livrer un objet. La coopération se vit dans chaque branche, sans être répétée comme une définition.
3. **La petite suite dans la vraie vie.** Après l’écoute, proposer au parent une seule activité courte facultative liée à l’histoire. Le suivi distingue « écouté », « revisité » et « observé par le parent » ; il n’affirme pas « acquis » sur la base d’une écoute.

Les propositions nécessitent conception et essais ; elles ne sont pas présentées comme déjà présentes.

## 9. Vitrine : rendre le produit compréhensible et désirable

La vitrine actuelle est un accueil, des chiffres, des phrases de promesse et un catalogue filtrable. Elle expose le volume total, y compris les contenus sans audio. Elle donne très peu de matière pour juger la qualité d’une histoire ou comprendre précisément l’usage familial.

L’évaluation est fondée sur le code HTML/JS/CSS, pas sur une inspection visuelle d’un site déployé.

### Structure proposée

| Zone | Question du parent | Contenu utile |
|---|---|---|
| Première vue | Qu’est-ce que c’est et pour qui ? | Une promesse précise, la tranche d’âge effectivement servie et un bouton d’écoute. |
| Démonstration | Est-ce agréable et différent ? | Un extrait édité contenant récit, deux voix et un vrai moment de choix, ou une histoire de démonstration. |
| Fonctionnement | Que dois-je faire ? | Choisir un besoin, préparer l’écoute, lancer l’histoire ; explication simple de l’interaction disponible. |
| Collections | Laquelle convient à mon enfant ? | Quelques collections éditorialisées, objectifs concrets et titres narratifs. |
| Confiance | Qui contrôle les contenus ? | Processus réellement suivi, versions, engagements vérifiables, identité/contact de l’éditeur. |
| Offre | Qu’est-ce que je paie et reçois ? | Prix en euros et acm si conservé, contenu inclus, disponibilité, modalités d’accès. |
| FAQ | Et dans ma vie réelle ? | Internet, appareil, durée, enfant non lecteur, mode calme, changement de téléphone, aide. |

Un extrait de dix secondes peut s’arrêter avant l’action ; l’allongement de l’introduction aggrave ce risque. Je propose de comparer l’extrait actuel à un extrait représentatif de 45–90 secondes, ou une histoire complète de démonstration. Ce serait une évolution explicite de la décision actuelle, pas un changement silencieux.

Conserver le symbole acm comme identité est possible ; la conversion ne devrait pas demander un calcul mental pour comprendre l’achat. À paramètres actuels : 10 € → 10 acm ; 20 € → 25 ; 30 € → 45 ; 40 € → 70 ; 50 € → 100. Ce sont les paramètres du code, pas une recommandation de tarif. L’équilibre économique doit intégrer le travail éditorial, l’audio, l’hébergement, l’assistance et les services personnalisés ; « Piper local » ne signifie pas « produit sans coût ».

La restriction à un appareil peut créer une friction familiale (deux parents, remplacement de téléphone). Il faut mesurer son utilité et prévoir une récupération accessible avant d’en faire une contrainte commerciale définitive.

Le logo à ramifications et les points de progression peuvent rester la signature ; ils n’imposent pas un décor de forêt dans l’espace parent, ce qui respecte la décision D14. La vitrine peut être chaleureuse et éditoriale, avec des illustrations facultatives, tout en gardant l’histoire compréhensible uniquement par l’audio.

## 10. Feuille de route avec critères de sortie

| Ordre | Livrable | Critère de sortie |
|---|---|---|
| 1 — Clarifier | Contrat produit et vocabulaire unifiés | Une définition de l’histoire, du chemin, de l’interaction, du calme et de la disponibilité. |
| 2 — Fermer les blocages | Commerce, accès, modes jour/nuit et lecture corrigés | Aucun achat indisponible, aucun crédit réel non payé, aucun service facturé sans livraison, choix effectivement accessibles. |
| 3 — Fiabiliser la publication | Validation Excel + versions + invalidation audio | Chaque produit public renvoie à un texte approuvé, un audio cohérent et tous ses chemins vérifiés. |
| 4 — Terminer la collection pilote | Récits relus et audio final | Continuité éditoriale, durée mesurée, voix/effets écoutés, test réel sur appareils cibles. |
| 5 — Tester en familles | Observations documentées | Compréhension du parent, démarrage, compréhension des choix, incidents et désir de réécoute observés. |
| 6 — Finaliser la vitrine | Démo, collections, prix et confiance | La démonstration correspond exactement à ce qui est livré ; aucun chiffre brouillon compté comme produit disponible. |
| 7 — Ouvrir progressivement | Offre limitée et exploitation prête | Paiement bout en bout, livraison, assistance, restauration et revue des obligations applicables au marché choisi. |
| 8 — Étendre au primaire | Référentiel et récits supplémentaires | Objectifs et niveaux validés, qualité du premier produit maintenue. |

Pour le pilote, recueillir séparément : arrivée → écoute de démo → inscription → première écoute complète → réécoute → achat. Mesurer aussi les abandons techniques, l’aide adulte nécessaire et la compréhension d’une scène. Définir les seuils après les premières observations plutôt qu’inventer des taux de réussite.

Avant ouverture, faire vérifier les conditions de vente, la confidentialité, le traitement des données des familles, les droits des contenus/voix/effets et les règles du marché ciblé. Cet audit ne constitue pas une vérification juridique ou de licences ; aucun registre complet de droits n’a été trouvé dans le dépôt examiné.

## 11. Décisions et preuves encore manquantes

- Où se trouvent les audios non versionnés, s’ils ont déjà été produits, et à quelle version de texte correspondent-ils ?
- Existe-t-il un site déployé, avec configuration et paiements distincts du développement ?
- Quel est le mode d’interaction retenu au lancement pour l’enfant non lecteur : accompagnement parent, commandes accessibles ou reconnaissance vocale validée ?
- Quelle tranche précise du début de primaire entre dans la première offre ?
- Qui valide les textes et les contenus sensibles, et avec quelle traçabilité ?
- Le modèle commercial prioritaire sera-t-il l’achat à l’unité, la collection ou un autre modèle ? Le dépôt ne démontre pas lequel les parents préfèrent.

Ces questions n’empêchent pas de commencer : la fermeture des blocages de vente, la fiabilisation des versions et l’amélioration d’un premier petit ensemble sont utiles dans tous ces scénarios.

## 12. Sources de référence

Les liens ci-dessous pointent au commit audité, pour conserver le contexte exact.

- [gestion_projet/specification/AcoMytha_Specification.md](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/gestion_projet/specification/AcoMytha_Specification.md)
- [gestion_projet/decisions/DECISIONS_APP.md](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/gestion_projet/decisions/DECISIONS_APP.md)
- [gestion_projet/backlog/Features.md](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/gestion_projet/backlog/Features.md)
- [gestion_projet/strategies/STRAT-001-validation.md](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/gestion_projet/strategies/STRAT-001-validation.md)
- [gestion_projet/strategies/STRAT-002-audio.md](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/gestion_projet/strategies/STRAT-002-audio.md)
- [gestion_projet/strategies/STRAT-003-modele-donnees.md](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/gestion_projet/strategies/STRAT-003-modele-donnees.md)
- [gestion_projet/strategies/STRAT-004-moteur-lecture.md](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/gestion_projet/strategies/STRAT-004-moteur-lecture.md)
- [gestion_projet/strategies/STRAT-005-application-web.md](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/gestion_projet/strategies/STRAT-005-application-web.md)
- [stories/REGLES.md](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/stories/REGLES.md)
- [stories/REWRITE.md](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/stories/REWRITE.md)
- [stories/DECISIONS_EXCEL.md](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/stories/DECISIONS_EXCEL.md)
- [stories/referentiel/lecons.xlsx](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/stories/referentiel/lecons.xlsx)
- [stories/referentiel/lecon_histoires.xlsx](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/stories/referentiel/lecon_histoires.xlsx)
- [stories/rapports/validation.json](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/stories/rapports/validation.json)
- [app/acomytha/catalog.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/acomytha/catalog.py)
- [app/acomytha/payments.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/acomytha/payments.py)
- [app/acomytha/api/shop.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/acomytha/api/shop.py)
- [app/acomytha/api/auth.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/acomytha/api/auth.py)
- [app/acomytha/api/public.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/acomytha/api/public.py)
- [app/acomytha/api/stories.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/acomytha/api/stories.py)
- [app/acomytha/graph.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/acomytha/graph.py)
- [app/acomytha/crypto_audio.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/acomytha/crypto_audio.py)
- [app/acomytha/preview.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/acomytha/preview.py)
- [app/acomytha/seed.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/acomytha/seed.py)
- [app/frontend/js/core/StoryEngine.js](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/frontend/js/core/StoryEngine.js)
- [app/frontend/js/core/CryptoPlayer.js](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/frontend/js/core/CryptoPlayer.js)
- [app/frontend/js/ui/HomeApp.js](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/frontend/js/ui/HomeApp.js)
- [app/frontend/js/ui/ParentApp.js](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/frontend/js/ui/ParentApp.js)
- [app/frontend/js/ui/ChildApp.js](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/app/frontend/js/ui/ChildApp.js)
- [stories/outils/validate.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/stories/outils/validate.py)
- [stories/outils/rewrite_story.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/stories/outils/rewrite_story.py)
- [stories/outils/xlsx_to_audio.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/stories/outils/xlsx_to_audio.py)
- [stories/outils/build_referentiel_xlsx.py](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/stories/outils/build_referentiel_xlsx.py)
- [stories/outils/fx/lexique.json](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/stories/outils/fx/lexique.json)
- [gitpush.sh](https://github.com/klaghmari-github/acomytha/blob/5e403fd1d4d205536d17053305a6573c84507ee8/gitpush.sh)

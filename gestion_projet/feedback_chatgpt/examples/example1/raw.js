#!/usr/bin/env node
/** Réécriture éditoriale v2 de TREE-AUT-001, graphe et identifiants inchangés. */

import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const root = process.cwd();
const xlsxPath = `${root}/stories/arbres/TREE-AUT-001.xlsx`;
const mergedPath = `${root}/stories/rewrites/TREE-AUT-001/merged.json`;

const S = (lines) => ({
  text: lines.map(([, phrase]) => phrase).join(" "),
  script: lines.map(([role, phrase]) => `${role}|${phrase}`).join("\n"),
});

const prep = {
  1: {
    labels: ["le manteau", "les bottes", "le petit linge"],
    scene: S([
      ["narrateur", "Amir choisit d'abord son manteau jaune."],
      ["narrateur", "Il cherche la manche retournée."],
      ["enfant-m", "Je l'ai trouvée !"],
      ["narrateur", "Il remet la manche dans le bon sens."],
      ["maman", "Ton manteau est prêt."],
      ["narrateur", "Amir glisse ensuite le bateau dans le sac."],
      ["narrateur", "Maman ajoute le petit linge."],
      ["narrateur", "Les bottes attendent près de la porte."],
    ]),
    question: S([["narrateur", "Où Amir range-t-il son bateau ?"]]),
    answer: ["dans le sac", "sac|le sac|dans le sac|au fond du sac", "Le bateau est dans le sac."],
    confirm: S([
      ["narrateur", "Le bateau repose au fond du sac."],
      ["narrateur", "Le linge protège sa voile."],
      ["papa", "Bottes aux pieds, capitaine ?"],
      ["enfant-m", "Bottes aux pieds, manteau fermé !"],
    ]),
    arrival: {
      1: "Le manteau jaune brille sous la gouttière.",
      2: "Une odeur de soupe reste dans son col.",
      3: "Le vent gonfle doucement son manteau jaune.",
    },
    coda: [
      ["narrateur", "Amir suspend son manteau jaune."],
      ["narrateur", "Une goutte tombe de sa capuche."],
    ],
  },
  2: {
    labels: ["le manteau", "les bottes", "le petit linge"],
    scene: S([
      ["narrateur", "Amir choisit d'abord ses bottes rouges."],
      ["narrateur", "Une botte porte encore de la boue."],
      ["maman", "Je te montre un petit coin de boue."],
      ["narrateur", "Maman commence avec le linge."],
      ["narrateur", "Puis Amir frotte jusqu'au bout."],
      ["enfant-m", "Elle est prête !"],
      ["narrateur", "Le bateau rejoint le sac."],
      ["narrateur", "Le manteau attend sur la chaise."],
    ]),
    question: S([["narrateur", "Qui termine d'essuyer la botte ?"]]),
    answer: ["Amir", "amir|c'est amir|amir termine|le garçon", "Amir termine d'essuyer la botte."],
    confirm: S([
      ["narrateur", "La semelle rouge est propre."],
      ["narrateur", "Amir enfile les deux bottes."],
      ["papa", "Et le manteau, capitaine ?"],
      ["enfant-m", "Fermé jusqu'en haut !"],
    ]),
    arrival: {
      1: "Ses bottes font floc sous la gouttière.",
      2: "Ses bottes traversent la terre molle.",
      3: "Ses bottes s'arrêtent au bord du sable.",
    },
    coda: [
      ["narrateur", "À la porte, Amir retire ses bottes."],
      ["narrateur", "Deux traces rouges restent sur le tapis."],
    ],
  },
  3: {
    labels: ["le manteau", "les bottes", "le petit linge"],
    scene: S([
      ["narrateur", "Amir choisit d'abord le petit linge bleu."],
      ["narrateur", "Il est encore chaud du radiateur."],
      ["maman", "À quoi servira-t-il ?"],
      ["enfant-m", "À sauver mon bateau mouillé."],
      ["narrateur", "Amir le roule comme un petit coussin."],
      ["narrateur", "Le bateau se pose dessus."],
      ["narrateur", "Le manteau et les bottes sont prêts."],
    ]),
    question: S([["narrateur", "Où Amir met-il le petit linge ?"]]),
    answer: ["dans le sac", "sac|le sac|dans le sac", "Le petit linge va dans le sac."],
    confirm: S([
      ["narrateur", "Le linge protège le bateau."],
      ["narrateur", "Amir ferme doucement le sac."],
      ["papa", "Tout est prêt, capitaine ?"],
      ["enfant-m", "Manteau, bottes et bateau !"],
    ]),
    arrival: {
      1: "Le linge bleu attend dans le sac.",
      2: "Le linge garde encore un peu de chaleur.",
      3: "Le linge attend le bateau mouillé.",
    },
    coda: [
      ["narrateur", "Amir enveloppe le bateau dans le linge."],
      ["narrateur", "Une tache humide dessine une petite île."],
    ],
  },
};

const opening = S([
  ["narrateur", "Au bout d'une petite rue vit Amir."],
  ["narrateur", "Sa maison possède un jardin minuscule."],
  ["narrateur", "Ce matin-là, la pluie vient de partir."],
  ["narrateur", "Les pavés brillent derrière la fenêtre."],
  ["narrateur", "Maman prépare une soupe dans la cuisine."],
  ["narrateur", "Papa travaille près du volet jaune."],
  ["narrateur", "Son ordinateur souffle comme un petit vent."],
  ["narrateur", "Sur le tapis, Amir plie une feuille."],
  ["narrateur", "Un pli devient coque."],
  ["narrateur", "Un autre pli devient voile."],
  ["enfant-m", "Capitaine Amir est prêt !"],
  ["narrateur", "Il pousse le bateau vers papa."],
  ["narrateur", "Le bateau heurte sa pantoufle."],
  ["papa", "Votre navire cherche-t-il la mer ?"],
  ["enfant-m", "Oui, mais la mer est très loin."],
  ["narrateur", "Une goutte tombe dehors."],
  ["narrateur", "Puis une deuxième rejoint la gouttière."],
  ["narrateur", "Amir colle son nez contre la vitre."],
  ["narrateur", "L'eau dessine des chemins dans le jardin."],
  ["enfant-m", "Papa, mon bateau peut voyager ici !"],
  ["papa", "Alors rapporte-nous une grande histoire."],
  ["enfant-m", "Et peut-être un trésor !"],
  ["narrateur", "Maman pose le petit sac près d'Amir."],
  ["maman", "Prépare ton expédition avant que le soleil sèche tout."],
]);

const t1 = S([
  ["narrateur", "Amir doit préparer trois choses."],
  ["narrateur", "Son manteau, ses bottes et un linge."],
  ["maman", "Laquelle prépares-tu d'abord ?"],
]);

const t2 = S([
  ["narrateur", "Dehors, trois chemins brillent encore."],
  ["narrateur", "La rivière de la gouttière."],
  ["narrateur", "Le port caché entre les choux."],
  ["narrateur", "Puis l'île devant le bac."],
  ["papa", "Quelle route choisis-tu, capitaine ?"],
]);

const routes = {
  1: {
    labels: ["attendre trois gouttes", "demander l'aide de papa", "chercher un autre départ"],
    arrival(p) { return S([
      ["narrateur", p.arrival[1]],
      ["narrateur", "Une rigole court sous la gouttière."],
      ["narrateur", "Amir pose le bateau sur l'eau."],
      ["narrateur", "Le voyage commence enfin."],
      ["narrateur", "Soudain, une grande feuille tourne."],
      ["narrateur", "Elle bouche toute la rivière."],
      ["narrateur", "Le bateau s'immobilise derrière elle."],
      ["enfant-m", "Vite, le soleil revient !"],
      ["papa", "L'eau baisse déjà."],
    ]); },
    prompt: S([
      ["narrateur", "La feuille tient bon."],
      ["narrateur", "L'eau devient moins profonde."],
      ["papa", "Que tente le capitaine ?"],
    ]),
    acts: {
      1: S([
        ["enfant-m", "J'attends trois gouttes."],
        ["narrateur", "La première frappe la feuille."],
        ["narrateur", "La deuxième soulève son bord."],
        ["narrateur", "La troisième la fait pivoter."],
        ["narrateur", "Un passage étroit apparaît."],
        ["enfant-m", "Maintenant, petit bateau !"],
        ["narrateur", "Le bateau file sous une brindille."],
      ]),
      2: S([
        ["enfant-m", "Papa, j'ai besoin de toi."],
        ["papa", "Tiens le bateau contre le courant."],
        ["narrateur", "Papa soulève doucement la feuille."],
        ["narrateur", "Amir maintient la coque bien droite."],
        ["papa", "Maintenant, laisse-le partir."],
        ["narrateur", "Le bateau bondit dans l'eau libre."],
      ]),
      3: S([
        ["enfant-m", "Je cherche un autre départ."],
        ["narrateur", "Amir longe la rivière sans courir."],
        ["narrateur", "Derrière un pot, l'eau recommence."],
        ["narrateur", "Il pose le bateau après la feuille."],
        ["narrateur", "Le courant l'emporte vers les violettes."],
        ["enfant-m", "J'ai trouvé le passage secret !"],
      ]),
    },
    endings: {
      1: S([
        ["narrateur", "Le bateau atteint le pot violet."],
        ["narrateur", "Une petite feuille colle à sa proue."],
        ["narrateur", "Amir la garde comme drapeau."],
        ["narrateur", "Puis il rentre avant la dernière goutte."],
        ["papa", "Quel trésor rapporte votre navire ?"],
        ["enfant-m", "Un drapeau gagné après trois gouttes."],
      ]),
      2: S([
        ["narrateur", "Le bateau traverse la rivière délivrée."],
        ["narrateur", "Une ligne brillante marque sa coque."],
        ["narrateur", "Amir la montre en rentrant."],
        ["papa", "Nous avons formé un bon équipage."],
        ["enfant-m", "Moi devant, et toi derrière !"],
      ]),
      3: S([
        ["narrateur", "Le courant dépose une brindille sur la voile."],
        ["narrateur", "Amir rapporte le bateau ainsi décoré."],
        ["papa", "Je reconnais le passage secret."],
        ["enfant-m", "Il commence derrière le grand pot."],
      ]),
    },
  },
  2: {
    labels: ["compter les passages", "attendre le courant", "demander conseil à maman"],
    arrival(p) { return S([
      ["narrateur", p.arrival[2]],
      ["narrateur", "Entre les choux se cache un port."],
      ["narrateur", "Trois feuilles flottent devant l'entrée."],
      ["narrateur", "Le bateau avance vers elles."],
      ["narrateur", "La première touche sa voile."],
      ["narrateur", "La deuxième ferme le passage."],
      ["narrateur", "La troisième frôle un jeune chou."],
      ["enfant-m", "Je ne veux rien abîmer."],
      ["narrateur", "Amir retient aussitôt son bateau."],
    ]); },
    prompt: S([
      ["narrateur", "Le port semble fermé."],
      ["narrateur", "Derrière, la terre forme un petit quai."],
      ["maman", "Comment entrera ton bateau ?"],
    ]),
    acts: {
      1: S([
        ["narrateur", "Amir observe les trois feuilles."],
        ["enfant-m", "Une, deux, trois."],
        ["narrateur", "Entre deux et trois, l'eau scintille."],
        ["narrateur", "Il guide doucement la proue."],
        ["narrateur", "Le bateau traverse sans toucher les choux."],
        ["enfant-m", "Quai numéro deux !"],
      ]),
      2: S([
        ["enfant-m", "J'attends le prochain courant."],
        ["narrateur", "Amir garde le bateau contre sa botte."],
        ["narrateur", "L'eau pousse lentement la première feuille."],
        ["narrateur", "Puis la seconde s'écarte aussi."],
        ["narrateur", "Le port s'ouvre juste assez."],
        ["narrateur", "Le bateau glisse jusqu'au quai."],
      ]),
      3: S([
        ["enfant-m", "Maman, peux-tu regarder mon port ?"],
        ["maman", "Vois-tu cette rigole près du thym ?"],
        ["narrateur", "Amir suit la rigole avec son doigt."],
        ["narrateur", "Elle contourne toutes les jeunes pousses."],
        ["enfant-m", "Voilà ma route !"],
        ["narrateur", "Le bateau rejoint le quai sans rien plier."],
      ]),
    },
    endings: {
      1: S([
        ["narrateur", "Au quai, une feuille devient drapeau."],
        ["narrateur", "Amir la plante dans le sable humide."],
        ["narrateur", "Les trois choux restent bien droits."],
        ["narrateur", "À table, Amir dessine son port."],
        ["maman", "Quel passage as-tu choisi ?"],
        ["enfant-m", "Celui entre deux et trois."],
      ]),
      2: S([
        ["narrateur", "Le bateau touche enfin le quai de terre."],
        ["narrateur", "Une odeur de chou monte de sa coque."],
        ["narrateur", "Amir éclate de rire en rentrant."],
        ["papa", "Ton trésor sent vraiment le potager !"],
        ["enfant-m", "C'est le parfum de mon port."],
      ]),
      3: S([
        ["narrateur", "La rigole conduit le bateau au thym."],
        ["narrateur", "Une minuscule fleur touche sa voile."],
        ["narrateur", "Amir rentre avec son navire parfumé."],
        ["maman", "Tu as trouvé sans écraser mes choux."],
        ["enfant-m", "La route passait près du thym."],
      ]),
    },
  },
  3: {
    labels: ["chercher une autre flaque", "creuser un petit canal", "faire une piste de sable"],
    arrival(p) { return S([
      ["narrateur", p.arrival[3]],
      ["narrateur", "Devant le bac brille une île ronde."],
      ["narrateur", "Au milieu repose un caillou blanc."],
      ["enfant-m", "Voilà l'île au trésor !"],
      ["narrateur", "Amir approche le bateau de l'eau."],
      ["narrateur", "Mais la flaque devient soudain plus petite."],
      ["narrateur", "Le sable boit ses derniers reflets."],
      ["enfant-m", "Mon île disparaît !"],
      ["papa", "Il reste encore un peu de temps."],
    ]); },
    prompt: S([
      ["narrateur", "Le bateau attend dans les mains d'Amir."],
      ["narrateur", "Le caillou blanc reste hors d'atteinte."],
      ["papa", "Comment sauver cette expédition ?"],
    ]),
    acts: {
      1: S([
        ["enfant-m", "Je cherche une autre flaque."],
        ["narrateur", "Amir regarde autour du bac."],
        ["narrateur", "Sous le banc, une eau claire résiste."],
        ["narrateur", "Il y pose vite son bateau."],
        ["narrateur", "Le navire contourne un galet gris."],
        ["enfant-m", "Une nouvelle île !"],
      ]),
      2: S([
        ["enfant-m", "Je creuse un petit canal."],
        ["narrateur", "Amir prend la pelle du bac."],
        ["narrateur", "Papa verse doucement un fond d'arrosoir."],
        ["narrateur", "L'eau suit le canal jusqu'au caillou."],
        ["narrateur", "Le bateau avance dans cette rivière neuve."],
        ["enfant-m", "L'île revient !"],
      ]),
      3: S([
        ["enfant-m", "Je fabrique une piste de sable."],
        ["narrateur", "Amir tasse une longue bande humide."],
        ["narrateur", "Il pose la coque bien droite."],
        ["narrateur", "Puis il souffle dans la voile."],
        ["narrateur", "Le bateau glisse jusqu'au caillou blanc."],
        ["enfant-m", "Aujourd'hui, mon bateau roule !"],
      ]),
    },
    endings: {
      1: S([
        ["narrateur", "Le galet gris devient le nouveau trésor."],
        ["narrateur", "Amir le laisse près de la flaque."],
        ["narrateur", "Il rapporte seulement son histoire."],
        ["papa", "L'île a changé, mais le voyage continue."],
        ["enfant-m", "Demain, je chercherai encore."],
      ]),
      2: S([
        ["narrateur", "Le bateau atteint enfin le caillou blanc."],
        ["narrateur", "Son reflet danse dans le petit canal."],
        ["narrateur", "Puis l'eau disparaît doucement dans le sable."],
        ["enfant-m", "J'ai vu mon île revenir."],
        ["papa", "Juste assez longtemps pour ton voyage."],
      ]),
      3: S([
        ["narrateur", "La proue touche doucement le caillou blanc."],
        ["narrateur", "Un grain doré reste sur la coque."],
        ["narrateur", "Amir le montre à papa en rentrant."],
        ["papa", "Un vrai trésor de capitaine."],
        ["enfant-m", "Mon bateau connaît aussi les routes."],
      ]),
    },
  },
};

const texts = new Map();
const questions = new Map();
const labels = new Map();
const put = (id, packed) => texts.set(id, packed);

put("CHK_T0000_P0000", opening);
put("CHK_T0001_P0000", t1);
labels.set("CHK_T0001_P0000", prep[1].labels);

for (const p of [1, 2, 3]) {
  const base = `CHK_T0001_P000${p}`;
  put(base, prep[p].scene);
  put(`${base}_Q0001`, prep[p].question);
  questions.set(`${base}_Q0001`, prep[p].answer);
  put(`${base}_C0001`, prep[p].confirm);
  put(`${base}_T0002_P0000`, t2);
  labels.set(`${base}_T0002_P0000`, ["la rivière de la gouttière", "le port des choux", "l'île du bac"]);
  for (const route of [1, 2, 3]) {
    const rb = `${base}_T0002_P000${route}`;
    put(rb, routes[route].arrival(prep[p]));
    put(`${rb}_T0003_P0000`, routes[route].prompt);
    labels.set(`${rb}_T0003_P0000`, routes[route].labels);
    for (const resolution of [1, 2, 3]) {
      const eb = `${rb}_T0003_P000${resolution}`;
      put(eb, routes[route].acts[resolution]);
      put(`${eb}_F0001`, S([
        ...routes[route].endings[resolution].script.split("\n").map((line) => line.split(/\|(.*)/s).slice(0, 2)),
        ...prep[p].coda,
        ["narrateur", "Le bateau sèche près du volet jaune."],
        ["narrateur", "Dans la cuisine, la soupe est prête."],
      ]));
    }
  }
}

const input = await FileBlob.load(xlsxPath);
const workbook = await SpreadsheetFile.importXlsx(input);
const chunks = workbook.worksheets.getItem("chunks");
const values = chunks.getRange("A1:AX87").values;
const header = Object.fromEntries(values[0].map((name, index) => [name, index]));

for (let r = 1; r < values.length; r++) {
  const id = values[r][header.chunk_id];
  const packed = texts.get(id);
  if (!packed) throw new Error(`Texte manquant pour ${id}`);
  for (const name of ["text", "text_ssml", "text_xai_tags"]) values[r][header[name]] = packed.text;
  values[r][header.script] = packed.script;
  if (labels.has(id)) {
    const choice = labels.get(id);
    values[r][header.option_1_label] = choice[0];
    values[r][header.option_2_label] = choice[1];
    values[r][header.option_3_label] = choice[2];
  }
  if (questions.has(id)) {
    const [expected, accepted, retry] = questions.get(id);
    values[r][header.expected_answer] = expected;
    values[r][header.accepted_examples] = accepted;
    values[r][header.retry_prompt] = retry;
  }
}
chunks.getRange("A1:AX87").values = values;

const meta = workbook.worksheets.getItem("meta");
const metaValues = meta.getRange("A1:B31").values;
for (const row of metaValues) {
  if (row[0] === "title") row[1] = "Amir et le bateau qui cherchait la mer";
  if (row[0] === "setting") row[1] = "une petite maison, puis le jardin après la pluie";
  if (row[0] === "fil_rouge") row[1] = "Après la pluie, Amir veut offrir un vrai voyage à son bateau et rapporter une histoire à ses parents. Il prépare son expédition, choisit une route du jardin, affronte un obstacle réel, trouve sa propre solution puis rentre avec une trace de l'aventure.";
}
meta.getRange("A1:B31").values = metaValues;

const journal = workbook.worksheets.getItem("journal");
journal.getRange("A13:B13").values = [["réécriture éditoriale v2", "promesse, urgence douce, objets utiles, 9 résolutions causales, 27 retours cohérents"]];

const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(xlsxPath);

const merged = JSON.parse(await fs.readFile(mergedPath, "utf8"));
merged.title = "Amir et le bateau qui cherchait la mer";
merged.setting = "une petite maison, puis le jardin après la pluie";
merged.fil_rouge = "Après la pluie, Amir veut offrir un vrai voyage à son bateau et rapporter une histoire à ses parents. Il prépare son expédition, choisit une route du jardin, affronte un obstacle réel, trouve sa propre solution puis rentre avec une trace de l'aventure.";
for (const chunk of merged.chunks) {
  const packed = texts.get(chunk.chunk_id);
  if (!packed) throw new Error(`JSON sans texte pour ${chunk.chunk_id}`);
  chunk.text = packed.text;
  chunk.text_ssml = packed.text;
  chunk.text_xai_tags = packed.text;
  chunk.script = packed.script;
  if (labels.has(chunk.chunk_id)) {
    const choice = labels.get(chunk.chunk_id);
    chunk.option_1_label = choice[0];
    chunk.option_2_label = choice[1];
    chunk.option_3_label = choice[2];
  }
  if (questions.has(chunk.chunk_id)) {
    const [expected, accepted, retry] = questions.get(chunk.chunk_id);
    chunk.expected_answer = expected;
    chunk.accepted_examples = accepted;
    chunk.retry_prompt = retry;
  }
}
await fs.writeFile(mergedPath, `${JSON.stringify(merged, null, 2)}\n`, "utf8");

console.log(`Réécriture appliquée : ${texts.size} chunks.`);

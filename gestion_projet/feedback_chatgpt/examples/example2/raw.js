import fs from 'node:fs';
import path from 'node:path';

const dir=path.dirname(new URL(import.meta.url).pathname);
const mergedPath=path.join(dir,'merged.json');
const sourcePath=path.join(dir,'source.json');
const current=JSON.parse(fs.readFileSync(mergedPath,'utf8'));
const skeleton=current.chunks;
const byId=new Map(skeleton.map(c=>[c.chunk_id,c]));

const STORY={
  title:"Aniss et le secret de la trace d'argent",
  fil_rouge:"Après une averse, Aniss découvre une piste brillante qui traverse le jardin. Il veut montrer l'escargot à ses parents avant que le soleil ne sèche la trace. Pour réussir, la famille doit s'écouter : la loupe, le carnet ou l'appel à la fenêtre lance l'enquête ; la piste mène aux pots de menthe, au portail ou au vélo ; une feuille, trois cailloux ou un moment d'observation permettent d'aider l'animal sans le toucher. Au dîner, Aniss raconte enfin toute l'aventure et chacun l'écoute jusqu'au bout.",
  characters:'Aniss, papa, maman',
  setting:'une petite maison et son jardin, juste après une averse'
};

function lines(...items){return items.map(([role,text])=>({role,text}))}
function plain(ls){return ls.map(x=>x.text).join(' ')}
function script(ls){return ls.map(x=>`${x.role}|${x.text}`).join('\n')}
function esc(s){return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;')}
function ssml(text,m){
  let body=esc(text);
  if(m.emphasis){const e=esc(m.emphasis);body=body.replace(e,`<emphasis level="moderate">${e}</emphasis>`)}
  return `<speak><prosody rate="${m.rate}" pitch="${m.pitchSsml}">${body}</prosody><break time="${m.pause}ms"/></speak>`;
}
function xai(text,m){
  let body=text;
  if(m.emphasis)body=body.replace(m.emphasis,`<emphasis>${m.emphasis}</emphasis>`);
  if(m.rate==='slow')body=`<slow>${body}</slow>`;
  if(m.volume==='soft')body=`<soft>${body}</soft>`;
  if(m.pitchTag)body=`<${m.pitchTag}>${body}</${m.pitchTag}>`;
  return `${body} ${m.pause>=800?'[long-pause]':m.pause>=400?'[pause]':''}`.trim();
}
const profiles={
  opening:{rate:'medium',wpm:142,speed:.98,piper:1.12,pitch:'medium',pitchSsml:'medium',pitchTag:null,volume:'medium',db:0,pause:500,sentence:260,energy:'warm',contour:'storytelling',noise:.36,emphasis:"trace d'argent",note:'arc=installation; intention=émerveiller; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=un secret vient de commencer; tempo=naturel; sourire=léger; respiration=ample'},
  choice:{rate:'slow',wpm:116,speed:.84,piper:1.30,pitch:'medium',pitchSsml:'medium',pitchTag:null,volume:'medium',db:0,pause:900,sentence:330,energy:'focused',contour:'rising',noise:.33,emphasis:null,note:'arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix'},
  clue:{rate:'slow',wpm:120,speed:.86,piper:1.27,pitch:'medium',pitchSsml:'medium',pitchTag:null,volume:'soft',db:-2,pause:700,sentence:320,energy:'focused',contour:'rising',noise:.32,emphasis:'escargot',note:'arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question'},
  confirm:{rate:'medium',wpm:132,speed:.92,piper:1.20,pitch:'medium',pitchSsml:'medium',pitchTag:null,volume:'medium',db:0,pause:450,sentence:280,energy:'bright',contour:'falling',noise:.34,emphasis:'escargot',note:'arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_piste_continue; tempo=naturel; sourire=léger; respiration=fluide'},
  action:{rate:'medium',wpm:146,speed:1.0,piper:1.10,pitch:'medium',pitchSsml:'medium',pitchTag:null,volume:'medium',db:0,pause:420,sentence:250,energy:'lively',contour:'dynamic',noise:.37,emphasis:null,note:'arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il_faut_faire_vite; tempo=vif; sourire=léger; respiration=courte'},
  obstacle:{rate:'medium',wpm:134,speed:.93,piper:1.18,pitch:'low',pitchSsml:'-2st',pitchTag:'low-pitch',volume:'medium',db:0,pause:520,sentence:300,energy:'tense',contour:'dynamic',noise:.34,emphasis:null,note:'arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=les_indices_doivent_s_assembler; tempo=resserré; sourire=aucun; respiration=retenue'},
  resolution:{rate:'medium',wpm:140,speed:.97,piper:1.14,pitch:'medium',pitchSsml:'medium',pitchTag:null,volume:'medium',db:0,pause:560,sentence:270,energy:'bright',contour:'falling',noise:.35,emphasis:null,note:'arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=la_solution_vient_de_l_attention; tempo=naturel; sourire=franc; respiration=relâchée'},
  ending:{rate:'slow',wpm:118,speed:.85,piper:1.28,pitch:'low',pitchSsml:'-2st',pitchTag:'low-pitch',volume:'soft',db:-3,pause:900,sentence:340,energy:'calm',contour:'falling',noise:.31,emphasis:null,note:'arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_parole_a_trouvé_sa_place; tempo=posé; sourire=léger; respiration=ample'}
};

function set(id,kind,ls,profileName,extra={}){
  const old=byId.get(id);if(!old)throw new Error(`Chunk absent: ${id}`);
  const m={...profiles[profileName],emphasis:extra.emphasis??profiles[profileName].emphasis};
  const text=plain(ls);
  Object.assign(old,{
    kind,text,script:script(ls),sons:extra.sons??'',
    text_ssml:ssml(text,m),text_xai_tags:xai(text,m),
    rate_wpm:m.wpm,rate_label:m.rate,speed_xai:m.speed,length_scale_piper:m.piper,
    pitch_label:m.pitch,pitch_ssml:m.pitchSsml,pitch_xai_tag:m.pitchTag,
    volume_label:m.volume,volume_db:m.db,emphasis_words:m.emphasis||'',
    pause_before_ms:extra.pauseBefore??0,pause_after_ms:m.pause,pause_sentence_ms:m.sentence,
    style_energy:m.energy,style_contour:m.contour,noise_scale_piper:m.noise,
    kokoro_speed:m.speed,melo_speed:m.speed,espeak_amp:m.volume==='soft'?82:100,
    espeak_pitch:m.pitch==='low'?42:50,espeak_word_gap:m.rate==='slow'?12:8,
    notes:m.note,night_policy:'play',locale:'fr-FR',voice_id:'fr_FR-siwis-medium'
  },extra.fields||{});
}

set('CHK_T0000_P0000','passage_debut',lines(
 ['narrateur',"Au bout d'une rue tranquille, une petite maison ouvre ses volets sur un jardin."],
 ['narrateur',"Aniss y vit avec papa et maman."],
 ['narrateur',"Ce matin-là, une averse vient de laver les dalles."],
 ['narrateur',"Les feuilles brillent, et le toit laisse tomber ses dernières gouttes."],
 ['narrateur',"Dans la cuisine, papa coupe de la menthe pour la soupe."],
 ['narrateur',"Maman compte les assiettes pendant que la casserole frémit."],
 ['narrateur',"En ce moment, Aniss construit un garage près de la fenêtre."],
 ['narrateur',"Soudain, un éclair argenté traverse la pierre dehors."],
 ['enfant-m',"On dirait une route pour une toute petite voiture !"],
 ['narrateur',"Aniss colle son nez à la vitre."],
 ['narrateur',"Au bout de la trace avance un escargot couleur noisette."],
 ['enfant-m',"Papa ! Maman ! Venez voir !"],
 ['narrateur',"Mais la casserole souffle au même instant."],
 ['papa',"Tu disais quelque chose, Aniss ?"],
 ['enfant-m',"L'escargot… Il va…"],
 ['narrateur',"Dehors, l'animal disparaît derrière un pot."],
 ['narrateur',"Un rayon de soleil glisse déjà sur les dalles."],
 ['enfant-m',"Sa route va sécher. Il faut la suivre maintenant !"],
 ['maman',"Montre-nous ton secret. Nous venons avec toi."],
 ['narrateur',"Aniss enfile ses bottes. L'enquête peut commencer."]
),'opening',{sons:'pluie-legere,casserole'});

set('CHK_T0001_P0000','transition_question',lines(
 ['narrateur',"Pour montrer la piste, Aniss peut prendre la loupe, son carnet bleu, ou appeler ses parents près de la fenêtre."],
 ['maman',"Que choisis-tu pour commencer l'enquête ?"]
),'choice',{fields:{option_1_label:'la loupe',option_2_label:'le carnet bleu',option_3_label:'la fenêtre'}});

const starts={
  1:{name:'la loupe',prop:'la loupe rouge',passage:lines(
    ['narrateur',"Aniss saisit la loupe rouge dans son coffre à trésors."],
    ['narrateur',"Il revient si vite que le tapis se plisse sous sa botte."],
    ['enfant-m',"Regardez ! La route brille comme une rivière."],
    ['narrateur',"Papa répond à maman au sujet de la soupe. Sa voix couvre celle d'Aniss."],
    ['narrateur',"Aniss ouvre la bouche une deuxième fois, puis s'arrête."],
    ['narrateur',"Il pose doucement la loupe près de la main de papa."],
    ['enfant-m',"Quand tu as fini, j'ai un secret urgent à vous montrer."],
    ['papa',"Une seconde… Voilà, je t'écoute."],
    ['narrateur',"Sous la loupe, la trace devient une suite de perles brillantes."],
    ['maman',"Et ces perles conduisent quelque part."]
  ),question:"Quel animal laisse cette route brillante derrière lui ?",confirm:lines(
    ['enfant-m',"Un escargot !"],['narrateur',"Oui, un escargot."],
    ['narrateur',"Aniss l'a dit quand les oreilles étaient prêtes."],
    ['narrateur',"Tous trois sortent. Sous la loupe, la piste file entre les dalles."]
  ),sons:'tiroir,pluie-legere'},
  2:{name:'le carnet bleu',prop:'le carnet bleu',passage:lines(
    ['narrateur',"Aniss prend son carnet bleu et un gros crayon."],
    ['narrateur',"Il dessine une ligne qui tourne autour d'une pierre."],
    ['narrateur',"Au bout, il ajoute une coquille en spirale."],
    ['enfant-m',"Papa, regarde mon indice !"],
    ['narrateur',"Papa parle encore avec maman. Il n'a entendu que le mot regarde."],
    ['papa',"Je termine ma phrase, puis c'est à toi."],
    ['narrateur',"Aniss serre son carnet. Le soleil avance sur le jardin."],
    ['papa',"Maintenant, montre-moi."],
    ['enfant-m',"La vraie trace est dehors. Elle va disparaître !"],
    ['maman',"Alors gardons aussi sa carte dans ton carnet."]
  ),question:"Qu'a dessiné Aniss au bout de la ligne : une coquille ou une roue ?",confirm:lines(
    ['enfant-m',"Une coquille !"],['narrateur',"Exactement : une coquille d'escargot."],
    ['narrateur',"Papa ferme le robinet. Maman prend les manteaux."],
    ['narrateur',"Aniss ouvre la marche, le carnet contre son cœur."]
  ),sons:'crayon,casserole'},
  3:{name:'la fenêtre',prop:'le reflet de la fenêtre',passage:lines(
    ['narrateur',"Aniss ne prend rien. Il court jusqu'à la cuisine."],
    ['enfant-m',"Venez à la fenêtre ! C'est pressé !"],
    ['narrateur',"Maman cherche une assiette pendant que papa lui répond."],
    ['narrateur',"Les mots d'Aniss se cognent aux leurs et personne ne comprend."],
    ['narrateur',"Alors il touche le coude de maman et attend qu'elle se tourne."],
    ['enfant-m',"Je peux vous montrer quelque chose avant que le soleil l'efface ?"],
    ['maman',"Oui. Nous t'écoutons."],
    ['narrateur',"À la fenêtre, le soleil coupe déjà la piste en deux."],
    ['papa',"Je vois le début, mais plus la fin."],
    ['enfant-m',"L'escargot était là. Vite, suivons ce qui reste !"]
  ),question:"Qu'est-ce que le soleil efface peu à peu ?",confirm:lines(
    ['enfant-m',"La trace de l'escargot !"],['narrateur',"Oui, sa fine trace d'argent."],
    ['narrateur',"Cette fois, papa et maman ont entendu toute la phrase."],
    ['narrateur',"La porte s'ouvre, et trois paires de pas entrent dans le jardin."]
  ),sons:'pas,porte'}
};

for(const [i,s] of Object.entries(starts)){
 const base=`CHK_T0001_P000${i}`;
 set(base,'passage',s.passage,'action',{sons:s.sons});
 const expected=i==='1'?'escargot':i==='2'?'coquille':'trace';
 set(`${base}_Q0001`,'passage_question',lines(['narrateur',s.question]),'clue',{fields:{expected_answer:expected,accepted_examples:i==='1'?'escargot | un escargot':i==='2'?'coquille | une coquille':'trace | la trace | trace de l’escargot',engine_ok_text:i==='1'?"Oui, c'est bien l'escargot.":i==='2'?"Oui, c'est bien une coquille.":"Oui, c'est bien la trace.",engine_near_text:"Tu es tout près. Reprenons l'indice.",retry_prompt:'Écoute bien l’indice et essaie encore.'}});
 set(`${base}_C0001`,'passage',s.confirm,'confirm');
 set(`${base}_T0002_P0000`,'transition_question',lines(
  ['narrateur',"La piste se partage autour d'une flaque."],
  ['papa',"Elle semble aller vers les pots de menthe, le petit portail, ou le vélo rouge."],
  ['maman',"Quel chemin suivons-nous ?"]
 ),'choice',{fields:{option_1_label:'les pots de menthe',option_2_label:'le petit portail',option_3_label:'le vélo rouge'}});
}

const locations={
  1:{name:'les pots de menthe',sound:'abeille,feuilles',passage:(s)=>lines(
    ['narrateur',`Avec ${s.prop}, Aniss suit les reflets jusqu'aux pots de menthe.`],
    ['narrateur',"La piste grimpe sur une soucoupe, puis disparaît sous les feuilles."],
    ['maman',"J'ai vu quelque chose bouger près de la tige."],
    ['papa',"Et moi, j'ai remarqué une feuille trouée…"],
    ['narrateur',"Ils commencent à parler ensemble. Aniss ne sait plus quel indice suivre."],
    ['enfant-m',"Papa d'abord. Après, maman nous montre ce qu'elle a vu."],
    ['narrateur',"Papa décrit la feuille grignotée. Maman indique la tige qui tremble."],
    ['narrateur',"Les deux indices se rejoignent sous le plus grand pot."],
    ['narrateur',"L'escargot est là, mais le soleil chauffe déjà le passage devant lui."]
  ),question:"Le passage est devenu trop chaud. Comment Aniss peut-il aider sans toucher l'escargot ?",labels:['une feuille','trois cailloux','attendre sans bouger']},
  2:{name:'le petit portail',sound:'goutte,portail',passage:(s)=>lines(
    ['narrateur',`Aniss avance vers le petit portail avec ${s.prop}.`],
    ['narrateur',"La piste traverse une rigole où l'eau court encore."],
    ['papa',"Je crois qu'elle passe à gauche."],
    ['maman',"Attends, j'ai vu une coquille près du gond."],
    ['narrateur',"Aniss regarde à gauche, puis près du gond. Rien."],
    ['enfant-m',"Un indice à la fois, sinon mes yeux se perdent."],
    ['narrateur',"Papa montre les gouttes déplacées. Maman montre une ombre ronde."],
    ['narrateur',"En réunissant les deux, Aniss aperçoit l'escargot au bord de la rigole."],
    ['narrateur',"Une nouvelle goutte arrive du toit et fait gonfler le petit courant."]
  ),question:"L'eau lui barre le passage. Comment Aniss peut-il l'aider sans le toucher ?",labels:['une feuille','trois cailloux','attendre sans bouger']},
  3:{name:'le vélo rouge',sound:'roue,merle',passage:(s)=>lines(
    ['narrateur',`La piste conduit ${s.prop==='le reflet de la fenêtre'?'la famille':'Aniss et sa famille'} jusqu'au vélo rouge.`],
    ['narrateur',"Elle passe juste sous la roue arrière."],
    ['papa',"Je vais ranger le vélo contre le mur."],
    ['narrateur',"Sa main attrape le guidon."],
    ['enfant-m',"Stop, papa ! L'escargot est peut-être dessous !"],
    ['narrateur',"Cette fois, Aniss n'attend pas : il y a un danger."],
    ['narrateur',"Papa lâche aussitôt le vélo et écoute."],
    ['maman',"Tu as bien fait de nous prévenir."],
    ['narrateur',"Tous se baissent. Une minuscule corne apparaît derrière la pédale."]
  ),question:"La roue est tout près. Comment Aniss peut-il protéger l'escargot sans le toucher ?",labels:['une feuille','trois cailloux','attendre sans bouger']}
};

const resolutions={
  1:{name:'une feuille',scenes:{
    1:lines(['narrateur',"Aniss choisit une large feuille de salade tombée du panier."],['narrateur',"Il la pose devant la zone chaude, sans toucher l'escargot."],['narrateur',"La feuille fait un petit toit et son bord rejoint l'ombre du pot."],['narrateur',"Après un instant, deux cornes prudentes sortent de la coquille."],['enfant-m',"Il a trouvé le passage frais !"],['narrateur',"L'escargot glisse sous la feuille. Une nouvelle virgule d'argent apparaît."],['papa',"Je n'aurais pas pensé à ce toit."],['maman',"Moi non plus. Heureusement que nous avons regardé ensemble."]),
    2:lines(['narrateur',"Aniss prend une feuille de platane, large comme sa main."],['narrateur',"Il la pose d'une rive à l'autre de la rigole."],['narrateur',"Le courant passe dessous ; le dessus reste presque sec."],['narrateur',"L'escargot touche la feuille avec une corne, puis avec l'autre."],['enfant-m',"Il essaie mon pont !"],['narrateur',"Très lentement, la coquille traverse."],['narrateur',"Personne ne parle pendant les trois derniers centimètres."],['maman',"Le voilà de l'autre côté."]),
    3:lines(['narrateur',"Aniss plante une grande feuille dans une fente du panier du vélo."],['narrateur',"Elle se dresse comme un petit drapeau vert au-dessus de la piste."],['enfant-m',"Comme ça, personne ne fera rouler le vélo."],['narrateur',"Papa soulève doucement l'arrière du cadre, sans avancer la roue."],['narrateur',"Sous la pédale, l'escargot se dirige vers l'herbe."],['maman',"Je garde le drapeau jusqu'à son arrivée."],['narrateur',"La coquille franchit l'ombre de la roue."],['narrateur',"Aniss respire enfin."])
  }},
  2:{name:'trois cailloux',scenes:{
    1:lines(['narrateur',"Aniss choisit trois cailloux clairs."],['narrateur',"Il les pose loin de la coquille, entre le soleil et le pot."],['narrateur',"Le premier marque le bord chaud. Le deuxième garde le passage."],['narrateur',"Le troisième montre à papa où poser son arrosoir."],['papa',"Je vois la petite zone à protéger."],['narrateur',"Une goutte tombe près de la menthe et rafraîchit la terre."],['narrateur',"L'escargot ressort, contourne les cailloux et gagne l'ombre."],['enfant-m',"Notre chemin lui a laissé son chemin."]),
    2:lines(['narrateur',"Aniss choisit trois cailloux plats."],['narrateur',"Avec papa, il les pose dans la rigole, espacés comme des marches."],['narrateur',"L'eau ralentit et forme trois minuscules cascades."],['narrateur',"Maman indique le côté le moins profond."],['narrateur',"Aniss attend qu'elle termine, puis rapproche le dernier caillou."],['enfant-m',"Maintenant, le bord ne glisse plus."],['narrateur',"L'escargot contourne l'eau par la pierre sèche."],['narrateur',"Derrière lui, la piste brille en zigzag."]),
    3:lines(['narrateur',"Aniss prend trois cailloux blancs près du mur."],['narrateur',"Il en pose un devant la roue, puis deux autour de la piste."],['enfant-m',"C'est une barrière pour les grandes roues."],['narrateur',"Papa comprend le message sans déplacer le vélo."],['narrateur',"Maman observe l'autre côté de la pédale."],['maman',"La sortie est libre vers l'herbe."],['narrateur',"L'escargot avance entre les cailloux comme entre trois bornes."],['narrateur',"Sa coquille quitte enfin l'ombre dangereuse."])
  }},
  3:{name:'attendre',scenes:{
    1:lines(['narrateur',"Aniss choisit de ne rien déplacer."],['enfant-m',"Chut. Peut-être qu'il nous montre lui-même le bon côté."],['narrateur',"La famille reste accroupie près de la menthe."],['narrateur',"Une abeille bourdonne. Une goutte tombe d'une feuille."],['narrateur',"Puis la coquille tourne lentement vers une fente fraîche sous le pot."],['papa',"Voilà ce que je n'avais pas vu."],['maman',"En attendant, nous avons eu sa réponse."],['narrateur',"L'escargot disparaît à l'ombre, sans que personne l'ait touché."]),
    2:lines(['narrateur',"Aniss choisit d'attendre sans bouger."],['narrateur',"Il observe le courant au lieu de regarder seulement la coquille."],['narrateur',"Une goutte tombe, puis l'eau baisse entre deux dalles."],['enfant-m',"Là ! Il y a un passage quand la vague est partie."],['narrateur',"L'escargot avance au moment calme."],['narrateur',"Papa retient le portail pour qu'il ne claque pas."],['narrateur',"Maman compte tout bas les secondes de la traversée."],['narrateur',"À dix, la coquille atteint la mousse du mur."]),
    3:lines(['narrateur',"Aniss choisit d'attendre sans bouger."],['narrateur',"Papa garde les mains loin du guidon. Maman s'accroupit de l'autre côté."],['narrateur',"On entend un merle, puis un petit frottement sous la pédale."],['maman',"Il avance vers toi, Aniss."],['narrateur',"Aniss ne répond pas tout de suite. Il laisse le silence à l'escargot."],['narrateur',"La tête apparaît, puis la coquille entière."],['enfant-m',"Maintenant, tu peux lever le vélo."],['narrateur',"Papa attend que l'animal atteigne l'herbe, puis range le vélo."])
  }}
};

function toolCallback(a,b,c){
 if(a===1)return b===1?"Sous la loupe, Aniss voit une goutte posée sur la coquille.":b===2?"La loupe transforme la rigole en rivière brillante.":"Avec la loupe, Aniss vérifie que la roue ne touche plus la piste.";
 if(a===2){
  if(b===1)return c===1?"Dans son carnet, la feuille devient un grand toit vert.":c===2?"Aniss dessine les trois cailloux devant la forêt de menthe.":"Aniss dessine une coquille tournée vers l'ombre du pot.";
  if(b===2)return c===1?"Aniss ajoute un pont de feuille et trois vaguelettes sur sa carte.":c===2?"Dans le carnet, trois pierres coupent la petite rivière.":"Aniss dessine la rigole calme et la mousse du mur.";
  return c===1?"Dans le carnet, le drapeau vert veille près de la montagne rouge.":c===2?"Aniss dessine trois bornes blanches devant la grande roue.":"Dans le carnet, l'escargot sort seul de l'ombre de la pédale.";
 }
 if(b===1)return c===1?"Depuis la fenêtre, la feuille ressemble à un toit vert.":c===2?"Depuis la fenêtre, les trois cailloux brillent près de la menthe.":"Depuis la fenêtre, le pot de menthe cache maintenant un secret.";
 if(b===2)return c===1?"Depuis la fenêtre, la feuille traverse la rigole comme un pont.":c===2?"Depuis la fenêtre, les trois cailloux découpent le courant.":"Depuis la fenêtre, la rigole ressemble à un fil qui brille.";
 return c===1?"Depuis la fenêtre, maman aperçoit le petit drapeau vert.":c===2?"Depuis la fenêtre, les trois cailloux blancs protègent la roue.":"Depuis la fenêtre, maman voit enfin papa ranger le vélo.";
}
function ending(a,b,c){
 const loc=locations[b];
 const spokenSolution=c===1?'une feuille':c===2?'trois cailloux':'un moment sans bouger';
 const keepsake=a===1?"La loupe est posée près du bol. Elle attrape un rond de lumière.":a===2?"Le carnet reste ouvert près d'Aniss. La carte de l'enquête traverse les deux pages.":"À travers la fenêtre, le jardin paraît redevenu très grand.";
 const callbacks=[
  "Au dîner, papa termine une phrase sur la soupe, puis pose sa cuillère.",
  "À toi, Aniss. Nous t'écoutons.",
  `Nous sommes allés vers ${loc.name}. J'ai choisi ${spokenSolution}, et l'escargot a retrouvé son chemin.`,
  keepsake,
  c===1?"Dans le jardin, la feuille bouge à peine.":c===2?"Dans le jardin, les trois cailloux gardent encore le souvenir du passage.":"Dans le jardin, personne ne voit plus l'escargot, mais sa trace neuve brille sous la haie."
 ];
 return lines(['narrateur',callbacks[0]],['maman',callbacks[1]],['enfant-m',callbacks[2]],['narrateur',callbacks[3]],['narrateur',callbacks[4]]);
}

for(let a=1;a<=3;a++)for(let b=1;b<=3;b++){
 const base=`CHK_T0001_P000${a}_T0002_P000${b}`;
 set(base,'passage',locations[b].passage(starts[a]),'obstacle',{sons:locations[b].sound});
 set(`${base}_T0003_P0000`,'transition_question',lines(
  ['narrateur',locations[b].question],['papa',"Une feuille, trois cailloux, ou attendre sans bouger ?"]
 ),'choice',{fields:{option_1_label:'une feuille',option_2_label:'trois cailloux',option_3_label:'attendre sans bouger'}});
 for(let c=1;c<=3;c++){
  const leaf=`${base}_T0003_P000${c}`;
  const body=[...resolutions[c].scenes[b],...lines(['narrateur',toolCallback(a,b,c)])];
  set(leaf,'passage',body,'resolution',{sons:c===1?'feuille':c===2?'cailloux':'jardin-calme'});
  set(`${leaf}_F0001`,'passage_fin',ending(a,b,c),'ending',{sons:b===1?'couverts,grillon':b===2?'couverts,goutte': 'couverts,merle'});
 }
}

// Ensure navigation and interactive fields from the structural skeleton remain untouched.
const updated={...current,...STORY,age_band:'N2',kind:'ramifiee',chunks:skeleton};
fs.writeFileSync(mergedPath,JSON.stringify(updated,null,2)+'\n');
fs.writeFileSync(sourcePath,JSON.stringify(updated,null,2)+'\n');
console.log(`Updated ${skeleton.length} chunks for ${updated.story_id}`);

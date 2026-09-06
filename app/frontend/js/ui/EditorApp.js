import { Component } from "../core/Component.js";
import { acmLogo } from "./acm.js";
import { EditorApi } from "../editor/core/EditorApi.js";
import "../editor/ui/DropZone.js";
import "../editor/ui/CastBoard.js";
import "../editor/ui/VoicePanel.js";
import "../editor/ui/ConvertPanel.js";
import "../editor/ui/ReplicaStudio.js";
import "../editor/ui/TroupeBoard.js";

/** Page éditeur officiel : troupe, JSON, empreintes, conversion, répliques. */
export class EditorApp extends Component {
  #stage = "source";

  async connectedCallback() {
    const tts = new EditorApi(this.api);
    this.classList.add("s-editor-host");
    this.innerHTML = `
      <div class="s-shell s-shell--admin">
        <aside class="s-rail">
          <div class="c-mark">${acmLogo({ size: "sm" })}<span class="c-mark__sub">Studio éditorial</span></div>
          <nav>
            <a href="#studio" class="is-on">Production</a>
            <a href="#troupe">Troupe & voix</a>
            <a href="#source">Histoire source</a>
            <a href="#render">Rendu & répliques</a>
            <a href="#/admin">Administration</a>
            <a href="#/parent">Vue parent</a>
          </nav>
          <div class="c-editor-rail-status"><span class="c-status-dot"></span><div><strong>Atelier prêt</strong><small>Excel → JSON → voix → audio</small></div></div>
          <button class="c-btn c-btn--ghost" data-out>Quitter</button>
        </aside>
        <main class="s-main c-editor" id="studio">
          <div class="c-editor-hero">
            <div>
              <p class="c-editor-kicker">Atelier de production</p>
              <h1>Donnez une voix<br>à chaque histoire.</h1>
              <p>Préparez le manuscrit, vérifiez la distribution, générez l’audio puis ajustez chaque réplique au même endroit.</p>
            </div>
            <div class="c-editor-hero__actions"><button type="button" class="c-btn c-btn--gold" data-excel>Mettre à jour les JSON</button><span>Source canonique : Excel</span></div>
          </div>
          <div class="c-editor-notice" data-excel-status hidden></div>
          <ol class="c-workflow" aria-label="Étapes de production">
            <li class="is-active" data-step="source"><span>1</span><div><strong>Préparer</strong><small>Choisir l’histoire</small></div></li>
            <li data-step="cast"><span>2</span><div><strong>Distribuer</strong><small>Vérifier les voix</small></div></li>
            <li data-step="render"><span>3</span><div><strong>Produire</strong><small>Générer et corriger</small></div></li>
          </ol>
          <section class="c-editor-section" id="troupe">
            <header><div><p class="c-editor-kicker">Bibliothèque vocale</p><h2>La troupe AcoMytha</h2></div><p>Retrouvez les personnages, leurs empreintes et les histoires dans lesquelles ils interviennent.</p></header>
            <troupe-board></troupe-board>
          </section>
          <section class="c-editor-section" id="source">
            <header><div><p class="c-editor-kicker">Étape 1</p><h2>Préparer une histoire</h2></div><p>Choisissez un JSON du catalogue ou importez un fichier ponctuel.</p></header>
            <div class="c-editor-grid"><drop-zone></drop-zone><cast-board></cast-board></div>
          </section>
          <section class="c-editor-section" id="render">
            <header><div><p class="c-editor-kicker">Étape 3</p><h2>Produire et affiner</h2></div><p>Générez le rendu complet, puis écoutez ou remplacez les répliques qui le méritent.</p></header>
            <convert-panel></convert-panel>
            <replica-studio></replica-studio>
          </section>
        </main>
      </div>
    `;
    this.on(this.querySelector("[data-out]"), "click", () => this.#logout());
    this.on(this.querySelector("[data-excel]"), "click", () => this.#excel(tts));

    const drop = this.querySelector("drop-zone");
    const board = this.querySelector("cast-board");
    const convert = this.querySelector("convert-panel");
    const replicas = this.querySelector("replica-studio");
    const troupe = this.querySelector("troupe-board");
    const voices = document.createElement("voice-panel");
    drop.api = tts;
    voices.api = tts;
    replicas.api = tts;
    troupe.api = tts;
    document.body.append(voices);
    drop.loadCatalog();
    troupe.load();

    this.on(drop, "story-parsed", (event) => {
      this.#setStage("cast");
      convert.hidePlayer();
      replicas.hide();
      convert.status("Personnages détectés. Vérifie les empreintes.");
      board.show(event.detail.preview);
      convert.enable(true);
    });
    this.on(drop, "studio-error", (event) => {
      this.#setNotice(event.detail.message, true);
      convert.enable(false);
      convert.status(event.detail.message, { error: true });
    });
    this.on(board, "voice-needed", (event) => voices.open(event.detail.member, event.detail.mode));
    this.on(troupe, "voice-needed", (event) => voices.open(event.detail.member, event.detail.mode));
    this.on(troupe, "story-open", (event) => drop.openCatalog(event.detail.storyId));
    this.on(voices, "voice-saved", (event) => {
      const profileId = event.detail.profile.id;
      board.assign(event.detail.member.speaker_key, profileId);
      troupe.markReady(profileId);
      convert.status(`Voix « ${event.detail.profile.display_name} » enregistrée au catalogue.`);
      this.#setNotice(`Empreinte de ${event.detail.profile.display_name} enregistrée.`, false);
    });
    this.on(convert, "convert-requested", () => this.#convert(tts, drop, board, convert, replicas));
  }

  async #excel(tts) {
    const status = this.querySelector("[data-excel-status]");
    status.hidden = false;
    status.classList.add("is-busy");
    status.textContent = "Mise à jour des JSON depuis les fichiers Excel…";
    try {
      const report = await tts.convertExcel();
      status.textContent = `${report.ok} JSON écrits, ${ (report.errors || []).length } erreur(s).`;
      status.classList.remove("is-busy");
      this.querySelector("troupe-board")?.load();
      this.querySelector("drop-zone")?.loadCatalog();
    } catch (err) {
      status.textContent = err.message;
      status.classList.remove("is-busy");
      status.classList.add("is-error");
    }
  }

  async #convert(tts, drop, board, convert, replicas) {
    if (!drop.storyId && !drop.file) return;
    convert.hidePlayer();
    replicas.hide();
    convert.status("Conversion…", { busy: true });
    this.#setStage("render");
    convert.enable(false);
    try {
      const started = drop.storyId
        ? await tts.convertCatalog(drop.storyId, board.assignments)
        : await tts.convert(drop.file, board.assignments);
      const done = await this.#poll(tts, started.job_id, convert);
      convert.ready(tts.audioUrl(done.job_id), done.title, done.job_id);
      await replicas.open(done.job_id);
      this.#setNotice(`« ${done.title} » est prête pour la relecture audio.`, false);
    } catch (err) {
      convert.status(err.message, { error: true });
    } finally {
      convert.enable(Boolean(drop.storyId || drop.file));
    }
  }

  #setStage(stage) {
    const order = ["source", "cast", "render"];
    this.#stage = stage;
    const current = order.indexOf(stage);
    this.querySelectorAll("[data-step]").forEach((item) => {
      const index = order.indexOf(item.dataset.step);
      item.classList.toggle("is-active", index === current);
      item.classList.toggle("is-done", index < current);
    });
  }

  #setNotice(message, error = false) {
    const notice = this.querySelector("[data-excel-status]");
    notice.hidden = false;
    notice.textContent = message;
    notice.classList.toggle("is-error", error);
    notice.classList.remove("is-busy");
  }

  async #poll(tts, jobId, convert) {
    const data = await tts.job(jobId);
    if (data.status === "done") return data;
    if (data.status === "error") throw new Error(data.message || "Conversion échouée.");
    convert.status(data.message || "Conversion en cours…", { busy: true, progress: data.progress ?? 0 });
    await new Promise((resolve) => setTimeout(resolve, 700));
    return this.#poll(tts, jobId, convert);
  }

  async #logout() {
    await this.api.post("/auth/logout", {});
    this.router.go("#/entrer");
  }
}

customElements.define("acomytha-editor", EditorApp);

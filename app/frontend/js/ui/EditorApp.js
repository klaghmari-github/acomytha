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
  async connectedCallback() {
    const tts = new EditorApi(this.api);
    this.classList.add("s-editor-host");
    this.innerHTML = `
      <div class="s-shell s-shell--admin">
        <aside class="s-rail">
          <div class="c-mark">${acmLogo({ size: "sm" })}<span class="c-mark__sub">L’atelier vocal.</span></div>
          <nav>
            <a href="#/admin">Veille</a>
            <a href="#/admin/editeur" class="is-on">Éditeur</a>
            <a href="#/parent">Vue parent</a>
          </nav>
          <button class="c-btn c-btn--ghost" data-out>Quitter</button>
        </aside>
        <main class="s-main o-stack c-editor">
          <div class="c-title">
            <div>
              <h1>Éditeur vocal</h1>
              <p>Personnages, histoires JSON, empreintes, conversion Excel → JSON → audio, édition des répliques.</p>
            </div>
            <button type="button" class="c-btn c-btn--gold" data-excel>Excel → JSON</button>
          </div>
          <p class="c-hint" data-excel-status></p>
          <troupe-board></troupe-board>
          <drop-zone></drop-zone>
          <cast-board></cast-board>
          <convert-panel></convert-panel>
          <replica-studio></replica-studio>
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
      convert.hidePlayer();
      replicas.hide();
      convert.status("Personnages détectés. Vérifie les empreintes.");
      board.show(event.detail.preview);
      convert.enable(true);
    });
    this.on(drop, "studio-error", (event) => {
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
    });
    this.on(convert, "convert-requested", () => this.#convert(tts, drop, board, convert, replicas));
  }

  async #excel(tts) {
    const status = this.querySelector("[data-excel-status]");
    status.textContent = "Conversion des Excel de stories/arbres/…";
    try {
      const report = await tts.convertExcel();
      status.textContent = `${report.ok} JSON écrits, ${ (report.errors || []).length } erreur(s).`;
      this.querySelector("troupe-board")?.load();
      this.querySelector("drop-zone")?.loadCatalog();
    } catch (err) {
      status.textContent = err.message;
    }
  }

  async #convert(tts, drop, board, convert, replicas) {
    if (!drop.storyId && !drop.file) return;
    convert.hidePlayer();
    replicas.hide();
    convert.status("Conversion…", { busy: true });
    convert.enable(false);
    try {
      const started = drop.storyId
        ? await tts.convertCatalog(drop.storyId, board.assignments)
        : await tts.convert(drop.file, board.assignments);
      const done = await this.#poll(tts, started.job_id, convert);
      convert.ready(tts.audioUrl(done.job_id), done.title, done.job_id);
      await replicas.open(done.job_id);
    } catch (err) {
      convert.status(err.message, { error: true });
    } finally {
      convert.enable(Boolean(drop.storyId || drop.file));
    }
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

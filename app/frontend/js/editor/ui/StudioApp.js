import { Component } from "../core/Component.js";
import "./DropZone.js?v=oop-1";
import "./CastBoard.js?v=oop-1";
import "./VoicePanel.js?v=oop-1";
import "./ConvertPanel.js?v=oop-1";
import "./ReplicaStudio.js?v=oop-1";
import "./TroupeBoard.js?v=oop-1";

export class StudioApp extends Component {
  connectedCallback() {
    this.classList.add("s-home");
    this.html`
      <div class="c-stage">
        <header class="c-top">
          <a class="c-logo" href="/" aria-label="AcoMythaTTS">
            <svg class="acm acm--sm" viewBox="0 0 100 112" aria-hidden="true"><use href="#acm-mark"></use></svg>
            <strong>AcoMythaTTS</strong>
          </a>
        </header>
        <section class="c-hero">
          <p class="c-kicker">AcoMythaTTS : le moteur vocal des histoires.</p>
          <div class="c-orb" aria-hidden="true">
            <span class="c-ring"></span>
            <span class="c-ring"></span>
            <span class="c-ring"></span>
            <span class="c-filament"></span>
            <div class="c-hero-logo">
              <svg class="acm acm--lg" viewBox="0 0 100 112"><use href="#acm-mark"></use></svg>
            </div>
          </div>
          <h1>Convertir<br>l’<em>histoire</em><br>en audio.</h1>
        </section>
        <main class="c-studio o-stack">
          <troupe-board></troupe-board>
          <drop-zone></drop-zone>
          <cast-board></cast-board>
          <convert-panel></convert-panel>
          <replica-studio></replica-studio>
        </main>
      </div>
    `;
    const drop = this.querySelector("drop-zone");
    const board = this.querySelector("cast-board");
    const convert = this.querySelector("convert-panel");
    const editor = this.querySelector("replica-studio");
    const troupe = this.querySelector("troupe-board");
    const voices = document.createElement("voice-panel");
    drop.api = this.api;
    voices.api = this.api;
    editor.api = this.api;
    troupe.api = this.api;
    document.body.append(voices);
    drop.loadCatalog();
    troupe.load();

    this.on(drop, "story-parsed", (event) => {
      convert.hidePlayer();
      editor.hide();
      convert.status("Personnages détectés. Vérifie les empreintes.");
      board.show(event.detail.preview);
      convert.enable(true);
    });
    this.on(drop, "studio-error", (event) => {
      convert.enable(false);
      convert.status(event.detail.message, { error: true });
    });
    this.on(board, "voice-needed", (event) => {
      voices.open(event.detail.member, event.detail.mode);
    });
    this.on(troupe, "voice-needed", (event) => {
      voices.open(event.detail.member, event.detail.mode);
    });
    this.on(troupe, "story-open", (event) => {
      drop.openCatalog(event.detail.storyId);
    });
    this.on(voices, "voice-saved", (event) => {
      const profileId = event.detail.profile.id;
      board.assign(event.detail.member.speaker_key, profileId);
      troupe.markReady(profileId);
      convert.status(`Voix « ${event.detail.profile.display_name} » enregistrée au catalogue.`);
    });
    this.on(convert, "convert-requested", () => this.#convert(drop, board, convert, editor));
  }

  async #convert(drop, board, convert, editor) {
    if (!drop.storyId && !drop.file) return;
    convert.hidePlayer();
    editor.hide();
    convert.status("Conversion…", { busy: true });
    convert.enable(false);
    try {
      const started = drop.storyId
        ? await this.api.convertCatalog(drop.storyId, board.assignments)
        : await this.api.convert(drop.file, board.assignments);
      const done = await this.#poll(started.job_id, convert);
      convert.ready(this.api.audioUrl(done.job_id), done.title, done.job_id);
      await editor.open(done.job_id);
    } catch (err) {
      convert.status(err.message, { error: true });
    } finally {
      convert.enable(Boolean(drop.storyId || drop.file));
    }
  }

  async #poll(jobId, convert) {
    const data = await this.api.job(jobId);
    if (data.status === "done") return data;
    if (data.status === "error") throw new Error(data.message || "Conversion échouée.");
    convert.status(data.message || "Conversion en cours…", {
      busy: true,
      progress: data.progress ?? 0,
    });
    await new Promise((resolve) => setTimeout(resolve, 700));
    return this.#poll(jobId, convert);
  }
}

customElements.define("studio-app", StudioApp);

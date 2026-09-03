import { Component } from "../core/Component.js";
import { CryptoPlayer } from "../core/CryptoPlayer.js";
import { StoryEngine } from "../core/StoryEngine.js";

export class HomeApp extends Component {
  constructor() {
    super();
    this.api = null;
    this.router = null;
    this.allStories = [];
    this.domainNames = new Map();
    this.engine = null;
    this.playingId = null;
    this.previewSeconds = 10;
    this._filterTimer = 0;
    this.me = null;
  }

  async connectedCallback() {
    this.innerHTML = `
      <div class="s-home">
        <header class="c-top">
          <strong>AcoMytha</strong>
          <nav>
            <a href="#/entrer">Connexion</a>
            <a class="c-btn" href="#/inscription">Créer un compte</a>
          </nav>
        </header>
        <section class="c-hero">
          <h1>Une multitude d’histoires.</h1>
          <p>Créer un compte. Les transmettre à votre enfant. Le laisser s’immerger.</p>
          <a class="c-btn c-btn--lg" href="#/inscription">Créer un compte</a>
        </section>
        <section class="c-stats" id="stats"></section>
        <section class="c-pitches">
          <blockquote>Votre enfant ne fait pas qu’écouter.</blockquote>
          <blockquote>Jour : plus d’interaction. Nuit : plus calme.</blockquote>
          <blockquote>Offrez à votre enfant l’opportunité d’apprendre par l’histoire.</blockquote>
        </section>
        <section class="c-catalog">
          <div class="c-filters">
            <input id="q" placeholder="Rechercher une histoire…" />
            <select id="domain"><option value="">Thème</option></select>
            <select id="age">
              <option value="">Âge</option>
              <option value="N1">3–4 ans</option>
              <option value="N2">4–5 ans</option>
              <option value="N3">5–6 ans</option>
            </select>
            <select id="kind">
              <option value="">Toutes</option>
              <option value="atomic">Courte</option>
              <option value="ramifiee">Avec des choix</option>
            </select>
          </div>
          <p class="c-hint" id="count"></p>
          <p class="c-error" id="msg"></p>
          <div class="o-grid" id="grid"></div>
        </section>
        <div class="c-nowbar" id="nowbar" hidden>
          <span id="nowtitle"></span>
          <button class="c-btn c-btn--stop" type="button" id="stop">Arrêt</button>
        </div>
      </div>`;
    this.on(this.querySelector("#q"), "input", () => this.scheduleRender());
    this.on(this.querySelector("#domain"), "change", () => this.render());
    this.on(this.querySelector("#age"), "change", () => this.render());
    this.on(this.querySelector("#kind"), "change", () => this.render());
    this.on(this.querySelector("#grid"), "click", (e) => this.onGridClick(e));
    this.on(this.querySelector("#stop"), "click", () => this.stopPlay());
    await this.boot();
  }

  disconnectedCallback() {
    clearTimeout(this._filterTimer);
    if (this.engine) this.engine.stop();
    super.disconnectedCallback();
  }

  async boot() {
    try {
      const [stats, lessons, stories] = await Promise.all([
        this.api.get("/public/stats"),
        this.api.get("/public/lessons"),
        this.api.get("/public/stories"),
      ]);
      this.previewSeconds = stats.preview_seconds || 10;
      this.allStories = stories;
      this.domainNames = new Map(lessons.map((l) => [l.domain_id, l.domain]));
      const sel = this.querySelector("#domain");
      for (const [id, name] of this.domainNames) {
        const o = document.createElement("option");
        o.value = id;
        o.textContent = name;
        sel.append(o);
      }
      this.querySelector("#stats").innerHTML = `
        <div><b>${stats.stories}</b><span>histoires</span></div>
        <div><b>${stats.themes}</b><span>thèmes</span></div>`;
      try {
        this.me = await this.api.get("/auth/me");
        const nav = this.querySelector(".c-top nav");
        nav.innerHTML = `<a class="c-btn" href="#/${this.me.role === "admin" ? "admin" : "parent"}">Mon espace</a>`;
      } catch {
        this.me = null;
      }
      this.render();
    } catch (e) {
      this.querySelector("#msg").textContent = e.message || "Catalogue indisponible.";
    }
  }

  scheduleRender() {
    clearTimeout(this._filterTimer);
    this._filterTimer = setTimeout(() => this.render(), 80);
  }

  render() {
    const q = fold(this.querySelector("#q").value);
    const domain = this.querySelector("#domain").value;
    const age = this.querySelector("#age").value;
    const kind = this.querySelector("#kind").value;
    const list = this.allStories.filter((s) => {
      if (domain && s.domain !== domain) return false;
      if (age && s.age_band !== age) return false;
      if (kind && s.kind !== kind) return false;
      if (q) {
        const blob = fold([s.title, s.setting, s.characters, s.lesson_id].join(" "));
        if (!blob.includes(q)) return false;
      }
      return true;
    });
    this.querySelector("#count").textContent = `${list.length} histoire${list.length > 1 ? "s" : ""}`;
    const grid = this.querySelector("#grid");
    grid.replaceChildren();
    for (const s of list) grid.append(this.card(s));
  }

  card(s) {
    const el = document.createElement("article");
    el.className = "c-card";
    const theme = this.domainNames.get(s.domain) || "";
    const where = [theme, s.setting].filter(Boolean).join(" · ");
    el.innerHTML = `
      <div class="o-row">
        <span class="c-pill">${ageLabel(s.age_band)}</span>
        <span class="c-pill ${s.kind === "ramifiee" ? "c-pill--ram" : ""}">${s.kind === "ramifiee" ? "Avec des choix" : "Courte"}</span>
      </div>
      <h3>${escapeHtml(s.title)}</h3>
      <p>${escapeHtml(where)}${s.duration_s ? ` · ${fmtDur(s.duration_s)}` : ""}</p>
      ${s.has_audio ? `<button class="c-btn c-btn--ghost" data-play="${s.story_id}">${this.playingId === s.story_id ? "Arrêt" : "Écouter"}</button>` : ""}`;
    return el;
  }

  onGridClick(e) {
    const play = e.target.closest("[data-play]");
    if (!play) return;
    const id = play.dataset.play;
    if (this.playingId === id) {
      this.stopPlay();
      return;
    }
    this.preview(id);
  }

  showBar(id, title) {
    this.playingId = id;
    const bar = this.querySelector("#nowbar");
    bar.hidden = !id;
    this.querySelector("#nowtitle").textContent = title || "";
    this.querySelectorAll("[data-play]").forEach((b) => {
      b.textContent = b.dataset.play === id ? "Arrêt" : "Écouter";
      b.classList.toggle("c-btn--stop", b.dataset.play === id);
    });
  }

  stopPlay() {
    if (this.engine) {
      this.engine.stop();
      this.engine = null;
    }
    this.showBar(null, "");
  }

  async preview(storyId) {
    if (this.engine) this.engine.stop();
    const story = this.allStories.find((s) => s.story_id === storyId);
    this.showBar(storyId, story ? story.title : "");
    this.engine = new StoryEngine({
      api: this.api,
      player: new CryptoPlayer(),
      preview: true,
      maxSeconds: this.previewSeconds,
      onDone: () => this.showBar(null, ""),
    });
    try {
      await this.engine.run(storyId);
    } catch (e) {
      this.querySelector("#msg").textContent = e.message;
      this.showBar(null, "");
    }
  }
}

function escapeHtml(s) {
  return String(s || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function ageLabel(band) {
  return { N1: "3–4 ans", N2: "4–5 ans", N3: "5–6 ans" }[band] || band;
}

function fmtDur(sec) {
  const m = Math.max(1, Math.round(Number(sec) / 60));
  return `${m} min`;
}

function fold(s) {
  return String(s || "")
    .normalize("NFD")
    .replace(/\p{M}/gu, "")
    .toLowerCase();
}

customElements.define("acomytha-home", HomeApp);

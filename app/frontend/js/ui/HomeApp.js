import { Component } from "../core/Component.js";
import { CryptoPlayer } from "../core/CryptoPlayer.js";
import { StoryEngine } from "../core/StoryEngine.js";
import { acmIcon, acmLogo } from "./acm.js";

export class HomeApp extends Component {
  constructor() {
    super();
    this.api = null;
    this.router = null;
    this.stories = [];
    this.total = 0;
    this.pageSize = 6;
    this.domainNames = new Map();
    this.engine = null;
    this.playingId = null;
    this.previewSeconds = 10;
    this.prices = { story: 1, tree: 1 };
    this._filterTimer = 0;
    this._loading = false;
    this._gen = 0;
    this._observer = null;
    this.me = null;
  }

  async connectedCallback() {
    this.innerHTML = `
      <div class="s-home">
        <div class="c-stage">
          <header class="c-top">
            ${acmLogo({ size: "sm" })}
            <nav class="c-nav">
              <a class="c-nav__ghost" href="#/entrer">Connexion</a>
              <a class="c-nav__gold" href="#/inscription">Créer un compte</a>
            </nav>
          </header>
          <section class="c-hero">
            <p class="c-kicker">AcoMytha : univers d’histoires ludiques et captivantes.</p>
            <div class="c-field" aria-hidden="true">
              <span class="c-ring"></span>
              <span class="c-ring"></span>
              <span class="c-ring"></span>
              <span class="c-filament"></span>
              <div class="c-hero-logo">${acmIcon("acm--lg")}</div>
            </div>
            <h1>Apprendre<br>par l’<em>histoire.</em></h1>
          </section>
          <section class="c-score" aria-label="AcoMytha">
            <article class="c-move">
              <span class="c-move__idx">01</span>
              <h2>AcoMytha, c’est quoi ?</h2>
              <p>L’enfant apprend par l’histoire, de façon interactive, uniquement par la voix, sans écran, sans bouton. Les histoires sont ludiques et contiennent des leçons qui peuvent varier : respect du feu rouge, partage des jouets, manger les légumes, etc.</p>
            </article>
            <article class="c-move c-move--modes">
              <span class="c-move__idx">02</span>
              <h2>AcoMytha, deux modes</h2>
              <div class="c-modes">
                <div class="c-mode c-mode--day">
                  <b>Jour</b>
                  <p>Interactif — questions / réponses et options d’histoires.</p>
                </div>
                <div class="c-mode c-mode--night">
                  <b>Nuit</b>
                  <p>Moins d’interaction. L’objectif est d’écouter jusqu’à dormir.</p>
                </div>
              </div>
            </article>
            <article class="c-move c-move--count">
              <span class="c-move__idx">03</span>
              <h2>AcoMytha en chiffres</h2>
              <div class="c-count">
                <div><b>1000+</b><span>histoires</span></div>
                <div><b>~10</b><span>thèmes</span></div>
                <div><b>~100</b><span>leçons</span></div>
              </div>
            </article>
            <p class="c-offer">Offrez à votre enfant l’opportunité d’apprendre par l’histoire.</p>
          </section>
        </div>
        <section class="c-catalog">
          <header class="c-catalog__head">
            <h2>Le catalogue</h2>
            <p class="c-hint" id="count"></p>
          </header>
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
              <option value="interaction">Avec interaction</option>
              <option value="ramifiee">Avec ramifications vers d’autres histoires</option>
            </select>
          </div>
          <p class="c-error" id="msg"></p>
          <div class="o-grid" id="grid"></div>
          <p class="c-more" id="more" hidden>Chargement…</p>
        </section>
        <div class="c-nowbar" id="nowbar" hidden>
          <span id="nowtitle"></span>
          <button class="c-btn c-btn--stop" type="button" id="stop">Arrêt</button>
        </div>
        <div class="c-modal" id="modal" hidden>
          <div class="c-modal__box" id="modalbox"></div>
        </div>
        <div class="c-modal c-gate" id="gate" hidden>
          <div class="c-gate__box" role="dialog" aria-labelledby="gate-title">
            <h2 id="gate-title">La suite est derrière la porte.</h2>
            <p>Vous venez d’écouter un aperçu. Connectez-vous ou créez un compte pour entendre l’histoire jusqu’au bout.</p>
            <div class="c-gate__actions">
              <a class="c-nav__gold" href="#/inscription">Créer un compte</a>
              <a class="c-nav__ghost" href="#/entrer">Connexion</a>
            </div>
            <button class="c-gate__close" type="button" data-close-gate="1">Plus tard</button>
          </div>
        </div>
      </div>`;
    this.on(this, "pointermove", (e) => {
      const field = this.querySelector(".c-field");
      if (!field) return;
      const r = field.getBoundingClientRect();
      if (r.width < 8) return;
      field.style.setProperty("--mx", ((e.clientX - r.left) / r.width - 0.5).toFixed(3));
      field.style.setProperty("--my", ((e.clientY - r.top) / r.height - 0.5).toFixed(3));
    });
    this.on(this.querySelector("#q"), "input", () => this.scheduleFetch());
    this.on(this.querySelector("#domain"), "change", () => this.fetchPage({ reset: true }));
    this.on(this.querySelector("#age"), "change", () => this.fetchPage({ reset: true }));
    this.on(this.querySelector("#kind"), "change", () => this.fetchPage({ reset: true }));
    this.on(this.querySelector("#grid"), "click", (e) => this.onGridClick(e));
    this.on(this.querySelector("#stop"), "click", () => this.stopPlay());
    this.on(this.querySelector("#modal"), "click", (e) => this.onModalClick(e));
    this.on(this.querySelector("#gate"), "click", (e) => {
      if (e.target.id === "gate" || e.target.closest("[data-close-gate]")) this.closeGate();
    });
    this.on(window, "keydown", (e) => {
      if (e.key === "Escape") {
        this.closeModal();
        this.closeGate();
      }
    });
    await this.boot();
  }

  disconnectedCallback() {
    clearTimeout(this._filterTimer);
    if (this._observer) this._observer.disconnect();
    if (this.engine) this.engine.stop();
    super.disconnectedCallback();
  }

  async boot() {
    try {
      const [stats, lessons] = await Promise.all([
        this.api.get("/public/stats"),
        this.api.get("/public/lessons"),
      ]);
      this.previewSeconds = stats.preview_seconds || 30;
      this.pageSize = Math.max(1, Math.min(Number(stats.home_catalog_page_size) || 6, 48));
      this.prices = {
        story: stats.price_story_acm ?? 1,
        tree: stats.price_tree_acm ?? 1,
      };
      this.domainNames = new Map(lessons.map((l) => [l.domain_id, l.domain]));
      const sel = this.querySelector("#domain");
      for (const [id, name] of this.domainNames) {
        const o = document.createElement("option");
        o.value = id;
        o.textContent = name;
        sel.append(o);
      }
      try {
        this.me = await this.api.get("/auth/me");
        const nav = this.querySelector(".c-top nav");
        nav.innerHTML = `<a class="c-nav__gold" href="#/${this.me.role === "admin" ? "admin" : "parent"}">Mon espace</a>`;
      } catch {
        this.me = null;
      }
      this.watchScroll();
      await this.fetchPage({ reset: true });
    } catch (e) {
      this.querySelector("#msg").textContent = e.message || "Catalogue indisponible.";
    }
  }

  watchScroll() {
    const more = this.querySelector("#more");
    if (!more || this._observer) return;
    this._observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) this.fetchPage();
      },
      { root: null, rootMargin: "480px", threshold: 0 }
    );
    this._observer.observe(more);
  }

  scheduleFetch() {
    clearTimeout(this._filterTimer);
    this._filterTimer = setTimeout(() => this.fetchPage({ reset: true }), 160);
  }

  filters() {
    return {
      q: (this.querySelector("#q")?.value || "").trim(),
      domain: this.querySelector("#domain")?.value || "",
      age_band: this.querySelector("#age")?.value || "",
      kind: this.querySelector("#kind")?.value || "",
    };
  }

  async fetchPage({ reset = false } = {}) {
    if (!reset && this._loading) return;
    if (!reset && this.total > 0 && this.stories.length >= this.total) return;
    const gen = reset ? ++this._gen : this._gen;
    this._loading = true;
    const more = this.querySelector("#more");
    if (more) more.hidden = false;
    try {
      const f = this.filters();
      const params = new URLSearchParams();
      if (f.q) params.set("q", f.q);
      if (f.domain) params.set("domain", f.domain);
      if (f.age_band) params.set("age_band", f.age_band);
      if (f.kind) params.set("kind", f.kind);
      params.set("limit", String(this.pageSize));
      params.set("offset", String(reset ? 0 : this.stories.length));
      const data = await this.api.get(`/public/stories?${params}`);
      if (gen !== this._gen) return;
      const items = data.items || [];
      this.total = Number(data.total) || 0;
      this.pageSize = Number(data.limit) || this.pageSize;
      if (reset) {
        this.stories = items;
        const grid = this.querySelector("#grid");
        grid.replaceChildren();
        for (const s of items) grid.append(this.card(s));
      } else {
        this.stories.push(...items);
        const grid = this.querySelector("#grid");
        for (const s of items) grid.append(this.card(s));
      }
      const count = this.querySelector("#count");
      if (count) {
        count.textContent =
          this.total === 0
            ? "Aucune histoire"
            : `${this.stories.length} / ${this.total} histoire${this.total > 1 ? "s" : ""}`;
      }
    } catch (e) {
      const msg = this.querySelector("#msg");
      if (msg) msg.textContent = e.message || "Catalogue indisponible.";
    } finally {
      if (gen === this._gen) {
        this._loading = false;
        if (more) {
          const done = this.total > 0 && this.stories.length >= this.total;
          more.hidden = done;
          if (this._observer) {
            this._observer.unobserve(more);
            if (!done) this._observer.observe(more);
          }
        }
      }
    }
  }

  related(s) {
    return Array.isArray(s.related) ? s.related : [];
  }

  card(s) {
    const el = document.createElement("article");
    el.className = "c-card c-sheet";
    const theme = this.domainNames.get(s.domain) || "";
    const where = [theme, s.setting].filter(Boolean).join(" · ");
    const form = formLabel(s);
    const rel = this.related(s);
    const links = rel.length
      ? `<ul class="c-links">${rel
          .map(
            (r) =>
              `<li><a href="#/" data-open="${r.story_id}">${escapeHtml(r.title)}</a></li>`
          )
          .join("")}</ul>`
      : "";
    el.innerHTML = `
      ${form ? `<div class="o-row"><span class="c-pill c-pill--ram">${form}</span></div>` : ""}
      <h3>${escapeHtml(s.title)}</h3>
      <p>${escapeHtml(where)}${s.duration_s ? ` · ${fmtDur(s.duration_s)}` : ""}</p>
      <button class="c-btn c-btn--ghost" data-play="${s.story_id}">${this.playingId === s.story_id ? "Arrêt" : "Écouter"}</button>
      ${links}`;
    return el;
  }

  onGridClick(e) {
    const open = e.target.closest("[data-open]");
    if (open) {
      e.preventDefault();
      this.openModal(open.dataset.open);
      return;
    }
    const play = e.target.closest("[data-play]");
    if (!play) return;
    const id = play.dataset.play;
    if (this.playingId === id) {
      this.stopPlay();
      return;
    }
    this.preview(id);
  }

  onModalClick(e) {
    if (e.target.id === "modal" || e.target.closest("[data-close]")) {
      this.closeModal();
      return;
    }
    const open = e.target.closest("[data-open]");
    if (open) {
      e.preventDefault();
      this.openModal(open.dataset.open);
      return;
    }
    const play = e.target.closest("[data-play]");
    if (!play) return;
    const id = play.dataset.play;
    if (this.playingId === id) this.stopPlay();
    else this.preview(id);
  }

  async openModal(storyId) {
    let s = this.stories.find((x) => x.story_id === storyId);
    if (!s) {
      try {
        s = await this.api.get(`/public/stories/${encodeURIComponent(storyId)}`);
        this.stories.push(s);
      } catch {
        return;
      }
    }
    const modal = this.querySelector("#modal");
    const box = this.querySelector("#modalbox");
    box.replaceChildren();
    const close = document.createElement("button");
    close.className = "c-modal__close";
    close.type = "button";
    close.dataset.close = "1";
    close.textContent = "Fermer";
    box.append(close);
    box.append(this.card(s));
    modal.hidden = false;
  }

  closeModal() {
    const modal = this.querySelector("#modal");
    if (modal) modal.hidden = true;
  }

  openGate() {
    const gate = this.querySelector("#gate");
    if (gate) gate.hidden = false;
  }

  closeGate() {
    const gate = this.querySelector("#gate");
    if (gate) gate.hidden = true;
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
    const story = this.stories.find((s) => s.story_id === storyId);
    this.showBar(storyId, story ? story.title : "");
    this.engine = new StoryEngine({
      api: this.api,
      player: new CryptoPlayer(),
      preview: true,
      maxSeconds: this.previewSeconds,
      onDone: ({ userStop } = {}) => {
        this.showBar(null, "");
        if (!userStop && !this.me) this.openGate();
      },
    });
    try {
      await this.engine.run(storyId);
    } catch (e) {
      this.showBar(null, "");
      if (!this.me) this.openGate();
      else {
        const msg = this.querySelector("#msg");
        if (msg) msg.textContent = e.message;
      }
    }
  }
}

function escapeHtml(s) {
  return String(s || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function formLabel(s) {
  if (s.kind === "ramifiee") return "Avec ramifications vers d’autres histoires";
  if (s.has_interaction) return "Avec interaction";
  return "";
}

function fmtDur(sec) {
  const m = Math.max(1, Math.round(Number(sec) / 60));
  return `${m} min`;
}

customElements.define("acomytha-home", HomeApp);

import { Component } from "../core/Component.js";
import { CryptoPlayer } from "../core/CryptoPlayer.js";
import { StoryEngine } from "../core/StoryEngine.js";
import { acmAmount, acmIcon, acmLogo } from "./acm.js";

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
        <header class="c-top">
          ${acmLogo({ size: "sm" })}
          <nav>
            <a href="#/entrer">Connexion</a>
            <a class="c-btn" href="#/inscription">Créer un compte</a>
          </nav>
        </header>
        <section class="c-hero">
          <div class="c-hero-logo">${acmIcon("acm--lg")}</div>
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
              <option value="interaction">Avec interaction</option>
              <option value="ramifiee">Avec ramifications vers d’autres histoires</option>
            </select>
          </div>
          <p class="c-hint" id="count"></p>
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
      </div>`;
    this.on(this.querySelector("#q"), "input", () => this.scheduleFetch());
    this.on(this.querySelector("#domain"), "change", () => this.fetchPage({ reset: true }));
    this.on(this.querySelector("#age"), "change", () => this.fetchPage({ reset: true }));
    this.on(this.querySelector("#kind"), "change", () => this.fetchPage({ reset: true }));
    this.on(this.querySelector("#grid"), "click", (e) => this.onGridClick(e));
    this.on(this.querySelector("#stop"), "click", () => this.stopPlay());
    this.on(this.querySelector("#modal"), "click", (e) => this.onModalClick(e));
    this.on(window, "keydown", (e) => {
      if (e.key === "Escape") this.closeModal();
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
      this.previewSeconds = stats.preview_seconds || 10;
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
    el.className = "c-card";
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
      <p>${acmAmount(s.kind === "ramifiee" ? this.prices.tree : this.prices.story)}</p>
      ${s.has_audio ? `<button class="c-btn c-btn--ghost" data-play="${s.story_id}">${this.playingId === s.story_id ? "Arrêt" : "Écouter"}</button>` : ""}
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

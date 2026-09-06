import { Component } from "../core/Component.js";
import { CryptoPlayer } from "../core/CryptoPlayer.js";
import { StoryEngine } from "../core/StoryEngine.js";
import { acmIcon, acmLogo } from "./acm.js";

const GUEST_CATALOG_KEY = "acomytha.guest.catalog.v1";
const GUEST_CATALOG_LIMIT = 2;

export class HomeApp extends Component {
  #stories = [];
  #total = 0;
  #pageSize = 6;
  #domainNames = new Map();
  #engine = null;
  #playingId = null;
  #previewSeconds = 30;
  #prices = { story: 1, tree: 1 };
  #filterTimer = 0;
  #loading = false;
  #gen = 0;
  #observer = null;
  #me = null;
  #guestCatalog = new Set();

  get stories() {
    return this.#stories;
  }
  set stories(value) {
    this.#stories = Array.isArray(value) ? value : [];
  }
  get total() {
    return this.#total;
  }
  set total(value) {
    this.#total = Math.max(0, Number(value) || 0);
  }
  get pageSize() {
    return this.#pageSize;
  }
  set pageSize(value) {
    const n = Number(value) || 6;
    this.#pageSize = Math.max(1, Math.min(n, 48));
  }
  get domainNames() {
    return this.#domainNames;
  }
  set domainNames(value) {
    this.#domainNames = value instanceof Map ? value : new Map();
  }
  get engine() {
    return this.#engine;
  }
  set engine(value) {
    this.#engine = value || null;
  }
  get playingId() {
    return this.#playingId;
  }
  set playingId(value) {
    this.#playingId = value || null;
  }
  get previewSeconds() {
    return this.#previewSeconds;
  }
  set previewSeconds(value) {
    this.#previewSeconds = Math.max(1, Number(value) || 30);
  }
  get prices() {
    return this.#prices;
  }
  set prices(value) {
    this.#prices = value && typeof value === "object" ? value : { story: 1, tree: 1 };
  }
  get me() {
    return this.#me;
  }
  set me(value) {
    this.#me = value || null;
  }

  get _filterTimer() {
    return this.#filterTimer;
  }
  set _filterTimer(value) {
    this.#filterTimer = value;
  }
  get _loading() {
    return this.#loading;
  }
  set _loading(value) {
    this.#loading = Boolean(value);
  }
  get _gen() {
    return this.#gen;
  }
  set _gen(value) {
    this.#gen = Number(value) || 0;
  }
  get _observer() {
    return this.#observer;
  }
  set _observer(value) {
    this.#observer = value || null;
  }

  async connectedCallback() {
    this.#guestCatalog = this.#readGuestCatalog();
    this.innerHTML = `
      <div class="s-home">
        <div class="c-stage">
          <header class="c-top">
            ${acmLogo({ size: "sm" })}
            <nav class="c-nav">
              <a class="c-nav__quiet" href="#catalogue">Explorer</a>
              <a class="c-nav__ghost" href="#/entrer">Connexion</a>
              <a class="c-nav__gold" href="#/inscription">Créer mon compte</a>
            </nav>
          </header>
          <section class="c-hero">
            <div class="c-hero__copy">
              <p class="c-kicker">Histoires audio interactives · 3–6 ans</p>
              <h1>Ce soir, une aventure.<br><em>Demain, un petit geste en plus.</em></h1>
              <p class="c-hero__lead">Des récits captivants que votre enfant écoute, choisit et fait avancer avec sa voix.</p>
              <div class="c-hero__actions">
                <a class="c-nav__gold c-hero__cta" href="#catalogue">Écouter une aventure</a>
                <button class="c-nav__ghost c-hero__cta" type="button" id="guest-child-mode">Essayer le mode enfant</button>
              </div>
              <p class="c-trust"><span aria-hidden="true">✓</span> Aucun nom ni prénom demandé. Seulement votre e-mail et un mot de passe.</p>
            </div>
            <div class="c-field" aria-hidden="true">
              <span class="c-ring"></span>
              <span class="c-ring"></span>
              <span class="c-ring"></span>
              <span class="c-filament"></span>
              <div class="c-hero-logo">${acmIcon("acm--lg")}</div>
            </div>
          </section>
          <section class="c-score" aria-label="AcoMytha">
            <article class="c-move">
              <p class="c-eyebrow">Grandir en écoutant</p>
              <h2>Une histoire d’abord.<br>Une leçon qui se vit.</h2>
              <p>Pas de cours déguisé : une vraie aventure, des personnages attachants et des choix qui aident l’enfant à comprendre les petits gestes du quotidien.</p>
            </article>
            <article class="c-move c-move--modes">
              <h2>AcoMytha, deux modes</h2>
              <div class="c-modes">
                <div class="c-mode c-mode--day">
                  <b>
                    <svg class="c-mode__icon" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><use href="#icon-sun"/></svg>
                    Jour
                  </b>
                  <p>Interactif — questions / réponses et options d’histoires.</p>
                </div>
                <div class="c-mode c-mode--night">
                  <b>
                    <svg class="c-mode__icon" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><use href="#icon-moon"/></svg>
                    Nuit
                  </b>
                  <p>Moins d’interaction. L’objectif est d’écouter jusqu’à dormir.</p>
                </div>
              </div>
            </article>
            <article class="c-move c-move--count">
              <h2>AcoMytha en chiffres</h2>
              <div class="c-count">
                <div><b>&gt; 1400</b><span>histoires</span></div>
                <div><b>&gt; 10</b><span>thèmes</span></div>
                <div><b>&gt; 80</b><span>leçons</span></div>
              </div>
            </article>
            <div class="c-free-callout">
              <div>
                <p class="c-eyebrow">Une porte ouverte sur AcoMytha</p>
                <h2>Créez un compte et accédez gratuitement à une multitude d’histoires.</h2>
              </div>
              <a class="c-nav__gold" href="#/inscription">Créer mon compte parent</a>
            </div>
          </section>
        <section class="c-catalog" id="catalogue">
          <header class="c-catalog__head">
            <div>
              <p class="c-eyebrow">Trouvez l’aventure de ce soir</p>
              <h2>Le catalogue</h2>
            </div>
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
          <div class="c-catalog-tools">
            <p><strong id="guest-count">${this.#guestCatalog.size}</strong> / ${GUEST_CATALOG_LIMIT} histoires dans votre sélection enfant</p>
            <button type="button" class="c-text-action" id="open-selection">Voir la sélection</button>
          </div>
          <p class="c-error" id="msg"></p>
          <div class="o-grid" id="grid"></div>
          <p class="c-more" id="more" hidden>Chargement…</p>
        </section>
        </div>
        <div class="c-nowbar" id="nowbar" hidden>
          <span id="nowtitle"></span>
          <button class="c-btn c-btn--stop" type="button" id="stop">Arrêt</button>
        </div>
        <div class="c-modal" id="modal" hidden>
          <div class="c-modal__box" id="modalbox"></div>
        </div>
        <div class="c-modal c-gate" id="gate" hidden>
          <div class="c-gate__box" role="dialog" aria-labelledby="gate-title">
            <p class="c-eyebrow">Votre aperçu de 30 secondes est terminé</p>
            <h2 id="gate-title">L’aventure ne fait que commencer.</h2>
            <p>Connectez-vous ou créez votre compte parent pour retrouver votre sélection et accéder gratuitement à une multitude d’histoires.</p>
            <p class="c-privacy-note">Aucun nom ni prénom demandé · validation de l’e-mail · données minimales</p>
            <div class="c-gate__actions">
              <a class="c-nav__gold" href="#/inscription">Créer mon compte parent</a>
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
    this.on(this.querySelector("#guest-child-mode"), "click", () => this.openGuestChildMode());
    this.on(this.querySelector("#open-selection"), "click", () => this.openSelection());
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
    const rel = this.related(s).slice(0, 3);
    const links = rel.length
      ? `<ul class="c-links">${rel
          .map(
            (r) =>
              `<li><a href="#/" data-open="${r.story_id}">${escapeHtml(r.title)}</a></li>`
          )
          .join("")}</ul>`
      : "";
    el.innerHTML = `
      ${form ? `<p class="c-sheet__kind">${form}</p>` : ""}
      <h3>${escapeHtml(s.title)}</h3>
      <p class="c-sheet__meta">${escapeHtml(where)}${s.duration_s ? ` · ${fmtDur(s.duration_s)}` : ""}</p>
      ${links}
      <div class="c-sheet__actions">
        <button class="c-listen" type="button" data-play="${s.story_id}">${this.playingId === s.story_id ? "Arrêt" : "Écouter 30 s"}</button>
        <button class="c-add ${this.#guestCatalog.has(s.story_id) ? "is-added" : ""}" type="button" data-add="${s.story_id}" aria-pressed="${this.#guestCatalog.has(s.story_id)}">
          ${this.#guestCatalog.has(s.story_id) ? "Ajoutée à l’enfant" : "Ajouter à un enfant"}
        </button>
      </div>`;
    return el;
  }

  onGridClick(e) {
    const open = e.target.closest("[data-open]");
    if (open) {
      e.preventDefault();
      this.openModal(open.dataset.open);
      return;
    }
    const add = e.target.closest("[data-add]");
    if (add) {
      this.toggleGuestStory(add.dataset.add);
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
    const add = e.target.closest("[data-add]");
    if (add) {
      this.toggleGuestStory(add.dataset.add);
      return;
    }
    if (e.target.closest("[data-child-demo]")) {
      this.openGuestChildMode();
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

  toggleGuestStory(storyId) {
    if (this.#guestCatalog.has(storyId)) {
      this.#guestCatalog.delete(storyId);
      this.#saveGuestCatalog();
      this.refreshGuestUi();
      return;
    }
    if (this.#guestCatalog.size >= GUEST_CATALOG_LIMIT) {
      this.openGate();
      return;
    }
    this.#guestCatalog.add(storyId);
    this.#saveGuestCatalog();
    this.refreshGuestUi();
  }

  refreshGuestUi() {
    const count = this.querySelector("#guest-count");
    if (count) count.textContent = String(this.#guestCatalog.size);
    this.querySelectorAll("[data-add]").forEach((button) => {
      const added = this.#guestCatalog.has(button.dataset.add);
      button.classList.toggle("is-added", added);
      button.setAttribute("aria-pressed", String(added));
      button.textContent = added ? "Ajoutée à l’enfant" : "Ajouter à un enfant";
    });
  }

  openSelection() {
    if (!this.#guestCatalog.size) {
      const box = this.querySelector("#modalbox");
      box.innerHTML = `<button class="c-modal__close" type="button" data-close="1">Fermer</button><div class="c-empty-selection"><p class="c-eyebrow">Sélection enfant</p><h2>Choisissez jusqu’à deux aventures.</h2><p>Ajoutez-les depuis le catalogue, puis essayez le mode enfant pendant 30 secondes.</p></div>`;
      this.querySelector("#modal").hidden = false;
      return;
    }
    const selected = this.stories.filter((story) => this.#guestCatalog.has(story.story_id));
    const box = this.querySelector("#modalbox");
    box.innerHTML = `<button class="c-modal__close" type="button" data-close="1">Fermer</button><div class="c-selection"><p class="c-eyebrow">Sélection enfant</p><h2>${selected.length} aventure${selected.length > 1 ? "s" : ""} prête${selected.length > 1 ? "s" : ""} à écouter</h2><div class="c-selection__list">${selected.map((story) => `<div><strong>${escapeHtml(story.title)}</strong><button type="button" data-play="${story.story_id}">Écouter 30 s</button></div>`).join("")}</div><button class="c-nav__gold" type="button" data-child-demo="1">Lancer le mode enfant</button></div>`;
    this.querySelector("#modal").hidden = false;
  }

  openGuestChildMode() {
    if (!this.#guestCatalog.size) {
      this.openSelection();
      return;
    }
    this.openSelection();
    const box = this.querySelector("#modalbox");
    const note = document.createElement("p");
    note.className = "c-voice-preview";
    note.textContent = "La démonstration vocale utilisera uniquement ces histoires. La recherche orale complète arrive dans la prochaine étape.";
    box.querySelector(".c-selection")?.append(note);
  }

  #readGuestCatalog() {
    try {
      const value = JSON.parse(localStorage.getItem(GUEST_CATALOG_KEY) || "[]");
      return new Set(Array.isArray(value) ? value.slice(0, GUEST_CATALOG_LIMIT) : []);
    } catch {
      return new Set();
    }
  }

  #saveGuestCatalog() {
    localStorage.setItem(GUEST_CATALOG_KEY, JSON.stringify([...this.#guestCatalog]));
  }

  showBar(id, title) {
    this.playingId = id;
    const bar = this.querySelector("#nowbar");
    bar.hidden = !id;
    this.querySelector("#nowtitle").textContent = title || "";
    this.querySelectorAll("[data-play]").forEach((b) => {
      b.textContent = b.dataset.play === id ? "Arrêt" : "Écouter";
      b.classList.toggle("c-btn--stop", b.dataset.play === id);
      b.classList.toggle("c-listen--stop", b.dataset.play === id);
    });
  }

  stopPlay() {
    const prev = this.engine;
    this.engine = null;
    if (prev) prev.stop();
    this.showBar(null, "");
  }

  #handoff() {
    const prev = this.engine;
    this.engine = null;
    if (prev) prev.stop({ replaced: true });
  }

  async preview(storyId) {
    this.#handoff();
    this.closeGate();
    const story = this.stories.find((s) => s.story_id === storyId);
    this.showBar(storyId, story ? story.title : "");
    const need = this.previewSeconds || 30;
    const engine = new StoryEngine({
      api: this.api,
      player: new CryptoPlayer(),
      preview: true,
      maxSeconds: need,
      onDone: ({ userStop, heard } = {}) => {
        if (this.engine !== engine) return;
        this.showBar(null, "");
        if (userStop || this.me) return;
        if ((heard || 0) >= need * 0.85) this.openGate();
      },
    });
    this.engine = engine;
    try {
      await engine.run(storyId);
    } catch (e) {
      if (this.engine !== engine) return;
      this.showBar(null, "");
      const msg = this.querySelector("#msg");
      if (msg) msg.textContent = "L’écoute n’a pas pu démarrer.";
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

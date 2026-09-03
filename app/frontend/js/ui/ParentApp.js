import { Component } from "../core/Component.js";
import { DeviceIdentity } from "../core/DeviceIdentity.js";
import { CryptoPlayer } from "../core/CryptoPlayer.js";
import { StoryEngine } from "../core/StoryEngine.js";

export class ParentApp extends Component {
  constructor() {
    super();
    this.api = null;
    this.router = null;
    this.me = null;
    this.selected = new Set();
    this.engine = null;
    this.allStories = [];
    this.domainNames = new Map();
    this._filterTimer = 0;
  }

  async connectedCallback() {
    this.innerHTML = `
      <div class="s-shell">
        <aside class="s-rail">
          <div class="c-mark"><strong>AcoMytha</strong><span>espace parent</span></div>
          <nav>
            <a href="#/parent" class="is-on">Histoires</a>
            <a href="#/enfant">Mode enfant</a>
          </nav>
          <button class="c-btn c-btn--ghost" id="out">Quitter</button>
        </aside>
        <main class="s-main">
          <div class="c-title">
            <div>
              <h1>Histoires</h1>
              <p>Cochez celles que votre enfant pourra écouter, puis enregistrez.</p>
            </div>
            <button class="c-btn" id="save">Enregistrer</button>
          </div>
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
        </main>
      </div>`;
    this.on(this.querySelector("#out"), "click", () => this.logout());
    this.on(this.querySelector("#save"), "click", () => this.save());
    this.on(this.querySelector("#q"), "input", () => this.scheduleRender());
    this.on(this.querySelector("#domain"), "change", () => this.render());
    this.on(this.querySelector("#age"), "change", () => this.render());
    this.on(this.querySelector("#kind"), "change", () => this.render());
    this.on(this.querySelector("#grid"), "change", (e) => this.onGridChange(e));
    this.on(this.querySelector("#grid"), "click", (e) => this.onGridClick(e));
    await this.boot();
  }

  disconnectedCallback() {
    clearTimeout(this._filterTimer);
    super.disconnectedCallback();
  }

  async boot() {
    const msg = this.querySelector("#msg");
    try {
      const [lessons, picked, stories] = await Promise.all([
        this.api.get("/lessons"),
        this.api.get("/parent/forest"),
        this.api.get("/stories"),
      ]);
      this.selected = new Set(picked.map((s) => s.story_id));
      this.allStories = stories;
      this.domainNames = new Map(lessons.map((l) => [l.domain_id, l.domain]));
      const domains = [...this.domainNames.entries()];
      const sel = this.querySelector("#domain");
      for (const [id, name] of domains) {
        const o = document.createElement("option");
        o.value = id;
        o.textContent = name;
        sel.append(o);
      }
      this.render();
    } catch (e) {
      msg.textContent = e.message || "Impossible de charger le catalogue.";
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
        const blob = fold([s.title, s.story_id, s.lesson_id, s.setting, s.characters, s.subdomain].join(" "));
        if (!blob.includes(q)) return false;
      }
      return true;
    });
    const count = this.querySelector("#count");
    count.textContent = list.length === this.allStories.length
      ? `${list.length} histoires`
      : `${list.length} histoire${list.length > 1 ? "s" : ""} · ${this.allStories.length} au catalogue`;
    const grid = this.querySelector("#grid");
    grid.replaceChildren();
    for (const s of list) {
      grid.append(this.card(s));
    }
  }

  card(s) {
    const el = document.createElement("article");
    el.className = "c-card";
    const checked = this.selected.has(s.story_id) ? "checked" : "";
    const theme = this.domainNames.get(s.domain) || "";
    const where = [theme, s.setting].filter(Boolean).join(" · ");
    el.innerHTML = `
      <div class="o-row">
        <span class="c-pill c-pill--${s.age_band.toLowerCase()}">${ageLabel(s.age_band)}</span>
        <span class="c-pill ${s.kind === "ramifiee" ? "c-pill--ram" : ""}">${s.kind === "ramifiee" ? "Avec des choix" : "Courte"}</span>
        ${s.has_audio ? '<span class="c-pill c-pill--audio">À écouter</span>' : ""}
      </div>
      <h3>${escapeHtml(s.title)}</h3>
      <p>${escapeHtml(where)}</p>
      <label class="o-row"><input type="checkbox" data-id="${s.story_id}" ${checked}/> Pour l’enfant</label>
      ${s.has_audio ? `<button class="c-btn c-btn--ghost" data-play="${s.story_id}">Écouter</button>` : ""}`;
    return el;
  }

  onGridChange(e) {
    const box = e.target.closest("input[data-id]");
    if (!box) return;
    if (box.checked) this.selected.add(box.dataset.id);
    else this.selected.delete(box.dataset.id);
  }

  onGridClick(e) {
    const play = e.target.closest("[data-play]");
    if (!play) return;
    this.preview(play.dataset.play, play);
  }

  async save() {
    const msg = this.querySelector("#msg");
    await this.api.put("/parent/forest", { story_ids: [...this.selected] });
    msg.textContent = "Sélection enregistrée.";
  }

  async preview(storyId, btn) {
    if (this.engine) this.engine.stop();
    btn.textContent = "Lecture…";
    this.engine = new StoryEngine({
      api: this.api,
      player: new CryptoPlayer(),
      onStatus: (n) => {
        btn.textContent = n.kind === "passage_fin" ? "Fin" : "Lecture…";
      },
      onDone: () => {
        btn.textContent = "Écouter";
      },
    });
    try {
      await this.engine.run(storyId);
    } catch (e) {
      this.querySelector("#msg").textContent = e.message;
      btn.textContent = "Écouter";
    }
  }

  async logout() {
    if (this.engine) this.engine.stop();
    await this.api.post("/auth/logout", {});
    this.router.go("#/entrer");
  }
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function ageLabel(band) {
  return { N1: "3–4 ans", N2: "4–5 ans", N3: "5–6 ans" }[band] || band;
}

function fold(s) {
  return String(s || "")
    .normalize("NFD")
    .replace(/\p{M}/gu, "")
    .toLowerCase();
}

customElements.define("acomytha-parent", ParentApp);

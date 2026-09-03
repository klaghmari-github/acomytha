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
    this.forest = new Set();
    this.engine = null;
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
              <h1>La forêt</h1>
              <p>Choisis les histoires que l’enfant pourra écouter. Filtre, coche, c’est tout.</p>
            </div>
            <button class="c-btn" id="save">Enregistrer la forêt</button>
          </div>
          <div class="c-filters">
            <input id="q" placeholder="Rechercher un titre, une leçon…" />
            <select id="domain"><option value="">Domaine</option></select>
            <select id="age">
              <option value="">Âge</option>
              <option value="N1">N1 · 3–4 ans</option>
              <option value="N2">N2 · 4–5 ans</option>
              <option value="N3">N3 · 5–6 ans</option>
            </select>
            <select id="kind">
              <option value="">Forme</option>
              <option value="atomic">Clairière</option>
              <option value="ramifiee">Histoire ramifiée</option>
            </select>
            <button class="c-btn c-btn--ghost" id="refresh">Filtrer</button>
          </div>
          <p class="c-error" id="msg"></p>
          <div class="o-grid" id="grid"></div>
        </main>
      </div>`;
    this.on(this.querySelector("#out"), "click", () => this.logout());
    this.on(this.querySelector("#save"), "click", () => this.save());
    this.on(this.querySelector("#refresh"), "click", () => this.loadStories());
    this.on(this.querySelector("#q"), "keydown", (e) => {
      if (e.key === "Enter") this.loadStories();
    });
    await this.boot();
  }

  async boot() {
    const [lessons, forest] = await Promise.all([this.api.get("/lessons"), this.api.get("/parent/forest")]);
    this.forest = new Set(forest.map((s) => s.story_id));
    const domains = [...new Map(lessons.map((l) => [l.domain_id, l.domain])).entries()];
    const sel = this.querySelector("#domain");
    for (const [id, name] of domains) {
      const o = document.createElement("option");
      o.value = id;
      o.textContent = name;
      sel.append(o);
    }
    await this.loadStories();
  }

  async loadStories() {
    const q = this.querySelector("#q").value;
    const domain = this.querySelector("#domain").value;
    const age_band = this.querySelector("#age").value;
    const kind = this.querySelector("#kind").value;
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (domain) params.set("domain", domain);
    if (age_band) params.set("age_band", age_band);
    if (kind) params.set("kind", kind);
    const stories = await this.api.get("/stories?" + params.toString());
    const grid = this.querySelector("#grid");
    grid.replaceChildren();
    for (const s of stories) {
      grid.append(this.card(s));
    }
  }

  card(s) {
    const el = document.createElement("article");
    el.className = "c-card";
    const checked = this.forest.has(s.story_id) ? "checked" : "";
    el.innerHTML = `
      <div class="o-row">
        <span class="c-pill c-pill--${s.age_band.toLowerCase()}">${s.age_band}</span>
        <span class="c-pill ${s.kind === "ramifiee" ? "c-pill--ram" : ""}">${s.kind === "ramifiee" ? "ramifié" : "clairière"}</span>
        ${s.has_audio ? '<span class="c-pill c-pill--audio">audio</span>' : ""}
      </div>
      <h3>${escapeHtml(s.title)}</h3>
      <p>${escapeHtml(s.lesson_id)} · ${escapeHtml(s.setting || "")}</p>
      <label class="o-row"><input type="checkbox" data-id="${s.story_id}" ${checked}/> Dans la forêt enfant</label>
      ${s.has_audio ? `<button class="c-btn c-btn--ghost" data-play="${s.story_id}">Préécouter</button>` : ""}`;
    const box = el.querySelector("input[type=checkbox]");
    this.on(box, "change", () => {
      if (box.checked) this.forest.add(s.story_id);
      else this.forest.delete(s.story_id);
    });
    const play = el.querySelector("[data-play]");
    if (play) this.on(play, "click", () => this.preview(s.story_id, play));
    return el;
  }

  async save() {
    const msg = this.querySelector("#msg");
    await this.api.put("/parent/forest", { story_ids: [...this.forest] });
    msg.textContent = "Forêt enregistrée.";
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
        btn.textContent = "Préécouter";
      },
    });
    try {
      await this.engine.run(storyId);
    } catch (e) {
      this.querySelector("#msg").textContent = e.message;
      btn.textContent = "Préécouter";
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

customElements.define("acomytha-parent", ParentApp);

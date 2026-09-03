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
    this.playingId = null;
    this.allStories = [];
    this.domainNames = new Map();
    this.wallet = { balance_a: 0, owned: [], prices: {}, preview_seconds: 10 };
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
            <a href="#/">Accueil</a>
          </nav>
          <div class="c-wallet" id="wallet"></div>
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
          <div class="c-shop" id="shop"></div>
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
              <option value="interaction">Avec interaction</option>
            </select>
          </div>
          <p class="c-hint" id="count"></p>
          <p class="c-error" id="msg"></p>
          <div class="o-grid" id="grid"></div>
          <div class="c-nowbar" id="nowbar" hidden>
            <span id="nowtitle"></span>
            <button class="c-btn c-btn--stop" type="button" id="stop">Arrêt</button>
          </div>
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
    this.on(this.querySelector("#stop"), "click", () => this.stopPlay());
    this.on(this.querySelector("#shop"), "click", (e) => this.onShopClick(e));
    this.on(this.querySelector("#shop"), "submit", (e) => this.onShopSubmit(e));
    await this.boot();
  }

  disconnectedCallback() {
    clearTimeout(this._filterTimer);
    this.stopPlay();
    super.disconnectedCallback();
  }

  async boot() {
    const msg = this.querySelector("#msg");
    try {
      const [lessons, picked, stories, wallet] = await Promise.all([
        this.api.get("/lessons"),
        this.api.get("/parent/forest"),
        this.api.get("/stories"),
        this.api.get("/shop/wallet").catch(() => this.wallet),
      ]);
      this.selected = new Set(picked.map((s) => s.story_id));
      this.allStories = stories;
      this.wallet = wallet;
      this.domainNames = new Map(lessons.map((l) => [l.domain_id, l.domain]));
      const domains = [...this.domainNames.entries()];
      const sel = this.querySelector("#domain");
      for (const [id, name] of domains) {
        const o = document.createElement("option");
        o.value = id;
        o.textContent = name;
        sel.append(o);
      }
      this.drawWallet();
      this.drawShop();
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
      if (kind === "atomic" && s.kind !== "atomic") return false;
      if (kind === "interaction" && !s.has_interaction) return false;
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
    const owned = (this.wallet.owned || []).includes(s.story_id);
    const price = s.kind === "ramifiee" ? this.wallet.prices?.tree : this.wallet.prices?.story;
    const theme = this.domainNames.get(s.domain) || "";
    const where = [theme, s.setting].filter(Boolean).join(" · ");
    el.innerHTML = `
      <div class="o-row">
        <span class="c-pill c-pill--${s.age_band.toLowerCase()}">${ageLabel(s.age_band)}</span>
        <span class="c-pill ${s.has_interaction ? "c-pill--ram" : ""}">${s.has_interaction ? "Avec interaction" : "Courte"}</span>
        ${owned ? '<span class="c-pill c-pill--audio">À vous</span>' : ""}
      </div>
      <h3>${escapeHtml(s.title)}</h3>
      <p>${escapeHtml(where)}${s.duration_s ? ` · ${fmtDur(s.duration_s)}` : ""}</p>
      ${owned ? `<label class="o-row"><input type="checkbox" data-id="${s.story_id}" ${checked}/> Pour l’enfant</label>` : ""}
      <div class="o-row">
        ${s.has_audio ? `<button class="c-btn ${this.playingId === s.story_id ? "c-btn--stop" : "c-btn--ghost"}" data-play="${s.story_id}">${this.playingId === s.story_id ? "Arrêt" : owned ? "Écouter" : "Écouter"}</button>` : ""}
        ${owned ? "" : `<button class="c-btn" data-buy="${s.story_id}">Débloquer <span class="c-ako">${price ?? 1}</span></button>`}
      </div>`;
    return el;
  }

  drawWallet() {
    const el = this.querySelector("#wallet");
    if (!el) return;
    el.innerHTML = `<span class="c-ako c-ako--lg">${this.wallet.balance_a ?? 0}</span>`;
  }

  drawShop() {
    const el = this.querySelector("#shop");
    if (!el) return;
    const p = this.wallet.prices || {};
    el.innerHTML = `
      <details class="c-panel">
        <summary>Commander une histoire · <span class="c-ako">${p.order ?? 1.5}</span> + <span class="c-ako">${p.ramification ?? 0.5}</span> / choix</summary>
        <form id="orderform" class="o-stack">
          <textarea name="context" rows="3" required minlength="8" placeholder="Le contexte, les personnages…"></textarea>
          <label>Choix <input type="number" name="ramifications" min="0" max="3" value="0" /></label>
          <button class="c-btn" type="submit">Commander</button>
        </form>
      </details>
      <details class="c-panel">
        <summary>Enregistrer une voix · <span class="c-ako">${p.voice ?? 5}</span></summary>
        <form id="voiceform" class="o-stack">
          <select name="role">
            <option value="narrateur">Narrateur</option>
            <option value="papa">Papa</option>
            <option value="maman">Maman</option>
            <option value="copain">Copain</option>
            <option value="copine">Copine</option>
            <option value="maitresse">Maîtresse</option>
          </select>
          <button class="c-btn" type="submit">Enregistrer</button>
        </form>
      </details>
      <details class="c-panel">
        <summary>Recharger</summary>
        <div class="o-row" id="recharge">
          <button class="c-btn c-btn--ghost" data-eur="10">10 €</button>
          <button class="c-btn c-btn--ghost" data-eur="20">20 €</button>
          <button class="c-btn c-btn--ghost" data-eur="30">30 €</button>
        </div>
        <p class="c-hint" id="recharge-msg">Le paiement arrivera bientôt.</p>
      </details>`;
  }

  onGridChange(e) {
    const box = e.target.closest("input[data-id]");
    if (!box) return;
    if (box.checked) this.selected.add(box.dataset.id);
    else this.selected.delete(box.dataset.id);
  }

  onGridClick(e) {
    const buy = e.target.closest("[data-buy]");
    if (buy) {
      this.buy(buy.dataset.buy);
      return;
    }
    const play = e.target.closest("[data-play]");
    if (!play) return;
    if (this.playingId === play.dataset.play) {
      this.stopPlay();
      return;
    }
    this.preview(play.dataset.play);
  }

  async buy(storyId) {
    const msg = this.querySelector("#msg");
    try {
      this.wallet = await this.api.post("/shop/buy", { story_id: storyId });
      this.selected.add(storyId);
      this.drawWallet();
      this.render();
      msg.textContent = "Histoire débloquée.";
    } catch (e) {
      msg.textContent = e.status === 402 ? "Solde insuffisant." : e.message;
    }
  }

  async onShopClick(e) {
    const eur = e.target.closest("[data-eur]");
    if (!eur) return;
    const msg = this.querySelector("#recharge-msg");
    try {
      const r = await this.api.post("/shop/recharge", { eur: Number(eur.dataset.eur) });
      msg.textContent = `${r.eur} € → ${r.would_credit_a} A. ${r.message}`;
    } catch (err) {
      msg.textContent = err.message;
    }
  }

  async onShopSubmit(e) {
    e.preventDefault();
    const msg = this.querySelector("#msg");
    const form = e.target;
    try {
      if (form.id === "orderform") {
        const fd = new FormData(form);
        this.wallet = await this.api.post("/shop/order", {
          context: fd.get("context"),
          ramifications: Number(fd.get("ramifications") || 0),
        });
        form.reset();
        msg.textContent = "Commande envoyée.";
      }
      if (form.id === "voiceform") {
        const fd = new FormData(form);
        const f = new FormData();
        f.set("role", fd.get("role"));
        this.wallet = await this.api.postForm("/shop/voice", f);
        msg.textContent = "Voix enregistrée pour les prochaines histoires.";
      }
      this.drawWallet();
      this.drawShop();
    } catch (err) {
      msg.textContent = err.status === 402 ? "Solde insuffisant." : err.message;
    }
  }

  async save() {
    const msg = this.querySelector("#msg");
    await this.api.put("/parent/forest", { story_ids: [...this.selected] });
    msg.textContent = "Sélection enregistrée.";
  }

  showBar(id, title) {
    this.playingId = id;
    const bar = this.querySelector("#nowbar");
    if (bar) bar.hidden = !id;
    const t = this.querySelector("#nowtitle");
    if (t) t.textContent = title || "";
    this.querySelectorAll("[data-play]").forEach((b) => {
      const on = b.dataset.play === id;
      b.textContent = on ? "Arrêt" : "Écouter";
      b.classList.toggle("c-btn--stop", on);
      b.classList.toggle("c-btn--ghost", !on);
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
    const owned = (this.wallet.owned || []).includes(storyId);
    const sec = this.wallet.preview_seconds || 10;
    this.showBar(storyId, story ? story.title : "");
    this.engine = new StoryEngine({
      api: this.api,
      player: new CryptoPlayer(),
      preview: !owned,
      maxSeconds: owned ? 0 : sec,
      onDone: () => this.showBar(null, ""),
    });
    try {
      await this.engine.run(storyId);
    } catch (e) {
      this.querySelector("#msg").textContent = e.message;
      this.showBar(null, "");
    }
  }

  async logout() {
    this.stopPlay();
    await this.api.post("/auth/logout", {});
    this.router.go("#/");
  }
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function fmtDur(sec) {
  const m = Math.max(1, Math.round(Number(sec) / 60));
  return `${m} min`;
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

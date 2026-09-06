import { Component } from "../core/Component.js";
import { DeviceIdentity } from "../core/DeviceIdentity.js";
import { CryptoPlayer } from "../core/CryptoPlayer.js";
import { StoryEngine } from "../core/StoryEngine.js";
import { acmAmount, acmLogo, formatAcm } from "./acm.js";

export class ParentApp extends Component {
  #me = null;
  #selected = new Set();
  #engine = null;
  #playingId = null;
  #allStories = [];
  #domainNames = new Map();
  #wallet = { balance_a: 0, owned: [], prices: {}, preview_seconds: 30, parent_preview_seconds: 30 };
  #filterTimer = 0;

  get me() {
    return this.#me;
  }
  set me(value) {
    this.#me = value || null;
  }
  get selected() {
    return this.#selected;
  }
  set selected(value) {
    this.#selected = value instanceof Set ? value : new Set(value || []);
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
  get allStories() {
    return this.#allStories;
  }
  set allStories(value) {
    this.#allStories = Array.isArray(value) ? value : [];
  }
  get domainNames() {
    return this.#domainNames;
  }
  set domainNames(value) {
    this.#domainNames = value instanceof Map ? value : new Map();
  }
  get wallet() {
    return this.#wallet;
  }
  set wallet(value) {
    this.#wallet = value && typeof value === "object" ? value : this.#wallet;
  }
  get _filterTimer() {
    return this.#filterTimer;
  }
  set _filterTimer(value) {
    this.#filterTimer = value;
  }
  async connectedCallback() {
    this.innerHTML = `
      <div class="s-shell">
        <aside class="s-rail">
          <div class="c-mark">${acmLogo({ size: "sm" })}<span class="c-mark__sub">L’écoute, à la maison.</span></div>
          <nav>
            <a href="#/parent" class="is-on">Histoires</a>
            <a href="#/enfant">Mode enfant</a>
            <a href="#/">Accueil</a>
          </nav>
          <div class="c-wallet" id="wallet"></div>
          <div class="c-shop" id="shop"></div>
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
              <option value="interaction">Avec interaction</option>
              <option value="ramifiee">Avec ramifications vers d’autres histoires</option>
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
      const checkout = new URLSearchParams(location.hash.split("?")[1] || "").get("checkout");
      if (checkout === "success") msg.textContent = "Paiement reçu. Votre solde est actualisé après confirmation de Stripe.";
      if (checkout === "cancelled") msg.textContent = "Paiement annulé : aucun montant n’a été débité.";
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
      if (kind === "interaction" && (!s.has_interaction || s.kind === "ramifiee")) return false;
      if (kind === "ramifiee" && s.kind !== "ramifiee") return false;
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
        <span class="c-pill ${s.kind === "ramifiee" || s.has_interaction ? "c-pill--ram" : ""}">${formLabel(s)}</span>
        ${owned ? '<span class="c-pill c-pill--audio">À vous</span>' : ""}
      </div>
      <h3>${escapeHtml(s.title)}</h3>
      <p>${escapeHtml(where)}${s.duration_s ? ` · ${fmtDur(s.duration_s)}` : ""}</p>
      ${owned ? `<label class="o-row"><input type="checkbox" data-id="${s.story_id}" ${checked}/> Pour l’enfant</label>` : ""}
      <div class="o-row">
        ${s.has_audio ? `<button class="c-btn ${this.playingId === s.story_id ? "c-btn--stop" : "c-btn--ghost"}" data-play="${s.story_id}">${this.playingId === s.story_id ? "Arrêt" : owned ? "Écouter" : "Écouter"}</button>` : ""}
        ${owned ? "" : `<button class="c-btn" data-buy="${s.story_id}">Débloquer ${acmAmount(price ?? 1)}</button>`}
      </div>`;
    return el;
  }

  drawWallet() {
    const el = this.querySelector("#wallet");
    if (!el) return;
    el.innerHTML = `<span class="c-wallet__label">Solde</span>${acmAmount(this.wallet.balance_a ?? 0, { unit: true, size: "lg" })}`;
  }

  drawShop() {
    const el = this.querySelector("#shop");
    if (!el) return;
    const p = this.wallet.prices || {};
    const paymentReady = ["test", "live"].includes(this.wallet.stripe);
    const paymentHint = this.wallet.stripe === "test"
      ? "Mode test Stripe : aucune somme réelle ne sera débitée."
      : this.wallet.stripe === "live"
        ? "Paiement sécurisé par Stripe."
        : this.wallet.stripe === "webhook_missing"
          ? "Paiement désactivé : le webhook Stripe doit être configuré."
          : this.wallet.stripe === "invalid"
            ? "Paiement désactivé : configuration Stripe invalide ou URL HTTPS manquante."
            : "Paiement Stripe pas encore configuré sur ce serveur.";
    el.innerHTML = `
      <details class="c-panel">
        <summary>Commander une histoire · ${acmAmount(p.order ?? 1.5)} + ${acmAmount(p.ramification ?? 0.5)} / choix</summary>
        <form id="orderform" class="o-stack">
          <textarea name="context" rows="3" required minlength="8" placeholder="Le contexte, les personnages…"></textarea>
          <label>Choix <input type="number" name="ramifications" min="0" max="3" value="0" /></label>
          <button class="c-btn" type="submit">Commander</button>
        </form>
      </details>
      <details class="c-panel">
        <summary>Enregistrer une voix · ${acmAmount(p.voice ?? 5)}</summary>
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
        <summary>Code à 4 chiffres</summary>
        <form id="pinform" class="o-stack">
          <input name="current_pin" inputmode="numeric" maxlength="4" pattern="[0-9]{4}" placeholder="Code actuel" required />
          <input name="new_pin" inputmode="numeric" maxlength="4" pattern="[0-9]{4}" placeholder="Nouveau code" required />
          <input name="new_pin2" inputmode="numeric" maxlength="4" pattern="[0-9]{4}" placeholder="Confirmer" required />
          <button class="c-btn" type="submit">Enregistrer le code</button>
        </form>
      </details>
      <details class="c-panel">
        <summary>Obtenir des pièces AcoMytha</summary>
        <p class="c-hint c-pack__legend">Vous versez des euros. Vous recevez des pièces acm.</p>
        <div class="c-packs" id="recharge">
          ${[10, 20, 30, 40, 50]
            .map((e) => {
              const a = aFor(e, this.wallet.fx);
              return `<button class="c-pack" type="button" data-eur="${e}" ${paymentReady ? "" : "disabled"} aria-label="${e} euros donnent ${formatAcm(a)} acm">
                <b>${e} €</b>
                <span class="c-pack__fx" aria-hidden="true">→</span>
                ${acmAmount(a)}
              </button>`;
            })
            .join("")}
        </div>
        <p class="c-hint" id="recharge-msg">${paymentHint}</p>
      </details>
      `;
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
      if (r.checkout_url) {
        window.location.href = r.checkout_url;
        return;
      }
      throw new Error("Stripe n’a pas fourni de page de paiement.");
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
      if (form.id === "pinform") {
        const fd = new FormData(form);
        const a = String(fd.get("new_pin") || "");
        const b = String(fd.get("new_pin2") || "");
        if (!/^\d{4}$/.test(a) || a !== b) {
          msg.textContent = "Le nouveau code doit avoir 4 chiffres, deux fois les mêmes.";
          return;
        }
        await this.api.put("/auth/pin", { current_pin: fd.get("current_pin"), new_pin: a });
        form.reset();
        msg.textContent = "Code enregistré.";
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
    const story = this.allStories.find((s) => s.story_id === storyId);
    const owned = (this.wallet.owned || []).includes(storyId);
    const sec = this.wallet.parent_preview_seconds || 30;
    this.showBar(storyId, story ? story.title : "");
    const engine = new StoryEngine({
      api: this.api,
      player: new CryptoPlayer(),
      preview: owned ? false : "parent",
      maxSeconds: owned ? 0 : sec,
      onDone: () => {
        if (this.engine !== engine) return;
        this.showBar(null, "");
      },
    });
    this.engine = engine;
    try {
      await engine.run(storyId);
    } catch (e) {
      if (this.engine !== engine) return;
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

function formLabel(s) {
  if (s.kind === "ramifiee") return "Avec ramifications vers d’autres histoires";
  if (s.has_interaction) return "Avec interaction";
  return "";
}

function aFor(eur, fx) {
  const start = Number(fx?.start ?? 1);
  const step = Number(fx?.step ?? 0.25);
  const every = Number(fx?.every ?? 10) || 10;
  const cap = Number(fx?.max ?? 5);
  const band = Math.floor((Math.max(eur, 1) - 1) / every);
  const rate = Math.min(cap, start + step * band);
  return Math.round(eur * rate * 100) / 100;
}

function fold(s) {
  return String(s || "")
    .normalize("NFD")
    .replace(/\p{M}/gu, "")
    .toLowerCase();
}

customElements.define("acomytha-parent", ParentApp);

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
  #profiles = [];
  #activeProfileId = null;
  #editingProfileId = null;
  #assignmentStoryId = null;

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
          <div class="c-mark">${acmLogo({ size: "sm" })}<span class="c-mark__sub">Votre espace famille</span></div>
          <nav>
            <a href="#/parent" class="is-on">Pour ce soir</a>
            <a href="#profiles">Mes enfants</a>
            <a href="#catalog">Toutes les histoires</a>
            <a href="#/">Accueil</a>
          </nav>
          <div class="c-wallet" id="wallet"></div>
          <div class="c-shop" id="shop"></div>
          <button class="c-btn c-btn--ghost" id="out">Quitter</button>
        </aside>
        <main class="s-main">
          <section class="c-parent-welcome">
            <div><p class="c-eyebrow">Un moment rien qu’à vous</p><h1>Que va-t-on écouter ce soir ?</h1><p>Choisissez un enfant, préparez sa sélection, puis confiez-lui l’aventure.</p></div>
            <button class="c-btn c-btn--gold c-btn--lg" id="child-mode" type="button">Activer le mode enfant</button>
          </section>
          <section class="c-children" id="profiles">
            <div class="c-section-head"><div><p class="c-eyebrow">Profils enfants</p><h2>Pour qui choisissez-vous ?</h2></div><button class="c-btn c-btn--ghost" id="add-profile" type="button">Ajouter un enfant</button></div>
            <div class="c-profile-list" id="profile-list"></div>
          </section>
          <section class="c-panel c-listening-history" aria-labelledby="history-title">
            <div class="c-section-head"><div><p class="c-eyebrow">Activité récente</p><h2 id="history-title">Les écoutes de votre enfant</h2></div></div>
            <div class="o-stack" id="listening-history"><p class="c-hint">Choisissez un profil enfant pour voir ses écoutes.</p></div>
          </section>
          <div class="c-title">
            <div>
              <h2 id="catalog">Toutes les histoires</h2>
              <p id="catalog-help">Ajoutez les histoires au catalogue de l’enfant sélectionné.</p>
            </div>
            <button class="c-btn" id="save">Enregistrer la sélection</button>
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
          <div class="c-modal" id="profile-modal" hidden><form class="c-modal__box c-parent-dialog" id="profile-form"><button class="c-modal__close" type="button" data-close-profile="1">Fermer</button><p class="c-eyebrow" id="profile-kicker">Nouveau profil</p><h2 id="profile-title">Ajouter un enfant</h2><label class="c-field">Prénom ou surnom<input name="display_name" maxlength="80" required placeholder="Ex. Amir" /></label><label class="c-field">Âge<select name="age_band"><option value="N1">3–4 ans</option><option value="N2">4–5 ans</option><option value="N3">5–6 ans</option></select></label><label class="c-field">Expérience d’écoute<select name="playback_mode"><option value="day">Mode jour · histoires interactives</option><option value="night">Mode nuit · écoute calme</option></select></label><p class="c-hint">Ce choix est verrouillé en mode enfant. Vous pourrez le modifier ici à tout moment.</p><button class="c-btn c-btn--wide" id="profile-submit" type="submit">Créer le profil</button><button class="c-btn c-btn--ghost c-btn--wide" id="delete-profile" type="button" hidden>Supprimer ce profil</button><p class="c-error" id="profile-error"></p></form></div>
          <div class="c-modal" id="child-modal" hidden><form class="c-modal__box c-parent-dialog" id="child-form"><button class="c-modal__close" type="button" data-close-child="1">Fermer</button><p class="c-eyebrow">Mode enfant</p><h2>Verrouiller l’écran pour <span id="child-name"></span></h2><label class="c-field">Pour cette écoute<select name="playback_mode"><option value="day">Mode jour · questions et choix</option><option value="night">Mode nuit · narration plus calme</option></select></label><p>Choisissez un code de 4 chiffres. Gardez-le en mémoire : il permettra de quitter le mode enfant.</p><input class="c-pin" name="pin" inputmode="numeric" maxlength="4" pattern="[0-9]{4}" autocomplete="off" required aria-label="Code de sortie à 4 chiffres" /><button class="c-btn c-btn--wide" type="submit">Mémoriser et lancer</button><p class="c-hint">En cas d’oubli, fermez l’application puis reconnectez-vous avec votre e-mail et votre mot de passe.</p><p class="c-error" id="child-error"></p></form></div>
          <div class="c-modal" id="assignment-modal" hidden><form class="c-modal__box c-parent-dialog" id="assignment-form"><button class="c-modal__close" type="button" data-close-assignment="1">Fermer</button><p class="c-eyebrow">Catalogues enfants</p><h2 id="assignment-title">À qui proposer cette histoire ?</h2><p>Choisissez un ou plusieurs enfants. Vous pourrez modifier ce choix à tout moment.</p><label class="o-row"><input type="checkbox" id="assignment-all" /> <strong>Tous les enfants</strong></label><div class="o-stack" id="assignment-profiles"></div><button class="c-btn c-btn--wide" type="submit">Enregistrer dans les catalogues</button><p class="c-error" id="assignment-error"></p></form></div>
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
    this.on(this.querySelector("#profile-list"), "click", (e) => this.onProfileClick(e));
    this.on(this.querySelector("#add-profile"), "click", () => this.openProfileModal());
    this.on(this.querySelector("#profile-form"), "submit", (e) => this.createProfile(e));
    this.on(this.querySelector("#delete-profile"), "click", () => this.deleteProfile());
    this.on(this.querySelector("#profile-modal"), "click", (e) => { if (e.target.id === "profile-modal" || e.target.closest("[data-close-profile]")) this.querySelector("#profile-modal").hidden = true; });
    this.on(this.querySelector("#child-mode"), "click", () => this.openChildModal());
    this.on(this.querySelector("#child-form"), "submit", (e) => this.enterChildMode(e));
    this.on(this.querySelector("#child-modal"), "click", (e) => { if (e.target.id === "child-modal" || e.target.closest("[data-close-child]")) this.querySelector("#child-modal").hidden = true; });
    this.on(this.querySelector("#assignment-modal"), "click", (e) => { if (e.target.id === "assignment-modal" || e.target.closest("[data-close-assignment]")) this.querySelector("#assignment-modal").hidden = true; });
    this.on(this.querySelector("#assignment-all"), "change", (e) => this.toggleAllAssignments(e.target.checked));
    this.on(this.querySelector("#assignment-profiles"), "change", () => this.syncAllAssignments());
    this.on(this.querySelector("#assignment-form"), "submit", (e) => this.saveAssignments(e));
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
      const [lessons, profiles, stories, wallet] = await Promise.all([
        this.api.get("/lessons"),
        this.api.get("/parent/profiles"),
        this.api.get("/stories"),
        this.api.get("/shop/wallet").catch(() => this.wallet),
      ]);
      this.#profiles = profiles.items || [];
      this.#activeProfileId = this.#profiles[0]?.id || null;
      await this.loadProfileCatalog();
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
      this.drawProfiles(profiles.limit);
      this.render();
      await this.loadListeningHistory();
      const checkout = new URLSearchParams(location.hash.split("?")[1] || "").get("checkout");
      if (checkout === "success") msg.textContent = "Paiement reçu. Votre solde est actualisé après confirmation de Stripe.";
      if (checkout === "cancelled") msg.textContent = "Paiement annulé : aucun montant n’a été débité.";
    } catch (e) {
      msg.textContent = e.message || "Impossible de charger le catalogue.";
    }
  }

  async loadProfileCatalog() {
    if (!this.#activeProfileId) { this.selected = new Set(); return; }
    const data = await this.api.get(`/parent/profiles/${this.#activeProfileId}/catalog`);
    this.selected = new Set(data.story_ids || []);
  }

  drawProfiles(limit = 10) {
    const list = this.querySelector("#profile-list");
    list.replaceChildren();
    for (const profile of this.#profiles) {
      const card = document.createElement("div");
      card.className = `c-profile ${profile.id === this.#activeProfileId ? "is-active" : ""}`;
      const mode = profile.playback_mode === "night" ? "Mode nuit" : "Mode jour";
      card.innerHTML = `<button type="button" class="c-profile__select" data-profile="${profile.id}"><span class="c-profile__avatar">${escapeHtml(profile.display_name.slice(0, 1).toUpperCase())}</span><span><strong>${escapeHtml(profile.display_name)}</strong><small>${profile.story_count} histoire${profile.story_count > 1 ? "s" : ""} · ${mode}</small></span></button><button type="button" class="c-text-action" data-edit-profile="${profile.id}" aria-label="Modifier le profil de ${escapeHtml(profile.display_name)}">Modifier</button>`;
      list.append(card);
    }
    const add = this.querySelector("#add-profile");
    add.disabled = this.#profiles.length >= limit;
    add.textContent = add.disabled ? `Limite de ${limit} profils atteinte` : "Ajouter un enfant";
    const current = this.#profiles.find((p) => p.id === this.#activeProfileId);
    this.querySelector("#catalog-help").textContent = current ? `Ajoutez les histoires au catalogue de ${current.display_name}.` : "Ajoutez d’abord un profil enfant.";
  }

  async onProfileClick(e) {
    const edit = e.target.closest("[data-edit-profile]");
    if (edit) {
      this.openProfileModal(this.#profiles.find((profile) => profile.id === Number(edit.dataset.editProfile)));
      return;
    }
    const button = e.target.closest("[data-profile]");
    if (!button) return;
    this.#activeProfileId = Number(button.dataset.profile);
    await this.loadProfileCatalog();
    this.drawProfiles();
    this.render();
    await this.loadListeningHistory();
  }

  openProfileModal(profile = null) {
    this.#editingProfileId = profile?.id || null;
    const form = this.querySelector("#profile-form");
    form.reset();
    form.elements.display_name.value = profile?.display_name || "";
    form.elements.age_band.value = profile?.age_band || "N1";
    form.elements.playback_mode.value = profile?.playback_mode || "day";
    this.querySelector("#profile-kicker").textContent = profile ? "Profil enfant" : "Nouveau profil";
    this.querySelector("#profile-title").textContent = profile ? `Modifier ${profile.display_name}` : "Ajouter un enfant";
    this.querySelector("#profile-submit").textContent = profile ? "Enregistrer les modifications" : "Créer le profil";
    this.querySelector("#delete-profile").hidden = !profile;
    this.querySelector("#profile-modal").hidden = false;
    this.querySelector("#profile-form input")?.focus();
  }

  async createProfile(e) {
    e.preventDefault();
    const fd = new FormData(e.target);
    const err = this.querySelector("#profile-error");
    err.textContent = "";
    try {
      const body = { display_name: fd.get("display_name"), age_band: fd.get("age_band"), color: "violet", playback_mode: fd.get("playback_mode") };
      const profile = this.#editingProfileId
        ? await this.api.put(`/parent/profiles/${this.#editingProfileId}`, body)
        : await this.api.post("/parent/profiles", body);
      const index = this.#profiles.findIndex((item) => item.id === profile.id);
      if (index >= 0) this.#profiles[index] = profile;
      else this.#profiles.push(profile);
      this.#activeProfileId = profile.id;
      this.selected = new Set();
      e.target.reset();
      this.querySelector("#profile-modal").hidden = true;
      this.drawProfiles();
      this.render();
    } catch (error) { err.textContent = error.message || "Impossible de créer le profil."; }
  }

  async deleteProfile() {
    if (!this.#editingProfileId) return;
    const profile = this.#profiles.find((item) => item.id === this.#editingProfileId);
    if (!profile || !window.confirm(`Supprimer le profil de ${profile.display_name} et son historique d'écoute ?`)) return;
    const err = this.querySelector("#profile-error");
    try {
      await this.api.delete(`/parent/profiles/${profile.id}`);
      this.#profiles = this.#profiles.filter((item) => item.id !== profile.id);
      this.#activeProfileId = this.#profiles[0]?.id || null;
      await this.loadProfileCatalog();
      this.querySelector("#profile-modal").hidden = true;
      this.drawProfiles();
      this.render();
      await this.loadListeningHistory();
    } catch (error) {
      err.textContent = error.message || "Ce profil ne peut pas être supprimé.";
    }
  }

  async loadListeningHistory() {
    const target = this.querySelector("#listening-history");
    if (!target || !this.#activeProfileId) return;
    target.innerHTML = "<p class=\"c-hint\">Chargement des écoutes…</p>";
    try {
      const rows = await this.api.get(`/parent/profiles/${this.#activeProfileId}/ecoutes`);
      if (!rows.length) {
        target.innerHTML = "<p class=\"c-hint\">Aucune écoute pour le moment. Les nouvelles aventures seront proposées en premier.</p>";
        return;
      }
      target.replaceChildren();
      for (const row of rows.slice(0, 8)) {
        const story = this.allStories.find((item) => item.story_id === row.story_id);
        const item = document.createElement("div");
        item.className = "o-row c-history-row";
        const status = row.completed ? "Terminée" : `Écoutée à ${Math.round(row.completion_percent || 0)} %`;
        item.innerHTML = `<span><strong>${escapeHtml(story?.title || row.story_id)}</strong><small>${status} · ${formatListeningDate(row.started_at)}</small></span><span class="c-pill">${Math.round(row.listened_seconds || 0)} s</span>`;
        target.append(item);
      }
    } catch (error) {
      target.innerHTML = `<p class="c-error">${escapeHtml(error.message || "Impossible de charger l’historique.")}</p>`;
    }
  }

  openChildModal() {
    const profile = this.#profiles.find((p) => p.id === this.#activeProfileId);
    if (!profile) { this.openProfileModal(); return; }
    this.querySelector("#child-name").textContent = profile.display_name;
    this.querySelector('#child-form select[name="playback_mode"]').value = profile.playback_mode || "day";
    this.querySelector("#child-modal").hidden = false;
    this.querySelector("#child-form input")?.focus();
  }

  async enterChildMode(e) {
    e.preventDefault();
    const data = new FormData(e.target);
    const pin = String(data.get("pin") || "");
    const err = this.querySelector("#child-error");
    if (!/^\d{4}$/.test(pin)) { err.textContent = "Saisissez exactement 4 chiffres."; return; }
    try {
      await this.save();
      const profile = this.#profiles.find((item) => item.id === this.#activeProfileId);
      const playbackMode = data.get("playback_mode") === "night" ? "night" : "day";
      if (profile && profile.playback_mode !== playbackMode) {
        const updated = await this.api.put(`/parent/profiles/${profile.id}`, {
          display_name: profile.display_name,
          age_band: profile.age_band,
          color: profile.color || "violet",
          playback_mode: playbackMode,
        });
        Object.assign(profile, updated);
      }
      await this.api.post("/auth/enfant", { profile_id: this.#activeProfileId, pin, device_id: DeviceIdentity.get() });
      this.router.go("#/enfant");
    } catch (error) { err.textContent = error.message || "Le mode enfant n’a pas pu démarrer."; }
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
      ${owned ? `<label class="o-row"><input type="checkbox" data-id="${s.story_id}" ${checked}/> Dans le catalogue de l’enfant sélectionné</label><button class="c-text-action" type="button" data-assign="${s.story_id}">Choisir les enfants</button>` : ""}
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
    const assign = e.target.closest("[data-assign]");
    if (assign) {
      this.openAssignments(assign.dataset.assign);
      return;
    }
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
      this.drawWallet();
      this.render();
      msg.textContent = "Histoire débloquée.";
      await this.openAssignments(storyId);
    } catch (e) {
      msg.textContent = e.status === 402 ? "Solde insuffisant." : e.message;
    }
  }

  async openAssignments(storyId) {
    const modal = this.querySelector("#assignment-modal");
    const error = this.querySelector("#assignment-error");
    const list = this.querySelector("#assignment-profiles");
    const story = this.allStories.find((item) => item.story_id === storyId);
    this.#assignmentStoryId = storyId;
    error.textContent = "";
    list.innerHTML = "<p class=\"c-hint\">Chargement des profils…</p>";
    this.querySelector("#assignment-title").textContent = story ? `À qui proposer « ${story.title} » ?` : "À qui proposer cette histoire ?";
    modal.hidden = false;
    try {
      const data = await this.api.get(`/parent/stories/${encodeURIComponent(storyId)}/profiles`);
      list.replaceChildren();
      for (const profile of data.profiles || []) {
        const label = document.createElement("label");
        label.className = "o-row";
        label.innerHTML = `<input type="checkbox" name="profile_id" value="${profile.id}" ${profile.selected ? "checked" : ""}/> <span><strong>${escapeHtml(profile.display_name)}</strong><small>${ageLabel(profile.age_band)}</small></span>`;
        list.append(label);
      }
      if (!list.children.length) list.innerHTML = "<p class=\"c-hint\">Ajoutez d’abord un profil enfant.</p>";
      this.syncAllAssignments();
    } catch (err) {
      error.textContent = err.message || "Impossible de charger les profils.";
    }
  }

  toggleAllAssignments(checked) {
    this.querySelectorAll('#assignment-profiles input[name="profile_id"]').forEach((input) => { input.checked = checked; });
  }

  syncAllAssignments() {
    const boxes = [...this.querySelectorAll('#assignment-profiles input[name="profile_id"]')];
    const all = this.querySelector("#assignment-all");
    all.checked = boxes.length > 0 && boxes.every((box) => box.checked);
    all.indeterminate = boxes.some((box) => box.checked) && !all.checked;
  }

  async saveAssignments(e) {
    e.preventDefault();
    if (!this.#assignmentStoryId) return;
    const error = this.querySelector("#assignment-error");
    const profileIds = [...this.querySelectorAll('#assignment-profiles input[name="profile_id"]:checked')].map((input) => Number(input.value));
    try {
      await this.api.put(`/parent/stories/${encodeURIComponent(this.#assignmentStoryId)}/profiles`, { profile_ids: profileIds });
      if (profileIds.includes(this.#activeProfileId)) this.selected.add(this.#assignmentStoryId);
      else this.selected.delete(this.#assignmentStoryId);
      this.#profiles = (await this.api.get("/parent/profiles")).items || this.#profiles;
      this.querySelector("#assignment-modal").hidden = true;
      this.drawProfiles();
      this.render();
      this.querySelector("#msg").textContent = profileIds.length
        ? `Histoire ajoutée à ${profileIds.length} catalogue${profileIds.length > 1 ? "s" : ""} enfant.`
        : "Histoire retirée des catalogues enfants.";
    } catch (err) {
      error.textContent = err.message || "Impossible d’enregistrer ce choix.";
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
    if (!this.#activeProfileId) { msg.textContent = "Ajoutez d’abord un profil enfant."; return; }
    await this.api.put(`/parent/profiles/${this.#activeProfileId}/catalog`, { story_ids: [...this.selected] });
    const profile = this.#profiles.find((p) => p.id === this.#activeProfileId);
    if (profile) profile.story_count = this.selected.size;
    this.drawProfiles();
    msg.textContent = `Sélection enregistrée${profile ? ` pour ${profile.display_name}` : ""}.`;
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

function ageLabel(ageBand) {
  return { N1: "3–4 ans", N2: "4–5 ans", N3: "5–6 ans" }[ageBand] || "";
}

function formatListeningDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "date inconnue";
  return new Intl.DateTimeFormat("fr-FR", { dateStyle: "short", timeStyle: "short" }).format(date);
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

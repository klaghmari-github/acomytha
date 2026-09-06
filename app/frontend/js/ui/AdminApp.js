import { Component } from "../core/Component.js";
import { acmLogo } from "./acm.js";

export class AdminApp extends Component {

  async connectedCallback() {
    this.innerHTML = `
      <div class="s-shell s-shell--admin">
        <aside class="s-rail">
          <div class="c-mark">${acmLogo({ size: "sm" })}<span class="c-mark__sub">La salle de veille.</span></div>
          <nav>
            <a href="#/admin" class="is-on">Veille</a>
            <a href="#/admin/editeur">Éditeur</a>
            <a href="#/parent">Vue parent</a>
          </nav>
          <button class="c-btn c-btn--ghost" id="out">Quitter</button>
        </aside>
        <main class="s-main o-stack">
          <div class="c-title">
            <div>
              <h1>Veille</h1>
              <p>Comptes, corpus, tentatives de redistribution d’accès.</p>
            </div>
          </div>
          <div class="o-grid" id="stats"></div>
          <article class="c-card">
            <h3>Alertes appareil</h3>
            <div id="alerts"></div>
          </article>
          <article class="c-card">
            <h3>Comptes</h3>
            <div style="overflow:auto"><table class="c-table" id="users"></table></div>
          </article>
          <article class="c-card">
            <h3>Paramètres (prix, acm, aperçu)</h3>
            <form id="settings" class="o-stack"></form>
            <p class="c-hint" id="setok"></p>
          </article>
          <article class="c-card">
            <h3>Nouveau foyer</h3>
            <form id="new" class="o-stack">
              <div class="c-filters">
                <input name="email" placeholder="email parent" required />
                <input name="display_name" placeholder="nom" required />
                <input name="password" type="password" placeholder="mot de passe (≥ 8)" required minlength="8" />
                <input name="child_pin" placeholder="PIN enfant" value="2468" required />
                <button class="c-btn c-btn--gold" type="submit">Créer</button>
              </div>
              <p class="c-error" id="msg"></p>
            </form>
          </article>
        </main>
      </div>`;
    this.on(this.querySelector("#out"), "click", () => this.logout());
    this.on(this.querySelector("#new"), "submit", (e) => this.create(e));
    this.on(this.querySelector("#settings"), "submit", (e) => this.saveSettings(e));
    await this.refresh();
  }

  async refresh() {
    const [stats, alerts, users, settings] = await Promise.all([
      this.api.get("/admin/stats"),
      this.api.get("/admin/alerts"),
      this.api.get("/admin/users"),
      this.api.get("/admin/settings"),
    ]);
    const statsEl = this.querySelector("#stats");
    statsEl.innerHTML = [
      ["Histoires", stats.stories],
      ["Passages", stats.chunks],
      ["Audio prêt", stats.with_audio],
      ["Alertes ouvertes", stats.alerts_open],
    ]
      .map(
        ([k, v]) => `<article class="c-card"><div class="c-stat">${v}</div><p>${k}</p></article>`
      )
      .join("");
    const alertsEl = this.querySelector("#alerts");
    const open = alerts.filter((a) => !a.acknowledged);
    if (!open.length) {
      alertsEl.innerHTML = "<p>Aucune tentative suspecte.</p>";
    } else {
      alertsEl.innerHTML = open
        .map(
          (a) => `<div class="c-alert">
            <strong>${escapeHtml(a.email || a.display_name)}</strong>
            a tenté un 2ᵉ appareil
            <code>${escapeHtml(a.attempted_device_id.slice(0, 8))}…</code>
            (lié à <code>${escapeHtml(a.bound_device_id.slice(0, 8))}…</code>)
            — ${escapeHtml(a.created_at)}
            <button class="c-btn c-btn--ghost" data-ack="${a.id}">Vu</button>
          </div>`
        )
        .join("");
      for (const b of alertsEl.querySelectorAll("[data-ack]")) {
        this.on(b, "click", async () => {
          await this.api.post(`/admin/alerts/${b.dataset.ack}/ack`, {});
          await this.refresh();
        });
      }
    }
    const table = this.querySelector("#users");
    table.innerHTML = `<tr><th>Nom</th><th>Rôle</th><th>Email</th><th>Appareil</th><th></th></tr>`;
    for (const u of users) {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${escapeHtml(u.display_name)}</td><td>${u.role}</td>
        <td>${escapeHtml(u.email || "—")}</td>
        <td>${u.device_id ? u.device_id.slice(0, 8) + "…" : "libre"}</td>
        <td>${u.role !== "child" ? `<button class="c-btn c-btn--ghost" data-reset="${u.id}">Reset appareil</button>` : ""}</td>`;
      table.append(tr);
    }
    const form = this.querySelector("#settings");
    form.innerHTML = settings
      .map(
        (s) => `<label class="c-field"><span>${escapeHtml(s.label)}</span>
          <input name="${escapeHtml(s.key)}" value="${escapeHtml(s.value)}" /></label>`
      )
      .join("") + `<button class="c-btn" type="submit">Enregistrer les paramètres</button>`;
    for (const b of table.querySelectorAll("[data-reset]")) {
      this.on(b, "click", async () => {
        await this.api.post(`/admin/users/${b.dataset.reset}/reset-device`, {});
        await this.refresh();
      });
    }
  }

  async create(ev) {
    ev.preventDefault();
    const fd = new FormData(ev.target);
    const msg = this.querySelector("#msg");
    msg.textContent = "";
    try {
      await this.api.post("/admin/users", Object.fromEntries(fd.entries()));
      ev.target.reset();
      await this.refresh();
    } catch (e) {
      msg.textContent = e.message;
    }
  }

  async saveSettings(ev) {
    ev.preventDefault();
    const fd = new FormData(ev.target);
    const values = Object.fromEntries(fd.entries());
    await this.api.put("/admin/settings", { values });
    this.querySelector("#setok").textContent = "Paramètres enregistrés.";
  }

  async logout() {
    await this.api.post("/auth/logout", {});
    this.router.go("#/entrer");
  }
}

function escapeHtml(s) {
  return String(s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

customElements.define("acomytha-admin", AdminApp);

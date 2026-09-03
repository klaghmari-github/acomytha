import { Component } from "../core/Component.js";
import { DeviceIdentity } from "../core/DeviceIdentity.js";
import { ApiError } from "../core/ApiClient.js";

export class LoginGate extends Component {
  constructor() {
    super();
    this.api = null;
    this.router = null;
  }

  connectedCallback() {
    this.innerHTML = `
      <section class="s-gate">
        <form class="c-paper" id="login">
          <div class="c-mark">
            <strong>Sentier</strong>
            <span>Des histoires audio pour grandir sans se faire peur.</span>
          </div>
          <div class="c-field">
            <label for="email">Adresse</label>
            <input id="email" name="email" type="email" autocomplete="username" required value="parent@sentier.local" />
          </div>
          <div class="c-field">
            <label for="password">Clé d’accès</label>
            <input id="password" name="password" type="password" autocomplete="current-password" required value="sentier-parent" />
          </div>
          <p class="c-error" id="err"></p>
          <button class="c-btn c-btn--wide" type="submit">Entrer dans la forêt</button>
        </form>
      </section>`;
    this.on(this.querySelector("#login"), "submit", (ev) => this.submit(ev));
  }

  async submit(ev) {
    ev.preventDefault();
    const err = this.querySelector("#err");
    err.textContent = "";
    const email = this.querySelector("#email").value.trim().toLowerCase();
    const password = this.querySelector("#password").value;
    try {
      const me = await this.api.post("/auth/login", {
        email,
        password,
        device_id: DeviceIdentity.get(),
        device_label: DeviceIdentity.label(),
      });
      this.router.go(me.role === "admin" ? "#/admin" : "#/parent");
    } catch (e) {
      if (e instanceof ApiError && e.status === 409) {
        const d = e.detail;
        err.textContent = d?.message || "Cet accès est déjà lié à un autre appareil. L’admin a été alerté.";
        return;
      }
      err.textContent = e.message || "Connexion impossible.";
    }
  }
}

customElements.define("sentier-login", LoginGate);

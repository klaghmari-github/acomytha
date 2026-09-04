import { Component } from "../core/Component.js";
import { DeviceIdentity } from "../core/DeviceIdentity.js";
import { ApiError } from "../core/ApiClient.js";
import { acmLogo } from "./acm.js";

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
            ${acmLogo({ size: "md" })}
          </div>
          <div class="c-field">
            <label for="email">E-mail</label>
            <input id="email" name="email" type="email" autocomplete="username" required value="parent@acomytha.local" />
          </div>
          <div class="c-field">
            <label for="password">Mot de passe</label>
            <input id="password" name="password" type="password" autocomplete="current-password" required value="acomytha-parent" />
          </div>
          <p class="c-error" id="err"></p>
          <button class="c-btn c-btn--wide" type="submit">Connexion</button>
          <p class="c-hint"><a href="#/inscription">Créer un compte</a> · <a href="#/">Accueil</a></p>
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
        err.textContent = d?.message || "Ce compte est déjà ouvert sur un autre appareil. Écrivez-nous si vous avez changé de téléphone.";
        return;
      }
      err.textContent = e.message || "Connexion impossible.";
    }
  }
}

customElements.define("acomytha-login", LoginGate);

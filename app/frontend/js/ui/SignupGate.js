import { Component } from "../core/Component.js";
import { DeviceIdentity } from "../core/DeviceIdentity.js";
import { ApiError } from "../core/ApiClient.js";
import { acmLogo } from "./acm.js";

export class SignupGate extends Component {

  connectedCallback() {
    this.innerHTML = `
      <section class="s-gate">
        <form class="c-paper" id="signup">
          <div class="c-mark">
            ${acmLogo({ size: "md" })}
            <span class="c-mark__sub">Accédez gratuitement à une multitude d’histoires.</span>
          </div>
          <div class="c-field">
            <label for="email">E-mail</label>
            <input id="email" name="email" type="email" autocomplete="username" required />
          </div>
          <div class="c-data-promise" aria-label="Protection de vos données">
            <strong>Votre famille reste votre histoire.</strong>
            <p>Nous ne demandons ni nom, ni prénom — seulement un e-mail et un mot de passe. Votre adresse sera validée avant l’activation du compte.</p>
          </div>
          <div class="c-field">
            <label for="password">Mot de passe</label>
            <input id="password" name="password" type="password" autocomplete="new-password" required minlength="8" />
          </div>
          <p class="c-error" id="err"></p>
          <button class="c-btn c-btn--wide" type="submit">Créer un compte</button>
          <p class="c-hint"><a href="#/entrer">J’ai déjà un compte</a> · <a href="#/">Accueil</a></p>
        </form>
      </section>`;
    this.on(this.querySelector("#signup"), "submit", (ev) => this.submit(ev));
  }

  async submit(ev) {
    ev.preventDefault();
    const err = this.querySelector("#err");
    err.textContent = "";
    try {
      const result = await this.api.post("/auth/signup", {
        email: this.querySelector("#email").value.trim().toLowerCase(),
        password: this.querySelector("#password").value,
        device_id: DeviceIdentity.get(),
        device_label: DeviceIdentity.label(),
      });
      if (result.verification_required) {
        sessionStorage.setItem("acomytha.pending.email", result.email);
        this.router.go("#/verification-envoyee");
      }
    } catch (e) {
      err.textContent = e instanceof ApiError ? e.message : "Inscription impossible.";
    }
  }
}

customElements.define("acomytha-signup", SignupGate);

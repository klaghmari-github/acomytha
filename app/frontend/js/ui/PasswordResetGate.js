import { Component } from "../core/Component.js";
import { acmLogo } from "./acm.js";

export class PasswordResetGate extends Component {
  connectedCallback() {
    const token = new URLSearchParams(location.hash.split("?")[1] || "").get("token");
    this.innerHTML = token ? this.#resetView(token) : this.#requestView();
    this.on(this.querySelector("#reset-request"), "submit", (event) => this.#request(event));
    this.on(this.querySelector("#reset-password"), "submit", (event) => this.#reset(event, token));
  }

  #requestView() {
    return `<section class="s-gate"><form class="c-paper" id="reset-request"><div class="c-mark">${acmLogo({ size: "md" })}<span class="c-mark__sub">Retrouvez votre espace famille.</span></div><h1>Mot de passe oublié</h1><p>Indiquez votre e-mail. Si un compte correspond, nous enverrons un lien valable une heure.</p><label class="c-field">E-mail<input name="email" type="email" autocomplete="email" maxlength="180" required /></label><p class="c-error" id="reset-error"></p><button class="c-btn c-btn--wide" type="submit">Recevoir le lien</button><p class="c-hint"><a href="#/entrer">Retour à la connexion</a></p></form></section>`;
  }

  #resetView() {
    return `<section class="s-gate"><form class="c-paper" id="reset-password"><div class="c-mark">${acmLogo({ size: "md" })}<span class="c-mark__sub">Choisissez un nouvel accès.</span></div><h1>Nouveau mot de passe</h1><label class="c-field">Nouveau mot de passe<input name="password" type="password" autocomplete="new-password" minlength="8" maxlength="256" required /></label><label class="c-field">Confirmer le mot de passe<input name="confirmation" type="password" autocomplete="new-password" minlength="8" maxlength="256" required /></label><p class="c-error" id="reset-error"></p><button class="c-btn c-btn--wide" type="submit">Enregistrer</button></form></section>`;
  }

  async #request(event) {
    event.preventDefault();
    const error = this.querySelector("#reset-error");
    try {
      await this.api.post("/auth/request-password-reset", { email: new FormData(event.target).get("email") });
      event.target.innerHTML = `<h1>Consultez votre messagerie</h1><p>Si cette adresse possède un compte actif, le lien vient d’être envoyé.</p><a class="c-btn c-btn--wide" href="#/entrer">Retour à la connexion</a>`;
    } catch (err) { error.textContent = err.message || "Veuillez réessayer plus tard."; }
  }

  async #reset(event, token) {
    event.preventDefault();
    const data = new FormData(event.target);
    const password = String(data.get("password") || "");
    const error = this.querySelector("#reset-error");
    if (password !== data.get("confirmation")) { error.textContent = "Les deux mots de passe doivent être identiques."; return; }
    try {
      await this.api.post("/auth/reset-password", { token, password });
      event.target.innerHTML = `<h1>Mot de passe modifié</h1><p>Vos anciennes sessions ont été fermées. Vous pouvez maintenant vous reconnecter.</p><a class="c-btn c-btn--wide" href="#/entrer">Se connecter</a>`;
    } catch (err) { error.textContent = err.message || "Ce lien ne peut pas être utilisé."; }
  }
}

customElements.define("acomytha-password-reset", PasswordResetGate);

import { Component } from "../core/Component.js";
import { DeviceIdentity } from "../core/DeviceIdentity.js";
import { acmLogo } from "./acm.js";

export class VerificationGate extends Component {
  async connectedCallback() {
    const token = new URLSearchParams(location.hash.split("?")[1] || "").get("token");
    this.innerHTML = `
      <section class="s-gate"><div class="c-paper o-stack">
        <div class="c-mark">${acmLogo({ size: "md" })}<span class="c-mark__sub">Validation du compte parent</span></div>
        <div id="verification-content"></div>
        <p class="c-hint"><a href="#/">Retour à l'accueil</a></p>
      </div></section>`;
    if (token) await this.#activate(token);
    else this.#showSent();
  }

  #showSent() {
    const email = sessionStorage.getItem("acomytha.pending.email") || "";
    this.querySelector("#verification-content").innerHTML = `
      <h1>Consultez votre boîte e-mail</h1>
      <p>Nous avons envoyé un lien d'activation${email ? ` à <strong>${escapeHtml(email)}</strong>` : ""}. Le compte restera fermé tant que ce lien n'aura pas été ouvert.</p>
      <button class="c-btn c-btn--ghost c-btn--wide" id="resend" type="button">Renvoyer le lien</button>
      <p class="c-hint" id="resent"></p>`;
    this.on(this.querySelector("#resend"), "click", async () => {
      if (email) await this.api.post("/auth/resend-verification", { email });
      this.querySelector("#resent").textContent = "Si le compte est en attente, un nouveau lien vient d'être envoyé.";
    });
  }

  async #activate(token) {
    const box = this.querySelector("#verification-content");
    box.innerHTML = "<h1>Activation en cours…</h1><p>Nous vérifions votre lien sécurisé.</p>";
    try {
      await this.api.post("/auth/verify-email", {
        token,
        device_id: DeviceIdentity.get(),
        device_label: DeviceIdentity.label(),
      });
      sessionStorage.removeItem("acomytha.pending.email");
      box.innerHTML = "<h1>Compte activé</h1><p>Bienvenue dans AcoMytha. Votre espace famille est prêt.</p>";
      window.setTimeout(() => this.router.go("#/parent"), 700);
    } catch (error) {
      box.innerHTML = `<h1>Lien inutilisable</h1><p class="c-error">${escapeHtml(error.message || "Ce lien est invalide ou a expiré.")}</p><a class="c-btn c-btn--wide" href="#/verification-envoyee">Demander un nouveau lien</a>`;
    }
  }
}

function escapeHtml(value) {
  return String(value || "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
}

customElements.define("acomytha-verification", VerificationGate);

import { ApiClient } from "./core/ApiClient.js";
import { Router } from "./core/Router.js";
import { Session } from "./core/Session.js";
import "./ui/HomeApp.js";
import "./ui/LoginGate.js";
import "./ui/SignupGate.js";
import "./ui/ParentApp.js";
import "./ui/AdminApp.js";
import "./ui/ChildApp.js";

class AcoMythaApp {
  #root;
  #api;
  #router;
  #session;

  constructor(root) {
    if (!root) throw new Error("racine manquante");
    this.#root = root;
    this.#api = new ApiClient("/api");
    this.#session = new Session(this.#api);
    this.#router = new Router(root);
    this.#router
      .on(/^#\/?$/, () => this.#show("acomytha-home"))
      .on(/^#\/entrer\/?$/, () => this.#show("acomytha-login"))
      .on(/^#\/inscription\/?$/, () => this.#show("acomytha-signup"))
      .on(/^#\/parent\/?$/, () => this.#guard(["parent", "admin"], "acomytha-parent"))
      .on(/^#\/admin\/?$/, () => this.#guard(["admin"], "acomytha-admin"))
      .on(/^#\/enfant\/?$/, () => this.#guard(["parent", "child"], "acomytha-child"));
    this.#router.resolve();
  }

  get api() {
    return this.#api;
  }

  get router() {
    return this.#router;
  }

  get session() {
    return this.#session;
  }

  #show(tag) {
    const el = document.createElement(tag);
    el.api = this.#api;
    el.router = this.#router;
    this.#root.replaceChildren(el);
  }

  async #guard(roles, tag) {
    try {
      const me = await this.#session.refresh();
      if (!roles.includes(me.role)) {
        this.#router.go(me.role === "admin" ? "#/admin" : me.role === "child" ? "#/enfant" : "#/parent");
        return;
      }
      this.#show(tag);
    } catch {
      this.#session.clear();
      this.#router.go("#/");
    }
  }
}

window.acomytha = new AcoMythaApp(document.getElementById("app"));

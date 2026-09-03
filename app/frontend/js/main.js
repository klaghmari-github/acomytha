import { ApiClient } from "./core/ApiClient.js";
import { Router } from "./core/Router.js";
import "./ui/LoginGate.js";
import "./ui/ParentApp.js";
import "./ui/AdminApp.js";
import "./ui/ChildApp.js";

class AcoMythaApp {
  constructor(root) {
    this.root = root;
    this.api = new ApiClient("/api");
    this.router = new Router(root);
    this.router
      .on(/^#\/entrer\/?$/, () => this.show("acomytha-login"))
      .on(/^#\/parent\/?$/, () => this.guard(["parent", "admin"], "acomytha-parent"))
      .on(/^#\/admin\/?$/, () => this.guard(["admin"], "acomytha-admin"))
      .on(/^#\/enfant\/?$/, () => this.guard(["parent", "child"], "acomytha-child"));
    this.router.resolve();
  }

  show(tag) {
    const el = document.createElement(tag);
    el.api = this.api;
    el.router = this.router;
    this.root.replaceChildren(el);
  }

  async guard(roles, tag) {
    try {
      const me = await this.api.get("/auth/me");
      if (!roles.includes(me.role)) {
        this.router.go(me.role === "admin" ? "#/admin" : me.role === "child" ? "#/enfant" : "#/parent");
        return;
      }
      this.show(tag);
    } catch {
      this.router.go("#/entrer");
    }
  }
}

window.acomytha = new AcoMythaApp(document.getElementById("app"));

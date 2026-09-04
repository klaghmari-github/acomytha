export class Router {
  #outlet;
  #routes = [];

  constructor(outlet) {
    this.#outlet = outlet;
    window.addEventListener("hashchange", () => this.resolve());
  }

  get outlet() {
    return this.#outlet;
  }

  on(re, handler) {
    this.#routes.push({ re, handler });
    return this;
  }

  go(hash) {
    if (!hash.startsWith("#")) hash = "#" + hash;
    if (location.hash === hash) this.resolve();
    else location.hash = hash;
  }

  resolve() {
    const hash = location.hash || "#/";
    for (const { re, handler } of this.#routes) {
      const m = hash.match(re);
      if (m) {
        handler(m);
        return;
      }
    }
    this.go("#/");
  }
}

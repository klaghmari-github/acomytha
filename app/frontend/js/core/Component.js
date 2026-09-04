/** Superclasse HTML : un écran = une classe. État privé, API publique. */

export class Component extends HTMLElement {
  #offs = [];
  #api = null;
  #router = null;

  get api() {
    return this.#api;
  }

  set api(value) {
    this.#api = value || null;
  }

  get router() {
    return this.#router;
  }

  set router(value) {
    this.#router = value || null;
  }

  on(el, ev, fn, opts) {
    if (!el) return;
    el.addEventListener(ev, fn, opts);
    this.#offs.push(() => el.removeEventListener(ev, fn, opts));
  }

  disconnectedCallback() {
    for (const off of this.#offs) off();
    this.#offs = [];
  }

  html(strings, ...vals) {
    this.innerHTML = String.raw({ raw: strings }, ...vals);
  }
}

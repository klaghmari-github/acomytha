/** Superclasse HTML : un écran = une classe. */

export class Component extends HTMLElement {
  constructor() {
    super();
    this._offs = [];
  }

  on(el, ev, fn, opts) {
    el.addEventListener(ev, fn, opts);
    this._offs.push(() => el.removeEventListener(ev, fn, opts));
  }

  disconnectedCallback() {
    for (const off of this._offs) off();
    this._offs = [];
  }

  html(strings, ...vals) {
    this.innerHTML = String.raw({ raw: strings }, ...vals);
  }
}

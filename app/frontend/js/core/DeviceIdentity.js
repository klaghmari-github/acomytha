/** UUID d'appareil persisté. Une clé serveur ne peut lier qu'un id. */

export class DeviceIdentity {
  static #KEY = "acomytha.device_id";
  static #instance = null;
  #id;

  constructor() {
    if (DeviceIdentity.#instance) return DeviceIdentity.#instance;
    let id = localStorage.getItem(DeviceIdentity.#KEY);
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem(DeviceIdentity.#KEY, id);
    }
    this.#id = id;
    DeviceIdentity.#instance = this;
  }

  get id() {
    return this.#id;
  }

  get label() {
    const ua = navigator.userAgent;
    if (/iPhone|iPad/.test(ua)) return "iOS";
    if (/Android/.test(ua)) return "Android";
    if (/Tablet|iPad/.test(ua)) return "tablette";
    return "navigateur";
  }

  static get() {
    return new DeviceIdentity().id;
  }

  static label() {
    return new DeviceIdentity().label;
  }
}

/** UUID d'appareil persisté. Une clé serveur ne peut lier qu'un id. */

export class DeviceIdentity {
  static KEY = "acomytha.device_id";

  static get() {
    let id = localStorage.getItem(this.KEY);
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem(this.KEY, id);
    }
    return id;
  }

  static label() {
    const ua = navigator.userAgent;
    if (/iPhone|iPad/.test(ua)) return "iOS";
    if (/Android/.test(ua)) return "Android";
    if (/Tablet|iPad/.test(ua)) return "tablette";
    return "navigateur";
  }
}

/** Déchiffre un .chk en RAM et le joue. Révoque le Blob ensuite. */

export class CryptoPlayer {
  #audio = new Audio();
  #url = null;
  #keyCache = new Map();
  #endPlay = null;

  stop() {
    const end = this.#endPlay;
    this.#endPlay = null;
    this.#audio.pause();
    this.#audio.removeAttribute("src");
    if (this.#url) {
      URL.revokeObjectURL(this.#url);
      this.#url = null;
    }
    if (end) end();
  }

  async importKey(b64) {
    if (this.#keyCache.has(b64)) return this.#keyCache.get(b64);
    const raw = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
    const key = await crypto.subtle.importKey("raw", raw, "AES-GCM", false, ["decrypt"]);
    this.#keyCache.set(b64, key);
    return key;
  }

  async decrypt(chk, keyB64) {
    const u8 = new Uint8Array(chk);
    const magic = String.fromCharCode(...u8.slice(0, 5));
    if (magic !== "SNT01") throw new Error("fichier audio inattendu");
    const hlen = (u8[5] << 8) | u8[6];
    const header = u8.slice(7, 7 + hlen);
    const iv = u8.slice(7 + hlen, 19 + hlen);
    const ct = u8.slice(19 + hlen);
    const key = await this.importKey(keyB64);
    return crypto.subtle.decrypt({ name: "AES-GCM", iv, additionalData: header, tagLength: 128 }, key, ct);
  }

  async play(chk, keyB64, { maxSeconds } = {}) {
    const plain = await this.decrypt(chk, keyB64);
    this.stop();
    const blob = new Blob([plain], { type: "audio/mpeg" });
    this.#url = URL.createObjectURL(blob);
    this.#audio.src = this.#url;
    await this.#audio.play();
    await new Promise((resolve, reject) => {
      let timer = 0;
      const ok = () => {
        cleanup();
        resolve();
      };
      const fail = () => {
        cleanup();
        reject(new Error("lecture audio"));
      };
      const cleanup = () => {
        if (timer) window.clearTimeout(timer);
        this.#endPlay = null;
        this.#audio.removeEventListener("ended", ok);
        this.#audio.removeEventListener("error", fail);
      };
      this.#endPlay = ok;
      this.#audio.addEventListener("ended", ok);
      this.#audio.addEventListener("error", fail);
      if (maxSeconds > 0) {
        timer = window.setTimeout(() => {
          this.#audio.pause();
          ok();
        }, maxSeconds * 1000);
      }
    });
    if (this.#url) {
      URL.revokeObjectURL(this.#url);
      this.#url = null;
    }
  }
}

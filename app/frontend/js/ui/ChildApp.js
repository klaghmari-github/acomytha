import { Component } from "../core/Component.js";
import { CryptoPlayer } from "../core/CryptoPlayer.js";
import { StoryEngine } from "../core/StoryEngine.js";

/** Mode enfant sans écran : narration, choix vocaux et sortie par appui long + PIN. */
export class ChildApp extends Component {
  #engine = null;
  #stories = [];
  #pressTimer = 0;
  #recognition = null;
  #listeningId = null;

  async connectedCallback() {
    this.innerHTML = `
      <section class="s-child s-child--voice" aria-label="Mode enfant audio">
        <p class="u-visually-hidden" id="voice-status" aria-live="polite">Mode enfant actif.</p>
        <div class="c-child-listening" aria-hidden="true"><span></span><span></span><span></span></div>
        <div class="c-child-unlock" id="unlock" hidden>
          <form id="backpin" class="c-child-unlock__box">
            <h1>Retour au compte parent</h1><p>Saisissez le code choisi au lancement.</p>
            <input id="pinback" class="c-pin" inputmode="numeric" maxlength="4" pattern="[0-9]{4}" required />
            <button class="c-btn c-btn--wide" type="submit">Déverrouiller</button>
            <button class="c-btn c-btn--ghost c-btn--wide" id="cancel-unlock" type="button">Rester en mode enfant</button>
            <p class="c-error" id="perr"></p>
          </form>
        </div>
      </section>`;
    const screen = this.querySelector(".s-child");
    this.on(screen, "pointerdown", () => this.#startUnlockGesture());
    this.on(screen, "pointerup", () => this.#cancelUnlockGesture());
    this.on(screen, "pointercancel", () => this.#cancelUnlockGesture());
    this.on(this.querySelector("#backpin"), "submit", (event) => this.#leave(event));
    this.on(this.querySelector("#cancel-unlock"), "click", () => { this.querySelector("#unlock").hidden = true; });
    await this.#boot();
  }

  disconnectedCallback() {
    window.clearTimeout(this.#pressTimer);
    this.#recognition?.abort?.();
    this.#engine?.stop();
    window.speechSynthesis?.cancel?.();
    super.disconnectedCallback();
  }

  async #boot() {
    const me = await this.api.get("/auth/me").catch(() => null);
    if (!me || me.role !== "child") {
      this.router.go(me?.roles?.includes("parent") ? "#/parent" : "#/entrer");
      return;
    }
    this.#stories = await this.api.get("/enfant/file");
    if (!this.#stories.length) {
      await this.#speak("Papa ou maman n'a pas encore choisi d'histoire pour toi.");
      return;
    }
    await this.#chooseStory();
  }

  async #chooseStory() {
    if (!this.isConnected || !this.#stories.length) return;
    const options = this.#stories.slice(0, 3);
    await this.#speak(`Dis AcoMytha, puis choisis ton histoire. ${this.#enumerate(options.map((story) => story.title))}`);
    const heard = await this.#hear(3000);
    const selected = this.#match(heard, options) || options[0];
    if (!heard) await this.#speak(`Je choisis ${selected.title}.`);
    await this.#play(selected);
  }

  async #play(story) {
    this.#listeningId = null;
    try {
      const opened = await this.api.post(`/enfant/ecoutes/${encodeURIComponent(story.story_id)}`, {});
      this.#listeningId = opened.listening_id;
    } catch { /* La narration reste disponible si la télémétrie échoue. */ }
    const engine = new StoryEngine({
      api: this.api,
      player: new CryptoPlayer(),
      onStatus: () => this.#status(`Lecture de ${story.title}`),
      onChoice: (options) => { if (options.length) this.#answerBranch(options); },
      onDone: async ({ heard = 0, chunkIds = [], reachedEnd = false, playbackMode = "day" } = {}) => {
        if (this.#engine !== engine) return;
        if (this.#listeningId) await this.api.put(`/enfant/ecoutes/${this.#listeningId}`, { listened_seconds: heard, chunk_ids: chunkIds, reached_end: reachedEnd, playback_mode: playbackMode }).catch(() => null);
        this.#engine = null;
        this.#stories = await this.api.get("/enfant/file").catch(() => this.#stories);
        await this.#speak("L'histoire est terminée.");
        await this.#chooseStory();
      },
    });
    this.#engine = engine;
    try {
      await engine.run(story.story_id);
    } catch {
      if (this.#engine !== engine) return;
      this.#engine = null;
      await this.#speak("Cette histoire n'est pas encore prête à être écoutée.");
    }
  }

  async #answerBranch(options) {
    const visible = options.slice(0, 3);
    await this.#speak(`Que choisis-tu ? ${this.#enumerate(visible.map((option) => option.label))}`);
    const heard = await this.#hear(3000);
    (this.#match(heard, visible) || visible[0])?.pick();
  }

  #match(heard, options) {
    const answer = fold(heard);
    if (!answer) return null;
    return options.find((option) => {
      const label = fold(option.title || option.label);
      return label.includes(answer) || answer.includes(label) || label.split(" ").some((word) => word.length > 3 && answer.includes(word));
    }) || null;
  }

  #enumerate(labels) {
    return labels.map((label, index) => `${index + 1}, ${label}`).join(". ");
  }

  #speak(text) {
    this.#status(text);
    if (!("speechSynthesis" in window)) return Promise.resolve();
    return new Promise((resolve) => {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = "fr-FR";
      utterance.rate = 0.92;
      utterance.onend = resolve;
      utterance.onerror = resolve;
      speechSynthesis.cancel();
      speechSynthesis.speak(utterance);
    });
  }

  #hear(timeoutMs) {
    const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!Recognition) return new Promise((resolve) => window.setTimeout(() => resolve(""), timeoutMs));
    return new Promise((resolve) => {
      const recognition = new Recognition();
      this.#recognition = recognition;
      recognition.lang = "fr-FR";
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;
      let done = false;
      let timer = 0;
      const finish = (value = "") => {
        if (done) return;
        done = true;
        window.clearTimeout(timer);
        this.#recognition = null;
        try { recognition.abort(); } catch { /* déjà terminé */ }
        resolve(value);
      };
      recognition.onresult = (event) => finish(event.results?.[0]?.[0]?.transcript || "");
      recognition.onerror = () => finish();
      recognition.onend = () => finish();
      timer = window.setTimeout(() => finish(), timeoutMs);
      try { recognition.start(); } catch { finish(); }
    });
  }

  #status(text) {
    const status = this.querySelector("#voice-status");
    if (status) status.textContent = text;
  }

  #startUnlockGesture() {
    window.clearTimeout(this.#pressTimer);
    this.#pressTimer = window.setTimeout(() => {
      this.#engine?.stop();
      this.#recognition?.abort?.();
      window.speechSynthesis?.cancel?.();
      this.querySelector("#unlock").hidden = false;
      this.querySelector("#pinback")?.focus();
    }, 1800);
  }

  #cancelUnlockGesture() {
    window.clearTimeout(this.#pressTimer);
  }

  async #leave(event) {
    event.preventDefault();
    try {
      await this.api.post("/auth/parent", { pin: this.querySelector("#pinback").value });
      this.router.go("#/parent");
    } catch {
      this.querySelector("#perr").textContent = "Ce n'est pas le bon code.";
    }
  }
}

function fold(value) {
  return String(value || "").normalize("NFD").replace(/\p{M}/gu, "").toLowerCase().trim();
}

customElements.define("acomytha-child", ChildApp);

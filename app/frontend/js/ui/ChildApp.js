import { Component } from "../core/Component.js";
import { DeviceIdentity } from "../core/DeviceIdentity.js";
import { CryptoPlayer } from "../core/CryptoPlayer.js";
import { StoryEngine } from "../core/StoryEngine.js";
import { acmLogo } from "./acm.js";

export class ChildApp extends Component {
  #engine = null;
  #night = false;

  get engine() {
    return this.#engine;
  }
  set engine(value) {
    this.#engine = value || null;
  }
  get night() {
    return this.#night;
  }
  set night(value) {
    this.#night = Boolean(value);
  }

  async connectedCallback() {
    this.innerHTML = `
      <section class="s-child">
        <header>
          ${acmLogo({ size: "sm", href: "#/enfant" })}
          <div class="o-row">
            <button class="c-btn c-btn--ghost" id="mode">Jour</button>
            <button class="c-btn c-btn--ghost" id="back">Parent</button>
          </div>
        </header>
        <div id="gate" class="o-stack"></div>
        <div id="file" class="o-stack"></div>
        <div id="player" hidden>
          <p class="c-now" id="now"></p>
          <button class="c-btn c-btn--stop c-btn--wide" id="stop" type="button">Arrêt</button>
          <div class="o-stack" id="choices"></div>
        </div>
      </section>`;
    this.on(this.querySelector("#back"), "click", () => this.leave());
    this.on(this.querySelector("#mode"), "click", () => this.toggleNight());
    this.on(this.querySelector("#stop"), "click", () => this.stopPlay());
    await this.ensureChild();
  }

  disconnectedCallback() {
    this.stopPlay();
    super.disconnectedCallback();
  }

  async ensureChild() {
    const me = await this.api.get("/auth/me");
    if (me.role === "parent") {
      this.showPin();
      return;
    }
    if (me.role !== "child") {
      this.router.go("#/entrer");
      return;
    }
    await this.loadFile();
  }

  showPin() {
    const gate = this.querySelector("#gate");
    gate.innerHTML = `
      <p>Code pour écouter.</p>
      <form class="o-stack" id="pinform">
        <input id="pin" class="c-pin" inputmode="numeric" autocomplete="one-time-code" maxlength="4" pattern="[0-9]{4}" required />
        <button class="c-btn c-btn--gold" type="submit">C’est parti</button>
        <p class="c-error" id="perr"></p>
      </form>`;
    this.on(gate.querySelector("#pinform"), "submit", async (ev) => {
      ev.preventDefault();
      try {
        await this.api.post("/auth/enfant", {
          pin: gate.querySelector("#pin").value,
          device_id: DeviceIdentity.get(),
        });
        gate.replaceChildren();
        await this.loadFile();
      } catch (e) {
        gate.querySelector("#perr").textContent = "Ce n’est pas le bon code.";
      }
    });
  }

  async loadFile() {
    const stories = await this.api.get("/enfant/file");
    const file = this.querySelector("#file");
    file.replaceChildren();
    if (!stories.length) {
      file.innerHTML = "<p>Papa ou maman n’a pas encore choisi d’histoire.</p>";
      return;
    }
    for (const s of stories) {
      const b = document.createElement("button");
      b.className = "c-play-card";
      const min = s.duration_s ? Math.max(1, Math.round(s.duration_s / 60)) : 0;
      b.textContent = min ? `${s.title} · ${min} min` : s.title;
      this.on(b, "click", () => this.play(s));
      file.append(b);
    }
  }

  toggleNight() {
    this.night = !this.night;
    this.querySelector("#mode").textContent = this.night ? "Nuit" : "Jour";
    this.querySelector(".s-child")?.classList.toggle("is-night", this.night);
    if (this.engine) this.engine.night = this.night;
  }

  async play(story) {
    this.stopPlay();
    this.querySelector("#file").hidden = true;
    this.querySelector("#player").hidden = false;
    this.querySelector("#now").textContent = story.title;
    const choices = this.querySelector("#choices");
    this.engine = new StoryEngine({
      api: this.api,
      player: new CryptoPlayer(),
      onStatus: (n) => {
        this.querySelector("#now").textContent = n.kind === "passage_fin" ? "C’est fini." : story.title;
      },
      onChoice: (opts) => {
        choices.replaceChildren();
        for (const o of opts) {
          const b = document.createElement("button");
          b.className = "c-choice";
          b.textContent = o.label;
          this.on(b, "click", () => o.pick());
          choices.append(b);
        }
      },
      onDone: () => {
        this.querySelector("#player").hidden = true;
        this.querySelector("#file").hidden = false;
      },
    });
    this.engine.night = this.night;
    await this.engine.run(story.story_id);
  }

  stopPlay() {
    if (this.engine) {
      this.engine.stop();
      this.engine = null;
    }
    this.querySelector("#player").hidden = true;
    this.querySelector("#file").hidden = false;
  }

  async leave() {
    this.stopPlay();
    const me = await this.api.get("/auth/me").catch(() => null);
    if (!me || me.role !== "child") {
      this.router.go("#/parent");
      return;
    }
    const gate = this.querySelector("#gate");
    gate.innerHTML = `
      <p>Code pour revenir.</p>
      <form class="o-stack" id="backpin">
        <input id="pinback" class="c-pin" inputmode="numeric" maxlength="4" pattern="[0-9]{4}" required />
        <button class="c-btn" type="submit">OK</button>
        <p class="c-error" id="perr"></p>
      </form>`;
    this.querySelector("#file").hidden = true;
    this.querySelector("#player").hidden = true;
    this.on(gate.querySelector("#backpin"), "submit", async (ev) => {
      ev.preventDefault();
      try {
        await this.api.post("/auth/parent", { pin: gate.querySelector("#pinback").value });
        this.router.go("#/parent");
      } catch {
        gate.querySelector("#perr").textContent = "Ce n’est pas le bon code.";
      }
    });
  }
}

customElements.define("acomytha-child", ChildApp);

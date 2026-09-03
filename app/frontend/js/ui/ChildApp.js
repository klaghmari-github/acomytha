import { Component } from "../core/Component.js";
import { DeviceIdentity } from "../core/DeviceIdentity.js";
import { CryptoPlayer } from "../core/CryptoPlayer.js";
import { StoryEngine } from "../core/StoryEngine.js";

export class ChildApp extends Component {
  constructor() {
    super();
    this.api = null;
    this.router = null;
    this.engine = null;
    this.night = false;
  }

  async connectedCallback() {
    this.innerHTML = `
      <section class="s-child">
        <header>
          <h1>AcoMytha</h1>
          <div class="o-row">
            <button class="c-btn c-btn--ghost" id="mode">Jour</button>
            <button class="c-btn c-btn--ghost" id="back">Parent</button>
          </div>
        </header>
        <div id="gate" class="o-stack"></div>
        <div id="file" class="o-stack"></div>
        <div id="player" hidden>
          <p class="c-now" id="now"></p>
          <button class="c-orb" id="stop" type="button">Stop</button>
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
        <input id="pin" inputmode="numeric" autocomplete="one-time-code" maxlength="8" />
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
      b.textContent = s.title;
      this.on(b, "click", () => this.play(s));
      file.append(b);
    }
  }

  toggleNight() {
    this.night = !this.night;
    this.querySelector("#mode").textContent = this.night ? "Nuit" : "Jour";
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
    try {
      const me = await this.api.get("/auth/me");
      if (me.role === "child") await this.api.post("/auth/parent", {});
    } catch {
      /* ignore */
    }
    this.router.go("#/parent");
  }
}

customElements.define("acomytha-child", ChildApp);

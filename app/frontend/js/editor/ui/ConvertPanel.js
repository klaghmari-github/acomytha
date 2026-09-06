import { Component } from "../core/Component.js";

export class ConvertPanel extends Component {
  connectedCallback() {
    this.classList.add("c-sheet", "c-convert");
    this.html`
      <p class="c-sheet__kind">Rendu</p>
      <div class="actions">
        <p class="hint" data-hint>Parse une histoire, puis affecte les voix.</p>
        <button type="button" class="c-listen" data-go disabled>Convertir en audio</button>
      </div>
      <p class="status-text" data-status></p>
      <div class="c-progress" data-progress hidden>
        <div class="c-progress__track"><div class="c-progress__bar" data-bar></div></div>
        <p class="c-progress__label" data-plabel></p>
      </div>
      <div class="spinner" data-spin hidden></div>
      <div class="player hidden" data-player>
        <audio data-audio controls></audio>
        <a class="c-listen" data-dl download="histoire.wav">Télécharger le WAV</a>
      </div>
    `;
    this.on(this.querySelector("[data-go]"), "click", () => this.emit("convert-requested"));
  }

  enable(on) {
    this.querySelector("[data-go]").disabled = !on;
  }

  status(message, { busy = false, error = false, progress = null } = {}) {
    const text = this.querySelector("[data-status]");
    text.textContent = message || "";
    text.classList.toggle("error", error);
    this.querySelector("[data-spin]").hidden = !busy;
    const wrap = this.querySelector("[data-progress]");
    const bar = this.querySelector("[data-bar]");
    const label = this.querySelector("[data-plabel]");
    if (!wrap || !bar) return;
    if (busy && progress != null) {
      wrap.hidden = false;
      const value = Math.max(0, Math.min(100, Number(progress) || 0));
      bar.style.width = `${value}%`;
      bar.classList.toggle("is-active", value < 100);
      if (label) label.textContent = message ? `${message} (${value} %)` : `${value} %`;
    } else if (!busy) {
      wrap.hidden = true;
      bar.classList.remove("is-active");
    }
  }

  ready(url, title, jobId) {
    const wrap = this.querySelector("[data-player]");
    const audio = this.querySelector("[data-audio]");
    const link = this.querySelector("[data-dl]");
    audio.src = `${url}?t=${Date.now()}`;
    link.href = `${url}?t=${Date.now()}`;
    link.download = `${title || "histoire"}.wav`;
    wrap.classList.remove("hidden");
    this.status("Audio généré. Tu peux éditer les répliques dans le studio ci-dessous.");
    if (jobId) this.emit("audio-ready", { jobId, title, url });
  }

  hidePlayer() {
    this.querySelector("[data-player]").classList.add("hidden");
    this.querySelector("[data-audio]").removeAttribute("src");
  }
}

customElements.define("convert-panel", ConvertPanel);

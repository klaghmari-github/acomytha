import { Component } from "../core/Component.js?v=oop-1";
import { MicRecorder } from "../core/MicRecorder.js?v=oop-1";
import { Utils } from "../core/Utils.js?v=oop-1";

const esc = Utils.esc;
const seconds = Utils.seconds;

export class ReplicaStudio extends Component {
  #jobId = null;
  #data = null;
  #filter = "";
  #checked = new Set();
  #busy = false;
  #mic = new MicRecorder();
  #recordingIndex = 0;
  #timer = 0;

  connectedCallback() {
    this.classList.add("c-sheet", "c-edit");
    this.hidden = true;
    this.on(this, "click", (event) => this.#onClick(event));
    this.on(this, "change", (event) => {
      const box = event.target.closest("[data-check]");
      if (!box) return;
      const index = Number(box.getAttribute("data-check"));
      if (box.checked) this.#checked.add(index);
      else this.#checked.delete(index);
      this.#syncToolbar();
    });
  }

  hide() {
    this.stop();
    this.#jobId = null;
    this.#data = null;
    this.#checked = new Set();
    this.#filter = "";
    this.hidden = true;
  }

  async open(jobId) {
    this.#jobId = jobId;
    this.#checked = new Set();
    this.#filter = "";
    this.#busy = false;
    this.hidden = false;
    await this.reload();
  }

  async reload() {
    if (!this.#jobId) return;
    this.#data = await this.api.edit(this.#jobId);
    this.render();
  }

  render() {
    const data = this.#data;
    if (!data) return;
    const recording = this.#mic.recording ? this.#recordingIndex : 0;
    const rows = this.#visible()
      .map((row) => {
        const checked = this.#checked.has(row.index) ? "checked" : "";
        const rec = recording === row.index;
        return `
          <article class="c-replica${this.#checked.has(row.index) ? " is-on" : ""}${rec ? " is-rec" : ""}" data-row="${row.index}">
            <label class="c-replica__pick">
              <input type="checkbox" data-check="${row.index}" ${checked} ${this.#busy ? "disabled" : ""}>
            </label>
            <button type="button" class="c-play" data-play="${row.index}" aria-label="Écouter">▶</button>
            <div class="c-replica__body">
              <p class="c-sheet__kind">${esc(row.display_name)} · ${row.index} · ${seconds(row.duration_ms)} · ${row.source === "record" ? "micro" : "synthèse"}</p>
              <p class="c-replica__text">${esc(row.text)}</p>
            </div>
            <div class="c-replica__actions">
              <button type="button" class="c-nav__ghost ${rec ? "is-rec" : ""}" data-rec-one="${row.index}" ${this.#busy && !rec ? "disabled" : ""}>${rec ? "Arrêter" : "Enregistrer"}</button>
              <button type="button" class="c-listen" data-regen-one="${row.index}" ${this.#busy ? "disabled" : ""}>Régénérer</button>
            </div>
          </article>
        `;
      })
      .join("");
    const chips = [
      `<button type="button" class="c-chip${!this.#filter ? " is-on" : ""}" data-filter="">Tous (${(data.replicas || []).length})</button>`,
      ...(data.speakers || []).map(
        (speaker) =>
          `<button type="button" class="c-chip${this.#filter === speaker.key ? " is-on" : ""}" data-filter="${esc(speaker.key)}">${esc(speaker.display_name)} (${speaker.count})</button>`
      ),
    ].join("");
    const selected = this.#checked.size;
    const stamp = Date.now();
    this.innerHTML = `
      <p class="c-sheet__kind">Studio des répliques</p>
      <h2>${esc(data.title || "Histoire")}</h2>
      <p class="hint">Écoute une réplique, recoche celles d’un personnage, régénère-les, ou réenregistre-les une par une. L’histoire se réassemble ensuite.</p>
      <audio data-story controls src="${esc(data.audio_url)}?t=${stamp}"></audio>
      <div class="c-chips">${chips}</div>
      <div class="c-edit__toolbar">
        <button type="button" class="c-nav__ghost" data-check-visible ${this.#busy ? "disabled" : ""}>Cocher ${this.#filter ? "ce personnage" : "toutes"}</button>
        <button type="button" class="c-listen" data-regen-sel ${this.#busy || !selected ? "disabled" : ""}>Régénérer la sélection (${selected})</button>
      </div>
      <div class="c-progress" data-progress hidden>
        <div class="c-progress__track"><div class="c-progress__bar" data-bar></div></div>
        <p class="c-progress__label" data-plabel></p>
      </div>
      <p class="c-error" data-err></p>
      <div class="c-replicas">${rows || "<p class='hint'>Aucune réplique dans ce filtre.</p>"}</div>
      <audio data-clip hidden></audio>
    `;
  }

  #visible() {
    const replicas = this.#data?.replicas || [];
    if (!this.#filter) return replicas;
    return replicas.filter((row) => row.speaker === this.#filter);
  }

  #onClick(event) {
    const chip = event.target.closest("[data-filter]");
    if (chip) {
      this.#filter = chip.getAttribute("data-filter") || "";
      this.render();
      return;
    }
    if (event.target.closest("[data-check-visible]")) {
      for (const row of this.#visible()) this.#checked.add(row.index);
      this.render();
      return;
    }
    if (event.target.closest("[data-regen-sel]")) {
      this.#regen([...this.#checked]);
      return;
    }
    const play = event.target.closest("[data-play]");
    if (play) {
      this.#play(Number(play.getAttribute("data-play")));
      return;
    }
    const one = event.target.closest("[data-regen-one]");
    if (one) {
      this.#regen([Number(one.getAttribute("data-regen-one"))]);
      return;
    }
    const rec = event.target.closest("[data-rec-one]");
    if (rec) this.#toggleRecord(Number(rec.getAttribute("data-rec-one")));
  }

  #syncToolbar() {
    const button = this.querySelector("[data-regen-sel]");
    if (button) {
      button.disabled = this.#busy || this.#checked.size === 0;
      button.textContent = `Régénérer la sélection (${this.#checked.size})`;
    }
    this.querySelectorAll("[data-row]").forEach((row) => {
      const index = Number(row.getAttribute("data-row"));
      row.classList.toggle("is-on", this.#checked.has(index));
    });
  }

  #error(message) {
    const err = this.querySelector("[data-err]");
    if (err) err.textContent = message || "";
  }

  #setProgress(percent, message) {
    const wrap = this.querySelector("[data-progress]");
    const bar = this.querySelector("[data-bar]");
    const label = this.querySelector("[data-plabel]");
    if (!wrap || !bar) return;
    wrap.hidden = false;
    const value = Math.max(0, Math.min(100, Number(percent) || 0));
    bar.style.width = `${value}%`;
    bar.classList.toggle("is-active", value < 100);
    if (label) label.textContent = message ? `${message} (${value} %)` : `${value} %`;
  }

  #play(index) {
    const story = this.querySelector("[data-story]");
    if (story) story.pause();
    const clip = this.querySelector("[data-clip]");
    if (!clip || !this.#jobId) return;
    clip.src = `${this.api.replicaUrl(this.#jobId, index)}?t=${Date.now()}`;
    clip.play();
  }

  async #regen(indices) {
    const unique = [...new Set(indices.map(Number).filter((n) => n > 0))];
    if (!unique.length || this.#busy || !this.#jobId) return;
    this.#busy = true;
    this.#error("");
    this.render();
    this.#setProgress(4, "Lancement…");
    try {
      const started = await this.api.regenerateReplicas(this.#jobId, unique);
      await this.#poll(started.edit_id);
      await this.reload();
    } catch (error) {
      this.#busy = false;
      this.#error(error.message);
      this.render();
      return;
    }
    this.#busy = false;
    this.render();
  }

  async #poll(editId) {
    const data = await this.api.editWork(editId);
    this.#setProgress(data.progress || 0, data.message || "");
    if (data.status === "done") return data;
    if (data.status === "error") throw new Error(data.message || "Régénération échouée.");
    await new Promise((resolve) => setTimeout(resolve, 400));
    return this.#poll(editId);
  }

  async #toggleRecord(index) {
    if (this.#mic.recording && this.#recordingIndex === index) {
      await this.#stopRecord();
      return;
    }
    if (this.#busy) return;
    this.#error("");
    try {
      await this.#mic.start();
    } catch {
      this.#error("Micro refusé ou indisponible.");
      return;
    }
    this.#recordingIndex = index;
    const button = this.querySelector(`[data-rec-one="${index}"]`);
    if (button) {
      button.textContent = "Arrêter";
      button.classList.add("is-rec");
    }
    const row = this.querySelector(`[data-row="${index}"]`);
    if (row) row.classList.add("is-rec");
  }

  async #stopRecord() {
    const index = this.#recordingIndex;
    this.#busy = true;
    const blob = await this.#mic.stop();
    this.#recordingIndex = 0;
    if (!blob || blob.size < 800) {
      this.#busy = false;
      this.#error("Enregistrement trop court. Parle, puis appuie sur Arrêter.");
      this.render();
      return;
    }
    this.#setProgress(40, "Envoi de la réplique…");
    try {
      const file = Utils.blobFile(blob, "replique");
      this.#data = await this.api.recordReplica(this.#jobId, index, file);
      this.#busy = false;
      this.render();
    } catch (error) {
      this.#busy = false;
      this.#error(error.message);
      this.render();
    }
  }

  stop() {
    window.clearTimeout(this.#timer);
    this.#mic.reset();
    this.#recordingIndex = 0;
  }
}

customElements.define("replica-studio", ReplicaStudio);

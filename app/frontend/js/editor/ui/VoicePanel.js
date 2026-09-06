import { Component } from "../core/Component.js?v=oop-1";
import { MicRecorder } from "../core/MicRecorder.js?v=oop-1";
import { Utils } from "../core/Utils.js?v=oop-1";

/** Modal empreinte : générer (Kokoro) ou enregistrer (micro). */
export class VoicePanel extends Component {
  #member = null;
  #mode = "generate";
  #mic = new MicRecorder();
  #busy = false;
  #timer = 0;
  #startedAt = 0;
  #run = 0;
  #statusText = "";
  #progressValue = 0;
  #progressLabel = "";

  connectedCallback() {
    this.classList.add("c-modal");
    if (!this.#member) this.hidden = true;
    this.on(this, "click", (event) => {
      if (event.target === this || event.target.closest("[data-cancel]")) {
        if (this.#busy && this.#mode === "generate") return;
        this.close();
        return;
      }
      if (event.target.closest("[data-save]")) this.#saveGenerate();
      const rec = event.target.closest("[data-rec]");
      if (rec) this.#toggleRecord();
    });
  }

  open(member, mode) {
    this.stop();
    this.#member = member;
    this.#mode = mode;
    this.#busy = false;
    this.#statusText = "";
    this.#progressValue = 0;
    this.#progressLabel = "";
    this.#run += 1;
    if (this.parentElement !== document.body) document.body.append(this);
    this.hidden = false;
    this.render();
    if (mode === "generate" && !member.has_fingerprint) {
      queueMicrotask(() => this.#saveGenerate());
    }
  }

  close() {
    this.#run += 1;
    this.stop();
    this.#busy = false;
    this.hidden = true;
  }

  render() {
    const member = this.#member;
    if (!member) return;
    const recording = this.#mic.recording;
    const locked = this.#busy;
    this.innerHTML = `
      <div class="c-modal__box">
        <p class="c-sheet__kind">${this.#mode === "record" ? "Enregistrer" : "Générer"} une empreinte</p>
        <h2>${member.given_name}</h2>
        <label class="c-field-line">Genre
          <select data-gender ${locked ? "disabled" : ""}>
            <option value="female" ${member.gender === "female" ? "selected" : ""}>femme</option>
            <option value="male" ${member.gender === "male" ? "selected" : ""}>homme</option>
          </select>
        </label>
        <label class="c-field-line">Âge
          <select data-age ${locked ? "disabled" : ""}>
            <option value="child" ${member.age_group === "child" ? "selected" : ""}>enfant</option>
            <option value="adult" ${member.age_group === "adult" ? "selected" : ""}>adulte</option>
            <option value="senior" ${member.age_group === "senior" ? "selected" : ""}>senior</option>
          </select>
        </label>
        <label class="c-field-line">Tempérament
          <select data-mood ${locked ? "disabled" : ""}>
            <option value="calme">calme</option>
            <option value="naturel" selected>naturel</option>
            <option value="vif">vif</option>
          </select>
        </label>
        ${
          this.#mode === "record"
            ? `<p class="hint">Appuie sur Parler, dis quelques phrases d’une seule voix, puis Arrêter. L’empreinte est alors sauvée et affectée à ${member.given_name}.</p>
               <button type="button" class="c-listen ${recording ? "is-rec" : ""}" data-rec ${locked && !recording ? "disabled" : ""}>${recording ? "Arrêter l’enregistrement" : "Parler"}</button>
               <p class="c-rec-time" data-time>${recording ? "Enregistrement…" : ""}</p>`
            : `<p class="hint">Kokoro crée l’empreinte (genre, âge, tempérament). La barre suit le chargement, puis la synthèse.</p>`
        }
        <div class="c-progress" data-progress ${this.#progressLabel ? "" : "hidden"}>
          <div class="c-progress__track"><div class="c-progress__bar${this.#busy && this.#progressValue < 100 ? " is-active" : ""}" data-bar style="width:${this.#progressValue}%"></div></div>
          <p class="c-progress__label" data-plabel>${this.#progressLabel ? `${this.#progressLabel} (${this.#progressValue} %)` : "0 %"}</p>
        </div>
        <p class="c-error" data-err>${this.#statusText}</p>
        <div class="c-gate__actions">
          <button type="button" class="c-nav__ghost" data-cancel ${locked && this.#mode === "generate" ? "disabled" : ""}>Annuler</button>
          ${
            this.#mode === "generate"
              ? `<button type="button" class="c-listen" data-save ${locked ? "disabled" : ""}>${locked ? "Génération…" : "Générer l’empreinte"}</button>`
              : ""
          }
        </div>
      </div>
    `;
  }

  fields() {
    return {
      id: this.#member.suggested_profile_id || this.#member.profile_id || this.#member.speaker_key,
      display_name: this.#member.given_name,
      gender: this.querySelector("[data-gender]").value,
      age_group: this.querySelector("[data-age]").value,
      temperament: this.querySelector("[data-mood]").value,
      role: this.#member.role,
    };
  }

  #setProgress(percent, message) {
    this.#progressValue = Math.max(0, Math.min(100, Number(percent) || 0));
    this.#progressLabel = message || "";
    const wrap = this.querySelector("[data-progress]");
    const bar = this.querySelector("[data-bar]");
    const label = this.querySelector("[data-plabel]");
    if (!wrap || !bar || !label) return;
    wrap.hidden = false;
    bar.style.width = `${this.#progressValue}%`;
    bar.classList.toggle("is-active", this.#busy && this.#progressValue < 100);
    label.textContent = this.#progressLabel
      ? `${this.#progressLabel} (${this.#progressValue} %)`
      : `${this.#progressValue} %`;
  }

  #error(message) {
    this.#statusText = message || "";
    const err = this.querySelector("[data-err]");
    if (err) err.textContent = this.#statusText;
  }

  async #saveGenerate() {
    if (this.#busy || this.#mode !== "generate") return;
    const run = this.#run;
    const member = this.#member;
    this.#busy = true;
    this.#error("");
    this.render();
    this.#setProgress(4, "Lancement…");
    try {
      const started = await this.api.generate(this.fields());
      const done = await this.#pollVoice(started.job_id, run);
      this.emit("voice-saved", { member, profile: done.profile });
      if (run === this.#run) this.close();
    } catch (error) {
      if (run !== this.#run) return;
      this.#busy = false;
      this.#error(error.message);
      this.render();
    }
  }

  async #pollVoice(jobId, run) {
    const data = await this.api.voiceJob(jobId);
    if (run === this.#run) this.#setProgress(data.progress || 0, data.message || "");
    if (data.status === "done") {
      if (!data.profile) throw new Error("Empreinte absente de la réponse.");
      return data;
    }
    if (data.status === "error") throw new Error(data.message || "Travail vocal échoué.");
    await new Promise((resolve) => setTimeout(resolve, 400));
    return this.#pollVoice(jobId, run);
  }

  async #toggleRecord() {
    if (this.#mode !== "record") return;
    if (this.#mic.recording) {
      await this.#stopAndSave();
      return;
    }
    if (this.#busy) return;
    this.#error("");
    this.#setProgress(5, "Demande d’accès au micro…");
    try {
      await this.#mic.start();
    } catch (error) {
      this.#setProgress(0, "");
      this.#error("Micro refusé ou indisponible. Autorise le micro, puis réessaie.");
      return;
    }
    this.#startedAt = Date.now();
    const rec = this.querySelector("[data-rec]");
    if (rec) {
      rec.textContent = "Arrêter l’enregistrement";
      rec.classList.add("is-rec");
    }
    this.#tick();
  }

  #tick() {
    const time = this.querySelector("[data-time]");
    if (!time || !this.#mic.recording) return;
    const seconds = Math.floor((Date.now() - this.#startedAt) / 1000);
    time.textContent = `Enregistrement… ${seconds}s — appuie sur Arrêter pour sauver.`;
    this.#setProgress(Math.min(90, 8 + seconds * 2), "Parle, puis appuie sur Arrêter");
    this.#timer = window.setTimeout(() => this.#tick(), 250);
  }

  async #stopAndSave() {
    const run = this.#run;
    const member = this.#member;
    this.#busy = true;
    this.#setProgress(20, "Arrêt de l’enregistrement…");
    const payload = this.fields();
    const blob = await this.#mic.stop();
    if (run !== this.#run) return;
    if (!blob || blob.size < 800) {
      this.#busy = false;
      this.#error("Enregistrement trop court. Appuie sur Parler, parle, puis Arrêter.");
      this.render();
      return;
    }
    this.#setProgress(40, "Envoi au catalogue…");
    this.render();
    this.#setProgress(40, "Envoi au catalogue…");
    try {
      const file = Utils.blobFile(blob, "voix");
      const started = await this.api.record(payload, file);
      const done = started.job_id && !started.id ? await this.#pollVoice(started.job_id, run) : { profile: started };
      if (!done.profile) throw new Error("Empreinte absente de la réponse.");
      this.#setProgress(100, "Empreinte enregistrée.");
      this.emit("voice-saved", { member, profile: done.profile });
      if (run === this.#run) this.close();
    } catch (error) {
      if (run !== this.#run) return;
      this.#busy = false;
      this.#error(error.message);
      this.render();
    }
  }

  stop() {
    window.clearTimeout(this.#timer);
    this.#mic.reset();
  }
}

customElements.define("voice-panel", VoicePanel);

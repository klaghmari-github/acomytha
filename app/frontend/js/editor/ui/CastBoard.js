import { Component } from "../core/Component.js";

export class CastBoard extends Component {
  #preview = null;
  #assignments = {};

  get assignments() {
    return { ...this.#assignments };
  }

  get preview() {
    return this.#preview;
  }

  show(preview) {
    this.#preview = preview;
    this.#assignments = {};
    for (const member of preview.cast || []) {
      this.#assignments[member.speaker_key] = member.profile_id || member.suggested_profile_id;
    }
    this.hidden = false;
    this.render();
  }

  assign(speakerKey, profileId) {
    this.#assignments[speakerKey] = profileId;
    const member = (this.#preview?.cast || []).find((item) => item.speaker_key === speakerKey);
    if (member) {
      member.profile_id = profileId;
      member.has_fingerprint = true;
    }
    this.render();
  }

  connectedCallback() {
    this.classList.add("c-sheet");
    this.hidden = true;
    this.on(this, "click", (event) => {
      const record = event.target.closest("[data-record]");
      const generate = event.target.closest("[data-generate]");
      if (record) this.#open(record.getAttribute("data-record"), "record");
      if (generate) this.#open(generate.getAttribute("data-generate"), "generate");
    });
  }

  render() {
    const preview = this.#preview;
    if (!preview) return;
    const rows = (preview.cast || [])
      .map((member) => {
        const missing = !member.has_fingerprint;
        return `
          <article class="c-cast ${missing ? "is-missing" : ""}" data-key="${member.speaker_key}">
            <p class="c-sheet__kind">${member.role} · ${member.gender} · ${member.age_group}</p>
            <h3>${member.given_name}</h3>
            <p class="c-cast__status">${missing ? "Empreinte vocale manquante" : "Empreinte prête"}</p>
            <div class="c-cast__actions">
              <button type="button" class="c-nav__ghost" data-record="${member.speaker_key}">Enregistrer</button>
              <button type="button" class="c-listen" data-generate="${member.speaker_key}">Générer</button>
            </div>
          </article>
        `;
      })
      .join("");
    this.innerHTML = `
      <p class="c-sheet__kind">Personnages</p>
      <h2>${preview.title || "Histoire"}</h2>
      <dl class="stats">
        <div><dt>Format</dt><dd>${preview.format}</dd></div>
        <div><dt>Répliques</dt><dd>${preview.segments}</dd></div>
        <div><dt>Locuteurs</dt><dd>${(preview.cast || []).length}</dd></div>
      </dl>
      <p class="excerpt">${preview.excerpt ? `« ${preview.excerpt} »` : ""}</p>
      <div class="c-cast-grid">${rows}</div>
    `;
  }

  #open(speakerKey, mode) {
    const member = (this.#preview?.cast || []).find((item) => item.speaker_key === speakerKey);
    if (!member) return;
    this.emit("voice-needed", { member, mode });
  }
}

customElements.define("cast-board", CastBoard);

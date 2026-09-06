import { Component } from "../core/Component.js";

export class DropZone extends Component {
  #file = null;
  #storyId = null;

  get file() {
    return this.#file;
  }

  get storyId() {
    return this.#storyId;
  }

  connectedCallback() {
    this.classList.add("c-sheet", "c-drop");
    this.html`
      <p class="c-sheet__kind">Histoire</p>
      <input id="file" type="file" accept=".json,application/json,.xlsx">
      <label class="c-drop__label" for="story">JSON dans stories/json/</label>
      <select id="story" data-story>
        <option value="">Chargement…</option>
      </select>
      <div class="drop-visual">
        <p><button type="button" class="c-listen" data-load disabled>Charger ce JSON</button></p>
        <p class="hint">Le dossier <code>stories/json/</code> est listé ci-dessus. Autre fichier : <button type="button" class="c-link" data-browse>parcourir</button></p>
      </div>
    `;
    const input = this.querySelector("#file");
    const select = this.querySelector("[data-story]");
    const load = this.querySelector("[data-load]");
    this.on(this.querySelector("[data-browse]"), "click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      input.click();
    });
    this.on(load, "click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      if (select.value) this.#takeCatalog(select.value);
    });
    this.on(select, "change", () => {
      load.disabled = !select.value;
      if (select.value) this.#takeCatalog(select.value);
    });
    this.on(select, "dblclick", () => {
      if (select.value) this.#takeCatalog(select.value);
    });
    this.on(input, "change", () => {
      if (input.files[0]) this.#takeFile(input.files[0]);
    });
    ["dragenter", "dragover"].forEach((name) => {
      this.on(this, name, (event) => {
        event.preventDefault();
        this.classList.add("is-drag");
      });
    });
    ["dragleave", "drop"].forEach((name) => {
      this.on(this, name, (event) => {
        event.preventDefault();
        this.classList.remove("is-drag");
      });
    });
    this.on(this, "drop", (event) => {
      const file = event.dataTransfer.files[0];
      if (file) this.#takeFile(file);
    });
  }

  loadCatalog() {
    return this.#fillCatalog();
  }

  openCatalog(storyId) {
    const select = this.querySelector("[data-story]");
    if (!select || !storyId) return;
    const found = [...select.options].some((option) => option.value === storyId);
    if (!found) return;
    select.value = storyId;
    const load = this.querySelector("[data-load]");
    if (load) load.disabled = false;
    return this.#takeCatalog(storyId);
  }

  async #fillCatalog() {
    const select = this.querySelector("[data-story]");
    const load = this.querySelector("[data-load]");
    try {
      const data = await this.api.stories();
      const stories = data.stories || [];
      select.replaceChildren();
      if (!stories.length) {
        select.append(this.#option("", "Aucun JSON dans stories/json/"));
        load.disabled = true;
        return;
      }
      select.append(this.#option("", "Choisir une histoire…"));
      for (const story of stories) {
        const label = story.title && story.title !== story.story_id
          ? `${story.title} (${story.story_id})`
          : story.story_id;
        select.append(this.#option(story.story_id, label));
      }
      load.disabled = true;
    } catch (err) {
      select.replaceChildren(this.#option("", err.message || "Catalogue JSON inaccessible"));
      load.disabled = true;
    }
  }

  #option(value, label) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    return option;
  }

  async #takeCatalog(storyId) {
    this.#storyId = storyId;
    this.#file = null;
    this.emit("file-chosen", { storyId });
    try {
      const preview = await this.api.parseCatalog(storyId);
      this.emit("story-parsed", { storyId, preview });
    } catch (err) {
      this.emit("studio-error", { message: err.message });
    }
  }

  async #takeFile(file) {
    this.#file = file;
    this.#storyId = null;
    this.emit("file-chosen", { file });
    try {
      const preview = await this.api.parse(file);
      this.emit("story-parsed", { file, preview });
    } catch (err) {
      this.emit("studio-error", { message: err.message });
    }
  }
}

customElements.define("drop-zone", DropZone);

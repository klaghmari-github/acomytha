import { Component } from "../core/Component.js?v=oop-1";
import { Utils } from "../core/Utils.js?v=oop-1";

const esc = Utils.esc;

export class TroupeBoard extends Component {
  #data = null;
  #view = "characters";
  #filter = "all";
  #openStories = new Set();

  connectedCallback() {
    this.classList.add("c-sheet", "c-troupe");
    this.on(this, "click", (event) => this.#onClick(event));
  }

  async load() {
    if (!this.api) return;
    this.#data = await this.api.roster();
    this.render();
  }

  markReady(profileId) {
    const item = (this.#data?.items || []).find((row) => row.id === profileId);
    if (item) item.has_fingerprint = true;
    for (const story of this.#data?.by_story || []) {
      for (const person of story.characters || []) {
        if (person.id === profileId) person.has_fingerprint = true;
      }
      story.missing = (story.characters || []).filter((person) => !person.has_fingerprint).length;
    }
    if (this.#data) {
      this.#data.missing = (this.#data.items || []).filter((row) => !row.has_fingerprint).length;
    }
    this.render();
  }

  render() {
    const data = this.#data;
    if (!data) {
      this.innerHTML = `<p class="c-sheet__kind">Catalogue</p><h2>Troupe</h2><p class="hint">Chargement…</p>`;
      return;
    }
    const byCharacters = this.#view === "characters";
    this.innerHTML = `
      <p class="c-sheet__kind">Catalogue</p>
      <h2>${byCharacters ? "Vue par personnages" : "Vue par histoires"}</h2>
      <p class="hint">${
        byCharacters
          ? "Chaque personnage du catalogue JSON, avec les histoires où il apparaît."
          : "Chaque histoire, avec les personnages qui y parlent."
      } S’il manque une empreinte : enregistrer ou générer.</p>
      <div class="c-view-switch" role="tablist">
        <button type="button" class="c-chip${byCharacters ? " is-on" : ""}" data-view="characters" role="tab" aria-selected="${byCharacters}">Par personnages (${data.characters})</button>
        <button type="button" class="c-chip${!byCharacters ? " is-on" : ""}" data-view="stories" role="tab" aria-selected="${!byCharacters}">Par histoires (${data.stories})</button>
      </div>
      <dl class="stats">
        <div><dt>Personnages</dt><dd>${data.characters}</dd></div>
        <div><dt>Empreintes manquantes</dt><dd>${data.missing}</dd></div>
        <div><dt>Histoires</dt><dd>${data.stories}</dd></div>
      </dl>
      ${byCharacters ? this.#characterFilters(data) : this.#storyFilters(data)}
      ${byCharacters ? this.#characterGrid() : this.#storyList()}
    `;
  }

  #characterFilters(data) {
    return `
      <div class="c-chips">
        <button type="button" class="c-chip${this.#filter === "missing" ? " is-on" : ""}" data-filter="missing">Manquantes (${data.missing})</button>
        <button type="button" class="c-chip${this.#filter === "ready" ? " is-on" : ""}" data-filter="ready">Prêtes (${data.characters - data.missing})</button>
        <button type="button" class="c-chip${this.#filter === "all" ? " is-on" : ""}" data-filter="all">Tous (${data.characters})</button>
      </div>
    `;
  }

  #storyFilters(data) {
    const incomplete = (data.by_story || []).filter((story) => story.missing > 0).length;
    return `
      <div class="c-chips">
        <button type="button" class="c-chip${this.#filter === "missing" ? " is-on" : ""}" data-filter="missing">Empreinte manquante (${incomplete})</button>
        <button type="button" class="c-chip${this.#filter === "ready" ? " is-on" : ""}" data-filter="ready">Complètes (${data.stories - incomplete})</button>
        <button type="button" class="c-chip${this.#filter === "all" ? " is-on" : ""}" data-filter="all">Toutes (${data.stories})</button>
      </div>
    `;
  }

  #characterGrid() {
    const items = this.#visibleCharacters();
    const rows = items.map((item) => this.#characterCard(item)).join("");
    return `<div class="c-cast-grid">${rows || "<p class='hint'>Aucun personnage dans ce filtre.</p>"}</div>`;
  }

  #characterCard(item) {
    const missing = !item.has_fingerprint;
    const stories = item.stories || [];
    const expanded = this.#openStories.has(item.id);
    const shown = expanded ? stories : stories.slice(0, 4);
    const rest = stories.length - shown.length;
    const storyChips = shown
      .map(
        (story) =>
          `<button type="button" class="c-story-chip" data-open-story="${esc(story.story_id)}" title="${esc(story.story_id)}">${esc(story.title)}</button>`
      )
      .join("");
    const more = rest
      ? `<button type="button" class="c-story-chip" data-expand="${esc(item.id)}">+${rest} autres</button>`
      : "";
    return `
      <article class="c-cast ${missing ? "is-missing" : ""}" data-id="${esc(item.id)}">
        <p class="c-sheet__kind">${esc(item.role)} · ${esc(item.gender)} · ${esc(item.age_group)}</p>
        <h3>${esc(item.display_name)}</h3>
        <p class="c-cast__status">${missing ? "Empreinte vocale manquante" : "Empreinte prête"}</p>
        <p class="c-troupe__count">${item.story_count} histoire${item.story_count > 1 ? "s" : ""}</p>
        <div class="c-troupe__stories">${storyChips}${more}</div>
        ${this.#voiceActions(item)}
      </article>
    `;
  }

  #storyList() {
    const stories = this.#visibleStories();
    const rows = stories
      .map((story) => {
        const people = (story.characters || [])
          .map((person) => {
            const missing = !person.has_fingerprint;
            return `
              <div class="c-story-person ${missing ? "is-missing" : ""}">
                <div>
                  <strong>${esc(person.display_name)}</strong>
                  <p class="c-cast__status">${missing ? "Empreinte manquante" : "Empreinte prête"} · ${esc(person.role)}</p>
                </div>
                ${this.#voiceActions(person)}
              </div>
            `;
          })
          .join("");
        return `
          <article class="c-story-card ${story.missing ? "is-missing" : ""}">
            <div class="c-story-card__head">
              <div>
                <p class="c-sheet__kind">${esc(story.story_id)}</p>
                <h3>${esc(story.title)}</h3>
                <p class="c-troupe__count">${story.character_count} personnage${story.character_count > 1 ? "s" : ""} · ${story.missing} empreinte${story.missing > 1 ? "s" : ""} manquante${story.missing > 1 ? "s" : ""}</p>
              </div>
              <button type="button" class="c-listen" data-open-story="${esc(story.story_id)}">Ouvrir</button>
            </div>
            <div class="c-story-people">${people}</div>
          </article>
        `;
      })
      .join("");
    return `<div class="c-story-list">${rows || "<p class='hint'>Aucune histoire dans ce filtre.</p>"}</div>`;
  }

  #voiceActions(item) {
    const missing = !item.has_fingerprint;
    return `
      <div class="c-cast__actions">
        <button type="button" class="c-nav__ghost" data-record="${esc(item.id)}">Enregistrer</button>
        <button type="button" class="c-listen" data-generate="${esc(item.id)}">${missing ? "Générer" : "Regénérer"}</button>
      </div>
    `;
  }

  #visibleCharacters() {
    const items = this.#data?.items || [];
    if (this.#filter === "missing") return items.filter((item) => !item.has_fingerprint);
    if (this.#filter === "ready") return items.filter((item) => item.has_fingerprint);
    return items;
  }

  #visibleStories() {
    const stories = this.#data?.by_story || [];
    if (this.#filter === "missing") return stories.filter((story) => story.missing > 0);
    if (this.#filter === "ready") return stories.filter((story) => !story.missing);
    return stories;
  }

  #onClick(event) {
    const view = event.target.closest("[data-view]");
    if (view) {
      this.#view = view.getAttribute("data-view") || "characters";
      this.#filter = "all";
      this.render();
      return;
    }
    const chip = event.target.closest("[data-filter]");
    if (chip) {
      this.#filter = chip.getAttribute("data-filter") || "all";
      this.render();
      return;
    }
    const expand = event.target.closest("[data-expand]");
    if (expand) {
      this.#openStories.add(expand.getAttribute("data-expand"));
      this.render();
      return;
    }
    const story = event.target.closest("[data-open-story]");
    if (story) {
      this.emit("story-open", { storyId: story.getAttribute("data-open-story") });
      return;
    }
    const record = event.target.closest("[data-record]");
    const generate = event.target.closest("[data-generate]");
    const id = (record || generate)?.getAttribute(record ? "data-record" : "data-generate");
    if (!id) return;
    const item =
      (this.#data?.items || []).find((row) => row.id === id) ||
      (this.#data?.by_story || []).flatMap((row) => row.characters || []).find((row) => row.id === id);
    if (!item) return;
    this.emit("voice-needed", {
      mode: record ? "record" : "generate",
      member: {
        speaker_key: item.id,
        given_name: item.display_name,
        gender: item.gender,
        age_group: item.age_group,
        role: item.role,
        profile_id: item.has_fingerprint ? item.id : null,
        has_fingerprint: item.has_fingerprint,
        suggested_profile_id: item.id,
      },
    });
  }
}

customElements.define("troupe-board", TroupeBoard);

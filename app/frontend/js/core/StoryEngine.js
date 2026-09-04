/** Moteur jour / nuit : enchaîne les chunks, 3 s, prefetch N+1. */

export class StoryEngine {
  #api;
  #player;
  #onChoice;
  #onStatus;
  #onDone;
  #maxSeconds = 0;
  #preview = false;
  #night = false;
  #abort = false;
  #userStop = false;
  #replaced = false;
  #prefetch = new Map();
  #remain = 0;
  #heard = 0;
  #graph = null;
  #key = "";

  constructor({ api, player, onChoice, onStatus, onDone, maxSeconds = 0, preview = false }) {
    this.#api = api;
    this.#player = player;
    this.#onChoice = onChoice;
    this.#onStatus = onStatus;
    this.#onDone = onDone;
    this.maxSeconds = maxSeconds;
    this.preview = preview;
  }

  get night() {
    return this.#night;
  }

  set night(value) {
    this.#night = Boolean(value);
  }

  get preview() {
    return this.#preview;
  }

  set preview(value) {
    this.#preview = value === "parent" ? "parent" : Boolean(value);
  }

  get maxSeconds() {
    return this.#maxSeconds;
  }

  set maxSeconds(value) {
    const n = Number(value) || 0;
    this.#maxSeconds = n > 0 ? n : 0;
    this.#remain = this.#maxSeconds;
  }

  get heard() {
    return this.#heard;
  }

  stop({ replaced = false } = {}) {
    this.#abort = true;
    this.#userStop = true;
    if (replaced) this.#replaced = true;
    this.#player.stop();
  }

  async run(storyId) {
    this.#abort = false;
    this.#userStop = false;
    this.#replaced = false;
    this.#heard = 0;
    this.#prefetch.clear();
    this.#remain = this.#maxSeconds > 0 ? this.#maxSeconds : 0;
    const graph = await this.#api.get(this.#graphPath(storyId));
    this.#graph = graph;
    this.#key = graph.key;
    let id = graph.root;
    while (id && !this.#abort) {
      const node = graph.chunks[id];
      if (!node) break;
      this.#onStatus?.(node);
      const policy = node.night_policy || "play";
      if (this.#night && policy === "skip") {
        id = node.default_next;
        continue;
      }
      if (node.kind === "transition_question") {
        if (this.#night && policy === "auto_default") {
          await this.#play(storyId, id);
          id = node.default_next || node.options?.[0]?.next;
          continue;
        }
        await this.#play(storyId, id);
        const wait = node.wait_ms || graph.wait_default_ms || 3000;
        id = await this.#ask(node, wait);
        continue;
      }
      if (node.kind === "passage_question") {
        if (this.#night && policy === "skip") {
          id = node.default_next;
          continue;
        }
        await this.#play(storyId, id);
        const wait = node.wait_ms || graph.wait_default_ms || 3000;
        await this.#sleep(wait);
        id = node.default_next;
        continue;
      }
      await this.#play(storyId, id);
      if (node.kind === "passage_fin" || !node.default_next) {
        break;
      }
      id = node.default_next;
    }
    this.#onChoice?.([]);
    if (this.#replaced) return;
    this.#onDone?.({ userStop: !!this.#userStop, heard: this.#heard || 0 });
  }

  async #play(storyId, chunkId) {
    const next = this.#graph.chunks[chunkId]?.default_next;
    if (next) this.#warm(storyId, next);
    const buf = await this.#load(storyId, chunkId);
    if (this.#abort) return;
    if (!buf) {
      if (this.#preview) throw new Error("aperçu audio absent");
      return;
    }
    const cap = this.#remain > 0 ? this.#remain : 0;
    const t0 = performance.now();
    await this.#player.play(buf, this.#key, { maxSeconds: cap });
    const used = (performance.now() - t0) / 1000;
    this.#heard += used;
    if (this.#maxSeconds > 0) {
      this.#remain = Math.max(0, this.#remain - used);
      if (this.#remain <= 0.05) this.#abort = true;
    }
  }

  async #load(storyId, chunkId) {
    if (this.#prefetch.has(chunkId)) return this.#prefetch.get(chunkId);
    const p = this.#api.blob(this.#chunkPath(storyId, chunkId));
    this.#prefetch.set(chunkId, p);
    return p;
  }

  #warm(storyId, chunkId) {
    if (!this.#prefetch.has(chunkId)) {
      this.#prefetch.set(chunkId, this.#api.blob(this.#chunkPath(storyId, chunkId)).catch(() => null));
    }
  }

  #graphPath(storyId) {
    const id = encodeURIComponent(storyId);
    if (this.#preview === "parent") return `/play/${id}/preview/graph`;
    if (this.#preview) return `/public/preview/${id}/graph`;
    return `/play/${id}/graph`;
  }

  #chunkPath(storyId, chunkId) {
    const id = encodeURIComponent(storyId);
    const ck = encodeURIComponent(chunkId);
    if (this.#preview === "parent") return `/play/${id}/preview/chunk/${ck}`;
    if (this.#preview) return `/public/preview/${id}/chunk/${ck}`;
    return `/play/${id}/chunk/${ck}`;
  }

  #ask(node, waitMs) {
    return new Promise((resolve) => {
      let done = false;
      const finish = (next) => {
        if (done) return;
        done = true;
        this.#onChoice?.([]);
        resolve(next);
      };
      this.#onChoice?.(
        node.options.map((o) => ({
          ...o,
          pick: () => finish(o.next),
        }))
      );
      window.setTimeout(() => finish(node.default_next || node.options[0]?.next), waitMs);
    });
  }

  #sleep(ms) {
    return new Promise((r) => window.setTimeout(r, ms));
  }
}

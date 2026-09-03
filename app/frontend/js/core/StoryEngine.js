/** Moteur jour / nuit : enchaîne les chunks, 3 s, prefetch N+1. */

export class StoryEngine {
  constructor({ api, player, onChoice, onStatus, onDone }) {
    this.api = api;
    this.player = player;
    this.onChoice = onChoice;
    this.onStatus = onStatus;
    this.onDone = onDone;
    this.night = false;
    this._abort = false;
    this._prefetch = new Map();
  }

  stop() {
    this._abort = true;
    this.player.stop();
  }

  async run(storyId) {
    this._abort = false;
    this._prefetch.clear();
    const graph = await this.api.get(`/play/${encodeURIComponent(storyId)}/graph`);
    this.graph = graph;
    this.key = graph.key;
    let id = graph.root;
    while (id && !this._abort) {
      const node = graph.chunks[id];
      if (!node) break;
      this.onStatus?.(node);
      const policy = node.night_policy || "play";
      if (this.night && policy === "skip") {
        id = node.default_next;
        continue;
      }
      if (node.kind === "transition_question") {
        if (this.night || policy === "auto_default") {
          await this._play(storyId, id);
          id = node.default_next || node.options?.[0]?.next;
          continue;
        }
        await this._play(storyId, id);
        const wait = node.wait_ms || graph.wait_default_ms || 3000;
        id = await this._ask(node, wait);
        continue;
      }
      if (node.kind === "passage_question") {
        if (this.night && policy === "skip") {
          id = node.default_next;
          continue;
        }
        await this._play(storyId, id);
        const wait = node.wait_ms || graph.wait_default_ms || 3000;
        await this._sleep(wait);
        id = node.default_next;
        continue;
      }
      await this._play(storyId, id);
      if (node.kind === "passage_fin" || !node.default_next) {
        break;
      }
      id = node.default_next;
    }
    this.onChoice?.([]);
    this.onDone?.();
  }

  async _play(storyId, chunkId) {
    const next = this.graph.chunks[chunkId]?.default_next;
    if (next) this._warm(storyId, next);
    const buf = await this._load(storyId, chunkId);
    if (this._abort) return;
    try {
      await this.player.play(buf, this.key);
    } catch {
      /* silence : on enchaîne plutôt que de bloquer l'enfant */
    }
  }

  async _load(storyId, chunkId) {
    if (this._prefetch.has(chunkId)) return this._prefetch.get(chunkId);
    const p = this.api.blob(`/play/${encodeURIComponent(storyId)}/chunk/${encodeURIComponent(chunkId)}`);
    this._prefetch.set(chunkId, p);
    return p;
  }

  _warm(storyId, chunkId) {
    if (!this._prefetch.has(chunkId)) {
      this._prefetch.set(
        chunkId,
        this.api.blob(`/play/${encodeURIComponent(storyId)}/chunk/${encodeURIComponent(chunkId)}`).catch(() => null)
      );
    }
  }

  _ask(node, waitMs) {
    return new Promise((resolve) => {
      let done = false;
      const finish = (next) => {
        if (done) return;
        done = true;
        this.onChoice?.([]);
        resolve(next);
      };
      this.onChoice?.(
        node.options.map((o) => ({
          ...o,
          pick: () => finish(o.next),
        }))
      );
      window.setTimeout(() => finish(node.default_next || node.options[0]?.next), waitMs);
    });
  }

  _sleep(ms) {
    return new Promise((r) => window.setTimeout(r, ms));
  }
}

/** Moteur jour / nuit : enchaîne les chunks, 3 s, prefetch N+1. */

export class StoryEngine {
  constructor({ api, player, onChoice, onStatus, onDone, maxSeconds = 0, preview = false }) {
    this.api = api;
    this.player = player;
    this.onChoice = onChoice;
    this.onStatus = onStatus;
    this.onDone = onDone;
    this.maxSeconds = maxSeconds;
    this.preview = preview; // false | true (visiteur) | "parent"
    this.night = false;
    this._abort = false;
    this._userStop = false;
    this._prefetch = new Map();
    this._remain = maxSeconds > 0 ? maxSeconds : 0;
    this._t0 = 0;
  }

  stop() {
    this._abort = true;
    this._userStop = true;
    this.player.stop();
  }

  async run(storyId) {
    this._abort = false;
    this._userStop = false;
    this._prefetch.clear();
    this._remain = this.maxSeconds > 0 ? this.maxSeconds : 0;
    const graph = await this.api.get(this._graphPath(storyId));
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
        // auto_default = nuit seulement. Le jour, l’enfant choisit (F-PLY-001).
        if (this.night && policy === "auto_default") {
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
    this.onDone?.({ userStop: !!this._userStop });
  }

  async _play(storyId, chunkId) {
    const next = this.graph.chunks[chunkId]?.default_next;
    if (next) this._warm(storyId, next);
    const buf = await this._load(storyId, chunkId);
    if (this._abort) return;
    const cap = this._remain > 0 ? this._remain : 0;
    const t0 = performance.now();
    try {
      await this.player.play(buf, this.key, { maxSeconds: cap });
      if (this.maxSeconds > 0) {
        const used = (performance.now() - t0) / 1000;
        this._remain = Math.max(0, (this._remain || this.maxSeconds) - used);
        if (this._remain <= 0.05) this._abort = true;
      }
    } catch {
      /* silence : on enchaîne plutôt que de bloquer l'enfant */
    }
  }

  async _load(storyId, chunkId) {
    if (this._prefetch.has(chunkId)) return this._prefetch.get(chunkId);
    const p = this.api.blob(this._chunkPath(storyId, chunkId));
    this._prefetch.set(chunkId, p);
    return p;
  }

  _warm(storyId, chunkId) {
    if (!this._prefetch.has(chunkId)) {
      this._prefetch.set(
        chunkId,
        this.api.blob(this._chunkPath(storyId, chunkId)).catch(() => null)
      );
    }
  }

  _graphPath(storyId) {
    const id = encodeURIComponent(storyId);
    if (this.preview === "parent") return `/play/${id}/preview/graph`;
    if (this.preview) return `/public/preview/${id}/graph`;
    return `/play/${id}/graph`;
  }

  _chunkPath(storyId, chunkId) {
    const id = encodeURIComponent(storyId);
    const ck = encodeURIComponent(chunkId);
    if (this.preview === "parent") return `/play/${id}/preview/chunk/${ck}`;
    if (this.preview) return `/public/preview/${id}/chunk/${ck}`;
    return `/play/${id}/chunk/${ck}`;
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

/** Client TTS : mêmes méthodes que le studio AkoMythaTTS, préfixe /editor. */

export class EditorApi {
  constructor(api) {
    this.api = api;
  }

  async #call(promise) {
    try {
      return await promise;
    } catch (err) {
      const detail = err.detail;
      const message = typeof detail === "string" ? detail : detail?.message || err.message;
      throw new Error(message || "Requête éditeur impossible.");
    }
  }

  stories() {
    return this.#call(this.api.get("/editor/stories"));
  }

  roster() {
    return this.#call(this.api.get("/editor/roster"));
  }

  parseCatalog(storyId) {
    return this.#call(this.api.post("/editor/parse", { story_id: storyId }));
  }

  parse(file) {
    const body = new FormData();
    body.append("file", file);
    return this.#call(this.api.postForm("/editor/parse", body));
  }

  generate(payload) {
    return this.#call(this.api.post("/editor/voices/generate", payload));
  }

  voiceJob(id) {
    return this.#call(this.api.get(`/editor/voices/jobs/${id}`));
  }

  record(fields, file) {
    const body = new FormData();
    Object.entries(fields).forEach(([key, value]) => body.append(key, value));
    body.append("file", file, file.name || "voix.webm");
    return this.#call(this.api.postForm("/editor/voices/record", body));
  }

  convert(file, assignments) {
    const body = new FormData();
    body.append("file", file);
    body.append("assignments", JSON.stringify(assignments));
    return this.#call(this.api.postForm("/editor/convert", body));
  }

  convertCatalog(storyId, assignments) {
    return this.#call(this.api.post("/editor/convert", { story_id: storyId, assignments }));
  }

  convertExcel() {
    return this.#call(this.api.post("/editor/excel", {}));
  }

  job(id) {
    return this.#call(this.api.get(`/editor/jobs/${id}`));
  }

  audioUrl(id) {
    return `/api/editor/jobs/${id}/audio`;
  }

  edit(jobId) {
    return this.#call(this.api.get(`/editor/jobs/${jobId}/edit`));
  }

  replicaUrl(jobId, index) {
    return `/api/editor/jobs/${jobId}/replicas/${index}/audio`;
  }

  regenerateReplicas(jobId, indices) {
    return this.#call(this.api.post(`/editor/jobs/${jobId}/replicas/regenerate`, { indices }));
  }

  recordReplica(jobId, index, file) {
    const body = new FormData();
    body.append("file", file, file.name || "replique.webm");
    return this.#call(this.api.postForm(`/editor/jobs/${jobId}/replicas/${index}/record`, body));
  }

  editWork(id) {
    return this.#call(this.api.get(`/editor/edits/${id}`));
  }
}

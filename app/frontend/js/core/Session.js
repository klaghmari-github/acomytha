/** Session courante : rôle, foyer, rafraîchissement. */

export class Session {
  #api;
  #me = null;

  constructor(api) {
    this.#api = api;
  }

  get me() {
    return this.#me;
  }

  get role() {
    return this.#me?.role || "guest";
  }

  get signedIn() {
    return Boolean(this.#me);
  }

  async refresh() {
    this.#me = await this.#api.get("/auth/me");
    return this.#me;
  }

  async tryRefresh() {
    try {
      return await this.refresh();
    } catch {
      this.#me = null;
      return null;
    }
  }

  clear() {
    this.#me = null;
  }
}

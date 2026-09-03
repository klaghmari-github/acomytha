export class ApiError extends Error {
  constructor(status, detail) {
    super(typeof detail === "string" ? detail : detail?.message || "erreur");
    this.status = status;
    this.detail = detail;
  }
}

export class ApiClient {
  constructor(base = "/api") {
    this.base = base;
  }

  async request(path, { method = "GET", body, raw = false } = {}) {
    const headers = {};
    let payload;
    if (body !== undefined) {
      headers["Content-Type"] = "application/json";
      payload = JSON.stringify(body);
    }
    const res = await fetch(this.base + path, {
      method,
      headers,
      body: payload,
      credentials: "include",
    });
    if (raw) {
      if (!res.ok) throw new ApiError(res.status, await res.text());
      return res.arrayBuffer();
    }
    const text = await res.text();
    const data = text ? JSON.parse(text) : null;
    if (!res.ok) throw new ApiError(res.status, data?.detail ?? data);
    return data;
  }

  get(path) {
    return this.request(path);
  }

  post(path, body) {
    return this.request(path, { method: "POST", body });
  }

  put(path, body) {
    return this.request(path, { method: "PUT", body });
  }

  blob(path) {
    return this.request(path, { raw: true });
  }
}

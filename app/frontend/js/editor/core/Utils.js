/** Helpers transverses du studio (échappement, attente, micro MIME). */

export class Utils {
  static esc(value) {
    return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    })[ch]);
  }

  static seconds(ms) {
    return `${(Number(ms || 0) / 1000).toFixed(1)} s`;
  }

  static sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  static recorderMime() {
    return ["audio/webm;codecs=opus", "audio/webm", "audio/mp4"].find((type) => MediaRecorder.isTypeSupported(type));
  }

  static blobFile(blob, stem) {
    const ext = (blob.type || "").includes("mp4") ? "m4a" : "webm";
    return new File([blob], `${stem}.${ext}`, { type: blob.type || "audio/webm" });
  }
}

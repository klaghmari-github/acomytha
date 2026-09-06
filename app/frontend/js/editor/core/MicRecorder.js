import { Utils } from "./Utils.js?v=oop-1";

/** Enregistrement micro : Parler / Arrêter, un Blob à la fin. */

export class MicRecorder {
  #recorder = null;
  #stream = null;
  #chunks = [];

  get recording() {
    return Boolean(this.#recorder && this.#recorder.state === "recording");
  }

  async start() {
    this.reset();
    this.#stream = await navigator.mediaDevices.getUserMedia({
      audio: { echoCancellation: true, noiseSuppression: true },
    });
    const mime = Utils.recorderMime();
    this.#chunks = [];
    this.#recorder = mime ? new MediaRecorder(this.#stream, { mimeType: mime }) : new MediaRecorder(this.#stream);
    this.#recorder.ondataavailable = (event) => {
      if (event.data && event.data.size) this.#chunks.push(event.data);
    };
    this.#recorder.start(200);
  }

  async stop() {
    const blob = await this.#stopBlob();
    this.reset();
    return blob;
  }

  reset() {
    if (this.#recorder && this.#recorder.state === "recording") {
      try {
        this.#recorder.stop();
      } catch {
        /* ignore */
      }
    }
    if (this.#stream) this.#stream.getTracks().forEach((track) => track.stop());
    this.#stream = null;
    this.#recorder = null;
  }

  #stopBlob() {
    return new Promise((resolve) => {
      const recorder = this.#recorder;
      const finish = () => {
        const type = recorder?.mimeType || "audio/webm";
        resolve(this.#chunks.length ? new Blob(this.#chunks, { type }) : null);
      };
      if (!recorder || recorder.state === "inactive") {
        finish();
        return;
      }
      const watchdog = window.setTimeout(finish, 4000);
      recorder.onstop = () => {
        window.clearTimeout(watchdog);
        finish();
      };
      try {
        recorder.requestData();
      } catch {
        /* ignore */
      }
      recorder.stop();
    });
  }
}

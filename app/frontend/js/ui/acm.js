/** Symbole acm : une définition SVG (#acm-mark dans index.html), partout réutilisée. */

export function formatAcm(n) {
  const x = Number(n);
  if (!Number.isFinite(x)) return "0";
  const s = Number.isInteger(x) ? String(x) : String(x);
  const [int, frac] = s.split(".");
  const grouped = int.replace(/\B(?=(\d{3})+(?!\d))/g, "\u202f");
  return frac ? `${grouped},${frac}` : grouped;
}

export function acmIcon(extraClass = "") {
  const cls = ["acm", extraClass].filter(Boolean).join(" ");
  return `<svg class="${cls}" viewBox="0 0 100 112" aria-hidden="true" focusable="false"><use href="#acm-mark"/></svg>`;
}

export function acmAmount(n, { unit = false, size = "" } = {}) {
  const cls = ["acm-amount", size ? `acm-amount--${size}` : ""].filter(Boolean).join(" ");
  const unitHtml = unit
    ? `<span class="unit" aria-hidden="true">acm</span>`
    : "";
  return `<span class="${cls}">${formatAcm(n)}${acmIcon()}<span class="sr-only"> acm</span>${unitHtml}</span>`;
}

export function acmLogo({ size = "sm", word = true, href = "#/" } = {}) {
  const icon = acmIcon(size === "xl" ? "acm--xl" : size === "lg" ? "acm--lg" : size === "md" ? "acm--md" : "acm--sm");
  if (!word) return `<span class="c-logo">${icon}</span>`;
  if (!href) {
    return `<span class="c-logo">${icon}<strong>AcoMytha</strong></span>`;
  }
  return `<a class="c-logo" href="${href}" aria-label="AcoMytha">${icon}<strong>AcoMytha</strong></a>`;
}

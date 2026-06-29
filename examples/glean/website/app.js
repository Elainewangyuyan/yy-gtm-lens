const CONFIG = window.REPORT_CONFIG || {};
const KEY = `${CONFIG.slug || "ai-company"}-owner-views`;

function esc(value) {
  return String(value).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  })[c]);
}

function ownerViews() {
  try {
    return [...(CONFIG.ownerViews || []), ...JSON.parse(localStorage.getItem(KEY) || "[]")];
  } catch {
    return CONFIG.ownerViews || [];
  }
}

function renderOwnerViews() {
  const mount = document.querySelector("[data-owner-views]");
  if (!mount) return;
  const fixed = (CONFIG.ownerViews || []).length;
  mount.innerHTML = ownerViews().map((view, index) => `
    <article class="opinion-card">
      ${index >= fixed ? `<button class="no-print" data-delete="${index - fixed}">删除</button>` : ""}
      <small>我的观点 · ${esc(view.date || "持续更新")}</small>
      <h4>${esc(view.title || "")}</h4>
      <p>${esc(view.body || "")}</p>
      <div>${(view.tags || []).map(tag => `<span>${esc(tag)}</span>`).join("")}</div>
    </article>`).join("");
  mount.querySelectorAll("[data-delete]").forEach(button => {
    button.addEventListener("click", () => {
      const custom = ownerViews().slice(fixed);
      custom.splice(Number(button.dataset.delete), 1);
      localStorage.setItem(KEY, JSON.stringify(custom));
      renderOwnerViews();
    });
  });
}

function setupOwnerViewForm() {
  const form = document.querySelector("[data-opinion-form]");
  if (!form) return;
  form.addEventListener("submit", event => {
    event.preventDefault();
    const data = new FormData(form);
    const fixed = (CONFIG.ownerViews || []).length;
    const custom = ownerViews().slice(fixed);
    custom.push({
      date: new Date().toISOString().slice(0, 10),
      title: String(data.get("title") || "").trim(),
      body: String(data.get("body") || "").trim(),
      tags: String(data.get("tags") || "").split(/[,，]/).map(x => x.trim()).filter(Boolean)
    });
    localStorage.setItem(KEY, JSON.stringify(custom));
    form.reset();
    renderOwnerViews();
  });
}

function renderComments() {
  const mount = document.querySelector("[data-comments]");
  if (!mount) return;
  const comments = CONFIG.comments || {};
  const configured = comments.enabled && comments.repo && comments.repo_id
    && comments.category && comments.category_id;
  if (!configured) {
    mount.innerHTML = "<h3>评论互动区</h3><p>发布到 GitHub 后可配置 Giscus；评论不会改动正式研究正文。</p>";
    return;
  }
  const script = document.createElement("script");
  script.src = "https://giscus.app/client.js";
  script.async = true;
  script.crossOrigin = "anonymous";
  const attrs = {
    repo: comments.repo,
    "repo-id": comments.repo_id,
    category: comments.category,
    "category-id": comments.category_id,
    mapping: comments.mapping || "pathname",
    strict: "0",
    "reactions-enabled": "1",
    "emit-metadata": "0",
    "input-position": "top",
    theme: "light",
    lang: comments.lang || "zh-CN",
    loading: "lazy"
  };
  Object.entries(attrs).forEach(([key, value]) => script.setAttribute(`data-${key}`, value));
  mount.appendChild(script);
}

function setupActions() {
  document.querySelectorAll("[data-print]").forEach(button =>
    button.addEventListener("click", () => window.print()));
  const share = document.querySelector("[data-share]");
  if (share) share.addEventListener("click", async () => {
    const original = share.textContent;
    try {
      await navigator.clipboard.writeText(location.href);
      share.textContent = "链接已复制";
    } catch {
      share.textContent = "请复制地址栏";
    }
    setTimeout(() => { share.textContent = original; }, 1500);
  });
}

function setupProgress() {
  const progress = document.querySelector("[data-progress]");
  if (!progress) return;
  const update = () => {
    const root = document.documentElement;
    const ratio = root.scrollTop / Math.max(1, root.scrollHeight - root.clientHeight);
    progress.style.transform = `scaleX(${Math.max(0, Math.min(1, ratio))})`;
  };
  addEventListener("scroll", update, { passive: true });
  update();
}

function setupNavigation() {
  const pages = [...document.querySelectorAll(".page[id]")];
  const links = [...document.querySelectorAll(".nav a[href^='#']")];
  if (!("IntersectionObserver" in window)) return;
  const observer = new IntersectionObserver(entries => {
    const active = entries.filter(entry => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!active) return;
    links.forEach(link => link.classList.toggle(
      "active", active.target.id.startsWith(link.getAttribute("href").slice(1))
    ));
  }, { rootMargin: "-20% 0px -65% 0px", threshold: [0.05, 0.2, 0.5] });
  pages.forEach(page => observer.observe(page));
}

async function setupPrintPreview() {
  if (new URLSearchParams(location.search).get("print-preview") !== "1") return;
  const response = await fetch("./print.css", { cache: "no-store" });
  const css = await response.text();
  const start = css.indexOf("@media print {");
  const end = css.lastIndexOf("}");
  if (start < 0 || end <= start) return;
  const style = document.createElement("style");
  style.dataset.printPreview = "true";
  style.textContent = css.slice(start + "@media print {".length, end);
  document.head.appendChild(style);
  document.documentElement.dataset.printPreview = "ready";
}

setupPrintPreview();
renderOwnerViews();
setupOwnerViewForm();
renderComments();
setupActions();
setupProgress();
setupNavigation();

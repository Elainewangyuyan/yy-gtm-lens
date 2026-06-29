const pageConfig = window.KIMI_PAGE_CONFIG || {};
const storageKey = "kimi-research-owner-views-v2";

function getOwnerViews() {
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || "[]");
    return [...(pageConfig.ownerViews || []), ...saved];
  } catch {
    return pageConfig.ownerViews || [];
  }
}

function saveCustomViews(views) {
  localStorage.setItem(storageKey, JSON.stringify(views));
}

function renderOwnerViews() {
  const mount = document.querySelector("[data-owner-views]");
  if (!mount) return;
  const seedCount = (pageConfig.ownerViews || []).length;
  mount.innerHTML = getOwnerViews().map((view, index) => `
    <article class="opinion-card">
      ${index >= seedCount ? `<button class="opinion-delete no-print" type="button" data-delete-view="${index - seedCount}">删除</button>` : ""}
      <small>${view.kicker || "我的观点"} · ${view.date || "持续更新"}</small>
      <h4>${escapeHtml(view.title || "")}</h4>
      <p>${escapeHtml(view.body || "")}</p>
      <div class="opinion-meta">${(view.tags || []).map(tag => `<span>${escapeHtml(tag)}</span>`).join("")}</div>
    </article>
  `).join("");

  mount.querySelectorAll("[data-delete-view]").forEach(button => {
    button.addEventListener("click", () => {
      const custom = getOwnerViews().slice(seedCount);
      custom.splice(Number(button.dataset.deleteView), 1);
      saveCustomViews(custom);
      renderOwnerViews();
    });
  });
}

function setupOpinionForm() {
  const form = document.querySelector("[data-opinion-form]");
  if (!form) return;
  form.addEventListener("submit", event => {
    event.preventDefault();
    const data = new FormData(form);
    const custom = getOwnerViews().slice((pageConfig.ownerViews || []).length);
    custom.push({
      kicker: "我的观点",
      date: new Date().toISOString().slice(0, 10),
      title: String(data.get("title") || "").trim(),
      body: String(data.get("body") || "").trim(),
      tags: String(data.get("tags") || "").split(/[,，]/).map(tag => tag.trim()).filter(Boolean)
    });
    saveCustomViews(custom);
    form.reset();
    renderOwnerViews();
  });
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  })[char]);
}

function renderComments() {
  const mount = document.querySelector("[data-comments]");
  if (!mount) return;
  const config = pageConfig.comments || {};
  const configured = config.enabled && config.repo && config.repoId && config.category && config.categoryId;
  if (!configured) {
    mount.innerHTML = `
      <div class="comments-placeholder">
        <div>
          <p class="eyebrow" style="color:var(--violet)">PUBLIC DISCUSSION</p>
          <h3>补充证据、提出反例，也分享你的增长判断</h3>
          <p>发布到 GitHub 后可接入 Giscus。评论保存在仓库 Discussions 中；“我的观点”新增功能则保存在当前浏览器，避免访客改动正式正文。</p>
        </div>
        <span class="status-pill">等待 GitHub 仓库配置</span>
      </div>`;
    return;
  }
  const script = document.createElement("script");
  script.src = "https://giscus.app/client.js";
  script.async = true;
  script.crossOrigin = "anonymous";
  for (const [key, value] of Object.entries({
    repo: config.repo, "repo-id": config.repoId, category: config.category,
    "category-id": config.categoryId, mapping: config.mapping || "pathname",
    strict: "0", "reactions-enabled": "1", "emit-metadata": "0",
    "input-position": "top", theme: "light", lang: config.lang || "zh-CN", loading: "lazy"
  })) script.setAttribute(`data-${key}`, value);
  mount.appendChild(script);
}

function setupProgress() {
  const progress = document.querySelector("[data-progress]");
  if (!progress) return;
  const update = () => {
    const root = document.documentElement;
    const ratio = root.scrollHeight > root.clientHeight
      ? root.scrollTop / (root.scrollHeight - root.clientHeight) : 0;
    progress.style.transform = `scaleX(${Math.max(0, Math.min(1, ratio))})`;
  };
  document.addEventListener("scroll", update, { passive: true });
  update();
}

function setupNav() {
  const sections = [...document.querySelectorAll(".report-page[id]")];
  const links = [...document.querySelectorAll(".side-nav a[href^='#']")];
  if (!("IntersectionObserver" in window)) return;
  const observer = new IntersectionObserver(entries => {
    const active = entries.filter(entry => entry.isIntersecting)
      .sort((a,b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!active) return;
    links.forEach(link => link.classList.toggle("is-active",
      active.target.id.startsWith(link.getAttribute("href").slice(1))));
  }, { rootMargin: "-20% 0px -65% 0px", threshold: [0.05,.2,.5] });
  sections.forEach(section => observer.observe(section));
}

function setupActions() {
  document.querySelectorAll("[data-print]").forEach(button =>
    button.addEventListener("click", () => window.print()));
  const share = document.querySelector("[data-share]");
  if (share) share.addEventListener("click", async () => {
    const label = share.textContent;
    try {
      await navigator.clipboard.writeText(location.href);
      share.textContent = "链接已复制";
    } catch {
      share.textContent = "请复制地址栏";
    }
    setTimeout(() => share.textContent = label, 1600);
  });
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
setupOpinionForm();
renderComments();
setupProgress();
setupNav();
setupActions();

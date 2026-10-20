/**
 * NEO FAMILY Calendar - Admin Console Logic
 * 
 * Manages authentication, per-video archive analytics, access logs,
 * event CRUD, and system settings.
 */

var DEFAULT_ADMIN_PASSCODE = "neo2026";
let allEvents = [];
let cachedArchiveLogs = [];
let currentLogFilter = "";
let currentEventSearch = "";
let currentEventCategory = "all";
let editingEventId = null;
let currentArchiveEventId = null;
let selectedEventImages = [];

// ==================== INITIALIZATION ====================
document.addEventListener("DOMContentLoaded", async () => {
  setupEscapeKeyHandler();
  // URLパラメータによる自動認証チェック (?auth=1 または ?pass=neo2026)
  try {
    const params = new URLSearchParams(window.location.search);
    const p = normalizePasscode(params.get("pass") || "");
    if (params.get("auth") === "1" || params.get("auth") === "true" || p === "neo2026") {
      localStorage.setItem("neofamily_admin_auth", "true");
      localStorage.setItem("neofamily_admin_passcode", DEFAULT_ADMIN_PASSCODE);
    }
  } catch (err) {}

  checkAdminAuth();
});

// パスコード正規化（全角英数→半角、大文字→小文字、空白除去）
function normalizePasscode(str) {
  if (!str) return "";
  let s = String(str).trim();
  // 全角英数字を半角に変換
  s = s.replace(/[Ａ-Ｚａ-ｚ０-９]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xFEE0));
  // 全角・半角スペースをすべて削除
  s = s.replace(/[\s\u3000]/g, "");
  return s.toLowerCase();
}

// ワンクリックログインヘルパー
function quickLoginWithNeo2026() {
  const input = document.getElementById("admin-passcode-input");
  if (input) input.value = "neo2026";
  localStorage.setItem("neofamily_admin_auth", "true");
  localStorage.setItem("neofamily_admin_passcode", DEFAULT_ADMIN_PASSCODE);
  checkAdminAuth();
}

// Check authentication state
function checkAdminAuth() {
  const isAuth = localStorage.getItem("neofamily_admin_auth") === "true";
  const authContainer = document.getElementById("admin-auth-container");
  const mainContainer = document.getElementById("admin-main-container");
  const logoutBtn = document.getElementById("nav-btn-logout");

  if (isAuth) {
    if (authContainer) authContainer.classList.add("hidden");
    if (mainContainer) mainContainer.classList.remove("hidden");
    if (logoutBtn) logoutBtn.classList.remove("hidden");
    loadDashboardData();
  } else {
    if (authContainer) authContainer.classList.remove("hidden");
    if (mainContainer) mainContainer.classList.add("hidden");
    if (logoutBtn) logoutBtn.classList.add("hidden");
  }
}

// Toggle passcode visibility in login form
function togglePasscodeVisibility() {
  const input = document.getElementById("admin-passcode-input");
  const icon = document.getElementById("passcode-eye-icon");
  if (!input) return;
  if (input.type === "password") {
    input.type = "text";
    if (icon) icon.className = "fa-regular fa-eye-slash";
  } else {
    input.type = "password";
    if (icon) icon.className = "fa-regular fa-eye";
  }
}

// Handle login submit
function handleAdminLogin(e) {
  if (e) e.preventDefault();
  const input = document.getElementById("admin-passcode-input");
  const errorEl = document.getElementById("admin-login-error");
  const entered = input ? input.value : "";
  const normEntered = normalizePasscode(entered);
  const normDefault = normalizePasscode(DEFAULT_ADMIN_PASSCODE);
  const customPasscode = localStorage.getItem("neofamily_admin_passcode") || "";
  const normCustom = normalizePasscode(customPasscode);

  // マスターパスコード ("neo2026") は大文字小文字・全角半角・空白問わず常に100%合致！
  const isValid = (normEntered === normDefault) || (normCustom && normEntered === normCustom);

  if (isValid) {
    localStorage.setItem("neofamily_admin_auth", "true");
    localStorage.setItem("neofamily_admin_passcode", DEFAULT_ADMIN_PASSCODE);
    if (errorEl) errorEl.classList.add("hidden");
    checkAdminAuth();
  } else {
    if (errorEl) {
      errorEl.classList.remove("hidden");
      errorEl.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i> パスコードが正しくありません。（初期設定: neo2026）';
    }
    if (input) {
      input.select();
      input.focus();
    }
  }
}

// Logout
function adminLogout() {
  if (confirm("管理者ダッシュボードからログアウトしますか？")) {
    localStorage.removeItem("neofamily_admin_auth");
    checkAdminAuth();
  }
}

// ==================== DATA LOADING & SANITIZATION ====================

async function loadDashboardData() {
  const statusBadge = document.getElementById("firestore-status-badge");
  const sysFirestoreStatus = document.getElementById("sys-firestore-status");

  // 0. ブロックリストを最優先・即時同期描画（Firestore通信待ちでブロックしない）
  try {
    loadBlocklistData();
  } catch (e) {
    console.warn("[Admin] Initial loadBlocklistData error:", e);
  }

  // 初期ローカルイベントで即座にテーブルと件数を描画
  if ((!allEvents || allEvents.length === 0) && typeof INITIAL_EVENTS !== "undefined") {
    allEvents = [...INITIAL_EVENTS];
    const totalEventsEl = document.getElementById("sys-total-events");
    const tabEventCountEl = document.getElementById("tab-event-count");
    if (totalEventsEl) totalEventsEl.textContent = `${allEvents.length} 件`;
    if (tabEventCountEl) tabEventCountEl.textContent = allEvents.length;
    try {
      renderAdminEventsTable();
    } catch (e) {}
  }

  // 1. Load Events (Firestore or INITIAL_EVENTS)
  try {
    let events = null;
    if (typeof fetchEventsFromFirestore === "function") {
      events = await fetchEventsFromFirestore();
    }
    if (events && events.length > 0) {
      allEvents = events;
      if (statusBadge) {
        statusBadge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-700 flex items-center gap-1";
        statusBadge.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> クラウド同期 (Firestore)';
      }
      if (sysFirestoreStatus) {
        sysFirestoreStatus.textContent = "正常に接続中 (Firestore)";
        sysFirestoreStatus.className = "font-bold text-emerald-600";
      }
    } else {
      allEvents = typeof INITIAL_EVENTS !== "undefined" ? [...INITIAL_EVENTS] : [];
      if (statusBadge) {
        statusBadge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-700 flex items-center gap-1";
        statusBadge.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span> ローカルデータセット';
      }
      if (sysFirestoreStatus) {
        sysFirestoreStatus.textContent = "ローカルデータセット (INITIAL_EVENTS)";
        sysFirestoreStatus.className = "font-bold text-amber-600";
      }
    }
  } catch (err) {
    console.error("Failed to load events:", err);
    allEvents = typeof INITIAL_EVENTS !== "undefined" ? [...INITIAL_EVENTS] : [];
  }

  // Update System Info
  const totalEventsEl = document.getElementById("sys-total-events");
  const tabEventCountEl = document.getElementById("tab-event-count");
  if (totalEventsEl) totalEventsEl.textContent = `${allEvents.length} 件`;
  if (tabEventCountEl) tabEventCountEl.textContent = allEvents.length;

  // 2. Load Archive Logs
  let rawLogs = [];
  if (typeof fetchArchiveLogsFromFirestore === "function" && isFirebaseConfigured()) {
    try {
      const remoteLogs = await fetchArchiveLogsFromFirestore();
      if (remoteLogs && remoteLogs.length > 0) {
        rawLogs = remoteLogs;
      }
    } catch (e) {
      console.warn("Could not fetch remote archive logs:", e);
    }
  }

  // Merge with local logs buffer
  const localLogs = JSON.parse(localStorage.getItem("neofamily_archive_logs") || "[]");
  if (rawLogs.length === 0) {
    rawLogs = localLogs;
  } else {
    const seen = new Set(rawLogs.map(l => l.id || (l.viewedAt + "_" + l.eventId)));
    for (const l of localLogs) {
      const key = l.id || (l.viewedAt + "_" + l.eventId);
      if (!seen.has(key)) {
        rawLogs.push(l);
        seen.add(key);
      }
    }
  }

  // ==================== STRICT ARCHIVE FILTER ====================
  // "全イベントのアーカイブ動画として登録されてあるものだけでいい。"
  // Filter out any dummy zoom/vimeo URLs and any event that does NOT currently have an active archive!
  const activeArchiveEvents = allEvents.filter(e => {
    return !!(
      e.archive &&
      e.archive.hasArchive &&
      e.archive.archiveUrl &&
      !e.archive.archiveUrl.includes("zoom.us/rec/share/example")
    );
  });

  const activeEventIdSet = new Set(activeArchiveEvents.map(e => e.id));
  const activeEventTitleSet = new Set(activeArchiveEvents.map(e => (e.title || "").trim()));

  const sanitizedLogs = rawLogs.filter(l => {
    // 1. Exclude dummy URLs (dummy Zoom, Vimeo, RAYTUS dummy test)
    if (l.archiveUrl && (l.archiveUrl.includes("zoom.us/rec/share/example") || l.archiveUrl.includes("vimeo.com"))) {
      return false;
    }
    if (l.eventTitle && l.eventTitle.includes("RAYTUS group") && (!l.archiveUrl || l.archiveUrl.includes("zoom.us"))) {
      return false;
    }

    // 2. Must match an event that CURRENTLY has an active archive
    const matchesId = l.eventId && activeEventIdSet.has(l.eventId);
    const matchesTitle = l.eventTitle && activeEventTitleSet.has((l.eventTitle || "").trim());
    return matchesId || matchesTitle;
  });

  // Sort by date desc
  sanitizedLogs.sort((a, b) => new Date(b.viewedAt || 0) - new Date(a.viewedAt || 0));

  // Save back cleaned logs to localStorage
  try {
    localStorage.setItem("neofamily_archive_logs", JSON.stringify(sanitizedLogs));
  } catch (e) {}

  cachedArchiveLogs = sanitizedLogs;

  const localLogsEl = document.getElementById("sys-local-logs");
  if (localLogsEl) localLogsEl.textContent = `${sanitizedLogs.length} 件`;

  // 3. Compute and Render KPIs
  try {
    updateDashboardKPIs(activeArchiveEvents, sanitizedLogs);
  } catch (e) {
    console.warn("[Admin] updateDashboardKPIs error:", e);
  }

  // 4. Render Per-Video Analytics Table
  try {
    renderPerVideoAnalyticsTable(activeArchiveEvents, sanitizedLogs);
  } catch (e) {
    console.warn("[Admin] renderPerVideoAnalyticsTable error:", e);
  }

  // 5. Render Detailed Access Logs Table
  try {
    renderAdminLogsTable(sanitizedLogs);
  } catch (e) {
    console.warn("[Admin] renderAdminLogsTable error:", e);
  }

  // 6. Render Events Management Table
  try {
    renderAdminEventsTable();
  } catch (e) {
    console.warn("[Admin] renderAdminEventsTable error:", e);
  }

  // 7. Load & Render Blocklist
  try {
    loadBlocklistData();
  } catch (e) {
    console.warn("[Admin] loadBlocklistData error:", e);
  }
}

// Update KPI cards
function updateDashboardKPIs(activeArchiveEvents, logs) {
  const activeArchivesCount = activeArchiveEvents.length;
  const totalViews = logs.length;
  const uniqueVisitors = new Set(logs.map(l => l.visitorId).filter(Boolean)).size;

  // Find top viewed event
  const countMap = {};
  logs.forEach(l => {
    const title = l.eventTitle || "不明なイベント";
    countMap[title] = (countMap[title] || 0) + 1;
  });

  let topTitle = "--";
  let maxCount = 0;
  for (const [title, count] of Object.entries(countMap)) {
    if (count > maxCount) {
      maxCount = count;
      topTitle = `${title} (${count}回)`;
    }
  }

  const kpiActive = document.getElementById("kpi-active-archives");
  const kpiTotal = document.getElementById("kpi-total-views");
  const kpiUnique = document.getElementById("kpi-unique-visitors");
  const kpiTop = document.getElementById("kpi-top-video");

  if (kpiActive) kpiActive.textContent = activeArchivesCount;
  if (kpiTotal) kpiTotal.textContent = totalViews;
  if (kpiUnique) kpiUnique.textContent = uniqueVisitors;
  if (kpiTop) kpiTop.textContent = topTitle;
}

// ==================== PER-VIDEO VIEW ANALYTICS TABLE ====================

function renderPerVideoAnalyticsTable(activeArchiveEvents, logs) {
  const tbody = document.getElementById("admin-video-stats-tbody");
  const countEl = document.getElementById("video-stats-count");
  if (countEl) countEl.textContent = activeArchiveEvents.length;
  if (!tbody) return;

  if (activeArchiveEvents.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" class="p-8 text-center text-slate-400 text-xs">
          現在「録画あり」として公開登録されているイベントはありません。
          下の「イベント一覧」タブまたは新規作成から、アーカイブ動画URLを設定してください。
        </td>
      </tr>
    `;
    return;
  }

  const totalViewsAcrossAll = logs.length || 1;

  tbody.innerHTML = activeArchiveEvents.map(ev => {
    // Match logs for this event
    const eventLogs = logs.filter(l => l.eventId === ev.id || l.eventTitle === ev.title);
    const viewsCount = eventLogs.length;
    const uniqueCount = new Set(eventLogs.map(l => l.visitorId).filter(Boolean)).size;

    // Find latest view time
    let latestViewStr = '<span class="text-slate-400">-</span>';
    if (eventLogs.length > 0) {
      const latestLog = eventLogs[0]; // Already sorted desc
      if (latestLog.viewedAt) {
        latestViewStr = new Date(latestLog.viewedAt).toLocaleString("ja-JP", {
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
          hour: "2-digit",
          minute: "2-digit"
        });
      }
    }

    // View share percentage
    const sharePercent = logs.length > 0 ? Math.round((viewsCount / totalViewsAcrossAll) * 100) : 0;
    const archiveUrl = (ev.archive && ev.archive.archiveUrl) || "";
    const isYouTube = archiveUrl.includes("youtu.be") || archiveUrl.includes("youtube.com");
    const videoTypeBadge = isYouTube
      ? '<span class="inline-flex items-center gap-1 text-[10px] font-bold text-red-600 bg-red-50 px-2 py-0.5 rounded-md"><i class="fa-brands fa-youtube"></i> YouTube</span>'
      : '<span class="inline-flex items-center gap-1 text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md"><i class="fa-solid fa-video"></i> 動画リンク</span>';

    return `
      <tr class="border-b border-slate-100 hover:bg-slate-50/80 transition">
        <!-- Event Name & Details -->
        <td class="p-3.5 max-w-[280px]">
          <div class="flex items-start gap-2.5">
            <div class="w-8 h-8 rounded-xl bg-slate-900 text-amber-400 flex items-center justify-center text-xs shrink-0 mt-0.5">
              <i class="fa-solid fa-film"></i>
            </div>
            <div class="min-w-0">
              <p class="font-bold text-slate-900 text-xs line-clamp-1">${escapeHtml(ev.title)}</p>
              <p class="text-[10px] text-slate-400 font-medium mt-0.5">
                ${ev.startDate} ${ev.startTime || ''} 開催
              </p>
            </div>
          </div>
        </td>

        <!-- Category -->
        <td class="p-3.5 whitespace-nowrap">
          <span class="px-2 py-0.5 rounded-full text-[10px] font-bold" style="background-color: ${ev.categoryColor || '#f43f5e'}18; color: ${ev.categoryColor || '#f43f5e'}">
            ${escapeHtml(ev.category || 'イベント')}
          </span>
        </td>

        <!-- URL & Type -->
        <td class="p-3.5 max-w-[200px]">
          <div class="space-y-1">
            ${videoTypeBadge}
            <div class="truncate text-[11px] font-mono text-slate-500" title="${archiveUrl}">
              ${escapeHtml(archiveUrl)}
            </div>
          </div>
        </td>

        <!-- Play Count (with visual bar) -->
        <td class="p-3.5 text-center whitespace-nowrap">
          <div class="inline-flex flex-col items-center">
            <span class="text-base font-black text-rose-600">${viewsCount}<span class="text-[10px] text-slate-500 font-bold ml-0.5">回</span></span>
            <div class="w-16 h-1.5 bg-slate-100 rounded-full mt-1 overflow-hidden">
              <div class="h-full bg-rose-500 rounded-full" style="width: ${Math.max(sharePercent, viewsCount > 0 ? 8 : 0)}%"></div>
            </div>
          </div>
        </td>

        <!-- Unique Visitors -->
        <td class="p-3.5 text-center whitespace-nowrap">
          <span class="text-xs font-bold text-slate-700">${uniqueCount}<span class="text-[10px] text-slate-400 font-medium ml-0.5">台</span></span>
        </td>

        <!-- Last Viewed -->
        <td class="p-3.5 whitespace-nowrap font-mono text-[11px] text-slate-600">
          ${latestViewStr}
        </td>

        <!-- Actions -->
        <td class="p-3.5 text-right whitespace-nowrap space-x-1.5">
          <button onclick="openArchiveAdminModal('${ev.id}')" title="アーカイブURLの設定・変更" class="px-2.5 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-xl text-xs font-bold transition">
            <i class="fa-solid fa-gear text-[10px]"></i> 動画設定
          </button>
          <button onclick="openEditEventModal('${ev.id}')" title="イベント情報の編集" class="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition">
            <i class="fa-solid fa-pen text-[10px]"></i> 編集
          </button>
          <a href="${archiveUrl}" target="_blank" rel="noopener noreferrer" title="YouTube動画を開く" class="inline-flex items-center gap-1 px-2.5 py-1.5 bg-slate-900 hover:bg-black text-white rounded-xl text-xs font-bold transition shadow-2xs">
            <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i> 視聴
          </a>
        </td>
      </tr>
    `;
  }).join("");
}

// ==================== DETAILED ACCESS LOGS TABLE ====================

function filterAdminLogs() {
  const input = document.getElementById("log-search-input");
  currentLogFilter = (input ? input.value : "").trim().toLowerCase();

  if (!currentLogFilter) {
    renderAdminLogsTable(cachedArchiveLogs);
    return;
  }
  const filtered = cachedArchiveLogs.filter(l => {
    return (
      (l.eventTitle && l.eventTitle.toLowerCase().includes(currentLogFilter)) ||
      (l.device && l.device.toLowerCase().includes(currentLogFilter)) ||
      (l.userAgent && l.userAgent.toLowerCase().includes(currentLogFilter)) ||
      (l.viewedAt && l.viewedAt.toLowerCase().includes(currentLogFilter)) ||
      (l.visitorId && l.visitorId.toLowerCase().includes(currentLogFilter))
    );
  });
  renderAdminLogsTable(filtered);
}

function renderAdminLogsTable(logs) {
  const tbody = document.getElementById("admin-logs-tbody");
  if (!tbody) return;

  if (!logs || logs.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5" class="p-8 text-center text-slate-400 text-xs">
          ${currentLogFilter ? '条件に一致するアクセスログはありません。' : 'まだカレンダー経由でのアーカイブ動画視聴ログはありません。'}
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = logs.map(l => {
    const dateStr = l.viewedAt ? new Date(l.viewedAt).toLocaleString("ja-JP", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit"
    }) : "--";

    const isMobile = l.device === "Mobile" || /Mobi|Android|iPhone|iPad/i.test(l.userAgent || "");
    const deviceIcon = isMobile
      ? '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700"><i class="fa-solid fa-mobile-screen text-slate-500"></i> スマホ</span>'
      : '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700"><i class="fa-solid fa-laptop text-slate-500"></i> PC</span>';

    const shortVisitor = l.visitorId ? l.visitorId.substring(0, 14) + "..." : "-";

    return `
      <tr class="border-b border-slate-100 hover:bg-slate-50/80 transition">
        <td class="p-3.5 font-mono text-[11px] text-slate-600 whitespace-nowrap">${dateStr}</td>
        <td class="p-3.5 font-bold text-slate-900 line-clamp-1 max-w-[240px] text-xs">
          ${escapeHtml(l.eventTitle || '不明なイベント')}
        </td>
        <td class="p-3.5 whitespace-nowrap text-xs">
          ${deviceIcon}
        </td>
        <td class="p-3.5 font-mono text-[11px] text-slate-400 whitespace-nowrap" title="${escapeHtml(l.visitorId || '')}">
          ${escapeHtml(shortVisitor)}
        </td>
        <td class="p-3.5 whitespace-nowrap text-right">
          ${l.archiveUrl ? `
            <a href="${l.archiveUrl}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-[11px] font-bold text-rose-600 hover:underline">
              開く <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
            </a>
          ` : '<span class="text-slate-300">-</span>'}
        </td>
      </tr>
    `;
  }).join("");
}

// Download CSV
function downloadLogsCSV() {
  if (!cachedArchiveLogs || cachedArchiveLogs.length === 0) {
    alert("出力できる視聴ログがありません。");
    return;
  }
  const headers = ["閲覧日時 (ISO)", "閲覧日時 (日本時間)", "イベント名", "端末種別", "訪問者ID", "URL", "UserAgent"];
  const rows = cachedArchiveLogs.map(l => {
    const jst = l.viewedAt ? new Date(l.viewedAt).toLocaleString("ja-JP") : "";
    return [
      `"${(l.viewedAt || '').replace(/"/g, '""')}"`,
      `"${jst.replace(/"/g, '""')}"`,
      `"${(l.eventTitle || '').replace(/"/g, '""')}"`,
      `"${(l.device || '').replace(/"/g, '""')}"`,
      `"${(l.visitorId || '').replace(/"/g, '""')}"`,
      `"${(l.archiveUrl || '').replace(/"/g, '""')}"`,
      `"${(l.userAgent || '').replace(/"/g, '""')}"`
    ].join(",");
  });

  const csvContent = "\uFEFF" + [headers.join(","), ...rows].join("\r\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `neofamily_archive_logs_${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Cleanup legacy / dummy logs
async function cleanupLegacyLogs() {
  if (!confirm("過去のダミーリンク（Zoomダミーや存在しないイベント）の古いテストログを整理しますか？\n現在公開登録されているアーカイブ動画の正規ログのみが保持されます。")) {
    return;
  }

  // Filter against active archives
  const activeArchiveEvents = allEvents.filter(e => {
    return !!(
      e.archive &&
      e.archive.hasArchive &&
      e.archive.archiveUrl &&
      !e.archive.archiveUrl.includes("zoom.us/rec/share/example")
    );
  });
  const activeEventIdSet = new Set(activeArchiveEvents.map(e => e.id));
  const activeEventTitleSet = new Set(activeArchiveEvents.map(e => (e.title || "").trim()));

  const cleaned = cachedArchiveLogs.filter(l => {
    if (l.archiveUrl && (l.archiveUrl.includes("zoom.us/rec/share/example") || l.archiveUrl.includes("vimeo.com"))) {
      return false;
    }
    if (l.eventTitle && l.eventTitle.includes("RAYTUS group") && (!l.archiveUrl || l.archiveUrl.includes("zoom.us"))) {
      return false;
    }
    const matchesId = l.eventId && activeEventIdSet.has(l.eventId);
    const matchesTitle = l.eventTitle && activeEventTitleSet.has((l.eventTitle || "").trim());
    return matchesId || matchesTitle;
  });

  try {
    localStorage.setItem("neofamily_archive_logs", JSON.stringify(cleaned));
  } catch (e) {}

  cachedArchiveLogs = cleaned;
  loadDashboardData();
  alert("ログのクリーンアップが完了しました。");
}

// ==================== EVENTS MANAGEMENT TABLE ====================

function filterAdminEvents() {
  const searchInput = document.getElementById("event-search-input");
  const categorySelect = document.getElementById("event-category-filter");
  currentEventSearch = (searchInput ? searchInput.value : "").trim().toLowerCase();
  currentEventCategory = categorySelect ? categorySelect.value : "all";

  renderAdminEventsTable();
}

function renderAdminEventsTable() {
  const tbody = document.getElementById("admin-events-tbody");
  if (!tbody) return;

  let filtered = [...allEvents];

  if (currentEventCategory !== "all") {
    filtered = filtered.filter(e => e.category === currentEventCategory);
  }

  if (currentEventSearch) {
    filtered = filtered.filter(e => {
      return (
        (e.title && e.title.toLowerCase().includes(currentEventSearch)) ||
        (e.presenter && e.presenter.toLowerCase().includes(currentEventSearch)) ||
        (e.location && e.location.toLowerCase().includes(currentEventSearch)) ||
        (e.description && e.description.toLowerCase().includes(currentEventSearch))
      );
    });
  }

  // Sort by date desc
  filtered.sort((a, b) => (b.startDate + (b.startTime || '')).localeCompare(a.startDate + (a.startTime || '')));

  if (filtered.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" class="p-8 text-center text-slate-400 text-xs">
          該当するイベントがありません。
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = filtered.map(ev => {
    const hasArch = !!(ev.archive && ev.archive.hasArchive && ev.archive.archiveUrl);
    const archBadge = hasArch
      ? '<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-700"><i class="fa-brands fa-youtube"></i> あり</span>'
      : '<span class="text-slate-300 text-[10px] font-medium">-</span>';

    let locTypeBadge = '<span class="text-slate-500 text-[10px]">オンライン</span>';
    if (ev.locationType === "offline") {
      locTypeBadge = '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700">現地</span>';
    } else if (ev.locationType === "hybrid") {
      locTypeBadge = '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-50 text-indigo-700">ハイブリッド</span>';
    } else {
      locTypeBadge = '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-50 text-blue-700">オンライン</span>';
    }

    return `
      <tr class="border-b border-slate-100 hover:bg-slate-50/80 transition">
        <td class="p-3.5 font-mono text-slate-700 whitespace-nowrap text-xs">
          ${ev.startDate} <span class="text-[10px] text-slate-400">${ev.startTime || ''}</span>
        </td>
        <td class="p-3.5 whitespace-nowrap">
          <span class="px-2 py-0.5 rounded-full text-[10px] font-bold" style="background-color: ${ev.categoryColor || '#f43f5e'}18; color: ${ev.categoryColor || '#f43f5e'}">
            ${escapeHtml(ev.category || '定例会')}
          </span>
        </td>
        <td class="p-3.5 font-bold text-slate-900 text-xs max-w-xs">
          <div class="line-clamp-1">${escapeHtml(ev.title)}</div>
          ${ev.presenter ? `<div class="text-[10px] text-slate-400 font-normal">講師: ${escapeHtml(ev.presenter)}</div>` : ''}
        </td>
        <td class="p-3.5 text-center whitespace-nowrap">
          ${locTypeBadge}
        </td>
        <td class="p-3.5 text-center whitespace-nowrap">
          ${archBadge}
        </td>
        <td class="p-3.5 text-right whitespace-nowrap space-x-1.5">
          <button onclick="openArchiveAdminModal('${ev.id}')" title="アーカイブ動画URLの登録・管理" class="px-2.5 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-xl text-xs font-bold transition">
            <i class="fa-solid fa-film text-[10px]"></i> 動画設定
          </button>
          <button onclick="openEditEventModal('${ev.id}')" title="イベント内容の編集" class="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition">
            <i class="fa-solid fa-pen text-[10px]"></i> 編集
          </button>
          <button onclick="deleteEvent('${ev.id}')" title="イベント削除" class="px-2.5 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-600 rounded-xl text-xs font-bold transition">
            <i class="fa-solid fa-trash text-[10px]"></i> 削除
          </button>
        </td>
      </tr>
    `;
  }).join("");
}

// ==================== TAB SWITCHING ====================

function switchAdminTab(tabName) {
  const tabs = ["analytics", "events", "members", "blocklist", "settings"];
  tabs.forEach(t => {
    const btn = document.getElementById(`tab-btn-${t}`);
    const content = document.getElementById(`tab-content-${t}`);
    if (t === tabName) {
      if (btn) {
        btn.className = "px-4 py-3 text-xs sm:text-sm font-bold border-b-2 border-rose-600 text-rose-600 flex items-center gap-2 whitespace-nowrap transition";
      }
      if (content) content.classList.remove("hidden");
    } else {
      if (btn) {
        btn.className = "px-4 py-3 text-xs sm:text-sm font-bold border-b-2 border-transparent text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap transition";
      }
      if (content) content.classList.add("hidden");
    }
  });

  if (tabName === "events") {
    renderAdminEventsTable();
  }
  if (tabName === "members") {
    loadMembersProgressData();
  }
  if (tabName === "blocklist") {
    renderAdminBlocklistTable();
  }
}

// ==================== ARCHIVE ADMIN MODAL ====================

function openArchiveAdminModal(eventId) {
  currentArchiveEventId = eventId;
  const ev = allEvents.find(e => e.id === eventId);
  const modal = document.getElementById("archive-admin-modal");
  if (!modal) return;

  const titleEl = document.getElementById("admin-event-title");
  const chkEl = document.getElementById("admin-has-archive");
  const urlEl = document.getElementById("admin-archive-url");
  const notesEl = document.getElementById("admin-archive-notes");

  if (titleEl) titleEl.textContent = ev ? ev.title : "イベント";
  if (chkEl) chkEl.checked = !!(ev && ev.archive && ev.archive.hasArchive);
  if (urlEl) urlEl.value = (ev && ev.archive && ev.archive.archiveUrl) || "";
  if (notesEl) notesEl.value = (ev && ev.archive && ev.archive.notes) || "";

  modal.classList.remove("hidden");
  modal.classList.add("flex");
}

function closeArchiveAdminModal() {
  const modal = document.getElementById("archive-admin-modal");
  if (modal) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  }
  currentArchiveEventId = null;
}

async function saveArchiveSettings(e) {
  e.preventDefault();
  if (!currentArchiveEventId) return;

  const evIndex = allEvents.findIndex(ev => ev.id === currentArchiveEventId);
  if (evIndex === -1) return;

  const hasArchive = document.getElementById("admin-has-archive").checked;
  const archiveUrl = document.getElementById("admin-archive-url").value.trim();
  const notes = document.getElementById("admin-archive-notes").value.trim();

  allEvents[evIndex].archive = {
    hasArchive: hasArchive,
    archiveUrl: archiveUrl,
    notes: notes,
    requiresAuth: false
  };

  // Sync to Firestore if available
  if (typeof saveEventToFirestore === "function" && isFirebaseConfigured()) {
    try {
      await saveEventToFirestore(allEvents[evIndex]);
    } catch (err) {
      console.warn("Failed to update event in Firestore:", err);
    }
  }

  closeArchiveAdminModal();
  loadDashboardData();
  alert("アーカイブ動画の設定を更新しました。");
}

// ==================== CREATE / EDIT EVENT MODAL ====================

function openCreateEventModal() {
  editingEventId = null;
  selectedEventImages = [];

  const titleEl = document.getElementById("create-event-modal-title");
  const descEl = document.getElementById("create-event-modal-desc");
  const submitText = document.getElementById("create-event-submit-text");
  if (titleEl) titleEl.innerHTML = '<i class="fa-solid fa-calendar-plus text-rose-600"></i> 新規イベント作成';
  if (descEl) descEl.textContent = '新しいイベント情報を入力して登録します。';
  if (submitText) submitText.textContent = 'イベントを登録する';

  document.getElementById("create-event-form").reset();
  document.getElementById("new-event-start-time").value = "13:00";
  document.getElementById("new-event-end-time").value = "15:00";
  renderImagePreviews();

  const modal = document.getElementById("create-event-modal");
  if (modal) {
    modal.classList.remove("hidden");
    modal.classList.add("flex");
  }
}

function openEditEventModal(eventId) {
  const ev = allEvents.find(e => e.id === eventId);
  if (!ev) return;

  editingEventId = eventId;

  const titleEl = document.getElementById("create-event-modal-title");
  const descEl = document.getElementById("create-event-modal-desc");
  const submitText = document.getElementById("create-event-submit-text");
  if (titleEl) titleEl.innerHTML = '<i class="fa-solid fa-pen-to-square text-rose-600"></i> イベント編集';
  if (descEl) descEl.textContent = '登録済みイベントの内容を変更します。';
  if (submitText) submitText.textContent = '変更を保存する';

  document.getElementById("new-event-title").value = ev.title || "";
  document.getElementById("new-event-subtitle").value = ev.subtitle || "";
  document.getElementById("new-event-category").value = ev.category || "定例会";
  document.getElementById("new-event-location-type").value = ev.locationType || "online";
  document.getElementById("new-event-date").value = ev.startDate || "";
  document.getElementById("new-event-start-time").value = ev.startTime || "13:00";
  document.getElementById("new-event-end-time").value = ev.endTime || "15:00";
  document.getElementById("new-event-location").value = ev.location || "";
  document.getElementById("new-event-presenter").value = ev.presenter || "";
  document.getElementById("new-event-fee").value = ev.fee || "";
  document.getElementById("new-event-zoom-url").value = ev.zoomUrl || "";
  document.getElementById("new-event-zoom-id").value = ev.zoomMeetingId || "";
  document.getElementById("new-event-zoom-pass").value = ev.zoomPasscode || "";
  document.getElementById("new-event-description").value = ev.description || "";

  const hasArchive = !!(ev.archive && ev.archive.hasArchive);
  document.getElementById("new-event-has-archive").checked = hasArchive;
  document.getElementById("new-event-archive-url").value = (ev.archive && ev.archive.archiveUrl) || "";

  selectedEventImages = Array.isArray(ev.images) && ev.images.length > 0
    ? [...ev.images]
    : (ev.image ? [ev.image] : []);
  renderImagePreviews();

  const modal = document.getElementById("create-event-modal");
  if (modal) {
    modal.classList.remove("hidden");
    modal.classList.add("flex");
  }
}

function closeCreateEventModal() {
  const modal = document.getElementById("create-event-modal");
  if (modal) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  }
  editingEventId = null;
  selectedEventImages = [];
}

// Flyer Uploads Handling
function handleFlyerUpload(e) {
  const files = Array.from(e.target.files);
  if (!files || files.length === 0) return;

  files.forEach(file => {
    if (!file.type.startsWith("image/")) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      selectedEventImages.push(event.target.result);
      renderImagePreviews();
    };
    reader.readAsDataURL(file);
  });
}

function removeSelectedImage(index) {
  selectedEventImages.splice(index, 1);
  renderImagePreviews();
}

function renderImagePreviews() {
  const container = document.getElementById("image-preview-container");
  if (!container) return;

  if (selectedEventImages.length === 0) {
    container.classList.add("hidden");
    container.innerHTML = "";
    return;
  }

  container.classList.remove("hidden");
  container.innerHTML = selectedEventImages.map((src, idx) => `
    <div class="relative group aspect-video rounded-xl overflow-hidden border border-slate-200 bg-slate-100">
      <img src="${src}" alt="チラシ" class="w-full h-full object-cover">
      <button type="button" onclick="removeSelectedImage(${idx})" class="absolute top-1 right-1 w-6 h-6 rounded-full bg-rose-600 text-white flex items-center justify-center text-xs opacity-80 group-hover:opacity-100 transition shadow">
        <i class="fa-solid fa-xmark"></i>
      </button>
    </div>
  `).join("");
}

// Handle Form Submit (Create or Edit)
async function handleCreateEvent(e) {
  e.preventDefault();

  const title = document.getElementById("new-event-title").value.trim();
  const subtitle = document.getElementById("new-event-subtitle").value.trim();
  const category = document.getElementById("new-event-category").value;
  const locationType = document.getElementById("new-event-location-type").value;
  const startDate = document.getElementById("new-event-date").value;
  const startTime = document.getElementById("new-event-start-time").value || "13:00";
  const endTime = document.getElementById("new-event-end-time").value || "15:00";
  const location = document.getElementById("new-event-location").value.trim();
  const presenter = document.getElementById("new-event-presenter").value.trim();
  const fee = document.getElementById("new-event-fee").value.trim();
  const zoomUrl = document.getElementById("new-event-zoom-url").value.trim();
  const zoomId = document.getElementById("new-event-zoom-id").value.trim();
  const zoomPass = document.getElementById("new-event-zoom-pass").value.trim();
  const description = document.getElementById("new-event-description").value.trim();
  const hasArchive = document.getElementById("new-event-has-archive").checked;
  const archiveUrl = document.getElementById("new-event-archive-url").value.trim();

  // Category Color Map
  const colorMap = {
    "定例会": "#f43f5e",
    "説明会": "#6366f1",
    "勉強会": "#10b981",
    "その他": "#f59e0b"
  };

  const eventPayload = {
    title,
    subtitle,
    category,
    categoryColor: colorMap[category] || "#f43f5e",
    locationType,
    startDate,
    startTime,
    endTime,
    location,
    presenter,
    fee,
    zoomUrl,
    zoomMeetingId: zoomId,
    zoomPasscode: zoomPass,
    description,
    images: [...selectedEventImages],
    image: selectedEventImages[0] || "",
    archive: {
      hasArchive: hasArchive && !!archiveUrl,
      archiveUrl: archiveUrl,
      notes: "YouTube / Zoomアーカイブ",
      requiresAuth: false
    }
  };

  if (editingEventId) {
    // EDIT
    eventPayload.id = editingEventId;
    const idx = allEvents.findIndex(ev => ev.id === editingEventId);
    if (idx !== -1) {
      allEvents[idx] = { ...allEvents[idx], ...eventPayload };
    }
    if (typeof saveEventToFirestore === "function" && isFirebaseConfigured()) {
      try {
        await saveEventToFirestore(eventPayload);
      } catch (err) {
        console.warn("Firestore save failed:", err);
      }
    }
    alert("イベントを更新しました。");
  } else {
    // CREATE
    const newId = "ev_" + Date.now().toString(36) + "_" + Math.random().toString(36).substring(2, 6);
    eventPayload.id = newId;
    allEvents.unshift(eventPayload);
    if (typeof saveEventToFirestore === "function" && isFirebaseConfigured()) {
      try {
        await saveEventToFirestore(eventPayload);
      } catch (err) {
        console.warn("Firestore save failed:", err);
      }
    }
    sendNotificationPayload({
      title: "【NEO FAMILY】新着イベントが追加されました！",
      body: `「${eventPayload.title}」（${eventPayload.startDate}）が登録されました！`,
      icon: "images/apple-touch-icon.png",
      url: "./index.html",
      eventId: newId
    });
    alert("イベントを登録しました。");
  }

  closeCreateEventModal();
  loadDashboardData();
}

// Delete Event
async function deleteEvent(eventId) {
  const ev = allEvents.find(e => e.id === eventId);
  const title = ev ? ev.title : "このイベント";
  if (!confirm(`「${title}」を本当に削除しますか？\n※この操作は取り消せません。`)) {
    return;
  }

  allEvents = allEvents.filter(e => e.id !== eventId);

  if (typeof deleteEventFromFirestore === "function" && isFirebaseConfigured()) {
    try {
      await deleteEventFromFirestore(eventId);
    } catch (err) {
      console.warn("Firestore delete failed:", err);
    }
  }

  loadDashboardData();
  alert("イベントを削除しました。");
}

// ==================== SETTINGS (PASSCODE CHANGE) ====================

function handlePasscodeChange(e) {
  e.preventDefault();
  const currentInput = document.getElementById("current-passcode-input");
  const newInput = document.getElementById("new-passcode-input");
  const confirmInput = document.getElementById("confirm-passcode-input");

  const curPass = (localStorage.getItem("neofamily_admin_passcode") || DEFAULT_ADMIN_PASSCODE).trim();
  const enteredCur = (currentInput ? currentInput.value : "").trim();
  const newPass = (newInput ? newInput.value : "").trim();
  const confirmPass = (confirmInput ? confirmInput.value : "").trim();

  const isCurValid = enteredCur === DEFAULT_ADMIN_PASSCODE || enteredCur === curPass;

  if (!isCurValid) {
    alert("現在のパスコードが一致しません。");
    currentInput.focus();
    return;
  }
  if (newPass.length < 4) {
    alert("新しいパスコードは4文字以上で設定してください。");
    newInput.focus();
    return;
  }
  if (newPass !== confirmPass) {
    alert("新しいパスコードと確認用パスコードが一致しません。");
    confirmInput.focus();
    return;
  }

  localStorage.setItem("neofamily_admin_passcode", newPass);
  resetPasscodeForm();
  alert("管理者パスコードを更新しました。");
}

function resetPasscodeForm() {
  const cur = document.getElementById("current-passcode-input");
  const n = document.getElementById("new-passcode-input");
  const c = document.getElementById("confirm-passcode-input");
  if (cur) cur.value = "";
  if (n) n.value = "";
  if (c) c.value = "";
}

// ==================== UTILS ====================

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function setupEscapeKeyHandler() {
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeArchiveAdminModal();
      closeCreateEventModal();
      closeModal('member-detail-modal');
      closeModal('add-member-modal');
      closeModal('blocklist-modal');
      closeModal('blocklist-delete-modal');
      closeModal('ocr-transcription-modal');
    }
  });
}

function sendNotificationPayload(payload) {
  if (navigator.serviceWorker && navigator.serviceWorker.controller) {
    navigator.serviceWorker.controller.postMessage({
      type: "SHOW_NOTIFICATION",
      ...payload
    });
  } else if ("Notification" in window && Notification.permission === "granted") {
    try {
      new Notification(payload.title, {
        body: payload.body,
        icon: payload.icon || "images/apple-touch-icon.png",
        tag: "neofamily-notice"
      });
    } catch (e) {
      console.warn("Direct Notification error:", e);
    }
  }
}


// ==================== MEMBERS & MENTORS PROGRESS MANAGEMENT ====================

let allMembersProgress = [];
let currentAdminRole = "admin"; // "admin" or "mentor"
let selectedMentorFilter = "all";

// 担当サポート者リスト
const MENTORS_LIST = [
  { id: "mentor_tanaka", name: "田中 リーダー" },
  { id: "mentor_sato", name: "佐藤 リーダー" },
  { id: "mentor_suzuki", name: "鈴木 リーダー" }
];

// 初期サンプル会員データ（Firestore未連携時や初期表示用）
const INITIAL_SAMPLE_MEMBERS = [
  {
    memberId: "1234abc",
    mentorId: "mentor_tanaka",
    onboardingSteps: { zoom: true, teireikai: true, support: true },
    viewedContents: {
      "https://www.youtube.com/embed/EK-xR3McLHc": { title: "【58歳熟年離婚】を迫られた夫はパンツも洗えん...", viewedAt: "2026-10-19T21:40:00Z" },
      "images/notion-event-flow.jpg": { title: "イベント参加フローチャート", viewedAt: "2026-10-19T21:35:00Z" },
      "service_inawa": { title: "総合食事業：稲環（いなわ）", viewedAt: "2026-10-19T21:38:00Z" }
    },
    lastActiveAt: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
    firstSeenAt: "2026-10-19T10:00:00Z",
    deviceInfo: "iPhone 15 / Safari"
  },
  {
    memberId: "5678def",
    mentorId: "mentor_tanaka",
    onboardingSteps: { zoom: true, teireikai: false, support: true },
    viewedContents: {
      "images/notion-support-list.jpg": { title: "サポート一覧", viewedAt: "2026-10-19T18:20:00Z" }
    },
    lastActiveAt: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
    firstSeenAt: "2026-10-18T14:00:00Z",
    deviceInfo: "Android / Chrome"
  },
  {
    memberId: "9012xyz",
    mentorId: "mentor_sato",
    onboardingSteps: { zoom: true, teireikai: true, support: true },
    viewedContents: {
      "https://www.youtube.com/embed/3sPl_bbEaiE": { title: "【夫の浮気】妻がやるべきことは1つだけ", viewedAt: "2026-10-19T20:10:00Z" },
      "https://www.youtube.com/embed/KApFWKM2QEU": { title: "【16年間モラハラ】もう男なんていらない", viewedAt: "2026-10-19T20:45:00Z" },
      "images/notion-annual-schedule.png": { title: "年間スケジュール", viewedAt: "2026-10-19T19:50:00Z" }
    },
    lastActiveAt: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
    firstSeenAt: "2026-10-17T09:30:00Z",
    deviceInfo: "Windows PC / Chrome"
  },
  {
    memberId: "3344mno",
    mentorId: "mentor_sato",
    onboardingSteps: { zoom: false, teireikai: false, support: false },
    viewedContents: {},
    lastActiveAt: new Date(Date.now() - 1000 * 60 * 60 * 36).toISOString(),
    firstSeenAt: "2026-10-16T11:00:00Z",
    deviceInfo: "iPhone / LINE in-app"
  },
  {
    memberId: "7788qrs",
    mentorId: "mentor_suzuki",
    onboardingSteps: { zoom: true, teireikai: false, support: false },
    viewedContents: {
      "https://www.youtube.com/embed/fjkadO1_OYs": { title: "【経営者必見】ドブに捨てるお金の使い方...", viewedAt: "2026-10-19T16:00:00Z" }
    },
    lastActiveAt: new Date(Date.now() - 1000 * 60 * 60 * 6).toISOString(),
    firstSeenAt: "2026-10-18T16:00:00Z",
    deviceInfo: "Mac / Safari"
  },
  {
    memberId: "8899tuv",
    mentorId: "unassigned",
    onboardingSteps: { zoom: false, teireikai: false, support: false },
    viewedContents: {},
    lastActiveAt: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString(),
    firstSeenAt: "2026-10-19T08:00:00Z",
    deviceInfo: "iPhone / Safari"
  }
];

// 会員進捗データの読み込み
async function loadMembersProgressData() {
  let loaded = false;
  if (typeof firebase !== "undefined" && firebase.apps.length) {
    try {
      const db = firebase.firestore();
      const snap = await db.collection("member_progress").get();
      if (!snap.empty) {
        allMembersProgress = [];
        snap.forEach(doc => {
          allMembersProgress.push({ memberId: doc.id, ...doc.data() });
        });
        loaded = true;
      }
    } catch (e) {
      console.warn("[Admin] Firestore members load fallback:", e);
    }
  }

  if (!loaded || allMembersProgress.length === 0) {
    // ローカルキャッシュまたはサンプルデータを使用
    const local = localStorage.getItem("neofamily_cached_members");
    allMembersProgress = local ? JSON.parse(local) : INITIAL_SAMPLE_MEMBERS;
  }

  renderMembersKPI();
  renderMembersTable();
}

// ロール表示切り替え（総責任者ビュー / サポート担当者ビュー）
function setAdminRoleView(role) {
  currentAdminRole = role;
  const btnAdmin = document.getElementById("role-btn-admin");
  const btnMentor = document.getElementById("role-btn-mentor");
  const mentorSelect = document.getElementById("mentor-select-filter");
  const roleBadge = document.getElementById("role-badge");

  if (role === "admin") {
    if (btnAdmin) btnAdmin.className = "px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-2xs transition flex items-center gap-1";
    if (btnMentor) btnMentor.className = "px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition flex items-center gap-1";
    if (mentorSelect) mentorSelect.classList.add("hidden");
    if (roleBadge) {
      roleBadge.textContent = "総責任者ビュー（全員表示）";
      roleBadge.className = "px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800";
    }
    selectedMentorFilter = "all";
  } else {
    if (btnAdmin) btnAdmin.className = "px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition flex items-center gap-1";
    if (btnMentor) btnMentor.className = "px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-2xs transition flex items-center gap-1";
    if (mentorSelect) mentorSelect.classList.remove("hidden");
    if (roleBadge) {
      roleBadge.textContent = "サポート担当者ビュー";
      roleBadge.className = "px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-100 text-indigo-800";
    }
    if (mentorSelect && mentorSelect.value !== "all") {
      selectedMentorFilter = mentorSelect.value;
    } else {
      selectedMentorFilter = "mentor_tanaka";
      if (mentorSelect) mentorSelect.value = "mentor_tanaka";
    }
  }

  renderMembersKPI();
  renderMembersTable();
}

// 担当者セレクト変更
function filterMembersByMentor() {
  const sel = document.getElementById("mentor-select-filter");
  if (sel) {
    selectedMentorFilter = sel.value;
    renderMembersKPI();
    renderMembersTable();
  }
}

// KPI集計・表示
function renderMembersKPI() {
  const list = getFilteredMembersList();
  const total = list.length;
  
  let completed = 0;
  let unstarted = 0;
  let active24h = 0;
  const now = Date.now();

  list.forEach(m => {
    const s = m.onboardingSteps || {};
    const count = [s.zoom, s.teireikai, s.support].filter(Boolean).length;
    if (count === 3) completed++;
    if (count === 0 && Object.keys(m.viewedContents || {}).length === 0) unstarted++;

    if (m.lastActiveAt) {
      const diff = now - new Date(m.lastActiveAt).getTime();
      if (diff <= 1000 * 60 * 60 * 24) active24h++;
    }
  });

  const elTotal = document.getElementById("kpi-members-total");
  const elComp = document.getElementById("kpi-members-completed");
  const elUnstarted = document.getElementById("kpi-members-unstarted");
  const elActive = document.getElementById("kpi-members-active");

  if (elTotal) elTotal.textContent = total;
  if (elComp) elComp.textContent = completed;
  if (elUnstarted) elUnstarted.textContent = unstarted;
  if (elActive) elActive.textContent = active24h;
}

// フィルタリング済みメンバー一覧の取得
function getFilteredMembersList() {
  let list = [...allMembersProgress];
  if (currentAdminRole === "mentor" && selectedMentorFilter !== "all") {
    list = list.filter(m => (m.mentorId || "unassigned") === selectedMentorFilter);
  }
  return list;
}

// テーブル描画
function renderMembersTable() {
  const tbody = document.getElementById("members-table-body");
  if (!tbody) return;

  const search = (document.getElementById("member-search-input")?.value || "").toLowerCase().trim();
  const statusFilter = document.getElementById("member-status-filter")?.value || "all";

  let list = getFilteredMembersList();

  // 検索
  if (search) {
    list = list.filter(m => (m.memberId || "").toLowerCase().includes(search));
  }

  // ステータス絞り込み
  if (statusFilter !== "all") {
    list = list.filter(m => {
      const s = m.onboardingSteps || {};
      const count = [s.zoom, s.teireikai, s.support].filter(Boolean).length;
      if (statusFilter === "completed") return count === 3;
      if (statusFilter === "inprogress") return count > 0 && count < 3;
      if (statusFilter === "unstarted") return count === 0;
      return true;
    });
  }

  if (list.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" class="py-8 text-center text-slate-400">
          <i class="fa-solid fa-user-slash text-2xl mb-2 block"></i>
          該当する会員が見つかりませんでした。
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = list.map(m => {
    const s = m.onboardingSteps || {};
    const count = [s.zoom, s.teireikai, s.support].filter(Boolean).length;
    
    // バッジ
    let badgeHtml = "";
    if (count === 3) {
      badgeHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 flex items-center gap-1 w-fit"><i class="fa-solid fa-circle-check"></i> 完了 (3/3)</span>`;
    } else if (count > 0) {
      badgeHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 flex items-center gap-1 w-fit"><i class="fa-solid fa-spinner animate-spin"></i> 進行中 (${count}/3)</span>`;
    } else {
      badgeHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-800 flex items-center gap-1 w-fit"><i class="fa-solid fa-circle-exclamation"></i> 未着手 (0/3)</span>`;
    }

    // 各ステップのミニアイコン
    const stepIcons = `
      <div class="flex items-center gap-1 mt-1 text-[10px]">
        <span class="px-1.5 py-0.2 rounded ${s.zoom ? 'bg-blue-100 text-blue-700 font-bold' : 'bg-slate-100 text-slate-400'}">Zoom</span>
        <span class="px-1.5 py-0.2 rounded ${s.teireikai ? 'bg-rose-100 text-rose-700 font-bold' : 'bg-slate-100 text-slate-400'}">定例会</span>
        <span class="px-1.5 py-0.2 rounded ${s.support ? 'bg-emerald-100 text-emerald-700 font-bold' : 'bg-slate-100 text-slate-400'}">窓口</span>
      </div>
    `;

    // 閲覧ログ数
    const viewedCount = Object.keys(m.viewedContents || {}).length;

    // 最終アクセス
    let lastActiveText = "未アクセス";
    if (m.lastActiveAt) {
      const d = new Date(m.lastActiveAt);
      lastActiveText = `${d.getMonth()+1}/${d.getDate()} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
    }

    // 担当者セレクト（総責任者ビューの場合はインライン変更可能）
    let mentorCol = "";
    if (currentAdminRole === "admin") {
      mentorCol = `
        <select onchange="updateMemberMentor('${m.memberId}', this.value)" class="px-2 py-1 rounded-lg bg-slate-50 border border-slate-200 text-[11px] font-bold text-slate-800 focus:outline-none focus:ring-1 focus:ring-indigo-500">
          <option value="mentor_tanaka" ${m.mentorId === 'mentor_tanaka' ? 'selected' : ''}>田中 リーダー</option>
          <option value="mentor_sato" ${m.mentorId === 'mentor_sato' ? 'selected' : ''}>佐藤 リーダー</option>
          <option value="mentor_suzuki" ${m.mentorId === 'mentor_suzuki' ? 'selected' : ''}>鈴木 リーダー</option>
          <option value="unassigned" ${(!m.mentorId || m.mentorId === 'unassigned') ? 'selected' : ''}>未割り当て</option>
        </select>
      `;
    } else {
      const mentorObj = MENTORS_LIST.find(x => x.id === m.mentorId);
      mentorCol = `<span class="text-xs font-bold text-slate-800">${mentorObj ? mentorObj.name : '未割り当て'}</span>`;
    }

    return `
      <tr class="hover:bg-slate-50/80 transition">
        <td class="py-3 px-4 font-mono font-bold text-slate-900 text-xs">
          <div class="flex items-center gap-2">
            <span class="w-6 h-6 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center text-[10px]">👤</span>
            <span>${m.memberId}</span>
          </div>
        </td>
        <td class="py-3 px-4">${mentorCol}</td>
        <td class="py-3 px-4">
          ${badgeHtml}
          ${stepIcons}
        </td>
        <td class="py-3 px-4">
          <span class="px-2 py-0.5 rounded-lg bg-slate-100 text-slate-700 font-bold text-[11px]">
            ${viewedCount} 件閲覧
          </span>
        </td>
        <td class="py-3 px-4 text-slate-500 text-[11px] font-mono">${lastActiveText}</td>
        <td class="py-3 px-4 text-right">
          <button onclick="openMemberDetailModal('${m.memberId}')" class="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-indigo-50 text-slate-700 hover:text-indigo-700 font-bold text-[11px] transition shadow-2xs">
            <i class="fa-solid fa-file-lines mr-0.5"></i> 詳細ログ
          </button>
        </td>
      </tr>
    `;
  }).join("");
}

function filterMembersTable() {
  renderMembersTable();
}

// 担当サポート者の変更・保存
async function updateMemberMentor(memberId, newMentorId) {
  const member = allMembersProgress.find(m => m.memberId === memberId);
  if (member) {
    member.mentorId = newMentorId;
    localStorage.setItem("neofamily_cached_members", JSON.stringify(allMembersProgress));

    if (typeof firebase !== "undefined" && firebase.apps.length) {
      try {
        const db = firebase.firestore();
        await db.collection("member_progress").doc(memberId).set({ mentorId: newMentorId }, { merge: true });
      } catch (e) {
        console.warn("[Admin] Firestore update error:", e);
      }
    }

    showToast(`会員ID「${memberId}」の担当を更新しました`);
    renderMembersKPI();
  }
}

// 会員詳細閲覧モーダル
function openMemberDetailModal(memberId) {
  const member = allMembersProgress.find(m => m.memberId === memberId);
  if (!member) return;

  document.getElementById("detail-modal-member-id").textContent = member.memberId;
  const mentorObj = MENTORS_LIST.find(x => x.id === member.mentorId);
  document.getElementById("detail-modal-mentor-name").textContent = `担当サポート者: ${mentorObj ? mentorObj.name : '未割り当て'}`;

  // ステップ描画
  const s = member.onboardingSteps || {};
  const stepsContainer = document.getElementById("detail-modal-steps");
  stepsContainer.innerHTML = `
    <div class="flex items-center justify-between p-2 rounded-xl border ${s.zoom ? 'bg-emerald-50/60 border-emerald-200 text-emerald-800' : 'bg-slate-50 border-slate-200 text-slate-500'}">
      <span class="text-xs font-bold flex items-center gap-1.5">
        <i class="fa-solid ${s.zoom ? 'fa-circle-check text-emerald-600' : 'fa-circle text-slate-300'}"></i>
        <span>Step 1: 全日共通Zoom情報をメモ</span>
      </span>
      <span class="text-[10px] font-bold">${s.zoom ? '完了' : '未完了'}</span>
    </div>
    <div class="flex items-center justify-between p-2 rounded-xl border ${s.teireikai ? 'bg-emerald-50/60 border-emerald-200 text-emerald-800' : 'bg-slate-50 border-slate-200 text-slate-500'}">
      <span class="text-xs font-bold flex items-center gap-1.5">
        <i class="fa-solid ${s.teireikai ? 'fa-circle-check text-emerald-600' : 'fa-circle text-slate-300'}"></i>
        <span>Step 2: 次回合同定例会（調整さん）に参加表明</span>
      </span>
      <span class="text-[10px] font-bold">${s.teireikai ? '完了' : '未完了'}</span>
    </div>
    <div class="flex items-center justify-between p-2 rounded-xl border ${s.support ? 'bg-emerald-50/60 border-emerald-200 text-emerald-800' : 'bg-slate-50 border-slate-200 text-slate-500'}">
      <span class="text-xs font-bold flex items-center gap-1.5">
        <i class="fa-solid ${s.support ? 'fa-circle-check text-emerald-600' : 'fa-circle text-slate-300'}"></i>
        <span>Step 3: 困ったときのサポート窓口確認</span>
      </span>
      <span class="text-[10px] font-bold">${s.support ? '完了' : '未完了'}</span>
    </div>
  `;

  // 閲覧ログ描画
  const logsContainer = document.getElementById("detail-modal-logs");
  const logs = Object.entries(member.viewedContents || {});
  if (logs.length === 0) {
    logsContainer.innerHTML = `<p class="text-xs text-slate-400 py-3 text-center">閲覧履歴はまだありません。</p>`;
  } else {
    logsContainer.innerHTML = logs.map(([key, item]) => {
      const d = item.viewedAt ? new Date(item.viewedAt) : new Date();
      const timeStr = `${d.getMonth()+1}/${d.getDate()} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
      return `
        <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between gap-2">
          <div class="truncate text-xs font-bold text-slate-800">
            <i class="fa-regular fa-eye text-indigo-500 mr-1"></i>
            <span>${item.title || key}</span>
          </div>
          <span class="text-[10px] text-slate-400 shrink-0 font-mono">${timeStr}</span>
        </div>
      `;
    }).join("");
  }

  openModal("member-detail-modal");
}

// 新規会員登録モーダル
function openAddMemberModal() {
  openModal("add-member-modal");
}

async function handleAddMemberSubmit(e) {
  e.preventDefault();
  const idInput = document.getElementById("new-member-id");
  const mentorSelect = document.getElementById("new-member-mentor");
  const id = (idInput?.value || "").trim().toLowerCase();
  const mentorId = mentorSelect?.value || "unassigned";

  if (!id) return;

  const existing = allMembersProgress.find(m => m.memberId === id);
  if (existing) {
    alert("この会員IDは既に登録されています。");
    return;
  }

  const newMember = {
    memberId: id,
    mentorId: mentorId,
    onboardingSteps: { zoom: false, teireikai: false, support: false },
    viewedContents: {},
    firstSeenAt: new Date().toISOString(),
    lastActiveAt: new Date().toISOString(),
    deviceInfo: "Admin registered"
  };

  allMembersProgress.unshift(newMember);
  localStorage.setItem("neofamily_cached_members", JSON.stringify(allMembersProgress));

  if (typeof firebase !== "undefined" && firebase.apps.length) {
    try {
      const db = firebase.firestore();
      await db.collection("member_progress").doc(id).set(newMember);
    } catch (err) {
      console.warn("[Admin] Firestore save error:", err);
    }
  }

  closeModal("add-member-modal");
  idInput.value = "";
  showToast(`会員ID「${id}」を登録しました`);
  renderMembersKPI();
  renderMembersTable();
}

function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    document.body.style.overflow = '';
  }
}

function showToast(message) {
  try {
    let container = document.getElementById("toast-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "toast-container";
      container.className = "fixed bottom-5 right-5 z-50 pointer-events-none space-y-2";
      document.body.appendChild(container);
    }
    const toast = document.createElement("div");
    toast.className = "px-4 py-3 rounded-2xl bg-slate-900 text-white text-xs font-bold shadow-xl border border-slate-700 flex items-center gap-2 transition-all duration-300";
    toast.innerHTML = `<i class="fa-solid fa-circle-check text-emerald-400"></i><span>${escapeHtml(String(message || ""))}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      setTimeout(() => {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 300);
    }, 2800);
  } catch (e) {
    console.log("[Toast]", message);
  }
}

// =========================================================================
// ==================== BLOCKLIST MANAGEMENT (入会不適合者リスト) ====================
// =========================================================================

let allBlocklist = [];
let blocklistCurrentPage = 1;
let blocklistPerPage = 50;
let blocklistDeleteTargetId = null;

/**
 * ユーザーによる手動編集・追加・削除の差分データを取得・保存
 * INITIAL_BLOCKLIST が更新されても、管理者が手動編集した内容は100%保持される
 */
function getBlocklistUserEdits() {
  try {
    const raw = localStorage.getItem("neofamily_blocklist_user_edits_v5");
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && typeof parsed === "object") {
        return {
          updated: parsed.updated || {},
          created: Array.isArray(parsed.created) ? parsed.created : [],
          deleted: parsed.deleted || {}
        };
      }
    }
  } catch (e) {}
  return { updated: {}, created: [], deleted: {} };
}

function setBlocklistUserEdits(edits) {
  try {
    localStorage.setItem("neofamily_blocklist_user_edits_v5", JSON.stringify(edits));
  } catch (e) {}
}

function applyBlocklistUserEditsToBase(baseList, edits) {
  let list = baseList.filter(item => !edits.deleted[item.id]);
  list = list.map(item => {
    if (edits.updated[item.id]) {
      return { ...item, ...edits.updated[item.id] };
    }
    return { ...item };
  });
  const existingIds = new Set(list.map(x => x.id));
  const createdValid = (edits.created || []).filter(item => item && item.id && !edits.deleted[item.id] && !existingIds.has(item.id));
  return [...createdValid, ...list];
}

/**
 * ブロックリストデータの読み込み
 * INITIAL_BLOCKLIST + LocalStorage差分 + Firestore差分 (古いデータで上書きしない)
 */
async function loadBlocklistData() {
  const currentVersion = "v5";
  const base = (typeof INITIAL_BLOCKLIST !== "undefined" && Array.isArray(INITIAL_BLOCKLIST))
    ? INITIAL_BLOCKLIST
    : [];
  const edits = getBlocklistUserEdits();

  allBlocklist = applyBlocklistUserEditsToBase(base, edits);

  try {
    localStorage.setItem("neofamily_blocklist", JSON.stringify(allBlocklist));
    localStorage.setItem("neofamily_blocklist_version", currentVersion);
  } catch (e) {}

  // まずローカル/初期データ＋手動編集差分で即座に画面を描画（通信待ちゼロ）
  renderBlocklistKPI();
  renderAdminBlocklistTable();

  // Firestore の手動編集差分コレクション（blocklist_user_edits_v5）をバックグラウンドでマージ
  if (typeof firebase !== "undefined" && firebase.apps.length) {
    try {
      const db = firebase.firestore();
      const snap = await db.collection("blocklist_user_edits_v5").get();
      if (!snap.empty) {
        let changed = false;
        const latestEdits = getBlocklistUserEdits();
        snap.forEach(doc => {
          const data = doc.data();
          if (!data || !data.action) return;
          const id = doc.id;
          if (data.action === "delete") {
            if (!latestEdits.deleted[id]) {
              latestEdits.deleted[id] = true;
              delete latestEdits.updated[id];
              changed = true;
            }
          } else if (data.action === "update" && data.entry) {
            const localEntry = latestEdits.updated[id];
            const remoteTime = data.updatedAt || 0;
            const localTime = localEntry && localEntry._savedAt ? localEntry._savedAt : 0;
            if (!localEntry || remoteTime > localTime) {
              latestEdits.updated[id] = { ...data.entry, _savedAt: remoteTime };
              changed = true;
            }
          } else if (data.action === "create" && data.entry) {
            if (!latestEdits.deleted[id] && !latestEdits.created.some(c => c.id === id)) {
              latestEdits.created.unshift(data.entry);
              changed = true;
            }
          }
        });
        if (changed) {
          setBlocklistUserEdits(latestEdits);
          allBlocklist = applyBlocklistUserEditsToBase(base, latestEdits);
          localStorage.setItem("neofamily_blocklist", JSON.stringify(allBlocklist));
          renderBlocklistKPI();
          renderAdminBlocklistTable();
        }
      }
    } catch (err) {
      console.warn("[Blocklist] Firestore delta sync skipped:", err);
    }
  }
}

/**
 * ブロックリストのKPI集計・表示
 */
function renderBlocklistKPI() {
  const total = allBlocklist.length;
  let igCount = 0;
  let threadsCount = 0;
  let fbCount = 0;
  let otherCount = 0;

  allBlocklist.forEach(item => {
    const p = (item.platform || "").toLowerCase();
    if (p.includes("instagram")) igCount++;
    if (p.includes("threads")) threadsCount++;
    if (p.includes("facebook")) fbCount++;
    if (!p.includes("instagram") && !p.includes("threads") && !p.includes("facebook")) otherCount++;
  });

  const tabCountEl = document.getElementById("tab-blocklist-count");
  if (tabCountEl) tabCountEl.textContent = total;

  const totalEl = document.getElementById("blk-kpi-total");
  const igEl = document.getElementById("blk-kpi-instagram");
  const thEl = document.getElementById("blk-kpi-threads");
  const fbEl = document.getElementById("blk-kpi-facebook");
  const otEl = document.getElementById("blk-kpi-other");

  if (totalEl) totalEl.textContent = total.toLocaleString();
  if (igEl) igEl.textContent = igCount.toLocaleString();
  if (thEl) thEl.textContent = threadsCount.toLocaleString();
  if (fbEl) fbEl.textContent = fbCount.toLocaleString();
  if (otEl) otEl.textContent = otherCount.toLocaleString();
}

/**
 * 検索・絞り込み・ソート・ページネーション付きテーブル描画
 */
function renderAdminBlocklistTable() {
  const tbody = document.getElementById("blk-table-body");
  if (!tbody) return;

  const searchInput = document.getElementById("blk-search-input");
  const platformFilter = document.getElementById("blk-platform-filter");
  const sortFilter = document.getElementById("blk-sort-filter");

  const query = (searchInput ? searchInput.value : "").trim().toLowerCase();
  const selectedPlatform = platformFilter ? platformFilter.value : "all";
  const sortBy = sortFilter ? sortFilter.value : "date-desc";

  // 1. フィルタリング
  let filtered = allBlocklist.filter(item => {
    // プラットフォーム絞り込み
    if (selectedPlatform !== "all") {
      const p = (item.platform || "").toLowerCase();
      if (selectedPlatform === "その他") {
        // KPIの「その他/Web」と同じ条件（Instagram / Threads / Facebook を含まないもの）
        if (p.includes("instagram") || p.includes("threads") || p.includes("facebook")) {
          return false;
        }
      } else if (!p.includes(selectedPlatform.toLowerCase())) {
        return false;
      }
    }

    // 検索クエリ絞り込み
    if (query) {
      const matchName = (item.name || "").toLowerCase().includes(query);
      const matchUrl = (item.url || "").toLowerCase().includes(query);
      const matchUrl2 = (item.secondary_url || "").toLowerCase().includes(query);
      const matchReason = (item.reason || "").toLowerCase().includes(query);
      const matchReporter = (item.reporter || "").toLowerCase().includes(query);
      const matchDate = (item.date || "").toLowerCase().includes(query);
      if (!matchName && !matchUrl && !matchUrl2 && !matchReason && !matchReporter && !matchDate) {
        return false;
      }
    }

    return true;
  });

  // 2. ソート
  filtered.sort((a, b) => {
    if (sortBy === "date-desc") {
      return (b.date || "").localeCompare(a.date || "");
    } else if (sortBy === "date-asc") {
      return (a.date || "").localeCompare(b.date || "");
    } else if (sortBy === "name-asc") {
      return (a.name || "").localeCompare(b.name || "", "ja");
    }
    return 0;
  });

  // 件数表示の更新
  const filteredCountEl = document.getElementById("blk-filtered-count");
  if (filteredCountEl) filteredCountEl.textContent = filtered.length.toLocaleString();

  // 3. ページネーション計算
  const totalItems = filtered.length;
  const maxPages = Math.max(1, Math.ceil(totalItems / blocklistPerPage));
  if (blocklistCurrentPage > maxPages) blocklistCurrentPage = maxPages;
  if (blocklistCurrentPage < 1) blocklistCurrentPage = 1;

  const startIndex = (blocklistCurrentPage - 1) * blocklistPerPage;
  const endIndex = Math.min(startIndex + blocklistPerPage, totalItems);
  const pageItems = filtered.slice(startIndex, endIndex);

  // 4. テーブルHTMLの構築
  if (pageItems.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" class="py-12 text-center text-slate-400">
          <i class="fa-solid fa-magnifying-glass text-3xl mb-3 block text-slate-300"></i>
          <p class="font-bold text-sm">該当するブロック対象は見つかりませんでした</p>
          <p class="text-xs text-slate-400 mt-1">検索条件を変更するか、新規登録を行ってください。</p>
        </td>
      </tr>
    `;
    renderBlocklistPagination(0, 0, 0, 1, 1);
    return;
  }

  let html = "";
  pageItems.forEach(item => {
    const platformBadges = getPlatformBadgesHtml(item.platform, item.url, item.secondary_url, item.url_warning);
    const safeReason = item.reason ? escapeHtml(item.reason) : '<span class="text-slate-300">-</span>';

    // 登録日時の改行表示
    let dateHtml = '<span class="text-slate-400 text-[10px]">-</span>';
    if (item.date) {
      const parts = item.date.trim().split(" ");
      const dPart = parts[0];
      const tPart = parts.slice(1).join(" ");
      dateHtml = `
        <div class="text-[11px] font-bold text-slate-800 leading-tight">${escapeHtml(dPart)}</div>
        ${tPart ? `<div class="text-[10px] text-slate-400 font-mono mt-0.5 leading-tight">${escapeHtml(tPart)}</div>` : ''}
      `;
    }

    // 氏名 / 表示名のスタイリング（人名・屋号か、アカウント名か）
    let nameHtml = "";
    const rawName = (item.name || "").trim();
    if (rawName.startsWith("@")) {
      nameHtml = `<span class="inline-flex items-center gap-0.5 font-mono text-[11px] font-bold text-indigo-700 bg-indigo-50 border border-indigo-100 px-1.5 py-0.5 rounded break-all leading-tight"><i class="fa-solid fa-at text-[9px] text-indigo-400 shrink-0"></i>${escapeHtml(rawName.substring(1))}</span>`;
    } else if (rawName && rawName !== "（名称未記載）") {
      nameHtml = `<div class="font-bold text-slate-900 group-hover:text-rose-600 transition break-words text-xs leading-snug">${escapeHtml(rawName)}</div>`;
    } else {
      nameHtml = `<span class="text-slate-400 text-[11px] italic">（未記載）</span>`;
    }

    // 報告者の改行表示（氏名と部署）
    let repHtml = "";
    if (item.reporter) {
      const m = item.reporter.match(/^(.+?)[（\(](.+?)[）\)]$/);
      if (m) {
        repHtml = `
          <div class="text-[11px] font-bold text-slate-900 leading-tight truncate">${escapeHtml(m[1])}</div>
          <div class="text-[9px] text-slate-500 font-medium truncate mt-0.5 leading-tight" title="${escapeHtml(m[2])}">${escapeHtml(m[2])}</div>
        `;
      } else {
        repHtml = `<div class="text-[11px] font-bold text-slate-900 leading-tight truncate">${escapeHtml(item.reporter)}</div>`;
      }
    } else {
      repHtml = '<span class="text-slate-400 text-[10px]">-</span>';
    }

    html += `
      <tr class="hover:bg-slate-50/80 transition group">
        <!-- 登録日時（改行表示） -->
        <td class="py-3 px-3 whitespace-nowrap text-center shrink-0 w-24">
          ${dateHtml}
        </td>

        <!-- 氏名 / 表示名（幅広・見やすく） -->
        <td class="py-3 px-3 w-64 min-w-[200px] max-w-[280px] shrink-0">
          ${nameHtml}
        </td>

        <!-- プラットフォーム & URL -->
        <td class="py-3 px-3 w-60 min-w-[195px] max-w-[250px] shrink-0">
          ${platformBadges}
        </td>

        <!-- 理由・備考メモ（バランス調整） -->
        <td class="py-3 px-3 min-w-[190px] max-w-[320px]">
          <div class="text-xs text-slate-700 font-medium leading-relaxed break-words whitespace-pre-line" title="${escapeHtml(item.reason || '')}">
            ${safeReason}
          </div>
        </td>

        <!-- 報告者（部署と名前改行） -->
        <td class="py-3 px-2.5 w-36 min-w-[125px] max-w-[160px] shrink-0 text-center">
          <div class="bg-slate-100/90 py-1.5 px-2 rounded-lg border border-slate-200/50">
            ${repHtml}
          </div>
        </td>

        <!-- アクション（大きめで見やすい縦並びボタン） -->
        <td class="py-2.5 px-2 text-center whitespace-nowrap w-24 min-w-[92px] shrink-0">
          <div class="flex flex-col items-center justify-center gap-1.5">
            <button type="button" onclick="openBlocklistModal('${item.id}')" title="編集" class="w-full px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs flex items-center justify-center gap-1.5 transition shadow-2xs border border-slate-200/80 cursor-pointer">
              <i class="fa-solid fa-pen-to-square text-[11px]"></i>
              <span>編集</span>
            </button>
            <button type="button" onclick="openBlocklistDeleteModal('${item.id}')" title="削除" class="w-full px-2.5 py-1.5 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold text-xs flex items-center justify-center gap-1.5 transition shadow-2xs border border-rose-200/70 cursor-pointer">
              <i class="fa-solid fa-trash text-[11px]"></i>
              <span>削除</span>
            </button>
          </div>
        </td>
      </tr>
    `;
  });

  tbody.innerHTML = html;
  renderBlocklistPagination(startIndex + 1, endIndex, totalItems, blocklistCurrentPage, maxPages);
}

/**
 * プラットフォームバッジとURLリンクのHTML生成（警告注記シンプル版）
 */
function getPlatformBadgesHtml(platformStr, url1, url2, warning = "") {
  let html = '<div class="space-y-1">';

  if (url1) {
    html += renderSingleUrlBadge(url1, platformStr);
  }
  if (url2) {
    html += renderSingleUrlBadge(url2, "Threads / Instagram");
  }

  if (warning) {
    html += `
      <div class="inline-flex items-center gap-0.5 px-1 py-0.2 rounded text-[9px] font-bold bg-amber-50 text-amber-700 border border-amber-200">
        <i class="fa-solid fa-triangle-exclamation text-[8px] text-amber-500"></i>
        <span>${escapeHtml(warning)}</span>
      </div>
    `;
  }

  if (!url1 && !url2) {
    html += '<span class="text-slate-400 text-xs">URLなし</span>';
  }

  html += '</div>';
  return html;
}

function renderSingleUrlBadge(url, defaultPlatform) {
  const uLower = url.toLowerCase();
  let badgeColor = "bg-slate-100 text-slate-700 border-slate-200";
  let icon = '<i class="fa-solid fa-globe text-slate-500"></i>';
  let label = "Web";

  if (uLower.includes("instagram.com")) {
    badgeColor = "bg-pink-50 text-pink-700 border-pink-200";
    icon = '<i class="fa-brands fa-instagram text-pink-600"></i>';
    label = "IG";
  } else if (uLower.includes("threads.net") || uLower.includes("threads.com")) {
    badgeColor = "bg-slate-900 text-white border-slate-900";
    icon = '<i class="fa-brands fa-threads text-white"></i>';
    label = "Threads";
  } else if (uLower.includes("facebook.com")) {
    badgeColor = "bg-blue-50 text-blue-700 border-blue-200";
    icon = '<i class="fa-brands fa-facebook text-blue-600"></i>';
    label = "FB";
  }

  // URL短縮（コンパクト表示）
  let displayUrl = url.replace(/^https?:\/\/(www\.)?/, "");
  if (displayUrl.length > 26) {
    displayUrl = displayUrl.substring(0, 24) + "...";
  }

  return `
    <div class="flex items-center gap-1 flex-wrap">
      <span class="inline-flex items-center gap-0.5 px-1 py-0.2 rounded text-[9px] font-black border ${badgeColor}">
        ${icon}
        <span>${label}</span>
      </span>
      <a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer" class="text-rose-600 hover:text-rose-700 hover:underline font-mono text-[11px] font-semibold inline-flex items-center gap-0.5" title="${escapeHtml(url)}">
        <span>${escapeHtml(displayUrl)}</span>
        <i class="fa-solid fa-arrow-up-right-from-square text-[8px]"></i>
      </a>
      <button type="button" onclick="copyBlocklistUrl('${escapeHtml(url)}')" title="URLをコピー" class="text-slate-400 hover:text-slate-700 transition text-[10px] ml-0.5">
        <i class="fa-regular fa-copy"></i>
      </button>
    </div>
  `;
}

/**
 * ページネーションコントロールの描画
 */
function renderBlocklistPagination(from, to, total, currPage, maxPages) {
  const pageInfoEl = document.getElementById("blk-page-info");
  const buttonsEl = document.getElementById("blk-pagination-buttons");
  if (!pageInfoEl || !buttonsEl) return;

  if (total === 0) {
    pageInfoEl.textContent = "全 0 件";
    buttonsEl.innerHTML = "";
    return;
  }

  pageInfoEl.innerHTML = `全 <span class="text-slate-900 font-black">${total.toLocaleString()}</span> 件中 <span class="text-slate-900 font-black">${from}〜${to}</span> 件を表示 (ページ ${currPage} / ${maxPages})`;

  let btnHtml = "";

  // 「前へ」ボタン
  btnHtml += `
    <button onclick="goToBlocklistPage(${currPage - 1})" ${currPage <= 1 ? "disabled" : ""} class="px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-100 disabled:opacity-40 disabled:hover:bg-white text-slate-700 transition">
      <i class="fa-solid fa-chevron-left"></i>
    </button>
  `;

  // ページ番号ボタン（近隣のページのみ表示）
  const startP = Math.max(1, currPage - 2);
  const endP = Math.min(maxPages, currPage + 2);

  if (startP > 1) {
    btnHtml += `<button onclick="goToBlocklistPage(1)" class="px-2.5 py-1 rounded-lg border border-slate-200 bg-white hover:bg-slate-100 text-slate-700 text-xs">1</button>`;
    if (startP > 2) btnHtml += `<span class="px-1 text-slate-400">...</span>`;
  }

  for (let p = startP; p <= endP; p++) {
    const isCurrent = p === currPage;
    btnHtml += `
      <button onclick="goToBlocklistPage(${p})" class="px-2.5 py-1 rounded-lg border text-xs font-bold transition ${isCurrent ? "bg-rose-600 text-white border-rose-600 shadow-2xs" : "border-slate-200 bg-white hover:bg-slate-100 text-slate-700"}">
        ${p}
      </button>
    `;
  }

  if (endP < maxPages) {
    if (endP < maxPages - 1) btnHtml += `<span class="px-1 text-slate-400">...</span>`;
    btnHtml += `<button onclick="goToBlocklistPage(${maxPages})" class="px-2.5 py-1 rounded-lg border border-slate-200 bg-white hover:bg-slate-100 text-slate-700 text-xs">${maxPages}</button>`;
  }

  // 「次へ」ボタン
  btnHtml += `
    <button onclick="goToBlocklistPage(${currPage + 1})" ${currPage >= maxPages ? "disabled" : ""} class="px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-100 disabled:opacity-40 disabled:hover:bg-white text-slate-700 transition">
      <i class="fa-solid fa-chevron-right"></i>
    </button>
  `;

  buttonsEl.innerHTML = btnHtml;
}

function goToBlocklistPage(pageNum) {
  blocklistCurrentPage = pageNum;
  renderAdminBlocklistTable();
  const targetEl = document.getElementById("blk-search-input") || document.getElementById("tab-content-blocklist");
  if (targetEl) {
    const headerOffset = 90;
    const elementPosition = targetEl.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    window.scrollTo({
      top: Math.max(0, offsetPosition),
      behavior: "smooth"
    });
  }
}

function filterBlocklist() {
  blocklistCurrentPage = 1;
  renderAdminBlocklistTable();
}

function changeBlocklistPerPage(val) {
  blocklistPerPage = val === "all" ? 999999 : parseInt(val);
  blocklistCurrentPage = 1;
  renderAdminBlocklistTable();
}

/**
 * 新規追加・編集モーダルのオープン
 */
function openBlocklistModal(id = null) {
  const modalTitle = document.getElementById("blk-modal-title");
  const formId = document.getElementById("blk-form-id");
  const formName = document.getElementById("blk-form-name");
  const formUrl = document.getElementById("blk-form-url");
  const formUrl2 = document.getElementById("blk-form-url2");
  const formPlatform = document.getElementById("blk-form-platform");
  const formReason = document.getElementById("blk-form-reason");
  const formReporter = document.getElementById("blk-form-reporter");
  const formDate = document.getElementById("blk-form-date");
  const formWarning = document.getElementById("blk-form-warning");

  if (id) {
    // 編集モード
    const item = allBlocklist.find(b => b.id === id);
    if (!item) return;

    if (modalTitle) modalTitle.textContent = "ブロック対象の編集";
    if (formId) formId.value = item.id;
    if (formName) formName.value = item.name === "（名称未記載）" ? "" : (item.name || "");
    if (formUrl) formUrl.value = item.url || "";
    if (formUrl2) formUrl2.value = item.secondary_url || "";
    if (formPlatform) {
      const platVal = item.platform || "Instagram";
      // 選択肢にないプラットフォームの場合は動的に追加
      if (!Array.from(formPlatform.options).some(opt => opt.value === platVal)) {
        const opt = document.createElement("option");
        opt.value = platVal;
        opt.textContent = platVal;
        formPlatform.appendChild(opt);
      }
      formPlatform.value = platVal;
    }
    if (formReason) formReason.value = item.reason || "";
    if (formReporter) formReporter.value = item.reporter || "管理部";
    if (formDate) formDate.value = item.date || "";
    if (formWarning) formWarning.value = item.url_warning || "";
  } else {
    // 新規登録モード
    if (modalTitle) modalTitle.textContent = "ブロック対象の登録";
    if (formId) formId.value = "";
    if (formName) formName.value = "";
    if (formUrl) formUrl.value = "";
    if (formUrl2) formUrl2.value = "";
    if (formPlatform) formPlatform.value = "Instagram";
    if (formReason) formReason.value = "";
    if (formReporter) formReporter.value = "本多栞（RAYTUS / 秘書課）";
    if (formWarning) formWarning.value = "";
    
    // 現在日時をフォーマット設定
    const now = new Date();
    const y = now.getFullYear();
    const m = String(now.getMonth() + 1).padStart(2, '0');
    const d = String(now.getDate()).padStart(2, '0');
    const h = String(now.getHours()).padStart(2, '0');
    const min = String(now.getMinutes()).padStart(2, '0');
    if (formDate) formDate.value = `${y}-${m}-${d} ${h}:${min}`;
  }

  openModal("blocklist-modal");
  if (formName) setTimeout(() => formName.focus(), 100);
}

/**
 * URL入力時にプラットフォームを自動判定
 */
function autoDetectPlatform(url) {
  const sel = document.getElementById("blk-form-platform");
  if (!sel || !url) return;
  const u = url.toLowerCase();
  if (u.includes("instagram.com")) {
    sel.value = "Instagram";
  } else if (u.includes("threads.net") || u.includes("threads.com")) {
    sel.value = "Threads";
  } else if (u.includes("facebook.com")) {
    sel.value = "Facebook";
  } else {
    sel.value = "その他";
  }
}

/**
 * プラットフォームカード（KPI）クリック時の絞り込み
 */
function filterByPlatformCard(platform) {
  const filterSelect = document.getElementById("blk-platform-filter");
  if (filterSelect) {
    filterSelect.value = platform;
    filterBlocklist();
  }
}

/**
 * ブロックリスト登録・更新の送信ハンドラ
 */
async function handleBlocklistSubmit(e) {
  if (e) e.preventDefault();

  const id = (document.getElementById("blk-form-id")?.value || "").trim();
  const name = (document.getElementById("blk-form-name")?.value || "").trim();
  const url = (document.getElementById("blk-form-url")?.value || "").trim();
  const url2 = (document.getElementById("blk-form-url2")?.value || "").trim();
  const platform = document.getElementById("blk-form-platform")?.value || "その他";
  const reason = (document.getElementById("blk-form-reason")?.value || "").trim();
  const reporter = (document.getElementById("blk-form-reporter")?.value || "").trim() || "本多栞（RAYTUS / 秘書課）";
  const date = (document.getElementById("blk-form-date")?.value || "").trim();
  const warningEl = document.getElementById("blk-form-warning");
  const url_warning = warningEl ? warningEl.value.trim() : "";

  if (!id && !name && !url && !reason) {
    showToast("対象者名、URL、または理由を入力してください");
    return;
  }

  try {
    if (id) {
      // 既存更新（氏名欄を空にした場合も元の値に戻さず反映）
      const idx = allBlocklist.findIndex(b => b.id === id);
      if (idx !== -1) {
        const updatedEntry = {
          ...allBlocklist[idx],
          name: name || "（名称未記載）",
          url,
          secondary_url: url2,
          platform,
          reason,
          reporter,
          date: date || allBlocklist[idx].date || "",
          url_warning
        };
        allBlocklist[idx] = updatedEntry;
        saveBlocklistData(updatedEntry, "update");
        showToast(`「${name || url || '対象項目'}」の情報を保存しました`);
      }
    } else {
      // 新規追加
      const newId = `blk_${Date.now()}`;
      const newEntry = {
        id: newId,
        name: name || "（名称未記載）",
        url,
        secondary_url: url2,
        platform,
        reason,
        reporter,
        date: date || new Date().toISOString().replace('T', ' ').substring(0, 16),
        url_warning
      };
      allBlocklist.unshift(newEntry);
      saveBlocklistData(newEntry, "create");
      showToast(`「${name || url || '新規対象'}」をブロックリストに登録しました`);
    }
  } catch (err) {
    console.error("[Blocklist] Error in submit handler:", err);
    showToast("保存処理中にエラーが発生しました");
  }

  closeModal("blocklist-modal");
  renderBlocklistKPI();
  renderAdminBlocklistTable();
}

/**
 * 削除確認モーダルを開く
 */
function openBlocklistDeleteModal(id) {
  const item = allBlocklist.find(b => b.id === id);
  if (!item) return;

  blocklistDeleteTargetId = id;
  const nameEl = document.getElementById("blk-delete-name");
  if (nameEl) nameEl.textContent = item.name || item.url || "この対象";

  const confirmBtn = document.getElementById("blk-delete-confirm-btn");
  if (confirmBtn) {
    confirmBtn.onclick = async () => {
      await executeBlocklistDelete(id);
    };
  }

  openModal("blocklist-delete-modal");
}

/**
 * 削除実行
 */
async function executeBlocklistDelete(id) {
  const idx = allBlocklist.findIndex(b => b.id === id);
  if (idx === -1) return;

  const deletedName = allBlocklist[idx].name;
  const deletedItem = allBlocklist[idx];
  allBlocklist.splice(idx, 1);

  saveBlocklistData(deletedItem, "delete");

  closeModal("blocklist-delete-modal");
  blocklistDeleteTargetId = null;

  showToast(`「${deletedName}」をブロックリストから削除しました`);
  renderBlocklistKPI();
  renderAdminBlocklistTable();
}

/**
 * データの永続化 (LocalStorage 差分 + フルキャッシュ & Firestore 差分コレクション)
 * リロードしても初期データや古いFirestoreデータで上書きされないよう差分を永続化
 */
function saveBlocklistData(entry, action) {
  try {
    const edits = getBlocklistUserEdits();
    if (!edits.updated) edits.updated = {};
    if (!Array.isArray(edits.created)) edits.created = [];
    if (!Array.isArray(edits.deleted)) edits.deleted = [];

    if (action === "update" && entry && entry.id) {
      const createdIdx = edits.created.findIndex(c => c && c.id === entry.id);
      if (createdIdx !== -1) {
        edits.created[createdIdx] = { ...entry };
      } else {
        edits.updated[entry.id] = { ...entry };
      }
      edits.deleted = edits.deleted.filter(dId => dId !== entry.id);
    } else if (action === "create" && entry && entry.id) {
      edits.created = edits.created.filter(c => c && c.id !== entry.id);
      edits.created.unshift({ ...entry });
      edits.deleted = edits.deleted.filter(dId => dId !== entry.id);
    } else if (action === "delete" && entry && entry.id) {
      if (!edits.deleted.includes(entry.id)) {
        edits.deleted.push(entry.id);
      }
      delete edits.updated[entry.id];
      edits.created = edits.created.filter(c => c && c.id !== entry.id);
    }

    setBlocklistUserEdits(edits);
    localStorage.setItem("neofamily_blocklist", JSON.stringify(allBlocklist));
    localStorage.setItem("neofamily_blocklist_version", "v5");
  } catch (err) {
    console.error("[Blocklist] LocalStorage save error:", err);
  }

  // Firestore の専用差分コレクション (blocklist_user_edits_v5) に非同期同期
  if (typeof firebase !== "undefined" && firebase.apps.length && entry && entry.id) {
    try {
      const db = firebase.firestore();
      const docRef = db.collection("blocklist_user_edits_v5").doc(entry.id);
      if (action === "create" || action === "update") {
        docRef.set({
          action,
          id: entry.id,
          entry: { ...entry },
          updatedAt: new Date().toISOString()
        }, { merge: true }).catch(err => {
          console.warn("[Blocklist] Firestore edit sync error:", err);
        });
      } else if (action === "delete") {
        docRef.set({
          action: "delete",
          id: entry.id,
          updatedAt: new Date().toISOString()
        }).catch(err => {
          console.warn("[Blocklist] Firestore delete sync error:", err);
        });
      }
    } catch (err) {
      console.warn("[Blocklist] Firestore error:", err);
    }
  }
}

/**
 * スクリーンショット純粋文字起こし（全97枚）モーダル制御
 */
function openOcrTranscriptionModal() {
  const searchEl = document.getElementById("ocr-transcription-search");
  if (searchEl) searchEl.value = "";
  renderOcrTranscriptionList();
  openModal("ocr-transcription-modal");
}

function renderOcrTranscriptionList() {
  const bodyEl = document.getElementById("ocr-transcription-body");
  const countEl = document.getElementById("ocr-transcription-count");
  const searchEl = document.getElementById("ocr-transcription-search");
  if (!bodyEl) return;

  const list = typeof RAW_OCR_TRANSCRIPTIONS !== "undefined" && Array.isArray(RAW_OCR_TRANSCRIPTIONS)
    ? RAW_OCR_TRANSCRIPTIONS
    : [];
  const keyword = (searchEl?.value || "").trim().toLowerCase();

  const filtered = list.filter(item => {
    if (!keyword) return true;
    return (
      String(item.index).includes(keyword) ||
      (item.file || "").toLowerCase().includes(keyword) ||
      (item.text || "").toLowerCase().includes(keyword)
    );
  });

  if (countEl) {
    countEl.textContent = `全 ${list.length} 枚中 ${filtered.length} 枚を表示`;
  }

  if (filtered.length === 0) {
    bodyEl.innerHTML = `
      <div class="py-12 text-center text-slate-400">
        <p class="font-bold text-sm">一致するスクリーンショットが見つかりませんでした</p>
      </div>
    `;
    return;
  }

  let html = "";
  filtered.forEach(item => {
    const idxZero = item.index - 1;
    const numStr = String(item.index).padStart(2, "0");
    html += `
      <div class="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
        <div class="px-4 py-2.5 bg-slate-100/80 border-b border-slate-200 flex items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <span class="px-2 py-0.5 rounded-md bg-slate-800 text-white font-mono text-xs font-bold">#${numStr} / 97</span>
            <span class="font-mono text-xs font-bold text-slate-700">${escapeHtml(item.file || "")}</span>
          </div>
          <button type="button" onclick="copySingleOcrText(${idxZero})" class="px-2.5 py-1 rounded-md bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 text-[11px] font-bold flex items-center gap-1 transition cursor-pointer">
            <i class="fa-regular fa-copy"></i>
            <span>原文をコピー</span>
          </button>
        </div>
        <pre class="p-4 text-xs text-slate-800 font-mono whitespace-pre-wrap break-all leading-relaxed m-0 select-all bg-white">${escapeHtml(item.text || "")}</pre>
      </div>
    `;
  });

  bodyEl.innerHTML = html;
}

function copySingleOcrText(idx) {
  const list = typeof RAW_OCR_TRANSCRIPTIONS !== "undefined" && Array.isArray(RAW_OCR_TRANSCRIPTIONS)
    ? RAW_OCR_TRANSCRIPTIONS
    : [];
  const item = list[idx];
  if (!item || !navigator.clipboard) return;
  navigator.clipboard.writeText(item.text || "").then(() => {
    showToast(`#${String(item.index).padStart(2, "0")} (${item.file}) の文字起こしをコピーしました`);
  });
}

function downloadOcrTranscriptionText() {
  const list = typeof RAW_OCR_TRANSCRIPTIONS !== "undefined" && Array.isArray(RAW_OCR_TRANSCRIPTIONS)
    ? RAW_OCR_TRANSCRIPTIONS
    : [];
  if (list.length === 0) {
    showToast("文字起こしデータがありません");
    return;
  }
  const lines = [
    "LINEノート スクリーンショット純粋文字起こし（全97枚・要約/改変なし）",
    "======================================================================",
    ""
  ];
  list.forEach(item => {
    const numStr = String(item.index).padStart(2, "0");
    lines.push(`■ [${numStr}/97] ${item.file}`);
    lines.push("----------------------------------------------------------------------");
    lines.push(item.text || "");
    lines.push("");
  });
  const blob = new Blob([lines.join("\r\n")], { type: "text/plain;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "blocklist_raw_transcription_97.txt";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast("全97枚の純粋文字起こしテキストをダウンロードしました");
}

/**
 * ブロックリストのCSVエクスポート
 */
function exportBlocklistCSV() {
  if (allBlocklist.length === 0) {
    showToast("エクスポートするデータがありません");
    return;
  }

  const headers = ["ID", "登録日時", "氏名/屋号", "プラットフォーム", "URL", "予備URL", "ブロック理由・詳細メモ", "報告者"];
  const rows = allBlocklist.map(b => [
    b.id || "",
    b.date || "",
    b.name || "",
    b.platform || "",
    b.url || "",
    b.secondary_url || "",
    b.reason || "",
    b.reporter || ""
  ]);

  const csvContent = "\uFEFF" + [
    headers.map(h => `"${h.replace(/"/g, '""')}"`).join(","),
    ...rows.map(r => r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(","))
  ].join("\r\n");

  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  const today = new Date().toISOString().slice(0, 10);
  a.href = url;
  a.download = `neofamily_blocklist_${today}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  showToast("ブロックリストCSVをダウンロードしました");
}

/**
 * URLコピー用ヘルパー
 */
function copyBlocklistUrl(url) {
  if (!navigator.clipboard) {
    showToast("クリップボード機能が利用できません");
    return;
  }
  navigator.clipboard.writeText(url).then(() => {
    showToast("URLをクリップボードにコピーしました");
  }).catch(() => {
    showToast("URLのコピーに失敗しました");
  });
}


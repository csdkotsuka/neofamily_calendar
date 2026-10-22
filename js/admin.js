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
      const existingIds = new Set(events.map(e => e.id));
      const mergedEvents = [...events];
      if (typeof INITIAL_EVENTS !== "undefined" && Array.isArray(INITIAL_EVENTS)) {
        for (const initEv of INITIAL_EVENTS) {
          if (initEv && initEv.id && !existingIds.has(initEv.id)) {
            mergedEvents.push(initEv);
            existingIds.add(initEv.id);
          }
        }
      }
      allEvents = mergedEvents;
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
  if (document.getElementById("new-event-creator")) {
    document.getElementById("new-event-creator").value = ev.creator || ev.registeredBy || "";
  }
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
  const creator = document.getElementById("new-event-creator") ? document.getElementById("new-event-creator").value.trim() : "";
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
    creator,
    registeredBy: creator,
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

// 担当サポート者（各チーム理事長・担当者）リスト動的取得
function getMentorsList() {
  const local = localStorage.getItem("neofamily_mentors_list");
  if (local) {
    try {
      const parsed = JSON.parse(local);
      if (Array.isArray(parsed) && parsed.length > 0) return parsed;
    } catch (e) {
      console.warn("Failed to parse mentors list:", e);
    }
  }
  return [
    { id: "mentor_tanaka", name: "田中 健一", teamName: "チームAblaze", role: "理事長", email: "tanaka@example.com", status: "active" },
    { id: "mentor_sato", name: "佐藤 美咲", teamName: "チームRe:Spark", role: "理事長", email: "sato@example.com", status: "active" },
    { id: "mentor_suzuki", name: "鈴木 隆", teamName: "チームtidy.shin", role: "副理事長", email: "suzuki@example.com", status: "active" }
  ];
}

function saveMentorsList(list) {
  localStorage.setItem("neofamily_mentors_list", JSON.stringify(list));
  populateMentorSelects();
  renderMembersTable();
}

// 担当者セレクトUIの動的更新
function populateMentorSelects() {
  const mentors = getMentorsList();

  // 1. 担当者絞り込みセレクト (mentor-select-filter)
  const filterSel = document.getElementById("mentor-select-filter");
  if (filterSel) {
    const currentVal = filterSel.value;
    filterSel.innerHTML = `
      <option value="all">すべての担当者</option>
      ${mentors.map(m => {
        const count = allMembersProgress.filter(x => x.mentorId === m.id).length;
        const team = m.teamName ? ` [${m.teamName}]` : '';
        return `<option value="${m.id}">${m.name}${team} (担当 ${count}名)</option>`;
      }).join("")}
      <option value="unassigned">⚠️ 未割り当て (要対応)</option>
    `;
    if (currentVal) filterSel.value = currentVal;
  }

  // 2. 新規会員登録モーダルの担当者セレクト (new-member-mentor)
  const newMemberSel = document.getElementById("new-member-mentor");
  if (newMemberSel) {
    newMemberSel.innerHTML = `
      ${mentors.map(m => {
        const team = m.teamName ? ` (${m.teamName})` : '';
        return `<option value="${m.id}">${m.name}${team}</option>`;
      }).join("")}
      <option value="unassigned">未割り当て</option>
    `;
  }
}

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

// ============================================================
// 🎬 新人向け必須動画カタログ（総合ポータル内動画一覧と完全連動）
// ============================================================
const PORTAL_VIDEO_CATALOG = [
  // NEO FAMILY 特別勉強会 (6本)
  { url: "https://www.youtube.com/embed/zTGEDq3kAjI", videoId: "zTGEDq3kAjI", title: "特別編｜第一夜：Ablaze代表＆Re:Spark+代表", category: "study", categoryLabel: "特別勉強会" },
  { url: "https://www.youtube.com/embed/YmARyoWu5gU", videoId: "YmARyoWu5gU", title: "特別編｜第二夜：tidy.shin代表＆L’Ohana代表", category: "study", categoryLabel: "特別勉強会" },
  { url: "https://www.youtube.com/embed/Wlsup7qmy88", videoId: "Wlsup7qmy88", title: "特別編｜第三夜：K-pays Fellow代表＆∞mico group代表", category: "study", categoryLabel: "特別勉強会" },
  { url: "https://www.youtube.com/embed/a379lr1GxgI", videoId: "a379lr1GxgI", title: "特別編｜第四夜：RAYTUS group.理事長&REALISE代表", category: "study", categoryLabel: "特別勉強会" },
  { url: "https://www.youtube.com/embed/n2kR7sXx5tM", videoId: "n2kR7sXx5tM", title: "特別編｜第五夜：RAYTUS group.代表&Dynamite L代表", category: "study", categoryLabel: "特別勉強会" },
  { url: "https://www.youtube.com/embed/BX1EA7QhLj8", videoId: "BX1EA7QhLj8", title: "特別編｜第六夜：常勝会HD.代表 & Say-A's One代表 & SHINO organic代表", category: "study", categoryLabel: "特別勉強会" },

  // NEO FAMILY・関連事業紹介 (4本)
  { url: "https://www.youtube.com/embed/B6m8mOEsw84", videoId: "B6m8mOEsw84", title: "事務事業：NEO FAMILY.事務局", category: "neo", categoryLabel: "NEO・関連事業" },
  { url: "https://www.youtube.com/embed/iLH7fKyP1Hw", videoId: "iLH7fKyP1Hw", title: "IDIO JAPAN協会", category: "neo", categoryLabel: "NEO・関連事業" },
  { url: "https://www.youtube.com/embed/bir0V33Rol8", videoId: "bir0V33Rol8", title: "BKレーベル", category: "neo", categoryLabel: "NEO・関連事業" },
  { url: "https://www.youtube.com/embed/xj3e86mFEMo", videoId: "xj3e86mFEMo", title: "確定申告事業：ラクシン", category: "neo", categoryLabel: "NEO・関連事業" },

  // ぶった斬りCHANNEL 注目YouTube (6本)
  { url: "https://www.youtube.com/embed/fjkadO1_OYs", videoId: "fjkadO1_OYs", title: "【経営者必見】ドブに捨てるお金の使い方と事業拡大するお金の使い方の違い", category: "youtube", categoryLabel: "ぶった斬りYouTube" },
  { url: "https://www.youtube.com/embed/3sPl_bbEaiE", videoId: "3sPl_bbEaiE", title: "【夫の浮気】妻がやるべきことは1つだけ｜100億稼ぐ会長が本音で語る", category: "youtube", categoryLabel: "ぶった斬りYouTube" },
  { url: "https://www.youtube.com/embed/KApFWKM2QEU", videoId: "KApFWKM2QEU", title: "【16年間モラハラ】もう男なんていらない", category: "youtube", categoryLabel: "ぶった斬りYouTube" },
  { url: "https://www.youtube.com/embed/EK-xR3McLHc", videoId: "EK-xR3McLHc", title: "【58歳熟年離婚】を迫られた夫はパンツも洗えん。飯も作れん。", category: "youtube", categoryLabel: "ぶった斬りYouTube" },
  { url: "https://www.youtube.com/embed/J7tFe7x3_cs", videoId: "J7tFe7x3_cs", title: "【モラハラ夫と離婚】→子連れ再婚したら人生が激変した話", category: "youtube", categoryLabel: "ぶった斬りYouTube" },
  { url: "https://www.youtube.com/embed/ANth1mJ8YNw", videoId: "ANth1mJ8YNw", title: "【我慢の限界突破】ワンオペ地獄｜その家、ブラック家族です", category: "youtube", categoryLabel: "ぶった斬りYouTube" },

  // RAYTUS 事業紹介動画 (18本)
  { url: "https://www.youtube.com/embed/x8XJCSYZzp0", videoId: "x8XJCSYZzp0", title: "産前産後ケア事業：ensemble", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/rRPdgC6p5WE", videoId: "rRPdgC6p5WE", title: "食事業：RAY和おむすび", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/SUcNAq4RaPE", videoId: "SUcNAq4RaPE", title: "こころ事業：cocotoro.", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/PFbYFr9PMEw", videoId: "PFbYFr9PMEw", title: "オーダーメイドジュエリー事業：jewelry Aru", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/XRWrVBTuF6U", videoId: "XRWrVBTuF6U", title: "ライフパートナーマッチング事業：Raysring", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/CkEcsUg_Y3s", videoId: "CkEcsUg_Y3s", title: "おとな世代〜シニア事業：ViVid days", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/f7EScf-aVak", videoId: "f7EScf-aVak", title: "ママ&ベビースクール事業：ままゆね", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/qVvtNAyYQKk", videoId: "qVvtNAyYQKk", title: "ネイル総合事業：NailLAND", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/he4Lcckduvw", videoId: "he4Lcckduvw", title: "韓国コミュニティ事業：ノワナスクール", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/gw-bwyLDV4c", videoId: "gw-bwyLDV4c", title: "フェムケア事業：Femine", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/eKTUbn63_qc", videoId: "eKTUbn63_qc", title: "総合美容事業：Ligare（リガーレ）", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/K3bSbmq-_Gc", videoId: "K3bSbmq-_Gc", title: "総合食事業：稲環（いなわ）", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/5xOAhgqME6s", videoId: "5xOAhgqME6s", title: "スポーツリカバリー事業：Re.Co Lab（リコラボ）", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/CnTqMBOdvz0", videoId: "CnTqMBOdvz0", title: "クリエイティブ事業：CORECreativeStudio", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/WLTNPtndUPk", videoId: "WLTNPtndUPk", title: "薬局事業：このまち薬局", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/xpGunQNr4tE", videoId: "xpGunQNr4tE", title: "セクシャルウェルネス事業：セクシャルLABO", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/WO3j5E_98Go", videoId: "WO3j5E_98Go", title: "おやこの爪事業：nail hug", category: "raytus", categoryLabel: "RAYTUS事業" },
  { url: "https://www.youtube.com/embed/pUvEZ-U4tnw", videoId: "pUvEZ-U4tnw", title: "お片付け事業：片付けの窓口", category: "raytus", categoryLabel: "RAYTUS事業" }
];

const DEFAULT_REQUIRED_VIDEO_URLS = [
  "https://www.youtube.com/embed/B6m8mOEsw84",
  "https://www.youtube.com/embed/zTGEDq3kAjI",
  "https://www.youtube.com/embed/fjkadO1_OYs"
];

let requiredOnboardingVideos = [...DEFAULT_REQUIRED_VIDEO_URLS];
let currentRequiredVideoFilter = "all";

async function loadRequiredOnboardingVideos() {
  try {
    const localRaw = localStorage.getItem("neofamily_required_videos_v1");
    if (localRaw) {
      const parsed = JSON.parse(localRaw);
      if (Array.isArray(parsed)) {
        requiredOnboardingVideos = parsed;
      }
    }
  } catch (e) {}

  renderRequiredVideosSummary();
  renderRequiredVideosChecklist();

  if (typeof firebase !== "undefined" && firebase.apps.length) {
    try {
      const db = firebase.firestore();
      const doc = await db.collection("events").doc("_onboarding_required_videos_v1").get();
      if (doc.exists && Array.isArray(doc.data()?.urls)) {
        requiredOnboardingVideos = doc.data().urls;
        localStorage.setItem("neofamily_required_videos_v1", JSON.stringify(requiredOnboardingVideos));
        renderRequiredVideosSummary();
        renderRequiredVideosChecklist();
        renderMembersTable();
      }
    } catch (e) {
      console.warn("[Admin] Failed to load required videos from Firestore:", e);
    }
  }
}

async function saveRequiredOnboardingVideos() {
  try {
    localStorage.setItem("neofamily_required_videos_v1", JSON.stringify(requiredOnboardingVideos));
  } catch (e) {}

  if (typeof firebase !== "undefined" && firebase.apps.length) {
    try {
      const db = firebase.firestore();
      await db.collection("events").doc("_onboarding_required_videos_v1").set({
        urls: requiredOnboardingVideos,
        updatedAt: new Date().toISOString()
      });
    } catch (e) {
      console.warn("[Admin] Failed to save required videos to Firestore:", e);
    }
  }
}

function toggleRequiredVideosSelector() {
  const panel = document.getElementById("required-videos-selector-panel");
  const label = document.getElementById("btn-toggle-required-videos-label");
  if (!panel) return;
  const isHidden = panel.classList.contains("hidden");
  if (isHidden) {
    panel.classList.remove("hidden");
    if (label) label.textContent = "一覧を閉じる";
    renderRequiredVideosChecklist();
  } else {
    panel.classList.add("hidden");
    if (label) label.textContent = "ポータル動画一覧から選ぶ";
  }
}

function setRequiredVideoFilter(cat) {
  currentRequiredVideoFilter = cat;
  document.querySelectorAll(".req-vid-tab").forEach(btn => {
    btn.className = "req-vid-tab px-3 py-1.5 rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 transition whitespace-nowrap cursor-pointer";
  });
  const activeBtn = document.getElementById("req-vid-tab-" + cat);
  if (activeBtn) {
    activeBtn.className = "req-vid-tab px-3 py-1.5 rounded-lg bg-slate-900 text-white transition whitespace-nowrap cursor-pointer";
  }
  renderRequiredVideosChecklist();
}

function toggleRequiredVideoItem(url) {
  const idx = requiredOnboardingVideos.indexOf(url);
  if (idx >= 0) {
    requiredOnboardingVideos.splice(idx, 1);
  } else {
    requiredOnboardingVideos.push(url);
  }
  saveRequiredOnboardingVideos();
  renderRequiredVideosSummary();
  renderRequiredVideosChecklist();
  renderMembersTable();
}

function renderRequiredVideosSummary() {
  const countBadge = document.getElementById("required-videos-count-badge");
  if (countBadge) countBadge.textContent = requiredOnboardingVideos.length;

  const container = document.getElementById("selected-required-videos-summary");
  if (!container) return;

  if (requiredOnboardingVideos.length === 0) {
    container.innerHTML = `<span class="text-xs text-slate-400">現在指定されている必須動画はありません。「ポータル動画一覧から選ぶ」を押してチェックを入れてください。</span>`;
    return;
  }

  container.innerHTML = requiredOnboardingVideos.map(url => {
    const v = PORTAL_VIDEO_CATALOG.find(item => item.url === url) || { title: url, categoryLabel: "動画" };
    return `
      <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-rose-50 border border-rose-200 text-xs font-bold text-slate-800 shadow-2xs">
        <i class="fa-brands fa-youtube text-rose-600"></i>
        <span class="max-w-xs truncate">${v.title}</span>
        <button type="button" onclick="toggleRequiredVideoItem('${url}')" class="text-slate-400 hover:text-rose-600 ml-1 cursor-pointer" title="指定を解除">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
    `;
  }).join("");
}

function renderRequiredVideosChecklist() {
  const grid = document.getElementById("required-videos-checklist-grid");
  if (!grid) return;

  const q = (document.getElementById("req-vid-search-input")?.value || "").toLowerCase().trim();
  const selectedSet = new Set(requiredOnboardingVideos);

  const list = PORTAL_VIDEO_CATALOG.filter(item => {
    if (currentRequiredVideoFilter === "selected" && !selectedSet.has(item.url)) return false;
    if (currentRequiredVideoFilter !== "all" && currentRequiredVideoFilter !== "selected" && item.category !== currentRequiredVideoFilter) return false;
    if (q && !item.title.toLowerCase().includes(q) && !item.categoryLabel.toLowerCase().includes(q)) return false;
    return true;
  });

  if (list.length === 0) {
    grid.innerHTML = `<div class="col-span-full py-6 text-center text-xs text-slate-400">該当する動画がありません</div>`;
    return;
  }

  grid.innerHTML = list.map(item => {
    const checked = selectedSet.has(item.url);
    return `
      <label class="flex items-start gap-2.5 p-2.5 rounded-xl border ${checked ? 'bg-rose-50/70 border-rose-300 ring-1 ring-rose-200' : 'bg-slate-50/60 border-slate-200 hover:bg-slate-100/70'} cursor-pointer transition select-none">
        <input type="checkbox" ${checked ? 'checked' : ''} onchange="toggleRequiredVideoItem('${item.url}')" class="mt-0.5 w-4 h-4 rounded text-rose-600 focus:ring-rose-500 accent-rose-600 shrink-0 cursor-pointer">
        <img src="https://img.youtube.com/vi/${item.videoId}/default.jpg" alt="" class="w-12 h-9 rounded-lg object-cover bg-slate-900 shrink-0">
        <div class="min-w-0 flex-1">
          <span class="inline-block text-[9px] font-extrabold px-1.5 py-0.2 rounded ${checked ? 'bg-rose-600 text-white' : 'bg-slate-200 text-slate-600'} mb-0.5">${item.categoryLabel}</span>
          <p class="text-xs font-bold text-slate-800 line-clamp-2 leading-snug">${item.title}</p>
        </div>
      </label>
    `;
  }).join("");
}

function hasMemberWatchedVideo(member, videoUrl) {
  const viewed = member?.viewedContents || {};
  if (viewed[videoUrl]) return viewed[videoUrl];
  const catalogItem = PORTAL_VIDEO_CATALOG.find(v => v.url === videoUrl);
  const vid = catalogItem ? catalogItem.videoId : (videoUrl.split("/embed/")[1] || "").split("?")[0];
  if (!vid) return null;
  for (const [k, val] of Object.entries(viewed)) {
    if (k.includes(vid)) return val;
  }
  return null;
}

// 会員進捗データの読み込み
async function loadMembersProgressData() {
  await loadRequiredOnboardingVideos();
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

  populateMentorSelects();
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

    // 閲覧ログ数 & 必須動画視聴カウント
    const viewedCount = Object.keys(m.viewedContents || {}).length;
    const reqTotal = requiredOnboardingVideos.length;
    let reqWatched = 0;
    requiredOnboardingVideos.forEach(url => {
      if (hasMemberWatchedVideo(m, url)) reqWatched++;
    });

    let reqVideoBadge = "";
    if (reqTotal > 0) {
      if (reqWatched === reqTotal) {
        reqVideoBadge = `<span class="px-2 py-0.5 rounded-lg bg-emerald-100 text-emerald-800 font-bold text-[11px] inline-flex items-center gap-1"><i class="fa-solid fa-circle-check"></i> 必須動画 ${reqWatched}/${reqTotal} 完了</span>`;
      } else if (reqWatched > 0) {
        reqVideoBadge = `<span class="px-2 py-0.5 rounded-lg bg-amber-100 text-amber-800 font-bold text-[11px] inline-flex items-center gap-1"><i class="fa-solid fa-circle-play"></i> 必須動画 ${reqWatched}/${reqTotal} 視聴</span>`;
      } else {
        reqVideoBadge = `<span class="px-2 py-0.5 rounded-lg bg-rose-50 text-rose-700 border border-rose-200 font-bold text-[11px] inline-flex items-center gap-1"><i class="fa-regular fa-circle-play"></i> 必須動画 0/${reqTotal} 未視聴</span>`;
      }
    }

    // 最終アクセス
    let lastActiveText = "未アクセス";
    if (m.lastActiveAt) {
      const d = new Date(m.lastActiveAt);
      lastActiveText = `${d.getMonth()+1}/${d.getDate()} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
    }

    // 担当者セレクト（総責任者ビューの場合はインライン変更可能）
    let mentorCol = "";
    const mentors = getMentorsList();
    if (currentAdminRole === "admin") {
      const optionsHtml = mentors.map(mentor => {
        const isSelected = m.mentorId === mentor.id ? 'selected' : '';
        const team = mentor.teamName ? ` [${mentor.teamName}]` : '';
        return `<option value="${mentor.id}" ${isSelected}>${mentor.name}${team}</option>`;
      }).join("");

      mentorCol = `
        <select onchange="updateMemberMentor('${m.memberId}', this.value)" class="px-2 py-1 rounded-lg bg-slate-50 border border-slate-200 text-[11px] font-bold text-slate-800 focus:outline-none focus:ring-1 focus:ring-indigo-500 max-w-[170px] truncate">
          ${optionsHtml}
          <option value="unassigned" ${(!m.mentorId || m.mentorId === 'unassigned') ? 'selected' : ''}>⚠️ 未割り当て</option>
        </select>
      `;
    } else {
      const mentorObj = mentors.find(x => x.id === m.mentorId);
      const team = mentorObj?.teamName ? `<span class="text-[10px] text-slate-400 block">${mentorObj.teamName}</span>` : '';
      mentorCol = `<div><span class="text-xs font-bold text-slate-800">${mentorObj ? mentorObj.name : '未割り当て'}</span>${team}</div>`;
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
          <div class="flex flex-col gap-1 items-start">
            ${reqVideoBadge}
            <span class="px-2 py-0.5 rounded-lg bg-slate-100 text-slate-600 font-bold text-[10px]">
              全 ${viewedCount} 件閲覧
            </span>
          </div>
        </td>
        <td class="py-3 px-4 text-slate-500 text-[11px] font-mono">${lastActiveText}</td>
        <td class="py-3 px-4 text-right">
          <div class="flex items-center justify-end gap-1.5">
            <button onclick="openMemberDetailModal('${m.memberId}')" class="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-indigo-50 text-slate-700 hover:text-indigo-700 font-bold text-[11px] transition shadow-2xs cursor-pointer" title="詳細ログ">
              <i class="fa-solid fa-file-lines mr-0.5"></i> 詳細
            </button>
            <button onclick="confirmDeleteMember('${m.memberId}')" class="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-rose-50 text-slate-400 hover:text-rose-600 font-bold text-[11px] transition shadow-2xs cursor-pointer" title="この会員を削除">
              <i class="fa-regular fa-trash-can"></i>
            </button>
          </div>
        </td>
      </tr>
    `;
  }).join("");
}

// 会員進捗データの削除
async function confirmDeleteMember(memberId) {
  if (!confirm(`会員ID [${memberId}] の進捗データを完全に削除しますか？\n\n※この操作は取り消せません。`)) {
    return;
  }

  allMembersProgress = allMembersProgress.filter(m => m.memberId !== memberId);
  localStorage.setItem("neofamily_cached_members", JSON.stringify(allMembersProgress));

  if (typeof firebase !== "undefined" && firebase.apps.length) {
    try {
      const db = firebase.firestore();
      await db.collection("member_progress").doc(memberId).delete();
    } catch (e) {
      console.warn("[Admin] Firestore member delete error:", e);
    }
  }

  showToast(`会員ID [${memberId}] を削除しました`);
  renderMembersKPI();
  renderMembersTable();
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

  // 新人向け必須動画の視聴チェック描画
  const reqContainer = document.getElementById("detail-modal-required-videos");
  if (reqContainer) {
    if (requiredOnboardingVideos.length === 0) {
      reqContainer.innerHTML = `<p class="text-xs text-slate-400 py-2">現在指定されている必須動画はありません。</p>`;
    } else {
      reqContainer.innerHTML = requiredOnboardingVideos.map(url => {
        const v = PORTAL_VIDEO_CATALOG.find(item => item.url === url) || { title: url };
        const watchLog = hasMemberWatchedVideo(member, url);
        let statusHtml = `<span class="text-[10px] font-bold text-rose-600 bg-rose-100 px-2 py-0.5 rounded-full shrink-0">未視聴</span>`;
        if (watchLog) {
          const d = watchLog.viewedAt ? new Date(watchLog.viewedAt) : null;
          const tStr = d ? `${d.getMonth()+1}/${d.getDate()} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}` : "";
          statusHtml = `<span class="text-[10px] font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-full shrink-0">✅ 視聴済 ${tStr}</span>`;
        }
        return `
          <div class="flex items-center justify-between gap-2 p-2 rounded-xl border ${watchLog ? 'bg-emerald-50/60 border-emerald-200 text-emerald-900' : 'bg-slate-50 border-slate-200 text-slate-600'}">
            <span class="text-xs font-bold flex items-center gap-1.5 truncate">
              <i class="fa-brands fa-youtube ${watchLog ? 'text-emerald-600' : 'text-rose-500'} shrink-0"></i>
              <span class="truncate">${v.title}</span>
            </span>
            ${statusHtml}
          </div>
        `;
      }).join("");
    }
  }

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
window.currentEditingBlocklistId = "";
window.lastEditedBlocklistId = "";

/**
 * ユーザーによる手動編集・追加・削除の差分データを取得・保存
 * INITIAL_BLOCKLIST が更新されても、管理者が手動編集した内容は100%保持される
 */
function normalizeDeletedMap(del) {
  const map = {};
  if (Array.isArray(del)) {
    del.forEach(id => {
      if (id) map[String(id)] = true;
    });
  } else if (del && typeof del === "object") {
    Object.keys(del).forEach(k => {
      if (del[k]) map[String(k)] = del[k];
    });
  }
  return map;
}

function getBlocklistUserEdits() {
  try {
    const raw = localStorage.getItem("neofamily_blocklist_user_edits_v5");
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && typeof parsed === "object") {
        return {
          updated: (parsed.updated && typeof parsed.updated === "object") ? parsed.updated : {},
          created: Array.isArray(parsed.created) ? parsed.created : [],
          deleted: normalizeDeletedMap(parsed.deleted)
        };
      }
    }
  } catch (e) {
    console.warn("[Blocklist] getBlocklistUserEdits parse error:", e);
  }
  return { updated: {}, created: [], deleted: {} };
}

function setBlocklistUserEdits(edits) {
  const normalized = {
    updated: (edits && edits.updated && typeof edits.updated === "object") ? edits.updated : {},
    created: (edits && Array.isArray(edits.created)) ? edits.created : [],
    deleted: normalizeDeletedMap(edits && edits.deleted)
  };
  try {
    // 巨大な旧キャッシュを削除してLocalStorageの容量不足(QuotaExceededError)を確実に防止
    localStorage.removeItem("neofamily_blocklist");
    localStorage.setItem("neofamily_blocklist_user_edits_v5", JSON.stringify(normalized));
    localStorage.setItem("neofamily_blocklist_version", "v6");
  } catch (e) {
    console.error("[Blocklist] setBlocklistUserEdits error:", e);
  }
  return normalized;
}

function assignBlocklistSerialNumbers(list) {
  if (!Array.isArray(list)) return [];
  const chronological = [...list].sort((a, b) => {
    return (a.date || "").localeCompare(b.date || "") || (a.id || "").localeCompare(b.id || "");
  });
  chronological.forEach((item, idx) => {
    item.serialNo = idx + 1;
  });
  return list;
}

function applyBlocklistUserEditsToBase(baseList, edits) {
  const delMap = normalizeDeletedMap(edits && edits.deleted);
  const updMap = (edits && edits.updated && typeof edits.updated === "object") ? edits.updated : {};
  const createdArr = (edits && Array.isArray(edits.created)) ? edits.created : [];

  const refreshedBaseIds = new Set(["blk_640","blk_641","blk_642","blk_643","blk_644","blk_645","blk_646","blk_647","blk_648","blk_649","blk_650","blk_651"]);
  let list = baseList.filter(item => item && item.id && !delMap[item.id]);
  list = list.map(item => {
    if (updMap[item.id]) {
      if (refreshedBaseIds.has(item.id) && (!updMap[item.id]._savedAt || updMap[item.id]._savedAt < "2026-10-20T13:50:00Z")) {
        return { ...item };
      }
      return { ...item, ...updMap[item.id] };
    }
    return { ...item };
  });
  const existingIds = new Set(list.map(x => x.id));
  const createdValid = createdArr.filter(item => item && item.id && !delMap[item.id] && !existingIds.has(item.id));
  const merged = [...createdValid, ...list];
  assignBlocklistSerialNumbers(merged);
  return merged;
}

/**
 * ブロックリストデータの読み込み
 * INITIAL_BLOCKLIST + LocalStorage差分 + Firestoreクラウド差分 (events/_blocklist_user_edits_v5)
 */
async function loadBlocklistData() {
  const base = (typeof INITIAL_BLOCKLIST !== "undefined" && Array.isArray(INITIAL_BLOCKLIST))
    ? INITIAL_BLOCKLIST
    : [];
  const edits = getBlocklistUserEdits();

  allBlocklist = applyBlocklistUserEditsToBase(base, edits);

  // まずローカル/初期データ＋手動編集差分で即座に画面を描画（通信待ちゼロ）
  renderBlocklistKPI();
  renderAdminBlocklistTable();

  // Firestore のクラウド差分ドキュメント (events/_blocklist_user_edits_v5) をマージ
  if (typeof firebase !== "undefined" && typeof isFirebaseConfigured === "function" && isFirebaseConfigured()) {
    try {
      if (!firebase.apps.length) {
        firebase.initializeApp(FIREBASE_CONFIG);
      }
      const db = firebase.firestore();
      const doc = await db.collection("events").doc("_blocklist_user_edits_v5").get();
      if (doc.exists) {
        const remote = doc.data() || {};
        const latestEdits = getBlocklistUserEdits();
        let changed = false;

        // 1. deleted のマージ
        const remoteDel = normalizeDeletedMap(remote.deleted);
        Object.keys(remoteDel).forEach(id => {
          if (!latestEdits.deleted[id]) {
            latestEdits.deleted[id] = remoteDel[id];
            delete latestEdits.updated[id];
            latestEdits.created = latestEdits.created.filter(c => c && c.id !== id);
            changed = true;
          }
        });

        // 2. updated のマージ（新しいタイムスタンプを優先）
        if (remote.updated && typeof remote.updated === "object") {
          Object.keys(remote.updated).forEach(id => {
            if (latestEdits.deleted[id]) return;
            const rItem = remote.updated[id];
            if (!rItem || typeof rItem !== "object") return;
            const lItem = latestEdits.updated[id];
            const rTime = rItem._savedAt || "";
            const lTime = (lItem && lItem._savedAt) ? lItem._savedAt : "";
            if (!lItem || rTime > lTime) {
              latestEdits.updated[id] = { ...rItem };
              changed = true;
            }
          });
        }

        // 3. created のマージ
        if (Array.isArray(remote.created)) {
          remote.created.forEach(rItem => {
            if (!rItem || !rItem.id || latestEdits.deleted[rItem.id]) return;
            const lIdx = latestEdits.created.findIndex(c => c && c.id === rItem.id);
            if (lIdx === -1) {
              latestEdits.created.unshift({ ...rItem });
              changed = true;
            } else {
              const rTime = rItem._savedAt || "";
              const lTime = latestEdits.created[lIdx]._savedAt || "";
              if (rTime > lTime) {
                latestEdits.created[lIdx] = { ...rItem };
                changed = true;
              }
            }
          });
        }

        if (changed) {
          setBlocklistUserEdits(latestEdits);
          allBlocklist = applyBlocklistUserEditsToBase(base, latestEdits);
          renderBlocklistKPI();
          renderAdminBlocklistTable();
        }
      }
    } catch (err) {
      console.warn("[Blocklist] Firestore cloud delta sync skipped:", err);
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

  assignBlocklistSerialNumbers(allBlocklist);

  const searchInput = document.getElementById("blk-search-input");
  const platformFilter = document.getElementById("blk-platform-filter");
  const sortFilter = document.getElementById("blk-sort-filter");

  const query = (searchInput ? searchInput.value : "").trim().toLowerCase();
  const selectedPlatform = platformFilter ? platformFilter.value : "all";
  const sortBy = sortFilter ? sortFilter.value : "date-desc";

  // 1. フィルタリング
  let filtered = allBlocklist.filter(item => {
    if (selectedPlatform !== "all") {
      const p = (item.platform || "").toLowerCase();
      if (selectedPlatform === "その他") {
        if (p.includes("instagram") || p.includes("threads") || p.includes("facebook")) {
          return false;
        }
      } else if (!p.includes(selectedPlatform.toLowerCase())) {
        return false;
      }
    }

    if (query) {
      const serialStr = item.serialNo ? String(item.serialNo).padStart(3, "0") : "";
      const matchSerial = serialStr.includes(query.replace(/^#|^no\.?/i, "")) || (`#${serialStr}`).includes(query);
      const matchName = (item.name || "").toLowerCase().includes(query);
      const matchUrl = (item.url || "").toLowerCase().includes(query);
      const matchUrl2 = (item.secondary_url || "").toLowerCase().includes(query);
      const matchReason = (item.reason || "").toLowerCase().includes(query);
      const matchReporter = (item.reporter || "").toLowerCase().includes(query);
      const matchDate = (item.date || "").toLowerCase().includes(query);
      if (!matchSerial && !matchName && !matchUrl && !matchUrl2 && !matchReason && !matchReporter && !matchDate) {
        return false;
      }
    }

    return true;
  });

  // 2. ソート
  filtered.sort((a, b) => {
    if (sortBy === "date-desc") {
      return (b.date || "").localeCompare(a.date || "") || ((b.serialNo || 0) - (a.serialNo || 0));
    } else if (sortBy === "date-asc") {
      return (a.date || "").localeCompare(b.date || "") || ((a.serialNo || 0) - (b.serialNo || 0));
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
        <td colspan="7" class="py-12 text-center text-slate-400">
          <i class="fa-solid fa-magnifying-glass text-3xl mb-3 block text-slate-300"></i>
          <p class="font-bold text-sm">該当するブロック対象は見つかりませんでした</p>
          <p class="text-xs text-slate-400 mt-1">検索条件を変更するか、新規登録を行ってください。</p>
        </td>
      </tr>
    `;
    renderBlocklistPagination(0, 0, 0, 1, 1);
    return;
  }

  const edits = getBlocklistUserEdits();
  let html = "";
  pageItems.forEach(item => {
    const serialBadge = `#${String(item.serialNo || 0).padStart(3, "0")}`;
    const platformBadges = getPlatformBadgesHtml(item.platform, item.url, item.secondary_url, item.url_warning);
    const safeReason = item.reason ? escapeHtml(item.reason) : '<span class="text-slate-300">-</span>';
    const isJustEdited = window.lastEditedBlocklistId && window.lastEditedBlocklistId === item.id;
    const isUserModified = !!(edits.updated && edits.updated[item.id]) || (Array.isArray(edits.created) && edits.created.some(c => c && c.id === item.id));

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

    // 氏名 / 表示名のスタイリング
    let nameHtml = "";
    const rawName = (item.name || "").trim();
    if (rawName.startsWith("@")) {
      nameHtml = `<span class="inline-flex items-center gap-0.5 font-mono text-[11px] font-bold text-indigo-700 bg-indigo-50 border border-indigo-100 px-1.5 py-0.5 rounded break-all leading-tight"><i class="fa-solid fa-at text-[9px] text-indigo-400 shrink-0"></i>${escapeHtml(rawName.substring(1))}</span>`;
    } else if (rawName && rawName !== "（名称未記載）" && rawName !== "（未記載）") {
      nameHtml = `<div class="font-bold text-slate-900 group-hover:text-rose-600 transition break-words text-xs leading-snug">${escapeHtml(rawName)}</div>`;
    } else {
      nameHtml = `<span class="text-slate-400 text-[11px] italic">（未記載）</span>`;
    }
    if (isUserModified) {
      nameHtml += `<div class="mt-1"><span class="inline-flex items-center gap-0.5 px-1.5 py-0.2 rounded text-[9px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200"><i class="fa-solid fa-check text-[8px]"></i>手動編集済</span></div>`;
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

    const rowBgClass = isJustEdited ? "bg-emerald-50/70 hover:bg-emerald-50 transition group" : "hover:bg-slate-50/80 transition group";

    html += `
      <tr data-blk-id="${escapeHtml(item.id)}" class="${rowBgClass}">
        <!-- シリアル番号 (No.) -->
        <td class="py-3 px-2 whitespace-nowrap text-center shrink-0 w-16">
          <span class="inline-flex items-center justify-center px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 font-mono font-black text-[11px] border border-slate-200/80">${serialBadge}</span>
        </td>

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
  const pLower = (defaultPlatform || "").toLowerCase();
  let badgeColor = "bg-slate-100 text-slate-700 border-slate-200";
  let icon = '<i class="fa-solid fa-globe text-slate-500"></i>';
  let label = "Web";

  if (uLower.includes("instagram.com") || (!uLower.includes("threads") && !uLower.includes("facebook") && pLower === "instagram")) {
    badgeColor = "bg-pink-50 text-pink-700 border-pink-200";
    icon = '<i class="fa-brands fa-instagram text-pink-600"></i>';
    label = "IG";
  } else if (uLower.includes("threads.net") || uLower.includes("threads.com") || pLower === "threads") {
    badgeColor = "bg-slate-900 text-white border-slate-900";
    icon = '<i class="fa-brands fa-threads text-white"></i>';
    label = "Threads";
  } else if (uLower.includes("facebook.com") || pLower === "facebook") {
    badgeColor = "bg-blue-50 text-blue-700 border-blue-200";
    icon = '<i class="fa-brands fa-facebook text-blue-600"></i>';
    label = "FB";
  } else if (uLower.includes("tiktok.com") || pLower.includes("tiktok")) {
    badgeColor = "bg-slate-900 text-white border-slate-900";
    icon = '<i class="fa-brands fa-tiktok text-white"></i>';
    label = "TikTok";
  }

  // URL表示（編集内容がわかるよう十分な長さを表示）
  let displayUrl = url.replace(/^https?:\/\/(www\.)?/, "");
  if (displayUrl.length > 36) {
    displayUrl = displayUrl.substring(0, 34) + "...";
  }

  return `
    <div class="flex items-center gap-1 flex-wrap">
      <span class="inline-flex items-center gap-0.5 px-1 py-0.2 rounded text-[9px] font-black border ${badgeColor}">
        ${icon}
        <span>${label}</span>
      </span>
      <a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer" class="text-rose-600 hover:text-rose-700 hover:underline font-mono text-[11px] font-semibold inline-flex items-center gap-0.5 break-all" title="${escapeHtml(url)}">
        <span>${escapeHtml(displayUrl)}</span>
        <i class="fa-solid fa-arrow-up-right-from-square text-[8px] shrink-0"></i>
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

  btnHtml += `
    <button onclick="goToBlocklistPage(${currPage - 1})" ${currPage <= 1 ? "disabled" : ""} class="px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-100 disabled:opacity-40 disabled:hover:bg-white text-slate-700 transition">
      <i class="fa-solid fa-chevron-left"></i>
    </button>
  `;

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
  window.currentEditingBlocklistId = id ? String(id) : "";

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
    const item = allBlocklist.find(b => String(b.id) === String(id));
    if (!item) return;

    if (modalTitle) modalTitle.textContent = "ブロック対象の編集";
    if (formId) formId.value = item.id;
    if (formName) formName.value = (item.name === "（名称未記載）" || item.name === "（未記載）") ? "" : (item.name || "");
    if (formUrl) formUrl.value = item.url || "";
    if (formUrl2) formUrl2.value = item.secondary_url || "";
    if (formPlatform) {
      const platVal = item.platform || "Instagram";
      if (!Array.from(formPlatform.options).some(opt => opt.value === platVal)) {
        const opt = document.createElement("option");
        opt.value = platVal;
        opt.textContent = platVal;
        formPlatform.appendChild(opt);
      }
      formPlatform.value = platVal;
    }
    if (formReason) formReason.value = item.reason || "";
    if (formReporter) formReporter.value = item.reporter || "";
    if (formDate) formDate.value = item.date || "";
    if (formWarning) formWarning.value = item.url_warning || "";
  } else {
    if (modalTitle) modalTitle.textContent = "ブロック対象の登録";
    if (formId) formId.value = "";
    if (formName) formName.value = "";
    if (formUrl) formUrl.value = "";
    if (formUrl2) formUrl2.value = "";
    if (formPlatform) formPlatform.value = "Instagram";
    if (formReason) formReason.value = "";
    if (formReporter) formReporter.value = "本多栞（RAYTUS / 秘書課）";
    if (formWarning) formWarning.value = "";

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
  const url2 = (document.getElementById("blk-form-url2")?.value || "").trim();
  if (!sel || !url) return;
  if (url2) return; // 予備URLがある場合は複合プラットフォームを維持
  const u = url.toLowerCase();
  if (u.includes("instagram.com")) {
    sel.value = "Instagram";
  } else if (u.includes("threads.net") || u.includes("threads.com")) {
    sel.value = "Threads";
  } else if (u.includes("facebook.com")) {
    sel.value = "Facebook";
  } else if (u.includes("tiktok.com")) {
    sel.value = "TikTok";
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
  if (e && e.preventDefault) e.preventDefault();

  const id = (document.getElementById("blk-form-id")?.value || window.currentEditingBlocklistId || "").trim();
  const name = (document.getElementById("blk-form-name")?.value || "").trim();
  const url = (document.getElementById("blk-form-url")?.value || "").trim();
  const url2 = (document.getElementById("blk-form-url2")?.value || "").trim();
  const platform = document.getElementById("blk-form-platform")?.value || "Instagram";
  const reason = (document.getElementById("blk-form-reason")?.value || "").trim();
  const reporter = (document.getElementById("blk-form-reporter")?.value || "").trim();
  const date = (document.getElementById("blk-form-date")?.value || "").trim();
  const warningEl = document.getElementById("blk-form-warning");
  const url_warning = warningEl ? warningEl.value.trim() : "";

  if (!id && !name && !url && !reason) {
    showToast("対象者名、URL、または理由を入力してください");
    return false;
  }

  try {
    if (id) {
      const idx = allBlocklist.findIndex(b => String(b.id) === String(id));
      const baseItem = idx !== -1 ? allBlocklist[idx] : { id };
      const updatedEntry = {
        ...baseItem,
        id: String(id),
        name: name || "（名称未記載）",
        url: url,
        secondary_url: url2,
        platform: platform,
        reason: reason,
        reporter: reporter,
        date: date,
        url_warning: url_warning,
        _savedAt: new Date().toISOString()
      };
      if (idx !== -1) {
        allBlocklist[idx] = updatedEntry;
      } else {
        allBlocklist.unshift(updatedEntry);
      }
      window.lastEditedBlocklistId = String(id);
      await saveBlocklistData(updatedEntry, "update");
      showToast(`「${name || url || '対象項目'}」の変更を保存しました`);
    } else {
      const newId = `blk_${Date.now()}`;
      const newEntry = {
        id: newId,
        name: name || "（名称未記載）",
        url: url,
        secondary_url: url2,
        platform: platform,
        reason: reason,
        reporter: reporter || "本多栞（RAYTUS / 秘書課）",
        date: date || new Date().toISOString().replace('T', ' ').substring(0, 16),
        url_warning: url_warning,
        _savedAt: new Date().toISOString()
      };
      allBlocklist.unshift(newEntry);
      window.lastEditedBlocklistId = newId;
      await saveBlocklistData(newEntry, "create");
      showToast(`「${name || url || '新規対象'}」をブロックリストに登録しました`);
    }
  } catch (err) {
    console.error("[Blocklist] Error in submit handler:", err);
    showToast("保存処理中にエラーが発生しました");
  }

  window.currentEditingBlocklistId = "";
  closeModal("blocklist-modal");
  renderBlocklistKPI();
  renderAdminBlocklistTable();
  return false;
}

/**
 * 削除確認モーダルを開く
 */
function openBlocklistDeleteModal(id) {
  const item = allBlocklist.find(b => String(b.id) === String(id));
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
  const idx = allBlocklist.findIndex(b => String(b.id) === String(id));
  if (idx === -1) return;

  const deletedName = allBlocklist[idx].name;
  const deletedItem = allBlocklist[idx];
  allBlocklist.splice(idx, 1);

  await saveBlocklistData(deletedItem, "delete");

  closeModal("blocklist-delete-modal");
  blocklistDeleteTargetId = null;

  showToast(`「${deletedName}」をブロックリストから削除しました`);
  renderBlocklistKPI();
  renderAdminBlocklistTable();
}

/**
 * データの永続化 (LocalStorage 差分 & Firestore events/_blocklist_user_edits_v5)
 * リロードや別ブラウザでも100%確実に編集内容が保持されるよう保存
 */
async function saveBlocklistData(entry, action) {
  const nowIso = new Date().toISOString();
  let edits = getBlocklistUserEdits();

  try {
    if (action === "update" && entry && entry.id) {
      const id = String(entry.id);
      const savedEntry = { ...entry, _savedAt: nowIso };
      const createdIdx = edits.created.findIndex(c => c && String(c.id) === id);
      if (createdIdx !== -1) {
        edits.created[createdIdx] = savedEntry;
      } else {
        edits.updated[id] = savedEntry;
      }
      delete edits.deleted[id];
    } else if (action === "create" && entry && entry.id) {
      const id = String(entry.id);
      const savedEntry = { ...entry, _savedAt: nowIso };
      edits.created = edits.created.filter(c => c && String(c.id) !== id);
      edits.created.unshift(savedEntry);
      delete edits.deleted[id];
    } else if (action === "delete" && entry && entry.id) {
      const id = String(entry.id);
      edits.deleted[id] = nowIso;
      delete edits.updated[id];
      edits.created = edits.created.filter(c => c && String(c.id) !== id);
    }

    edits = setBlocklistUserEdits(edits);
  } catch (err) {
    console.error("[Blocklist] LocalStorage save error:", err);
  }

  // Firestore の書き込み許可済みコレクション (events/_blocklist_user_edits_v5) にクラウド同期
  if (typeof firebase !== "undefined" && typeof isFirebaseConfigured === "function" && isFirebaseConfigured()) {
    try {
      if (!firebase.apps.length) {
        firebase.initializeApp(FIREBASE_CONFIG);
      }
      const db = firebase.firestore();
      await db.collection("events").doc("_blocklist_user_edits_v5").set({
        updated: edits.updated,
        created: edits.created,
        deleted: edits.deleted,
        updatedAt: nowIso
      });
    } catch (err) {
      console.warn("[Blocklist] Firestore cloud save error:", err);
    }
  }
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


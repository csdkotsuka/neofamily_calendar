/**
 * NEO FAMILY Calendar - Admin Console Logic
 * 
 * Manages authentication, per-video archive analytics, access logs,
 * event CRUD, and system settings.
 */

const DEFAULT_ADMIN_PASSCODE = "neo2026";
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
  checkAdminAuth();
});

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
  e.preventDefault();
  const input = document.getElementById("admin-passcode-input");
  const errorEl = document.getElementById("admin-login-error");
  const entered = (input ? input.value : "").trim();
  const currentPasscode = (localStorage.getItem("neofamily_admin_passcode") || DEFAULT_ADMIN_PASSCODE).trim();

  if (entered === currentPasscode) {
    localStorage.setItem("neofamily_admin_auth", "true");
    if (errorEl) errorEl.classList.add("hidden");
    checkAdminAuth();
  } else {
    if (errorEl) {
      errorEl.classList.remove("hidden");
      errorEl.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i> パスコードが正しくありません。';
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
  updateDashboardKPIs(activeArchiveEvents, sanitizedLogs);

  // 4. Render Per-Video Analytics Table
  renderPerVideoAnalyticsTable(activeArchiveEvents, sanitizedLogs);

  // 5. Render Detailed Access Logs Table
  renderAdminLogsTable(sanitizedLogs);

  // 6. Render Events Management Table
  renderAdminEventsTable();
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
  const tabs = ["analytics", "events", "settings"];
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

  if (enteredCur !== curPass) {
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
    }
  });
}

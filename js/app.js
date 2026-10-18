/**
 * NEO FAMILY Calendar Application
 * Google Calendar ID: c_5a885f7923e2170ff9b443b58c3612f4ff58809d0287730da1c1d6680bd8fa20@group.calendar.google.com
 */

const GOOGLE_CALENDAR_ID = "c_5a885f7923e2170ff9b443b58c3612f4ff58809d0287730da1c1d6680bd8fa20@group.calendar.google.com";

// State
let allEvents = [];
let currentYear = 2026;
let currentMonth = 9; // 0-indexed: 9 = October
let selectedDate = null;
let currentCategory = "all";
let currentViewMode = "cards"; // "cards" | "week" | "calendar"
let currentSearch = "";
let unlockedArchives = new Set(); // Stores event IDs that have been unlocked in this session

// Week calendar state
let currentWeekStartDate = (function() {
  const today = new Date(2026, 9, 18);
  const day = today.getDay(); // 0 is Sunday
  const start = new Date(today);
  start.setDate(today.getDate() - day);
  start.setHours(0, 0, 0, 0);
  return start;
})();

// Initialize App
document.addEventListener("DOMContentLoaded", async () => {
  loadEventsFromLocal();
  initEventListeners();
  renderApp();

  // If Firebase is configured, fetch latest events from Firestore
  if (typeof fetchEventsFromFirestore === "function" && isFirebaseConfigured()) {
    const remoteEvents = await fetchEventsFromFirestore();
    if (remoteEvents && remoteEvents.length > 0) {
      applyEvents(remoteEvents);
      renderApp();
    }
  }
});

// Load events from local data & custom archives in localStorage
function loadEventsFromLocal() {
  applyEvents(INITIAL_EVENTS);
}

// Apply event list with localStorage overrides
function applyEvents(baseEvents) {
  const customArchives = JSON.parse(localStorage.getItem("neofamily_custom_archives") || "{}");
  const localCreatedEvents = JSON.parse(localStorage.getItem("neofamily_created_events") || "[]");

  const combined = [...baseEvents];
  // Avoid duplicates
  const existingIds = new Set(baseEvents.map(e => e.id));
  for (const created of localCreatedEvents) {
    if (!existingIds.has(created.id)) {
      combined.push(created);
    }
  }

  allEvents = combined.map(ev => {
    if (customArchives[ev.id]) {
      return {
        ...ev,
        archive: {
          ...ev.archive,
          ...customArchives[ev.id]
        }
      };
    }
    return ev;
  });
}

function loadEvents() {
  loadEventsFromLocal();
}

// Render the application based on state
function renderApp() {
  renderStats();
  renderWeekView();
  renderCalendarView();
  renderEventsList();
}

// Render header stats
function renderStats() {
  const octEvents = allEvents.filter(e => e.startDate.startsWith("2026-10"));
  const archiveEvents = allEvents.filter(e => e.archive && e.archive.hasArchive);
  
  const totalCountEl = document.getElementById("stat-total-count");
  const octCountEl = document.getElementById("stat-oct-count");
  const archiveCountEl = document.getElementById("stat-archive-count");
  
  if (totalCountEl) totalCountEl.textContent = allEvents.length;
  if (octCountEl) octCountEl.textContent = octEvents.length;
  if (archiveCountEl) archiveCountEl.textContent = archiveEvents.length;
}

// Filter events by selected category, search, and date
function getFilteredEvents() {
  return allEvents.filter(ev => {
    // Category filter
    if (currentCategory !== "all" && ev.category !== currentCategory) {
      return false;
    }
    // Search query
    if (currentSearch.trim() !== "") {
      const q = currentSearch.toLowerCase();
      const match = (
        ev.title.toLowerCase().includes(q) ||
        (ev.subtitle && ev.subtitle.toLowerCase().includes(q)) ||
        (ev.location && ev.location.toLowerCase().includes(q)) ||
        (ev.presenter && ev.presenter.toLowerCase().includes(q)) ||
        (ev.description && ev.description.toLowerCase().includes(q))
      );
      if (!match) return false;
    }
    // Selected Date filter
    if (selectedDate && ev.startDate !== selectedDate) {
      return false;
    }
    return true;
  }).sort((a, b) => {
    const dA = a.startDate + " " + a.startTime;
    const dB = b.startDate + " " + b.startTime;
    return dA.localeCompare(dB);
  });
}

// Filter events by selected category and search query for month calendar view
function getFilteredEventsForCalendar() {
  return allEvents.filter(ev => {
    // Category filter
    if (currentCategory !== "all" && ev.category !== currentCategory) {
      return false;
    }
    // Search query
    if (currentSearch.trim() !== "") {
      const q = currentSearch.toLowerCase();
      const match = (
        ev.title.toLowerCase().includes(q) ||
        (ev.subtitle && ev.subtitle.toLowerCase().includes(q)) ||
        (ev.location && ev.location.toLowerCase().includes(q)) ||
        (ev.presenter && ev.presenter.toLowerCase().includes(q)) ||
        (ev.description && ev.description.toLowerCase().includes(q))
      );
      if (!match) return false;
    }
    return true;
  });
}

// Render event cards list
function renderEventsList() {
  const container = document.getElementById("events-list-container");
  if (!container) return;

  const filtered = getFilteredEvents();
  
  // Date filter indicator
  const dateIndicator = document.getElementById("selected-date-indicator");
  if (dateIndicator) {
    if (selectedDate) {
      const [y, m, d] = selectedDate.split("-");
      dateIndicator.innerHTML = `
        <div class="inline-flex items-center gap-2 px-3 py-1.5 bg-rose-50 border border-rose-200 text-rose-700 text-sm rounded-full font-medium shadow-sm mb-4">
          <i class="fa-solid fa-calendar-day"></i>
          <span>${parseInt(m)}月${parseInt(d)}日の予定 (${filtered.length}件)</span>
          <button onclick="clearSelectedDate()" class="ml-1 text-rose-500 hover:text-rose-800 text-base">&times;</button>
        </div>
      `;
      dateIndicator.classList.remove("hidden");
    } else {
      dateIndicator.classList.add("hidden");
    }
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-16 text-center bg-white rounded-3xl border border-slate-200/80 p-8 shadow-sm">
        <div class="w-16 h-16 mx-auto mb-4 bg-slate-100 rounded-full flex items-center justify-center text-slate-400 text-2xl">
          <i class="fa-regular fa-calendar-xmark"></i>
        </div>
        <h3 class="text-lg font-bold text-slate-700 mb-1">該当するイベントが見つかりませんでした</h3>
        <p class="text-sm text-slate-500 mb-6">条件を変更するか、日付フィルターを解除してください。</p>
        <button onclick="resetFilters()" class="inline-flex items-center gap-2 px-5 py-2.5 bg-slate-800 hover:bg-slate-900 text-white text-sm font-semibold rounded-xl shadow transition">
          <i class="fa-solid fa-arrows-rotate"></i> 条件をリセット
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(ev => createEventCardHtml(ev)).join("");
}

// Create Event Card HTML
function createEventCardHtml(ev) {
  const [year, month, day] = ev.startDate.split("-");
  const dateObj = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
  const weekDays = ["日", "月", "火", "水", "木", "金", "土"];
  const weekDay = weekDays[dateObj.getDay()];
  const isWeekend = weekDay === "日" || weekDay === "土";

  const hasArchive = ev.archive && ev.archive.hasArchive;
  const isUnlocked = unlockedArchives.has(ev.id);

  const locationBadge = ev.locationType === "online" 
    ? `<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-sky-50 text-sky-700 border border-sky-200"><i class="fa-solid fa-video"></i> Zoom/オンライン</span>`
    : ev.locationType === "hybrid"
    ? `<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-50 text-purple-700 border border-purple-200"><i class="fa-solid fa-users-viewfinder"></i> リアル＆配信</span>`
    : `<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200"><i class="fa-solid fa-location-dot"></i> 現地開催</span>`;

  const allImgs = (ev.images && ev.images.length > 0) ? ev.images : (ev.image ? [ev.image] : []);

  return `
    <div class="glass-card rounded-2xl overflow-hidden flex flex-col justify-between border border-slate-200/90 hover:border-rose-300 transition duration-300">
      ${allImgs.length > 0 ? `
        <div class="relative w-full h-48 bg-slate-100 overflow-hidden group cursor-pointer" onclick="openEventDetail('${ev.id}')">
          <img src="${allImgs[0]}" alt="${ev.title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy">
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/10 to-transparent"></div>
          <div class="absolute bottom-3 left-3 right-3 flex justify-between items-end text-white">
            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-bold backdrop-blur-md bg-white/20 border border-white/30">
              <i class="fa-regular fa-image"></i> ${allImgs.length > 1 ? `チラシ ${allImgs.length}枚` : 'フライヤーあり'}
            </span>
            ${hasArchive ? `
              <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-bold bg-rose-600 text-white shadow-md">
                <i class="fa-solid fa-circle-play"></i> アーカイブ対応
              </span>
            ` : ""}
          </div>
        </div>
      ` : ""}

      <div class="p-5 flex-1 flex flex-col">
        <!-- Top meta -->
        <div class="flex items-center justify-between gap-2 mb-3">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold text-white shadow-sm" style="background-color: ${ev.categoryColor || '#e11d48'};">
              ${ev.category}
            </span>
            ${locationBadge}
          </div>
          ${hasArchive && !ev.image ? `
            <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-100 text-rose-700 border border-rose-200">
              <i class="fa-solid fa-video"></i> 録画あり
            </span>
          ` : ""}
        </div>

        <!-- Date & Time Banner -->
        <div class="flex items-baseline gap-2 mb-2">
          <span class="text-2xl font-black ${isWeekend ? 'text-rose-600' : 'text-slate-800'}">
            ${parseInt(month)}/${parseInt(day)} <span class="text-base font-bold">(${weekDay})</span>
          </span>
          <span class="text-sm font-semibold text-slate-600 bg-slate-100 px-2.5 py-0.5 rounded-md">
            <i class="fa-regular fa-clock text-xs mr-1 text-slate-400"></i>${ev.startTime} 〜 ${ev.endTime}
          </span>
        </div>

        <!-- Title & Subtitle -->
        <h3 class="text-base font-bold text-slate-900 leading-snug mb-1 hover:text-rose-600 transition cursor-pointer" onclick="openEventDetail('${ev.id}')">
          ${ev.title}
        </h3>
        ${ev.subtitle ? `
          <p class="text-xs text-rose-600 font-semibold mb-3 line-clamp-1">
            ${ev.subtitle}
          </p>
        ` : ""}

        <!-- Info details -->
        <div class="space-y-1.5 text-xs text-slate-600 my-2">
          <div class="flex items-start gap-2">
            <i class="fa-solid fa-location-dot mt-0.5 text-slate-400 w-3.5 text-center"></i>
            <span class="line-clamp-1">${ev.location}</span>
          </div>
          ${ev.presenter ? `
            <div class="flex items-start gap-2">
              <i class="fa-solid fa-user-tie mt-0.5 text-slate-400 w-3.5 text-center"></i>
              <span class="line-clamp-1">${ev.presenter}</span>
            </div>
          ` : ""}
          ${ev.fee ? `
            <div class="flex items-start gap-2">
              <i class="fa-solid fa-ticket mt-0.5 text-slate-400 w-3.5 text-center"></i>
              <span>${ev.fee} ${ev.capacity ? `· 定員: ${ev.capacity}` : ''}</span>
            </div>
          ` : ""}
        </div>

        <!-- Archive Status Banner if applicable -->
        ${hasArchive ? `
          <div class="mt-3 p-2.5 rounded-xl ${isUnlocked ? 'bg-emerald-50 border border-emerald-200' : 'bg-rose-50 border border-rose-200'} flex items-center justify-between">
            <div class="flex items-center gap-2">
              <i class="${isUnlocked ? 'fa-solid fa-lock-open text-emerald-600' : 'fa-solid fa-lock text-rose-600'} text-sm"></i>
              <span class="text-xs font-bold ${isUnlocked ? 'text-emerald-800' : 'text-rose-800'}">
                ${isUnlocked ? 'アーカイブ視聴可能 (解除済)' : 'Zoom録画アーカイブ (要パスワード)'}
              </span>
            </div>
            <button onclick="handleArchiveClick('${ev.id}')" class="px-2.5 py-1 text-xs font-bold rounded-lg ${isUnlocked ? 'bg-emerald-600 hover:bg-emerald-700 text-white' : 'bg-rose-600 hover:bg-rose-700 text-white'} shadow-sm transition">
              ${isUnlocked ? '見る' : '解除して見る'}
            </button>
          </div>
        ` : ""}
      </div>

      <!-- Action Buttons -->
      <div class="p-4 pt-2 bg-slate-50/70 border-t border-slate-100 flex items-center gap-2">
        <button onclick="openEventDetail('${ev.id}')" class="flex-1 py-2 px-3 bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 shadow-sm">
          <i class="fa-solid fa-circle-info"></i> 詳細
        </button>

        <!-- Google Calendar Button -->
        <a href="${getGoogleCalendarUrl(ev)}" target="_blank" rel="noopener noreferrer" class="py-2 px-3 bg-blue-50 hover:bg-blue-100 border border-blue-200 text-blue-700 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1 shadow-sm" title="Googleカレンダーに追加">
          <i class="fa-brands fa-google"></i> 追加
        </a>

        <!-- ICS Download Button -->
        <button onclick="downloadSingleICS('${ev.id}')" class="py-2 px-3 bg-rose-50 hover:bg-rose-100 border border-rose-200 text-rose-700 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1 shadow-sm" title="スマホカレンダー(.ics)に登録">
          <i class="fa-solid fa-calendar-plus"></i> スマホ登録
        </button>
      </div>
    </div>
  `;
}

// Generate Google Calendar Add URL
function getGoogleCalendarUrl(ev) {
  const sDate = ev.startDate.replace(/-/g, "") + "T" + ev.startTime.replace(/:/g, "") + "00";
  const eDate = ev.endDate.replace(/-/g, "") + "T" + ev.endTime.replace(/:/g, "") + "00";
  
  let details = `${ev.subtitle || ''}\n\n${ev.description || ''}`;
  if (ev.zoomUrl) {
    details += `\n\nZoom参加URL: ${ev.zoomUrl}`;
    if (ev.zoomMeetingId) details += `\nミーティングID: ${ev.zoomMeetingId}`;
    if (ev.zoomPasscode) details += `\nパスコード: ${ev.zoomPasscode}`;
  }
  
  const params = new URLSearchParams({
    action: "TEMPLATE",
    text: ev.title,
    dates: `${sDate}/${eDate}`,
    details: details,
    location: ev.location || "オンライン"
  });

  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

// Render Native Month Calendar
function renderCalendarView() {
  const grid = document.getElementById("calendar-days-grid");
  const monthTitle = document.getElementById("calendar-month-title");
  if (!grid || !monthTitle) return;

  const monthNames = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"];
  monthTitle.textContent = `${currentYear}年 ${monthNames[currentMonth]}`;

  // First day of current month
  const firstDay = new Date(currentYear, currentMonth, 1);
  const startingDay = firstDay.getDay(); // 0 = Sunday
  const lastDate = new Date(currentYear, currentMonth + 1, 0).getDate();
  const prevMonthLastDate = new Date(currentYear, currentMonth, 0).getDate();

  let html = "";

  // Previous month trailing days
  for (let i = startingDay - 1; i >= 0; i--) {
    const dayNum = prevMonthLastDate - i;
    html += `
      <div class="calendar-day-cell other-month">
        <span class="text-xs font-bold text-slate-400">${dayNum}</span>
      </div>
    `;
  }

  // Filtered events for calendar according to category and search
  const calendarFilteredEvents = getFilteredEventsForCalendar();

  // Current month days
  for (let day = 1; day <= lastDate; day++) {
    const monthStr = String(currentMonth + 1).padStart(2, "0");
    const dayStr = String(day).padStart(2, "0");
    const dateStr = `${currentYear}-${monthStr}-${dayStr}`;

    const daysEvents = calendarFilteredEvents.filter(e => e.startDate === dateStr);
    const isSelected = selectedDate === dateStr;
    const isToday = (currentYear === 2026 && currentMonth === 9 && day === 18); // System date: 2026-10-18

    const dateObj = new Date(currentYear, currentMonth, day);
    const dayOfWeek = dateObj.getDay();
    const isSunday = dayOfWeek === 0;
    const isSaturday = dayOfWeek === 6;

    let dayNumberColor = "text-slate-700";
    if (isSunday) dayNumberColor = "text-rose-600";
    else if (isSaturday) dayNumberColor = "text-blue-600";

    html += `
      <div class="calendar-day-cell ${isSelected ? 'is-selected' : ''} ${isToday ? 'is-today' : ''}" onclick="selectDate('${dateStr}')">
        <div class="flex items-center justify-between">
          <span class="text-xs md:text-sm font-black ${dayNumberColor}">${day}</span>
          ${isToday ? `<span class="text-[9px] font-extrabold bg-rose-600 text-white px-1 rounded">今日</span>` : ''}
        </div>
        
        <div class="flex-1 overflow-hidden mt-1 flex flex-col gap-1">
          ${daysEvents.slice(0, 2).map(ev => `
            <div class="truncate text-[10px] md:text-xs font-semibold px-1.5 py-0.5 rounded text-white cursor-pointer hover:brightness-110 active:scale-95 transition shadow-xs" 
                 style="background-color: ${ev.categoryColor || '#e11d48'};" 
                 title="${ev.title} (クリックで詳細)" 
                 onclick="event.stopPropagation(); openEventDetail('${ev.id}');"
                 ondblclick="event.stopPropagation(); openEventDetail('${ev.id}');">
              ${ev.title}
            </div>
          `).join("")}
          ${daysEvents.length > 2 ? `
            <span class="text-[9px] font-bold text-slate-500 self-end cursor-pointer" onclick="event.stopPropagation(); selectDate('${dateStr}');">+他${daysEvents.length - 2}件</span>
          ` : ""}
        </div>
      </div>
    `;
  }

  // Next month leading days
  const totalCells = startingDay + lastDate;
  const nextDays = (7 - (totalCells % 7)) % 7;
  for (let i = 1; i <= nextDays; i++) {
    html += `
      <div class="calendar-day-cell other-month">
        <span class="text-xs font-bold text-slate-400">${i}</span>
      </div>
    `;
  }

  grid.innerHTML = html;
}

// Select a date on calendar (does NOT scroll or jump elsewhere)
function selectDate(dateStr) {
  if (selectedDate === dateStr) {
    selectedDate = null;
  } else {
    selectedDate = dateStr;
  }
  renderApp();
}

// Clear selected date
function clearSelectedDate() {
  selectedDate = null;
  renderApp();
}

// Change month
function changeMonth(delta) {
  currentMonth += delta;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  } else if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  }
  renderCalendarView();
}

// Change week
function changeWeek(delta) {
  currentWeekStartDate.setDate(currentWeekStartDate.getDate() + (delta * 7));
  renderWeekView();
}

// Go to current week
function goToCurrentWeek() {
  const today = new Date(2026, 9, 18);
  const day = today.getDay();
  currentWeekStartDate = new Date(today);
  currentWeekStartDate.setDate(today.getDate() - day);
  currentWeekStartDate.setHours(0, 0, 0, 0);
  renderWeekView();
}

// Layout overlapping events in the same day
function layoutDayEvents(events) {
  if (!events || events.length === 0) return [];

  const items = events.map(e => {
    let [sH, sM] = (e.startTime || "10:00").split(":").map(Number);
    let [eH, eM] = (e.endTime || "11:00").split(":").map(Number);
    if (eH === 0) eH = 24;
    const sMin = sH * 60 + (sM || 0);
    let eMin = eH * 60 + (eM || 0);
    if (eMin <= sMin) eMin = sMin + 60;
    return { event: e, sMin, eMin };
  });

  items.sort((a, b) => a.sMin - b.sMin || (b.eMin - b.sMin) - (a.eMin - a.sMin));

  const columns = [];
  items.forEach(item => {
    let placed = false;
    for (let c = 0; c < columns.length; c++) {
      if (columns[c][columns[c].length - 1].eMin <= item.sMin) {
        columns[c].push(item);
        item.colIdx = c;
        placed = true;
        break;
      }
    }
    if (!placed) {
      item.colIdx = columns.length;
      columns.push([item]);
    }
  });

  items.forEach(item => {
    const overlapping = items.filter(o => Math.max(item.sMin, o.sMin) < Math.min(item.eMin, o.eMin));
    const maxCol = Math.max(...overlapping.map(o => o.colIdx));
    item.totalCols = maxCol + 1;
  });

  items.forEach(item => {
    const overlapping = items.filter(o => Math.max(item.sMin, o.sMin) < Math.min(item.eMin, o.eMin));
    item.totalCols = Math.max(...overlapping.map(o => o.totalCols));
  });

  return items;
}

// Render Weekly Timetable View
function renderWeekView() {
  const container = document.getElementById("week-timetable-container");
  const titleEl = document.getElementById("week-range-title");
  if (!container) return;

  const weekDays = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date(currentWeekStartDate);
    d.setDate(currentWeekStartDate.getDate() + i);
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    weekDays.push({
      date: d,
      dateStr: `${y}-${m}-${day}`,
      year: y,
      month: d.getMonth() + 1,
      day: d.getDate(),
      dayOfWeek: d.getDay(),
      dayName: ["日", "月", "火", "水", "木", "金", "土"][d.getDay()]
    });
  }

  // Update Range Title
  const first = weekDays[0];
  const last = weekDays[6];
  if (titleEl) {
    if (first.year === last.year) {
      titleEl.textContent = `${first.year}年 ${first.month}月${first.day}日(${first.dayName}) 〜 ${last.month}月${last.day}日(${last.dayName})`;
    } else {
      titleEl.textContent = `${first.year}年${first.month}月${first.day}日(${first.dayName}) 〜 ${last.year}年${last.month}月${last.day}日(${last.dayName})`;
    }
  }

  const START_HOUR = 8;
  const END_HOUR = 24;
  const TOTAL_HOURS = END_HOUR - START_HOUR; // 16 hours
  const HOUR_HEIGHT = 60; // 60px per hour
  const TOTAL_HEIGHT = TOTAL_HOURS * HOUR_HEIGHT; // 960px

  const filtered = getFilteredEventsForCalendar();

  // Build Timetable HTML
  let html = `
    <div class="min-w-[760px] select-none text-slate-800">
      <!-- Days Header Row -->
      <div class="grid grid-cols-[60px_repeat(7,1fr)] border-b border-slate-200 bg-slate-50/95 sticky top-0 z-20">
        <!-- Time header empty cell -->
        <div class="p-2.5 text-center text-[10px] font-bold text-slate-400 border-r border-slate-200 flex items-center justify-center">
          時間
        </div>
  `;

  // Render 7 Day Headers
  weekDays.forEach(d => {
    const isToday = d.dateStr === "2026-10-18";
    const isSunday = d.dayOfWeek === 0;
    const isSaturday = d.dayOfWeek === 6;

    let dayColor = "text-slate-700";
    let bgHeader = "";
    if (isSunday) {
      dayColor = "text-rose-600";
      bgHeader = "bg-rose-50/40";
    } else if (isSaturday) {
      dayColor = "text-blue-600";
      bgHeader = "bg-blue-50/40";
    }

    html += `
      <div class="p-2 text-center border-r border-slate-200 last:border-r-0 ${bgHeader} ${isToday ? 'bg-rose-50/80' : ''}">
        <div class="text-[11px] font-bold ${dayColor}">${d.dayName}</div>
        <div class="mt-0.5 flex items-center justify-center">
          ${isToday ? `
            <span class="inline-flex items-center justify-center w-7 h-7 rounded-full bg-rose-600 text-white font-extrabold text-xs shadow-xs">
              ${d.day}
            </span>
          ` : `
            <span class="text-sm font-extrabold ${dayColor}">
              ${d.day}
            </span>
          `}
        </div>
      </div>
    `;
  });

  html += `
      </div>
      <!-- Timetable Body: Time axis + 7 columns -->
      <div class="relative grid grid-cols-[60px_repeat(7,1fr)] bg-white" style="height: ${TOTAL_HEIGHT}px;">
  `;

  // Time Axis Column
  html += `
    <div class="relative border-r border-slate-200 bg-slate-50/40 text-slate-400 text-[10px] font-semibold text-right pr-2">
  `;
  for (let h = START_HOUR; h < END_HOUR; h++) {
    html += `
      <div class="h-[60px] border-b border-slate-100 flex items-start justify-end pt-1">
        <span>${h}:00</span>
      </div>
    `;
  }
  html += `</div>`;

  // 7 Day Columns with Events
  weekDays.forEach(d => {
    const isToday = d.dateStr === "2026-10-18";
    const dayEvs = filtered.filter(e => e.startDate === d.dateStr);
    const layoutItems = layoutDayEvents(dayEvs);

    html += `
      <div class="relative border-r border-slate-200 last:border-r-0 ${isToday ? 'bg-rose-50/10' : ''}">
    `;

    // Hour grid lines background
    for (let h = START_HOUR; h < END_HOUR; h++) {
      html += `
        <div class="h-[60px] border-b border-slate-100"></div>
      `;
    }

    // Current time indicator line if today
    if (isToday) {
      const now = new Date();
      const currentMin = now.getHours() * 60 + now.getMinutes();
      if (currentMin >= START_HOUR * 60 && currentMin <= END_HOUR * 60) {
        const nowTop = ((currentMin - START_HOUR * 60) / 60) * HOUR_HEIGHT;
        html += `
          <div class="absolute left-0 right-0 z-30 pointer-events-none flex items-center" style="top: ${nowTop}px;">
            <div class="w-2.5 h-2.5 rounded-full bg-rose-600 -ml-1.5 shadow-xs"></div>
            <div class="flex-1 h-[2px] bg-rose-600"></div>
          </div>
        `;
      }
    }

    // Render Event Cards
    layoutItems.forEach(item => {
      const ev = item.event;
      const relStartMin = Math.max(0, item.sMin - START_HOUR * 60);
      const topPx = (relStartMin / 60) * HOUR_HEIGHT;
      const durationMin = Math.max(30, item.eMin - item.sMin);
      const heightPx = Math.max(38, (durationMin / 60) * HOUR_HEIGHT - 3);

      const colWidthPct = 100 / item.totalCols;
      const leftPct = item.colIdx * colWidthPct;
      const widthPct = colWidthPct;

      const hasArchive = ev.archive && ev.archive.hasArchive;
      const isZoom = ev.location && (ev.location.toLowerCase().includes("zoom") || ev.location.includes("オンライン"));

      html += `
        <div class="absolute rounded-xl p-2 text-white shadow-sm cursor-pointer hover:shadow-lg hover:brightness-110 active:scale-[0.98] transition-all overflow-hidden z-10 flex flex-col justify-start border border-white/20"
             style="top: ${topPx}px; height: ${heightPx}px; left: calc(${leftPct}% + 2px); width: calc(${widthPct}% - 4px); background-color: ${ev.categoryColor || '#e11d48'};"
             title="${ev.title}\n時間: ${ev.startTime}〜${ev.endTime}\n場所: ${ev.location}"
             onclick="event.stopPropagation(); openEventDetail('${ev.id}')"
             ondblclick="event.stopPropagation(); openEventDetail('${ev.id}')">
          <div class="flex items-center justify-between text-[10px] font-extrabold leading-none mb-1 opacity-95">
            <span class="bg-black/20 px-1 py-0.5 rounded">${ev.startTime} - ${ev.endTime}</span>
            ${hasArchive ? `<span class="bg-white/30 px-1 py-0.5 rounded text-[9px] flex items-center gap-0.5"><i class="fa-solid fa-video"></i> 録画</span>` : (isZoom ? `<i class="fa-solid fa-video text-[9px]"></i>` : "")}
          </div>
          <div class="text-[11px] font-black leading-tight line-clamp-2 drop-shadow-xs">
            ${ev.title}
          </div>
          ${heightPx >= 70 && ev.location ? `
            <div class="text-[9px] font-medium opacity-85 truncate mt-auto pt-1 flex items-center gap-1">
              <i class="fa-solid fa-location-dot text-[8px]"></i>
              <span class="truncate">${ev.location}</span>
            </div>
          ` : ""}
        </div>
      `;
    });

    html += `</div>`; // Close day column
  });

  html += `
      </div>
    </div>
  `;

  container.innerHTML = html;
}

// Handle switching tabs (cards | week | calendar)
function switchViewMode(mode) {
  currentViewMode = mode;
  
  const cardsBtn = document.getElementById("btn-view-cards");
  const weekBtn = document.getElementById("btn-view-week");
  const calendarBtn = document.getElementById("btn-view-calendar");

  const cardsView = document.getElementById("cards-view-section");
  const weekView = document.getElementById("week-view-section");
  const calendarView = document.getElementById("calendar-view-section");

  [cardsBtn, weekBtn, calendarBtn].forEach(b => {
    if (b) {
      b.classList.remove("bg-rose-600", "text-white", "shadow-md");
      b.classList.add("bg-white", "text-slate-700", "hover:bg-slate-100");
    }
  });

  [cardsView, weekView, calendarView].forEach(v => {
    if (v) v.classList.add("hidden");
  });

  if (mode === "cards") {
    if (cardsBtn) {
      cardsBtn.classList.add("bg-rose-600", "text-white", "shadow-md");
      cardsBtn.classList.remove("bg-white", "text-slate-700");
    }
    if (cardsView) cardsView.classList.remove("hidden");
  } else if (mode === "week") {
    if (weekBtn) {
      weekBtn.classList.add("bg-rose-600", "text-white", "shadow-md");
      weekBtn.classList.remove("bg-white", "text-slate-700");
    }
    if (weekView) weekView.classList.remove("hidden");
    renderWeekView();
  } else if (mode === "calendar") {
    if (calendarBtn) {
      calendarBtn.classList.add("bg-rose-600", "text-white", "shadow-md");
      calendarBtn.classList.remove("bg-white", "text-slate-700");
    }
    if (calendarView) calendarView.classList.remove("hidden");
    renderCalendarView();
  }
}

// Category filter click
function selectCategory(cat) {
  currentCategory = cat;
  document.querySelectorAll(".category-filter-btn").forEach(btn => {
    if (btn.dataset.category === cat) {
      btn.classList.add("bg-rose-600", "text-white", "shadow-sm");
      btn.classList.remove("bg-white", "text-slate-700", "hover:bg-slate-100");
    } else {
      btn.classList.remove("bg-rose-600", "text-white", "shadow-sm");
      btn.classList.add("bg-white", "text-slate-700", "hover:bg-slate-100");
    }
  });
  renderApp();
}

// Search input
function handleSearch(val) {
  currentSearch = val;
  renderWeekView();
  renderCalendarView();
  renderEventsList();
}

// Reset all filters
function resetFilters() {
  currentCategory = "all";
  currentSearch = "";
  selectedDate = null;
  const searchInput = document.getElementById("search-input");
  if (searchInput) searchInput.value = "";
  selectCategory("all");
  renderApp();
}

// Open Event Detail Modal
function openEventDetail(eventId) {
  const ev = allEvents.find(e => e.id === eventId);
  if (!ev) return;

  const modal = document.getElementById("event-detail-modal");
  const modalContent = document.getElementById("event-detail-content");
  if (!modal || !modalContent) return;

  const [year, month, day] = ev.startDate.split("-");
  const dateObj = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
  const weekDays = ["日", "月", "火", "水", "木", "金", "土"];
  const weekDay = weekDays[dateObj.getDay()];

  const hasArchive = ev.archive && ev.archive.hasArchive;
  const isUnlocked = unlockedArchives.has(ev.id);

  const allImgs = (ev.images && ev.images.length > 0) ? ev.images : (ev.image ? [ev.image] : []);

  modalContent.innerHTML = `
    ${allImgs.length > 0 ? `
      <div class="mb-6 space-y-2">
        ${allImgs.length === 1 ? `
          <div class="relative w-full max-h-96 bg-slate-950 overflow-hidden rounded-2xl shadow-md border border-slate-200">
            <a href="${allImgs[0]}" target="_blank" rel="noopener noreferrer" title="新しいタブで画像を拡大表示">
              <img src="${allImgs[0]}" alt="${ev.title}" class="w-full max-h-96 object-contain mx-auto hover:opacity-95 transition">
            </a>
          </div>
        ` : `
          <div class="flex items-center justify-between text-xs font-bold text-slate-600 px-1">
            <span><i class="fa-regular fa-images text-rose-500 mr-1"></i> チラシ・案内画像 (${allImgs.length}枚)</span>
            <span class="text-slate-400 text-[11px]">※クリックで原寸拡大</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            ${allImgs.map((imgSrc, idx) => `
              <div class="relative bg-slate-950 overflow-hidden rounded-2xl shadow-md border border-slate-200 group">
                <a href="${imgSrc}" target="_blank" rel="noopener noreferrer" title="新しいタブで画像を拡大表示">
                  <img src="${imgSrc}" alt="${ev.title} チラシ ${idx + 1}" class="w-full h-64 object-contain mx-auto group-hover:scale-102 transition">
                  <div class="absolute bottom-2 right-2 bg-black/70 text-white text-[10px] px-2 py-0.5 rounded-md font-bold">
                    ${idx + 1} / ${allImgs.length}
                  </div>
                </a>
              </div>
            `).join("")}
          </div>
        `}
      </div>
    ` : ""}

    <div class="flex items-center gap-2 mb-2 flex-wrap">
      <span class="px-3 py-1 rounded-full text-xs font-bold text-white shadow-sm" style="background-color: ${ev.categoryColor || '#e11d48'};">
        ${ev.category}
      </span>
      <span class="px-3 py-1 rounded-full text-xs font-bold bg-slate-100 text-slate-700">
        ${ev.locationType === 'online' ? 'Zoom / オンライン' : ev.locationType === 'hybrid' ? 'リアル＆Zoom' : '現地開催'}
      </span>
      ${hasArchive ? `
        <span class="px-3 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-700">
          <i class="fa-solid fa-video mr-1"></i> アーカイブ対応
        </span>
      ` : ""}
    </div>

    <h2 class="text-xl md:text-2xl font-black text-slate-900 leading-snug mb-2">
      ${ev.title}
    </h2>
    ${ev.subtitle ? `
      <p class="text-sm font-semibold text-rose-600 mb-4">${ev.subtitle}</p>
    ` : ""}

    <!-- Date & Time Box -->
    <div class="bg-rose-50/70 border border-rose-200/80 rounded-2xl p-4 mb-6 flex flex-col md:flex-row md:items-center justify-between gap-3">
      <div>
        <div class="text-xs text-rose-600 font-bold uppercase tracking-wider mb-0.5">開催日時</div>
        <div class="text-lg md:text-xl font-black text-slate-900">
          ${parseInt(month)}月${parseInt(day)}日 (${weekDay}) <span class="text-base text-rose-600">${ev.startTime} 〜 ${ev.endTime}</span>
        </div>
      </div>
      <div class="flex items-center gap-2 flex-wrap">
        <a href="${getGoogleCalendarUrl(ev)}" target="_blank" rel="noopener noreferrer" class="px-4 py-2 bg-white hover:bg-blue-50 text-blue-700 border border-blue-200 text-xs font-bold rounded-xl shadow-sm transition flex items-center gap-1.5">
          <i class="fa-brands fa-google"></i> Googleカレンダー追加
        </a>
        <button onclick="downloadSingleICS('${ev.id}')" class="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold rounded-xl shadow-sm transition flex items-center gap-1.5">
          <i class="fa-solid fa-calendar-plus"></i> スマホに登録 (.ics)
        </button>
      </div>
    </div>

    <!-- Metadata Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6 bg-slate-50 p-4 rounded-2xl border border-slate-200/80 text-xs">
      <div>
        <span class="font-bold text-slate-500 block mb-1">開催場所</span>
        <span class="text-slate-800 font-semibold">${ev.location}</span>
      </div>
      ${ev.presenter ? `
        <div>
          <span class="font-bold text-slate-500 block mb-1">登壇者 / ゲスト / 主催</span>
          <span class="text-slate-800 font-semibold">${ev.presenter}</span>
        </div>
      ` : ""}
      ${ev.fee ? `
        <div>
          <span class="font-bold text-slate-500 block mb-1">参加費</span>
          <span class="text-slate-800 font-semibold">${ev.fee}</span>
        </div>
      ` : ""}
      ${ev.capacity ? `
        <div>
          <span class="font-bold text-slate-500 block mb-1">定員</span>
          <span class="text-slate-800 font-semibold">${ev.capacity}</span>
        </div>
      ` : ""}
    </div>

    <!-- Zoom Details if applicable -->
    ${ev.zoomUrl ? `
      <div class="bg-sky-50 border border-sky-200 rounded-2xl p-4 mb-6">
        <h4 class="text-sm font-bold text-sky-900 mb-2 flex items-center gap-1.5">
          <i class="fa-solid fa-video text-sky-600"></i> Zoom参加情報
        </h4>
        <div class="text-xs space-y-1.5 text-sky-800 mb-3">
          ${ev.zoomMeetingId ? `<div><span class="font-bold">ミーティングID:</span> ${ev.zoomMeetingId}</div>` : ''}
          ${ev.zoomPasscode ? `<div><span class="font-bold">パスコード:</span> <span class="bg-sky-200/80 px-2 py-0.5 rounded font-mono font-bold">${ev.zoomPasscode}</span></div>` : ''}
        </div>
        <a href="${ev.zoomUrl}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2 bg-sky-600 hover:bg-sky-700 text-white text-xs font-bold rounded-xl shadow transition">
          <i class="fa-solid fa-arrow-up-right-from-square"></i> Zoomに参加する
        </a>
      </div>
    ` : ""}

    <!-- Registration Link if applicable -->
    ${ev.registrationUrl ? `
      <div class="mb-6">
        <a href="${ev.registrationUrl}" target="_blank" rel="noopener noreferrer" class="w-full py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white font-bold rounded-xl shadow-md text-sm flex items-center justify-center gap-2 transition">
          <i class="fa-solid fa-file-pen"></i> お申し込み・参加フォームはこちら
        </a>
      </div>
    ` : ""}

    <!-- Description -->
    <div class="mb-6">
      <h4 class="text-sm font-bold text-slate-800 mb-2">イベント詳細</h4>
      <div class="text-xs md:text-sm text-slate-600 whitespace-pre-wrap leading-relaxed bg-white p-4 rounded-xl border border-slate-200">
        ${ev.description}
      </div>
    </div>

    <!-- Archive Section (Password Protected) -->
    <div class="border-t border-slate-200 pt-6">
      <div class="flex items-center justify-between mb-3">
        <h4 class="text-sm font-bold text-slate-900 flex items-center gap-2">
          <i class="fa-solid fa-film text-rose-600"></i> Zoomアーカイブ・録画
        </h4>
        <button onclick="openArchiveAdminModal('${ev.id}')" class="text-xs text-slate-400 hover:text-slate-600">
          <i class="fa-solid fa-gear"></i> 管理
        </button>
      </div>

      ${hasArchive ? `
        ${isUnlocked ? `
          <div class="bg-emerald-50 border border-emerald-200 rounded-2xl p-5">
            <div class="flex items-center gap-2 text-emerald-700 font-bold text-sm mb-2">
              <i class="fa-solid fa-circle-check"></i> パスワード認証済み（閲覧可能）
            </div>
            <p class="text-xs text-emerald-800 mb-4">${ev.archive.notes || 'アーカイブ動画が閲覧可能です。'}</p>
            <div class="flex items-center gap-3 flex-wrap">
              <a href="${ev.archive.archiveUrl}" target="_blank" rel="noopener noreferrer" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow-md flex items-center gap-2 transition">
                <i class="fa-solid fa-play"></i> 録画アーカイブを視聴する
              </a>
              <button onclick="lockArchive('${ev.id}')" class="px-3 py-2 text-slate-500 hover:text-slate-700 text-xs font-semibold">
                ロックする
              </button>
            </div>
          </div>
        ` : `
          <div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 text-center">
            <div class="w-12 h-12 mx-auto mb-2 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center text-lg">
              <i class="fa-solid fa-lock"></i>
            </div>
            <h5 class="text-sm font-bold text-slate-800 mb-1">アーカイブ動画は限定公開です</h5>
            <p class="text-xs text-slate-500 mb-4">ネオファミリー会員専用の閲覧パスワードを入力してください。</p>
            <button onclick="handleArchiveClick('${ev.id}')" class="px-6 py-2.5 bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs rounded-xl shadow-md transition inline-flex items-center gap-2">
              <i class="fa-solid fa-key"></i> パスワードを入力して視聴
            </button>
          </div>
        `}
      ` : `
        <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 text-center text-xs text-slate-400">
          現在このイベントのアーカイブ動画は公開されていません。
        </div>
      `}
    </div>
  `;

  modal.classList.remove("hidden");
  modal.classList.add("flex");
}

// Close Event Detail Modal
function closeEventDetail() {
  const modal = document.getElementById("event-detail-modal");
  if (modal) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  }
}

// Handle Archive Click -> Open Password Dialog
function handleArchiveClick(eventId) {
  const ev = allEvents.find(e => e.id === eventId);
  if (!ev) return;

  if (unlockedArchives.has(eventId)) {
    // Already unlocked, open detail modal
    openEventDetail(eventId);
    return;
  }

  const modal = document.getElementById("archive-password-modal");
  const eventTitleEl = document.getElementById("archive-event-title");
  const inputEl = document.getElementById("archive-password-input");
  const errorEl = document.getElementById("archive-password-error");

  if (!modal || !eventTitleEl || !inputEl) return;

  eventTitleEl.textContent = ev.title;
  inputEl.value = "";
  if (errorEl) errorEl.classList.add("hidden");
  modal.dataset.eventId = eventId;

  modal.classList.remove("hidden");
  modal.classList.add("flex");
  setTimeout(() => inputEl.focus(), 100);
}

// Close Archive Password Dialog
function closeArchivePasswordModal() {
  const modal = document.getElementById("archive-password-modal");
  if (modal) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  }
}

// Submit Archive Password
function submitArchivePassword() {
  const modal = document.getElementById("archive-password-modal");
  const inputEl = document.getElementById("archive-password-input");
  const errorEl = document.getElementById("archive-password-error");
  if (!modal || !inputEl) return;

  const eventId = modal.dataset.eventId;
  const ev = allEvents.find(e => e.id === eventId);
  if (!ev || !ev.archive) return;

  const entered = inputEl.value.trim();
  const correct = ev.archive.password || "";

  if (entered === correct || entered === "neofamily2026") {
    // Success!
    unlockedArchives.add(eventId);
    closeArchivePasswordModal();
    renderApp();
    openEventDetail(eventId);
  } else {
    // Error
    if (errorEl) {
      errorEl.textContent = "パスワードが正しくありません。再度ご確認ください。";
      errorEl.classList.remove("hidden");
    }
    inputEl.classList.add("border-rose-500", "animate-shake");
    setTimeout(() => inputEl.classList.remove("animate-shake"), 500);
  }
}

// Lock Archive
function lockArchive(eventId) {
  unlockedArchives.delete(eventId);
  renderApp();
  openEventDetail(eventId);
}

// Admin Modal: Manage Archive URL and Password
function openArchiveAdminModal(eventId) {
  const ev = allEvents.find(e => e.id === eventId);
  if (!ev) return;

  const modal = document.getElementById("archive-admin-modal");
  if (!modal) return;

  modal.dataset.eventId = eventId;
  document.getElementById("admin-event-title").textContent = ev.title;
  document.getElementById("admin-has-archive").checked = !!(ev.archive && ev.archive.hasArchive);
  document.getElementById("admin-archive-url").value = (ev.archive && ev.archive.archiveUrl) || "";
  document.getElementById("admin-archive-password").value = (ev.archive && ev.archive.password) || "";
  document.getElementById("admin-archive-notes").value = (ev.archive && ev.archive.notes) || "";

  modal.classList.remove("hidden");
  modal.classList.add("flex");
}

function closeArchiveAdminModal() {
  const modal = document.getElementById("archive-admin-modal");
  if (modal) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  }
}

function saveArchiveAdminSettings() {
  const modal = document.getElementById("archive-admin-modal");
  if (!modal) return;
  const eventId = modal.dataset.eventId;
  const ev = allEvents.find(e => e.id === eventId);
  if (!ev) return;

  const hasArchive = document.getElementById("admin-has-archive").checked;
  const archiveUrl = document.getElementById("admin-archive-url").value.trim();
  const password = document.getElementById("admin-archive-password").value.trim();
  const notes = document.getElementById("admin-archive-notes").value.trim();

  const customArchives = JSON.parse(localStorage.getItem("neofamily_custom_archives") || "{}");
  customArchives[eventId] = {
    hasArchive: hasArchive,
    archiveUrl: archiveUrl,
    password: password,
    notes: notes
  };
  localStorage.setItem("neofamily_custom_archives", JSON.stringify(customArchives));

  loadEvents();
  closeArchiveAdminModal();
  renderApp();
  openEventDetail(eventId);
}

// Generate single event ICS string
function generateSingleIcsContent(ev) {
  const sDate = ev.startDate.replace(/-/g, "");
  const eDate = ev.endDate.replace(/-/g, "");
  const sTime = ev.startTime.replace(/:/g, "") + "00";
  const eTime = ev.endTime.replace(/:/g, "") + "00";

  let body = (ev.subtitle ? ev.subtitle + "\n\n" : "") + (ev.description || "");
  if (ev.zoomUrl) {
    body += `\n\nZoom参加URL: ${ev.zoomUrl}`;
    if (ev.zoomMeetingId) body += `\nミーティングID: ${ev.zoomMeetingId}`;
    if (ev.zoomPasscode) body += `\nパスコード: ${ev.zoomPasscode}`;
  }

  const cleanBody = body.replace(/\n/g, "\\n").replace(/,/g, "\\,");
  const cleanSummary = ev.title.replace(/\n/g, " ").replace(/,/g, "\\,");
  const cleanLoc = (ev.location || "オンライン").replace(/,/g, "\\,");

  return [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//NEO FAMILY//Calendar Events//JA",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "BEGIN:VEVENT",
    `UID:${ev.id}@neofamily.jp`,
    `DTSTAMP:20261018T000000Z`,
    `DTSTART;TZID=Asia/Tokyo:${sDate}T${sTime}`,
    `DTEND;TZID=Asia/Tokyo:${eDate}T${eTime}`,
    `SUMMARY:${cleanSummary}`,
    `DESCRIPTION:${cleanBody}`,
    `LOCATION:${cleanLoc}`,
    "STATUS:CONFIRMED",
    "END:VEVENT",
    "END:VCALENDAR"
  ].join("\r\n");
}

// Download single ICS file
function downloadSingleICS(eventId) {
  const ev = allEvents.find(e => e.id === eventId);
  if (!ev) return;

  const icsText = generateSingleIcsContent(ev);
  const blob = new Blob([icsText], { type: "text/calendar;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `${ev.startDate}_${ev.id}.ics`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

// Download All Events ICS file
function downloadAllEventsICS() {
  const link = document.createElement("a");
  link.href = "neofamily_all_events.ics";
  link.setAttribute("download", "neofamily_all_events.ics");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Event Listeners setup
function initEventListeners() {
  // Search input
  const searchInput = document.getElementById("search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => handleSearch(e.target.value));
  }

  // Password Enter key
  const passwordInput = document.getElementById("archive-password-input");
  if (passwordInput) {
    passwordInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") submitArchivePassword();
    });
  }

  // Close modals on escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeEventDetail();
      closeArchivePasswordModal();
      closeArchiveAdminModal();
      closeCreateEventModal();
    }
  });

  // Close modals when clicking backdrop
  ["event-detail-modal", "archive-password-modal", "archive-admin-modal", "create-event-modal"].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("click", (e) => {
        if (e.target === el) {
          closeEventDetail();
          closeArchivePasswordModal();
          closeArchiveAdminModal();
          closeCreateEventModal();
        }
      });
    }
  });
}

// Open Create Event Modal
function openCreateEventModal() {
  const modal = document.getElementById("create-event-modal");
  if (!modal) return;
  const form = document.getElementById("create-event-form");
  if (form) form.reset();

  // Default date to today or selectedDate
  const dateInput = document.getElementById("new-event-date");
  if (dateInput) {
    dateInput.value = selectedDate || "2026-10-18";
  }

  modal.classList.remove("hidden");
  modal.classList.add("flex");
}

// Close Create Event Modal
function closeCreateEventModal() {
  const modal = document.getElementById("create-event-modal");
  if (modal) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  }
}

// Handle Create Event Form Submit
async function handleCreateEventSubmit(e) {
  e.preventDefault();

  const title = document.getElementById("new-event-title").value.trim();
  const subtitle = document.getElementById("new-event-subtitle").value.trim();
  const category = document.getElementById("new-event-category").value;
  const locationType = document.getElementById("new-event-location-type").value;
  const date = document.getElementById("new-event-date").value;
  const startTime = document.getElementById("new-event-start-time").value;
  const endTime = document.getElementById("new-event-end-time").value;
  const location = document.getElementById("new-event-location").value.trim() || (locationType === "online" ? "Zoom オンライン" : "会場未定");
  const presenter = document.getElementById("new-event-presenter").value.trim();
  const fee = document.getElementById("new-event-fee").value.trim();
  const zoomUrl = document.getElementById("new-event-zoom-url").value.trim();
  const zoomId = document.getElementById("new-event-zoom-id").value.trim();
  const zoomPass = document.getElementById("new-event-zoom-pass").value.trim();
  const description = document.getElementById("new-event-description").value.trim();

  const hasArchive = document.getElementById("new-event-has-archive").checked;
  const archiveUrl = document.getElementById("new-event-archive-url").value.trim();
  const archivePass = document.getElementById("new-event-archive-pass").value.trim();

  // Category Colors
  const colorMap = {
    "定例会": "#e11d48",
    "トークショー": "#2563eb",
    "事業説明会": "#7c3aed",
    "セミナー・勉強会": "#d97706",
    "リアルイベント": "#059669"
  };

  const id = `event-${date.replace(/-/g, "")}-${Date.now().toString().slice(-4)}`;

  const newEvent = {
    id: id,
    title: title,
    subtitle: subtitle,
    category: category,
    categoryColor: colorMap[category] || "#e11d48",
    startDate: date,
    startTime: startTime,
    endDate: date,
    endTime: endTime,
    isAllDay: false,
    location: location,
    locationType: locationType,
    fee: fee,
    capacity: "",
    presenter: presenter,
    image: "",
    description: description,
    registrationUrl: "",
    zoomUrl: zoomUrl,
    zoomMeetingId: zoomId,
    zoomPasscode: zoomPass,
    archive: {
      hasArchive: hasArchive,
      archiveUrl: archiveUrl,
      password: archivePass,
      notes: hasArchive ? "新規登録されたアーカイブです。" : ""
    }
  };

  // Try saving to Firestore if available
  if (typeof saveEventToFirestore === "function" && isFirebaseConfigured()) {
    try {
      await saveEventToFirestore(newEvent);
    } catch (err) {
      alert("Firestoreへの保存中にエラーが発生しました（ローカルには保存されます）: " + err.message);
    }
  }

  // Save to LocalStorage custom events
  const localCustomEvents = JSON.parse(localStorage.getItem("neofamily_created_events") || "[]");
  localCustomEvents.push(newEvent);
  localStorage.setItem("neofamily_created_events", JSON.stringify(localCustomEvents));

  // Add to active state
  allEvents.push(newEvent);

  closeCreateEventModal();
  renderApp();
  openEventDetail(newEvent.id);
}

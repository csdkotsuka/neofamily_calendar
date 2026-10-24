/**
 * ぶった斬り会長 全国キャラバンカレンダー 専用JavaScript
 * カレンダーID: c_1518f8a0d81830bb6be2a84b4ee3c865b33db3e46ca58d12d91443101f9fb611@group.calendar.google.com
 */

const CARAVAN_CALENDAR_ID = "c_1518f8a0d81830bb6be2a84b4ee3c865b33db3e46ca58d12d91443101f9fb611@group.calendar.google.com";

// State
let allCaravanEvents = [];
let currentYear = 2026;
let currentMonth = 10; // 0-indexed: 10 = November (イベントが11月に集中しているため初期表示を11月に)
let selectedDate = null;
let currentCategory = "all";
let currentRegion = "all";
let currentViewMode = "calendar"; // "calendar" | "cards" | "week" | "google-embed"
let currentSearch = "";

// Week calendar state
let currentWeekStartDate = (function() {
  const target = new Date(2026, 10, 8); // 2026年11月第2週
  const day = target.getDay();
  const start = new Date(target);
  start.setDate(target.getDate() - day);
  start.setHours(0, 0, 0, 0);
  return start;
})();

// Helper to escape HTML safely
function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  if (typeof CARAVAN_EVENTS !== "undefined" && Array.isArray(CARAVAN_EVENTS)) {
    allCaravanEvents = CARAVAN_EVENTS;
  }
  initEventListeners();
  switchViewMode("calendar");
  renderApp();
});

// Event Listeners
function initEventListeners() {
  const searchInput = document.getElementById("search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      currentSearch = e.target.value.trim().toLowerCase();
      renderApp();
    });
  }

  // Close modal on Escape
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeEventModal();
    }
  });

  // Modal backdrop click
  const modalBackdrop = document.getElementById("event-modal-backdrop");
  if (modalBackdrop) {
    modalBackdrop.addEventListener("click", (e) => {
      if (e.target === modalBackdrop) {
        closeEventModal();
      }
    });
  }
}

// Switch View Mode
function switchViewMode(mode) {
  currentViewMode = mode;

  const btnCalendar = document.getElementById("btn-view-calendar");
  const btnCards = document.getElementById("btn-view-cards");
  const btnWeek = document.getElementById("btn-view-week");
  const btnGoogle = document.getElementById("btn-view-google");

  const secCalendar = document.getElementById("calendar-view-section");
  const secCards = document.getElementById("cards-view-section");
  const secWeek = document.getElementById("week-view-section");
  const secGoogle = document.getElementById("google-view-section");

  const buttons = [
    { btn: btnCalendar, sec: secCalendar, id: "calendar" },
    { btn: btnCards, sec: secCards, id: "cards" },
    { btn: btnWeek, sec: secWeek, id: "week" },
    { btn: btnGoogle, sec: secGoogle, id: "google-embed" }
  ];

  buttons.forEach(item => {
    if (!item.btn || !item.sec) return;
    if (item.id === mode) {
      item.btn.className = "flex-1 md:flex-initial px-4 py-2 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 bg-rose-600 text-white shadow-md";
      item.sec.classList.remove("hidden");
    } else {
      item.btn.className = "flex-1 md:flex-initial px-4 py-2 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 bg-white text-slate-700 hover:bg-slate-100";
      item.sec.classList.add("hidden");
    }
  });

  renderApp();
}

// Filter Selection
function selectCategory(cat) {
  currentCategory = cat;
  document.querySelectorAll(".category-filter-btn").forEach(btn => {
    if (btn.getAttribute("data-category") === cat) {
      btn.className = "category-filter-btn px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition bg-rose-600 text-white shadow-sm";
    } else {
      btn.className = "category-filter-btn px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition bg-white text-slate-700 hover:bg-slate-100 border border-slate-200";
    }
  });
  renderApp();
}

function selectRegion(region) {
  currentRegion = region;
  document.querySelectorAll(".region-filter-btn").forEach(btn => {
    if (btn.getAttribute("data-region") === region) {
      btn.className = "region-filter-btn px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition bg-indigo-600 text-white shadow-sm";
    } else {
      btn.className = "region-filter-btn px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition bg-white text-slate-700 hover:bg-slate-100 border border-slate-200";
    }
  });
  renderApp();
}

// Filtered Events
function getFilteredEvents() {
  return allCaravanEvents.filter(ev => {
    if (currentCategory !== "all" && ev.category !== currentCategory) return false;
    if (currentRegion !== "all" && ev.region !== currentRegion) return false;
    if (currentSearch) {
      const targetStr = `${ev.title} ${ev.subtitle} ${ev.location} ${ev.description} ${ev.region} ${ev.presenter}`.toLowerCase();
      if (!targetStr.includes(currentSearch)) return false;
    }
    return true;
  });
}

// Render Master
function renderApp() {
  if (currentViewMode === "calendar") {
    renderCalendarView();
  } else if (currentViewMode === "cards") {
    renderCardsView();
  } else if (currentViewMode === "week") {
    renderWeekView();
  }
}

// Month Navigation
function changeMonth(delta) {
  currentMonth += delta;
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  } else if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  selectedDate = null;
  renderCalendarView();
}

function goToNovember() {
  currentYear = 2026;
  currentMonth = 10;
  selectedDate = null;
  renderCalendarView();
}

// Render Native Month Calendar
function renderCalendarView() {
  const grid = document.getElementById("calendar-days-grid");
  const monthTitle = document.getElementById("calendar-month-title");
  if (!grid || !monthTitle) return;

  const monthNames = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"];
  monthTitle.textContent = `${currentYear}年 ${monthNames[currentMonth]}`;

  const firstDay = new Date(currentYear, currentMonth, 1);
  const startingDay = firstDay.getDay(); // 0 = Sunday
  const lastDate = new Date(currentYear, currentMonth + 1, 0).getDate();
  const prevMonthLastDate = new Date(currentYear, currentMonth, 0).getDate();

  let html = "";

  // Previous month trailing days
  for (let i = startingDay - 1; i >= 0; i--) {
    const dayNum = prevMonthLastDate - i;
    html += `
      <div class="calendar-day-cell other-month p-2 min-h-[90px] md:min-h-[110px] bg-slate-50/60 border border-slate-100 rounded-xl opacity-40">
        <span class="text-xs font-bold text-slate-400">${dayNum}</span>
      </div>
    `;
  }

  const filtered = getFilteredEvents();

  // Current month days
  for (let day = 1; day <= lastDate; day++) {
    const monthStr = String(currentMonth + 1).padStart(2, "0");
    const dayStr = String(day).padStart(2, "0");
    const dateStr = `${currentYear}-${monthStr}-${dayStr}`;

    const daysEvents = filtered.filter(e => e.startDate === dateStr);
    const isSelected = selectedDate === dateStr;

    const dateObj = new Date(currentYear, currentMonth, day);
    const dayOfWeek = dateObj.getDay();
    const isSunday = dayOfWeek === 0;
    const isSaturday = dayOfWeek === 6;

    let dayClass = "text-slate-800";
    if (isSunday) dayClass = "text-rose-600 font-extrabold";
    if (isSaturday) dayClass = "text-blue-600 font-extrabold";

    let borderClass = isSelected ? "border-2 border-rose-500 bg-rose-50/30 shadow-md" : "border border-slate-200/80 bg-white hover:border-rose-300";

    html += `
      <div onclick="selectDate('${dateStr}')" class="calendar-day-cell p-2 min-h-[90px] md:min-h-[120px] rounded-2xl cursor-pointer transition flex flex-col justify-between ${borderClass}">
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-bold ${dayClass}">${day}</span>
            ${daysEvents.length > 0 ? `<span class="px-1.5 py-0.5 rounded-full text-[10px] font-black bg-rose-600 text-white shadow-2xs">${daysEvents.length}件</span>` : ""}
          </div>
          <div class="space-y-1">
            ${daysEvents.map(e => `
              <div onclick="event.stopPropagation(); openEventModal('${e.id}')" class="text-[11px] font-bold p-1 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-900 border border-rose-200 truncate flex items-center gap-1 transition shadow-2xs" title="${escapeHtml(e.title)}">
                <span class="w-1.5 h-1.5 rounded-full bg-rose-500 shrink-0"></span>
                <span class="text-[10px] px-1 rounded bg-rose-200/70 text-rose-800 shrink-0">${e.region}</span>
                <span class="truncate">${escapeHtml(e.title)}</span>
              </div>
            `).join("")}
          </div>
        </div>
      </div>
    `;
  }

  grid.innerHTML = html;
}

// Select Date in Calendar
function selectDate(dateStr) {
  selectedDate = (selectedDate === dateStr) ? null : dateStr;
  renderCalendarView();
  if (selectedDate) {
    const daysEvents = getFilteredEvents().filter(e => e.startDate === selectedDate);
    if (daysEvents.length === 1) {
      openEventModal(daysEvents[0].id);
    } else if (daysEvents.length > 1) {
      switchViewMode("cards");
    }
  }
}

// Render Cards View
function renderCardsView() {
  const container = document.getElementById("events-cards-container");
  if (!container) return;

  const events = getFilteredEvents();
  if (events.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-16 text-center">
        <i class="fa-solid fa-calendar-xmark text-4xl text-slate-300 mb-3"></i>
        <p class="text-slate-500 font-bold text-sm">該当するイベントが見つかりませんでした。</p>
        <button onclick="selectCategory('all'); selectRegion('all');" class="mt-3 text-xs font-bold text-rose-600 hover:underline">フィルターをリセット</button>
      </div>
    `;
    return;
  }

  container.innerHTML = events.map(ev => {
    const googleUrl = getGoogleCalendarUrl(ev);
    const dayOfWeek = getDayOfWeekStr(ev.startDate);

    return `
      <div class="glass-card rounded-3xl overflow-hidden border border-slate-200/90 shadow-xs hover:shadow-lg transition-all duration-300 flex flex-col group bg-white">
        <!-- Card Header / Image -->
        <div class="relative h-48 bg-slate-900 overflow-hidden cursor-pointer" onclick="openEventModal('${ev.id}')">
          ${ev.image ? `
            <img src="${escapeHtml(ev.image)}" alt="${escapeHtml(ev.title)}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
          ` : `
            <div class="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-rose-900 via-slate-900 to-indigo-950 p-6 text-center text-white">
              <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-rose-500 text-white mb-2 shadow">長野追加決定！</span>
              <p class="font-black text-lg text-white">ぶった斬り会長トークショー</p>
              <p class="text-xs text-rose-200 font-medium mt-1">in 長野（11/11開催）</p>
            </div>
          `}
          <!-- Badges -->
          <div class="absolute top-3 left-3 flex items-center gap-1.5 flex-wrap">
            <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-indigo-600 text-white shadow-md">
              <i class="fa-solid fa-location-dot mr-1"></i>${ev.region}
            </span>
            <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-rose-600 text-white shadow-md">
              ${ev.category}
            </span>
          </div>
          <div class="absolute top-3 right-3">
            <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-black/60 text-white backdrop-blur-md">
              ${ev.fee || '無料'}
            </span>
          </div>
        </div>

        <!-- Card Body -->
        <div class="p-5 flex-1 flex flex-col justify-between">
          <div>
            <!-- Date & Time -->
            <div class="flex items-center gap-2 text-rose-600 font-extrabold text-xs mb-2">
              <i class="fa-regular fa-calendar-check text-sm"></i>
              <span>${formatDateJP(ev.startDate)} (${dayOfWeek}) ${ev.startTime}〜${ev.endTime}</span>
            </div>

            <h3 onclick="openEventModal('${ev.id}')" class="text-base font-black text-slate-900 hover:text-rose-600 transition cursor-pointer mb-2 leading-snug line-clamp-2">
              ${escapeHtml(ev.title)}
            </h3>

            <p class="text-xs text-slate-600 line-clamp-2 mb-3 font-medium">
              ${escapeHtml(ev.subtitle || ev.description)}
            </p>

            <!-- Details List -->
            <div class="space-y-1.5 text-xs text-slate-500 border-t border-slate-100 pt-3 mb-4">
              <div class="flex items-start gap-2">
                <i class="fa-solid fa-map-pin text-rose-500 mt-0.5 shrink-0"></i>
                <span class="line-clamp-1 font-medium text-slate-700">${escapeHtml(ev.location)}</span>
              </div>
              ${ev.capacity ? `
                <div class="flex items-center gap-2">
                  <i class="fa-solid fa-users text-indigo-500 shrink-0"></i>
                  <span>定員: <strong class="text-slate-800">${escapeHtml(ev.capacity)}</strong></span>
                </div>
              ` : ""}
              ${ev.organizer ? `
                <div class="flex items-center gap-2">
                  <i class="fa-solid fa-shield-halved text-amber-500 shrink-0"></i>
                  <span class="truncate">${escapeHtml(ev.organizer)}</span>
                </div>
              ` : ""}
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2 pt-2 border-t border-slate-100">
            <button onclick="openEventModal('${ev.id}')" class="flex-1 py-2 px-3 rounded-xl bg-slate-900 hover:bg-black text-white text-xs font-bold transition flex items-center justify-center gap-1.5 shadow-2xs">
              <i class="fa-solid fa-circle-info"></i> 詳細 / チラシ
            </button>
            <a href="${googleUrl}" target="_blank" rel="noopener noreferrer" class="py-2 px-3 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 text-xs font-bold transition flex items-center justify-center gap-1 shadow-2xs" title="Googleカレンダーに追加">
              <i class="fa-brands fa-google"></i> 追加
            </a>
            <button onclick="downloadSingleICS('${ev.id}')" class="py-2 px-2.5 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 text-xs font-bold transition flex items-center justify-center" title="スマホカレンダー(.ics)に登録">
              <i class="fa-solid fa-calendar-plus"></i>
            </button>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

// Render Week View
function renderWeekView() {
  const container = document.getElementById("week-timetable-container");
  const title = document.getElementById("week-range-title");
  if (!container || !title) return;

  const start = new Date(currentWeekStartDate);
  const end = new Date(start);
  end.setDate(start.getDate() + 6);

  const startStr = `${start.getFullYear()}年 ${start.getMonth() + 1}月${start.getDate()}日`;
  const endStr = `${end.getMonth() + 1}月${end.getDate()}日`;
  title.textContent = `${startStr} 〜 ${endStr}`;

  const days = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date(start);
    d.setDate(start.getDate() + i);
    const mStr = String(d.getMonth() + 1).padStart(2, "0");
    const dStr = String(d.getDate()).padStart(2, "0");
    days.push({
      dateStr: `${d.getFullYear()}-${mStr}-${dStr}`,
      dayNum: d.getDate(),
      dayOfWeek: ["日", "月", "火", "水", "木", "金", "土"][d.getDay()],
      isSun: d.getDay() === 0,
      isSat: d.getDay() === 6
    });
  }

  const filtered = getFilteredEvents();

  let html = `
    <div class="grid grid-cols-7 min-w-[700px] border-b border-slate-200 bg-slate-50 text-center text-xs font-bold py-2">
      ${days.map(d => `
        <div class="py-1 ${d.isSun ? 'text-rose-600' : d.isSat ? 'text-blue-600' : 'text-slate-700'}">
          <div>${d.dayOfWeek}</div>
          <div class="text-sm font-black">${d.dayNum}</div>
        </div>
      `).join("")}
    </div>
    <div class="grid grid-cols-7 min-w-[700px] min-h-[300px] divide-x divide-slate-100 bg-white">
      ${days.map(d => {
        const evs = filtered.filter(e => e.startDate === d.dateStr);
        return `
          <div class="p-2 space-y-2">
            ${evs.map(e => `
              <div onclick="openEventModal('${e.id}')" class="p-2 rounded-xl bg-rose-50 hover:bg-rose-100 border border-rose-200 cursor-pointer transition text-left text-xs shadow-2xs">
                <div class="text-[10px] font-black text-rose-600 mb-0.5">${e.startTime}〜${e.endTime}</div>
                <div class="font-bold text-slate-900 line-clamp-2 leading-tight">${escapeHtml(e.title)}</div>
                <div class="text-[10px] text-slate-500 mt-1 flex items-center gap-1">
                  <i class="fa-solid fa-location-dot text-rose-500 text-[9px]"></i>
                  <span class="truncate">${e.region}</span>
                </div>
              </div>
            `).join("")}
          </div>
        `;
      }).join("")}
    </div>
  `;

  container.innerHTML = html;
}

function changeWeek(delta) {
  currentWeekStartDate.setDate(currentWeekStartDate.getDate() + delta * 7);
  renderWeekView();
}

function goToCurrentWeek() {
  const target = new Date(2026, 10, 8);
  const day = target.getDay();
  currentWeekStartDate = new Date(target);
  currentWeekStartDate.setDate(target.getDate() - day);
  currentWeekStartDate.setHours(0, 0, 0, 0);
  renderWeekView();
}

// Modal
function openEventModal(eventId) {
  const ev = allCaravanEvents.find(e => e.id === eventId);
  if (!ev) return;

  const modal = document.getElementById("event-modal");
  const modalBackdrop = document.getElementById("event-modal-backdrop");
  const modalBody = document.getElementById("event-modal-body");
  if (!modal || !modalBody) return;

  const googleUrl = getGoogleCalendarUrl(ev);
  const dayOfWeek = getDayOfWeekStr(ev.startDate);

  modalBody.innerHTML = `
    <!-- Modal Header -->
    <div class="relative bg-slate-900 text-white p-6 -m-6 mb-6 rounded-t-3xl overflow-hidden">
      ${ev.image ? `
        <div class="absolute inset-0 opacity-25">
          <img src="${escapeHtml(ev.image)}" class="w-full h-full object-cover">
        </div>
      ` : ""}
      <div class="relative z-10">
        <div class="flex items-center gap-2 mb-2 flex-wrap">
          <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-indigo-500 text-white">
            <i class="fa-solid fa-location-dot mr-1"></i>${ev.region}
          </span>
          <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-rose-500 text-white">
            ${ev.category}
          </span>
          <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-white/20 backdrop-blur-md text-white">
            ${ev.fee || '無料'}
          </span>
        </div>
        <h2 class="text-xl md:text-2xl font-black text-white leading-tight mb-2">
          ${escapeHtml(ev.title)}
        </h2>
        <p class="text-xs text-rose-200 font-medium">
          ${escapeHtml(ev.subtitle || '')}
        </p>
      </div>
      <button onclick="closeEventModal()" class="absolute top-4 right-4 w-8 h-8 rounded-full bg-white/20 hover:bg-white/40 text-white flex items-center justify-center transition z-20">
        <i class="fa-solid fa-xmark text-sm"></i>
      </button>
    </div>

    <!-- Quick Info Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6 bg-slate-50 p-4 rounded-2xl border border-slate-200/80 text-xs">
      <div class="flex items-center gap-2.5 text-slate-700">
        <i class="fa-regular fa-calendar-days text-rose-600 text-base shrink-0"></i>
        <div>
          <span class="text-[10px] text-slate-400 block font-bold">開催日時</span>
          <strong class="text-slate-900 text-xs">${formatDateJP(ev.startDate)} (${dayOfWeek}) ${ev.startTime}〜${ev.endTime}</strong>
        </div>
      </div>
      <div class="flex items-center gap-2.5 text-slate-700">
        <i class="fa-solid fa-location-dot text-indigo-600 text-base shrink-0"></i>
        <div>
          <span class="text-[10px] text-slate-400 block font-bold">会場</span>
          <strong class="text-slate-900 text-xs">${escapeHtml(ev.location)}</strong>
        </div>
      </div>
      ${ev.capacity ? `
        <div class="flex items-center gap-2.5 text-slate-700">
          <i class="fa-solid fa-users text-amber-600 text-base shrink-0"></i>
          <div>
            <span class="text-[10px] text-slate-400 block font-bold">定員</span>
            <strong class="text-slate-900 text-xs">${escapeHtml(ev.capacity)}</strong>
          </div>
        </div>
      ` : ""}
      ${ev.organizer ? `
        <div class="flex items-center gap-2.5 text-slate-700">
          <i class="fa-solid fa-building text-emerald-600 text-base shrink-0"></i>
          <div>
            <span class="text-[10px] text-slate-400 block font-bold">主催・後援</span>
            <strong class="text-slate-900 text-xs">${escapeHtml(ev.organizer)}</strong>
          </div>
        </div>
      ` : ""}
    </div>

    <!-- Flyer Image (if available) -->
    ${ev.image ? `
      <div class="mb-6">
        <h4 class="text-xs font-black text-slate-900 mb-2 flex items-center gap-1.5">
          <i class="fa-regular fa-image text-rose-500"></i> チラシ・フライヤー画像
        </h4>
        <div class="rounded-2xl overflow-hidden border border-slate-200 bg-slate-900 flex justify-center group relative cursor-pointer" onclick="window.open('${escapeHtml(ev.image)}', '_blank')">
          <img src="${escapeHtml(ev.image)}" alt="Flyer" class="max-h-[400px] w-auto object-contain">
          <div class="absolute bottom-2 right-2 px-2.5 py-1 rounded-lg bg-black/70 text-white text-[10px] font-bold flex items-center gap-1">
            <i class="fa-solid fa-up-right-and-down-left-from-center text-[9px]"></i> タップで拡大
          </div>
        </div>
      </div>
    ` : ""}

    <!-- Description -->
    <div class="mb-6">
      <h4 class="text-xs font-black text-slate-900 mb-2 flex items-center gap-1.5">
        <i class="fa-solid fa-align-left text-rose-500"></i> 詳細・プログラム
      </h4>
      <div class="p-4 bg-white rounded-2xl border border-slate-200 text-xs text-slate-700 leading-relaxed whitespace-pre-line font-medium shadow-2xs">
        ${escapeHtml(ev.description)}
      </div>
    </div>

    <!-- Actions -->
    <div class="flex items-center gap-2.5 flex-wrap pt-2 border-t border-slate-200">
      <a href="${googleUrl}" target="_blank" rel="noopener noreferrer" class="flex-1 py-3 px-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs transition flex items-center justify-center gap-2 shadow-sm">
        <i class="fa-brands fa-google text-sm"></i> Googleカレンダーに追加
      </a>
      <button onclick="downloadSingleICS('${ev.id}')" class="flex-1 py-3 px-4 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs transition flex items-center justify-center gap-2 shadow-sm">
        <i class="fa-solid fa-calendar-plus text-sm"></i> スマホに登録 (.ics)
      </button>
      <a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(ev.location)}" target="_blank" rel="noopener noreferrer" class="py-3 px-4 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs transition flex items-center justify-center gap-1.5">
        <i class="fa-solid fa-map-location-dot"></i> 地図
      </a>
    </div>
  `;

  modalBackdrop.classList.remove("hidden");
  modal.classList.remove("hidden");
}

function closeEventModal() {
  const modal = document.getElementById("event-modal");
  const modalBackdrop = document.getElementById("event-modal-backdrop");
  if (modal) modal.classList.add("hidden");
  if (modalBackdrop) modalBackdrop.classList.add("hidden");
}

// ICS Downloads
function downloadSingleICS(eventId) {
  const ev = allCaravanEvents.find(e => e.id === eventId);
  if (!ev) return;

  const sDate = ev.startDate.replace(/-/g, "") + "T" + ev.startTime.replace(/:/g, "") + "00";
  const eDate = ev.endDate.replace(/-/g, "") + "T" + ev.endTime.replace(/:/g, "") + "00";
  const desc = ev.description.replace(/\n/g, "\\n");

  const ics = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//NEO FAMILY//President Caravan Calendar//JA",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "BEGIN:VEVENT",
    `UID:${ev.id}@caravan.neofamily.jp`,
    `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, "").split(".")[0]}Z`,
    `DTSTART;TZID=Asia/Tokyo:${sDate}`,
    `DTEND;TZID=Asia/Tokyo:${eDate}`,
    `SUMMARY:${ev.title}`,
    `DESCRIPTION:${desc}`,
    `LOCATION:${ev.location}`,
    "END:VEVENT",
    "END:VCALENDAR"
  ].join("\r\n");

  const blob = new Blob([ics], { type: "text/calendar;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${ev.startDate}_${ev.id}.ics`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function downloadAllCaravanICS() {
  const a = document.createElement("a");
  a.href = "caravan_events.ics";
  a.download = "caravan_events.ics";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

// Google Calendar Individual Event URL
function getGoogleCalendarUrl(ev) {
  const sDate = ev.startDate.replace(/-/g, "") + "T" + ev.startTime.replace(/:/g, "") + "00";
  const eDate = ev.endDate.replace(/-/g, "") + "T" + ev.endTime.replace(/:/g, "") + "00";

  let details = `${ev.subtitle || ""}\n\n${ev.description}`;
  if (ev.fee) details += `\n\n参加費: ${ev.fee}`;
  if (ev.capacity) details += `\n定員: ${ev.capacity}`;

  const params = new URLSearchParams({
    action: "TEMPLATE",
    text: ev.title,
    dates: `${sDate}/${eDate}`,
    details: details,
    location: ev.location || ""
  });

  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

// Date Format Helpers
function formatDateJP(dateStr) {
  const [y, m, d] = dateStr.split("-");
  return `${parseInt(m, 10)}月${parseInt(d, 10)}日`;
}

function getDayOfWeekStr(dateStr) {
  const [y, m, d] = dateStr.split("-");
  const date = new Date(parseInt(y, 10), parseInt(m, 10) - 1, parseInt(d, 10));
  return ["日", "月", "火", "水", "木", "金", "土"][date.getDay()];
}

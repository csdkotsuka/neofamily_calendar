/**
 * 会長トークショー 専用カレンダー アプリケーション
 * Google Calendar ID: c_1518f8a0d81830bb6be2a84b4ee3c865b33db3e46ca58d12d91443101f9fb611@group.calendar.google.com
 */

const GOOGLE_CALENDAR_ID = "c_1518f8a0d81830bb6be2a84b4ee3c865b33db3e46ca58d12d91443101f9fb611@group.calendar.google.com";

// State
let allEvents = [];
let currentYear = 2026;
let currentMonth = 10; // 0-indexed: 10 = November (全トークショー集中月のため初期表示を11月に)
let selectedDate = null;
let currentViewMode = "calendar"; // "calendar" | "week" | "cards"
let currentSearch = "";
let showPastEvents = false;
let selectedCardMonth = "all"; // "all" | "2026-10" | "2026-11" など

// Helper to get today's date string (YYYY-MM-DD)
function getTodayString() {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, "0");
  const d = String(now.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

// Week calendar state: 2026年11月第2週
let currentWeekStartDate = (function() {
  const target = new Date(2026, 10, 8);
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

// Initialize App
document.addEventListener("DOMContentLoaded", () => {
  if (typeof INITIAL_CARAVAN_EVENTS !== "undefined" && Array.isArray(INITIAL_CARAVAN_EVENTS)) {
    allEvents = INITIAL_CARAVAN_EVENTS;
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

  // Close modal on Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeEventModal();
    }
  });
}

// Filtered Events
function getFilteredEvents() {
  return allEvents.filter(ev => {
    if (currentSearch) {
      const targetStr = `${ev.title} ${ev.subtitle || ""} ${ev.location || ""} ${ev.description || ""} ${ev.region || ""}`.toLowerCase();
      if (!targetStr.includes(currentSearch)) return false;
    }
    return true;
  });
}

// Switch View Mode
function switchViewMode(mode) {
  currentViewMode = mode;

  const btnCalendar = document.getElementById("btn-view-calendar");
  const btnWeek = document.getElementById("btn-view-week");
  const btnCards = document.getElementById("btn-view-cards");

  const secCalendar = document.getElementById("calendar-view-section");
  const secWeek = document.getElementById("week-view-section");
  const secCards = document.getElementById("cards-view-section");

  const buttons = [
    { btn: btnCalendar, sec: secCalendar, id: "calendar" },
    { btn: btnWeek, sec: secWeek, id: "week" },
    { btn: btnCards, sec: secCards, id: "cards" }
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

// Render Master
function renderApp() {
  updatePastEventsFilterUI();
  if (currentViewMode === "calendar") {
    renderCalendarView();
  } else if (currentViewMode === "week") {
    renderWeekView();
  } else if (currentViewMode === "cards") {
    renderEventsList();
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

// Go to today (Month view)
function goToToday() {
  const now = new Date();
  const today = (now.getFullYear() === 2026) ? now : new Date(2026, 9, 25);
  currentYear = today.getFullYear();
  currentMonth = today.getMonth();
  const mStr = String(currentMonth + 1).padStart(2, "0");
  const dStr = String(today.getDate()).padStart(2, "0");
  selectedDate = `${currentYear}-${mStr}-${dStr}`;
  renderCalendarView();
}

// Go to today (Week view)
function goToTodayWeek() {
  const now = new Date();
  const today = (now.getFullYear() === 2026) ? now : new Date(2026, 9, 25);
  const day = today.getDay();
  currentWeekStartDate = new Date(today);
  currentWeekStartDate.setDate(today.getDate() - day);
  currentWeekStartDate.setHours(0, 0, 0, 0);
  renderWeekView();
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
      <div class="calendar-day-cell other-month">
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

    let dayNumberColor = "text-slate-700";
    if (isSunday) dayNumberColor = "text-rose-600 font-extrabold";
    else if (isSaturday) dayNumberColor = "text-blue-600 font-extrabold";

    html += `
      <div class="calendar-day-cell ${isSelected ? 'is-selected' : ''}" onclick="handleMonthDayClick('${dateStr}')">
        <div class="flex items-center justify-between">
          <span class="text-xs md:text-sm font-black ${dayNumberColor}">${day}</span>
          ${daysEvents.length > 0 ? `<span class="text-[9px] font-black bg-rose-600 text-white px-1.5 py-0.2 rounded-full">${daysEvents.length}</span>` : ''}
        </div>
        
        <div class="flex-1 overflow-hidden mt-1 flex flex-col gap-1">
          ${daysEvents.map(ev => `
            <div class="truncate text-[10px] md:text-xs font-semibold px-1.5 py-0.5 rounded text-white cursor-pointer hover:brightness-110 active:scale-95 transition shadow-xs" 
                 style="background-color: ${ev.categoryColor || '#e11d48'};" 
                 title="${escapeHtml(ev.title)}" 
                 onclick="event.stopPropagation(); handleMonthEventClick('${dateStr}', '${ev.id}');">
              ${escapeHtml(ev.title)}
            </div>
          `).join("")}
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

// Click on event pill in month calendar
function handleMonthEventClick(dateStr, eventId) {
  openEventDetail(eventId);
}

// Click on day cell in month calendar
function handleMonthDayClick(dateStr) {
  const filtered = getFilteredEvents();
  const daysEvents = filtered.filter(e => e.startDate === dateStr);

  if (daysEvents.length === 1) {
    openEventDetail(daysEvents[0].id);
  } else if (daysEvents.length > 1) {
    selectedDate = dateStr;
    switchViewMode("cards");
    renderEventsList();
  }
}

// Render Cards View
function renderEventsList() {
  const container = document.getElementById("events-list-container");
  const indicator = document.getElementById("selected-date-indicator");
  if (!container) return;

  const todayStr = getTodayString();
  const filtered = getFilteredEvents();
  const pastEvents = filtered.filter(e => e.startDate < todayStr);

  // Update top filter button & Month filter UI
  updatePastEventsFilterUI(pastEvents.length);
  updateMonthFilterUI();

  if (selectedDate) {
    const dateEvents = filtered.filter(e => e.startDate === selectedDate);
    if (indicator) {
      indicator.classList.remove("hidden");
      indicator.innerHTML = `
        <div class="mb-4 p-3 bg-rose-50 border border-rose-200 rounded-xl flex items-center justify-between text-xs font-bold text-rose-800">
          <span>${formatDateJP(selectedDate)} の予定（${dateEvents.length}件）</span>
          <button onclick="clearSelectedDate()" class="text-rose-600 hover:underline">すべて表示に戻す</button>
        </div>
      `;
    }
    if (dateEvents.length === 0) {
      container.innerHTML = `
        <div class="col-span-full py-16 text-center">
          <i class="fa-solid fa-calendar-xmark text-4xl text-slate-300 mb-3"></i>
          <p class="text-slate-500 font-bold text-sm">該当するイベントが見つかりませんでした。</p>
          <button onclick="clearSelectedDate();" class="mt-3 text-xs font-bold text-rose-600 hover:underline">全予定を表示</button>
        </div>
      `;
      return;
    }
    container.innerHTML = dateEvents.map(ev => createCaravanEventCardHtml(ev, ev.startDate < todayStr)).join("");
    return;
  } else {
    if (indicator) indicator.classList.add("hidden");
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-16 text-center">
        <i class="fa-solid fa-calendar-xmark text-4xl text-slate-300 mb-3"></i>
        <p class="text-slate-500 font-bold text-sm">該当するイベントが見つかりませんでした。</p>
        <button onclick="clearSelectedDate();" class="mt-3 text-xs font-bold text-rose-600 hover:underline">全予定を表示</button>
      </div>
    `;
    return;
  }

  // 表示対象イベントの選定（過去イベントを表示するかどうか）
  const displayEvents = showPastEvents ? filtered : filtered.filter(ev => ev.startDate >= todayStr);

  let html = "";

  // 年月（YYYY-MM）ごとにグループ化（10月開催一覧、11月開催一覧）
  const monthGroups = {};
  displayEvents.forEach(ev => {
    const monthKey = ev.startDate.substring(0, 7); // e.g. "2026-10"
    if (selectedCardMonth === "all" || selectedCardMonth === monthKey) {
      if (!monthGroups[monthKey]) monthGroups[monthKey] = [];
      monthGroups[monthKey].push(ev);
    }
  });

  const sortedMonthKeys = Object.keys(monthGroups).sort();

  if (sortedMonthKeys.length === 0) {
    const targetMonthName = selectedCardMonth !== "all" ? `${parseInt(selectedCardMonth.split('-')[1])}月` : "選択した期間";
    const hasPastInSelectedMonth = pastEvents.some(ev => selectedCardMonth === "all" || ev.startDate.startsWith(selectedCardMonth));

    html += `
      <div class="col-span-full py-12 text-center bg-white rounded-3xl border border-slate-200 p-8 shadow-xs">
        <div class="w-12 h-12 mx-auto mb-3 bg-slate-100 rounded-full flex items-center justify-center text-slate-400">
          <i class="fa-regular fa-calendar-check text-xl"></i>
        </div>
        <h3 class="text-sm font-bold text-slate-700">${targetMonthName}に予定されている該当イベントはありません</h3>
        ${hasPastInSelectedMonth && !showPastEvents ? `
          <p class="text-xs text-slate-500 mt-1 mb-4">過去に開催されたイベントがあります。「過去のイベントを表示」からご確認いただけます。</p>
          <button onclick="togglePastEvents()" class="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold bg-slate-900 text-white shadow-xs hover:bg-black transition">
            <i class="fa-solid fa-clock-rotate-left"></i> 過去のイベントを表示する
          </button>
        ` : `
          <p class="text-xs text-slate-500 mt-1">他の月を選択するか、「すべて表示」をお試しください。</p>
          <button onclick="selectCardMonth('all')" class="mt-3 inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200 transition">
            すべて表示に戻す
          </button>
        `}
      </div>
    `;
  } else {
    sortedMonthKeys.forEach(monthKey => {
      const [year, month] = monthKey.split("-");
      const monthEvents = monthGroups[monthKey];
      const monthLabel = `${parseInt(month)}月開催一覧`;

      html += `
        <!-- ${monthLabel} ヘッダー -->
        <div class="col-span-full mt-6 mb-2 first:mt-0">
          <div class="flex items-center justify-between pb-3 border-b-2 border-slate-200/90">
            <div class="flex items-center gap-2.5">
              <span class="w-8 h-8 rounded-xl bg-rose-50 text-rose-600 border border-rose-200/60 flex items-center justify-center font-black text-sm shadow-2xs">
                <i class="fa-solid fa-bullhorn"></i>
              </span>
              <h3 class="text-base sm:text-lg font-black text-slate-900 tracking-tight">
                ${year}年 ${monthLabel}
              </h3>
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-100 text-slate-600 border border-slate-200">
                ${monthEvents.length}件
              </span>
            </div>
          </div>
        </div>
      `;

      html += monthEvents.map(ev => createCaravanEventCardHtml(ev, ev.startDate < todayStr)).join("");
    });
  }

  // 過去のイベントが存在する場合のボタントグル（カード一覧下部）
  if (pastEvents.length > 0) {
    if (!showPastEvents) {
      html += `
        <div class="col-span-full my-6 text-center">
          <button onclick="togglePastEvents()" class="inline-flex items-center gap-2.5 px-6 py-3.5 rounded-2xl bg-white hover:bg-slate-100 text-slate-700 text-xs sm:text-sm font-bold border border-slate-300 shadow-xs transition hover:shadow group">
            <i class="fa-solid fa-clock-rotate-left text-slate-500 group-hover:-rotate-45 transition duration-300"></i>
            <span>過去のイベントを表示する（${pastEvents.length}件）</span>
            <i class="fa-solid fa-chevron-down text-[11px] text-slate-400"></i>
          </button>
        </div>
      `;
    } else {
      html += `
        <div class="col-span-full my-6 text-center">
          <button onclick="togglePastEvents()" class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold border border-slate-300 shadow-2xs transition">
            <i class="fa-solid fa-chevron-up text-[10px]"></i>
            <span>過去のイベントを折りたたむ</span>
          </button>
        </div>
      `;
    }
  }

  container.innerHTML = html;
}

// カード一覧 月別フィルター選択
function selectCardMonth(monthKey) {
  selectedCardMonth = monthKey;
  updateMonthFilterUI();
  renderEventsList();
}

// カード一覧 月別フィルターUI更新
function updateMonthFilterUI() {
  const container = document.getElementById("cards-month-filters");
  if (!container) return;
  const buttons = container.querySelectorAll(".month-filter-btn");
  buttons.forEach(btn => {
    const m = btn.getAttribute("data-month");
    if (m === selectedCardMonth) {
      btn.className = "month-filter-btn px-3.5 py-1.5 rounded-full text-xs font-black whitespace-nowrap transition bg-rose-600 text-white shadow-xs";
    } else {
      btn.className = "month-filter-btn px-3.5 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition bg-white text-slate-700 hover:bg-slate-100 border border-slate-200";
    }
  });
}

// 過去イベントフィルターUIの更新
function updatePastEventsFilterUI(pastCount) {
  const btn = document.getElementById("btn-past-events-filter");
  const text = document.getElementById("past-events-filter-text");
  const badge = document.getElementById("past-events-filter-badge");

  if (pastCount === undefined) {
    const todayStr = getTodayString();
    pastCount = getFilteredEvents().filter(e => e.startDate < todayStr).length;
  }

  if (badge) {
    badge.textContent = `${pastCount}件`;
  }

  if (btn && text) {
    if (showPastEvents) {
      btn.className = "px-3.5 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition border border-slate-900 bg-slate-900 text-white shadow-sm flex items-center gap-1.5 shrink-0";
      text.textContent = "過去のイベントを表示中";
    } else {
      btn.className = "px-3.5 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition border border-slate-200 bg-white text-slate-700 hover:bg-slate-100 shadow-2xs flex items-center gap-1.5 shrink-0";
      text.textContent = "過去のイベントを表示";
    }
  }
}

// 過去のイベント表示切り替え
function togglePastEvents() {
  showPastEvents = !showPastEvents;
  updatePastEventsFilterUI();
  renderEventsList();
}

// Create Caravan Event Card HTML
function createCaravanEventCardHtml(ev, isPast = false) {
  const googleUrl = getGoogleCalendarUrl(ev);
  const dayOfWeek = getDayOfWeekStr(ev.startDate);

  return `
    <div class="glass-card rounded-3xl overflow-hidden border border-slate-200/90 shadow-xs hover:shadow-lg transition-all duration-300 flex flex-col group bg-white ${isPast ? "opacity-80" : ""}">
      <!-- Card Image Header -->
      <div class="relative h-48 bg-slate-900 overflow-hidden cursor-pointer" onclick="openEventDetail('${ev.id}')">
        ${ev.image ? `
          <img src="${escapeHtml(ev.image)}" alt="${escapeHtml(ev.title)}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ${isPast ? "grayscale-[30%]" : ""}">
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
        ` : `
          <div class="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-rose-900 via-slate-900 to-indigo-950 p-6 text-center text-white">
            <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-rose-500 text-white mb-2 shadow">会長トークショー</span>
            <p class="font-black text-lg text-white">${escapeHtml(ev.title)}</p>
            <p class="text-xs text-rose-200 font-medium mt-1">${escapeHtml(ev.subtitle || '')}</p>
          </div>
        `}
        <!-- Category & Fee Badges -->
        <div class="absolute top-3 left-3 flex items-center gap-1.5 flex-wrap">
          ${isPast ? `
            <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-slate-800/90 text-slate-300 border border-slate-700 shadow-md">
              <i class="fa-solid fa-check mr-1"></i>終了
            </span>
          ` : ""}
          ${ev.region ? `
            <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-indigo-600 text-white shadow-md">
              <i class="fa-solid fa-location-dot mr-1"></i>${escapeHtml(ev.region)}
            </span>
          ` : ""}
          <span class="px-2.5 py-1 rounded-full text-[10px] font-black text-white shadow-md" style="background-color: ${ev.categoryColor || '#e11d48'};">
            ${escapeHtml(ev.category || 'トークショー')}
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
          <div class="flex items-center gap-2 ${isPast ? 'text-slate-500' : 'text-rose-600'} font-extrabold text-xs mb-2">
            <i class="fa-regular fa-calendar-check text-sm"></i>
            <span>${formatDateJP(ev.startDate)} (${dayOfWeek}) ${ev.startTime}〜${ev.endTime}</span>
          </div>

          <h3 onclick="openEventDetail('${ev.id}')" class="text-base font-black text-slate-900 hover:text-rose-600 transition cursor-pointer mb-2 leading-snug line-clamp-2">
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
        <div class="flex items-center gap-2 pt-3 border-t border-slate-100">
          <button onclick="openEventDetail('${ev.id}')" class="flex-1 py-2 px-3 rounded-xl bg-slate-900 hover:bg-black text-white text-xs font-bold transition flex items-center justify-center gap-1.5 shadow-xs">
            <i class="fa-solid fa-circle-info"></i> 詳細
          </button>
          <a href="${googleUrl}" target="_blank" rel="noopener noreferrer" class="py-2 px-3 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 text-xs font-bold transition flex items-center justify-center gap-1 shadow-xs" title="Googleカレンダーに追加">
            <i class="fa-brands fa-google"></i> 追加
          </a>
          <button onclick="downloadSingleICS('${ev.id}')" class="py-2 px-3 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 text-xs font-bold transition flex items-center justify-center gap-1 shadow-xs" title="スマホカレンダー(.ics)に登録">
            <i class="fa-solid fa-calendar-plus"></i> スマホ登録
          </button>
        </div>
      </div>
    </div>
  `;
}

function clearSelectedDate() {
  selectedDate = null;
  renderEventsList();
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
        <div class="py-1 ${d.isSun ? 'text-rose-600 font-extrabold' : d.isSat ? 'text-blue-600 font-extrabold' : 'text-slate-700'}">
          <div>${d.dayOfWeek}</div>
          <div class="text-sm font-black">${d.dayNum}</div>
        </div>
      `).join("")}
    </div>
    <div class="grid grid-cols-7 min-w-[700px] min-h-[320px] divide-x divide-slate-100 bg-white">
      ${days.map(d => {
        const evs = filtered.filter(e => e.startDate === d.dateStr);
        return `
          <div class="p-2 space-y-2">
            ${evs.map(e => `
              <div onclick="openEventDetail('${e.id}')" class="p-2 rounded-xl bg-rose-50 hover:bg-rose-100 border border-rose-200 cursor-pointer transition text-left text-xs shadow-xs">
                <div class="text-[10px] font-black text-rose-600 mb-0.5">${e.startTime}〜${e.endTime}</div>
                <div class="font-bold text-slate-900 line-clamp-2 leading-tight">${escapeHtml(e.title)}</div>
                <div class="text-[10px] text-slate-500 mt-1 flex items-center gap-1">
                  <i class="fa-solid fa-location-dot text-rose-500 text-[9px]"></i>
                  <span class="truncate">${escapeHtml(e.region || '')}</span>
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

// Modal Detail (ESCキーまたは外側クリックで閉じる)
function openEventDetail(eventId) {
  const ev = allEvents.find(e => e.id === eventId);
  if (!ev) return;

  const modal = document.getElementById("event-modal");
  const modalBody = document.getElementById("event-modal-body");
  if (!modal || !modalBody) return;

  const googleUrl = getGoogleCalendarUrl(ev);
  const dayOfWeek = getDayOfWeekStr(ev.startDate);

  modalBody.innerHTML = `
    <!-- Modal Header -->
    <div class="relative bg-slate-900 text-white p-6 -m-6 sm:-m-8 mb-6 rounded-t-3xl overflow-hidden">
      ${ev.image ? `
        <div class="absolute inset-0 opacity-25">
          <img src="${escapeHtml(ev.image)}" class="w-full h-full object-cover">
        </div>
      ` : ""}
      <div class="relative z-10">
        <div class="flex items-center gap-2 mb-2 flex-wrap">
          ${ev.region ? `
            <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-indigo-500 text-white">
              <i class="fa-solid fa-location-dot mr-1"></i>${escapeHtml(ev.region)}
            </span>
          ` : ""}
          <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-rose-500 text-white">
            ${escapeHtml(ev.category || 'トークショー')}
          </span>
          <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-white/20 backdrop-blur-md text-white">
            ${ev.fee || '無料'}
          </span>
        </div>
        <h2 class="text-xl md:text-2xl font-black text-white leading-tight mb-2 pr-8">
          ${escapeHtml(ev.title)}
        </h2>
        <p class="text-xs text-rose-200 font-medium">
          ${escapeHtml(ev.subtitle || '')}
        </p>
      </div>
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
          <img src="${escapeHtml(ev.image)}" alt="Flyer" class="max-h-[380px] w-auto object-contain">
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

    <!-- Actions: Google Calendar & ICS Download -->
    <div class="flex items-center gap-2.5 flex-wrap pt-3 border-t border-slate-200">
      <a href="${googleUrl}" target="_blank" rel="noopener noreferrer" class="flex-1 py-3 px-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs transition flex items-center justify-center gap-2 shadow-sm">
        <i class="fa-brands fa-google text-sm"></i> Googleカレンダー追加
      </a>
      <button onclick="downloadSingleICS('${ev.id}')" class="flex-1 py-3 px-4 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs transition flex items-center justify-center gap-2 shadow-sm">
        <i class="fa-solid fa-calendar-plus text-sm"></i> スマホに登録 (.ics)
      </button>
      <button onclick="closeEventModal()" class="py-3 px-4 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs transition flex items-center justify-center">
        閉じる
      </button>
    </div>
  `;

  modal.classList.remove("hidden");
  modal.classList.add("flex");
  document.body.style.overflow = "hidden";

  const modalContent = document.getElementById("event-modal-content");
  if (modalContent) {
    modalContent.scrollTop = 0;
  }
}

function closeEventModal() {
  const modal = document.getElementById("event-modal");
  if (modal) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  }
  document.body.style.overflow = "";
}

// Download single ICS
function downloadSingleICS(eventId) {
  const ev = allEvents.find(e => e.id === eventId);
  if (!ev) return;

  const sDate = ev.startDate.replace(/-/g, "") + "T" + ev.startTime.replace(/:/g, "") + "00";
  const eDate = ev.endDate.replace(/-/g, "") + "T" + ev.endTime.replace(/:/g, "") + "00";
  const desc = (ev.description || "").replace(/\n/g, "\\n");

  const ics = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//NEO FAMILY//President Talkshow Calendar//JA",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "BEGIN:VEVENT",
    `UID:${ev.id}@talkshow.neofamily.jp`,
    `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, "").split(".")[0]}Z`,
    `DTSTART;TZID=Asia/Tokyo:${sDate}`,
    `DTEND;TZID=Asia/Tokyo:${eDate}`,
    `SUMMARY:${ev.title}`,
    `DESCRIPTION:${desc}`,
    `LOCATION:${ev.location || ""}`,
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

// Google Calendar URL generator
function getGoogleCalendarUrl(ev) {
  const sDate = ev.startDate.replace(/-/g, "") + "T" + ev.startTime.replace(/:/g, "") + "00";
  const eDate = ev.endDate.replace(/-/g, "") + "T" + ev.endTime.replace(/:/g, "") + "00";

  let details = `${ev.subtitle || ""}\n\n${ev.description || ""}`;
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

// Helpers
function formatDateJP(dateStr) {
  const [y, m, d] = dateStr.split("-");
  return `${parseInt(m, 10)}月${parseInt(d, 10)}日`;
}

function getDayOfWeekStr(dateStr) {
  const [y, m, d] = dateStr.split("-");
  const date = new Date(parseInt(y, 10), parseInt(m, 10) - 1, parseInt(d, 10));
  return ["日", "月", "火", "水", "木", "金", "土"][date.getDay()];
}

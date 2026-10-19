import re

with open('js/admin.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. switchAdminTab の更新
old_switch_tab = '''function switchAdminTab(tabName) {
  const tabs = ["analytics", "events", "settings"];'''

new_switch_tab = '''function switchAdminTab(tabName) {
  const tabs = ["analytics", "events", "members", "settings"];'''

assert old_switch_tab in js, 'old_switch_tab not found'
js = js.replace(old_switch_tab, new_switch_tab)

old_events_call = '''  if (tabName === "events") {
    renderAdminEventsTable();
  }'''

new_events_call = '''  if (tabName === "events") {
    renderAdminEventsTable();
  }
  if (tabName === "members") {
    loadMembersProgressData();
  }'''

assert old_events_call in js, 'old_events_call not found'
js = js.replace(old_events_call, new_events_call)
print("1. switchAdminTab updated with members tab.")

# 2. 会員進捗管理ロジックの追加
members_logic_js = '''
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
'''

js += members_logic_js

with open('js/admin.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("2. js/admin.js successfully updated with members & mentors management logic!")

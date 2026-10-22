/**
 * NEO FAMILY & RAYTUS group
 * 👑 総合管理コントロールパネル (Super Admin)
 */

(function () {
  'use strict';

  const SUPER_PASSCODE = "neo2026";
  const AUTH_KEY = "neofamily_super_admin_auth";
  const MENTORS_STORAGE_KEY = "neofamily_mentors_list";
  const MEMBERS_STORAGE_KEY = "neofamily_cached_members";

  let mentorsList = [];
  let membersList = [];

  // ==================== AUTHENTICATION ====================

  function checkSuperAuth() {
    const isAuthed = sessionStorage.getItem(AUTH_KEY) === "true";
    const gate = document.getElementById("super-login-gate");
    const dashboard = document.getElementById("super-main-dashboard");
    const btnLogout = document.getElementById("super-btn-logout");

    if (isAuthed) {
      if (gate) gate.classList.add("hidden");
      if (dashboard) dashboard.classList.remove("hidden");
      if (btnLogout) btnLogout.classList.remove("hidden");
      loadSuperAdminData();
    } else {
      if (gate) gate.classList.remove("hidden");
      if (dashboard) dashboard.classList.add("hidden");
      if (btnLogout) btnLogout.classList.add("hidden");
    }
  }

  window.handleSuperLogin = function () {
    const input = document.getElementById("super-passcode-input");
    const err = document.getElementById("super-login-error");
    if (!input) return;

    if (input.value.trim() === SUPER_PASSCODE) {
      sessionStorage.setItem(AUTH_KEY, "true");
      if (err) err.classList.add("hidden");
      input.value = "";
      checkSuperAuth();
    } else {
      if (err) err.classList.remove("hidden");
      input.focus();
    }
  };

  window.quickSuperLogin = function () {
    const input = document.getElementById("super-passcode-input");
    if (input) input.value = SUPER_PASSCODE;
    window.handleSuperLogin();
  };

  window.superAdminLogout = function () {
    if (confirm("総合管理パネルからログアウトしますか？")) {
      sessionStorage.removeItem(AUTH_KEY);
      checkSuperAuth();
    }
  };

  window.toggleSuperPasscodeVisibility = function () {
    const input = document.getElementById("super-passcode-input");
    const icon = document.getElementById("super-eye-icon");
    if (!input || !icon) return;
    if (input.type === "password") {
      input.type = "text";
      icon.className = "fa-regular fa-eye-slash";
    } else {
      input.type = "password";
      icon.className = "fa-regular fa-eye";
    }
  };

  // ==================== DATA MANAGEMENT ====================

  function loadSuperAdminData() {
    // 1. 理事長・担当者メンバー
    const localMentors = localStorage.getItem(MENTORS_STORAGE_KEY);
    if (localMentors) {
      try {
        mentorsList = JSON.parse(localMentors);
      } catch (e) {
        mentorsList = getDefaultMentors();
      }
    } else {
      mentorsList = getDefaultMentors();
      localStorage.setItem(MENTORS_STORAGE_KEY, JSON.stringify(mentorsList));
    }

    // 2. 会員進捗データ
    const localMembers = localStorage.getItem(MEMBERS_STORAGE_KEY);
    if (localMembers) {
      try {
        membersList = JSON.parse(localMembers);
      } catch (e) {
        membersList = [];
      }
    } else {
      membersList = [];
    }

    renderAllSuperAdminUI();
  }

  function getDefaultMentors() {
    return [
      { id: "mentor_tanaka", name: "田中 健一", teamName: "チームAblaze", role: "理事長", email: "tanaka@example.com", status: "active" },
      { id: "mentor_sato", name: "佐藤 美咲", teamName: "チームRe:Spark", role: "理事長", email: "sato@example.com", status: "active" },
      { id: "mentor_suzuki", name: "鈴木 隆", teamName: "チームtidy.shin", role: "副理事長", email: "suzuki@example.com", status: "active" }
    ];
  }

  function saveMentors() {
    localStorage.setItem(MENTORS_STORAGE_KEY, JSON.stringify(mentorsList));
    renderAllSuperAdminUI();
  }

  // ==================== UI RENDERING ====================

  window.renderAllSuperAdminUI = function () {
    renderKPI();
    renderMentorsTable();
  };

  function renderKPI() {
    const elMentors = document.getElementById("kpi-super-mentors-count");
    const elTeams = document.getElementById("kpi-super-teams-count");
    const elMembers = document.getElementById("kpi-super-members-count");
    const elUnassigned = document.getElementById("kpi-super-unassigned-count");

    if (elMentors) elMentors.textContent = mentorsList.length;

    // ユニークチーム数
    const teams = new Set(mentorsList.map(m => m.teamName).filter(Boolean));
    if (elTeams) elTeams.textContent = teams.size;

    if (elMembers) elMembers.textContent = membersList.length;

    const unassignedCount = membersList.filter(m => !m.mentorId || m.mentorId === "unassigned").length;
    if (elUnassigned) elUnassigned.textContent = unassignedCount;
  }

  function renderMentorsTable() {
    const tbody = document.getElementById("super-mentors-table-body");
    if (!tbody) return;

    if (mentorsList.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="7" class="py-8 text-center text-slate-400">
            <i class="fa-solid fa-users-slash text-2xl mb-2 block"></i>
            登録されている理事長・担当者がいません。「新規 理事長 / 担当者を追加」から登録してください。
          </td>
        </tr>
      `;
      return;
    }

    tbody.innerHTML = mentorsList.map((m, idx) => {
      // 担当している会員数
      const assignedCount = membersList.filter(x => x.mentorId === m.id).length;
      const statusBadge = m.status === "active"
        ? `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800"><i class="fa-solid fa-circle-check text-[9px]"></i> 有効</span>`
        : `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-600">休止中</span>`;

      return `
        <tr class="hover:bg-slate-50/80 transition">
          <td class="py-3 px-4 font-bold text-slate-900">
            <div class="flex items-center gap-2">
              <span class="w-7 h-7 rounded-lg bg-purple-100 text-purple-700 font-bold flex items-center justify-center text-xs">
                ${m.name.charAt(0)}
              </span>
              <span>${m.name}</span>
            </div>
          </td>
          <td class="py-3 px-4 font-semibold text-slate-800">${m.teamName || '—'}</td>
          <td class="py-3 px-4 font-bold text-indigo-700">${m.role || '理事長'}</td>
          <td class="py-3 px-4 font-mono text-[11px] text-slate-500">${m.email || '未設定'}</td>
          <td class="py-3 px-4 text-center">
            <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-bold ${assignedCount > 0 ? 'bg-indigo-50 text-indigo-700 border border-indigo-200' : 'bg-slate-100 text-slate-400'}">
              ${assignedCount} 名
            </span>
          </td>
          <td class="py-3 px-4 text-center">${statusBadge}</td>
          <td class="py-3 px-4 text-right">
            <div class="flex items-center justify-end gap-1.5">
              <button onclick="editMentor('${m.id}')" class="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-purple-50 text-slate-600 hover:text-purple-700 font-bold text-xs transition shadow-2xs cursor-pointer">
                <i class="fa-solid fa-pen-to-square mr-0.5"></i> 編集
              </button>
              <button onclick="deleteMentor('${m.id}')" class="px-2 py-1.5 rounded-lg bg-slate-100 hover:bg-rose-50 text-slate-400 hover:text-rose-600 font-bold text-xs transition shadow-2xs cursor-pointer" title="削除">
                <i class="fa-regular fa-trash-can"></i>
              </button>
            </div>
          </td>
        </tr>
      `;
    }).join("");
  }

  // ==================== MENTOR MODAL & CRUD ====================

  window.openMentorModal = function (mentorId = null) {
    const modal = document.getElementById("mentor-modal");
    const title = document.getElementById("mentor-modal-title");
    const formId = document.getElementById("mentor-form-id");
    const formName = document.getElementById("mentor-form-name");
    const formTeam = document.getElementById("mentor-form-team");
    const formRole = document.getElementById("mentor-form-role");
    const formEmail = document.getElementById("mentor-form-email");
    const formStatus = document.getElementById("mentor-form-status");

    if (!modal) return;

    if (mentorId) {
      const target = mentorsList.find(m => m.id === mentorId);
      if (!target) return;
      title.textContent = "理事長・担当者を編集";
      formId.value = target.id;
      formName.value = target.name || "";
      formTeam.value = target.teamName || "";
      formRole.value = target.role || "理事長";
      formEmail.value = target.email || "";
      formStatus.value = target.status || "active";
    } else {
      title.textContent = "新規 理事長・担当者を登録";
      formId.value = "";
      formName.value = "";
      formTeam.value = "";
      formRole.value = "理事長";
      formEmail.value = "";
      formStatus.value = "active";
    }

    modal.classList.remove("hidden");
  };

  window.closeMentorModal = function () {
    const modal = document.getElementById("mentor-modal");
    if (modal) modal.classList.add("hidden");
  };

  window.editMentor = function (mentorId) {
    window.openMentorModal(mentorId);
  };

  window.handleMentorFormSubmit = function (e) {
    e.preventDefault();
    const id = document.getElementById("mentor-form-id").value;
    const name = document.getElementById("mentor-form-name").value.trim();
    const teamName = document.getElementById("mentor-form-team").value.trim();
    const role = document.getElementById("mentor-form-role").value;
    const email = document.getElementById("mentor-form-email").value.trim();
    const status = document.getElementById("mentor-form-status").value;

    if (!name || !teamName) {
      alert("氏名と所属チーム名は必須です。");
      return;
    }

    if (id) {
      // 編集
      const target = mentorsList.find(m => m.id === id);
      if (target) {
        target.name = name;
        target.teamName = teamName;
        target.role = role;
        target.email = email;
        target.status = status;
      }
    } else {
      // 新規登録
      const newId = "mentor_" + Date.now().toString(36);
      mentorsList.push({
        id: newId,
        name,
        teamName,
        role,
        email,
        status
      });
    }

    saveMentors();
    window.closeMentorModal();
    alert("理事長・担当者メンバー情報を保存しました。\n（一般管理画面の選択肢にも自動反映されます）");
  };

  window.deleteMentor = function (mentorId) {
    const target = mentorsList.find(m => m.id === mentorId);
    if (!target) return;

    const assignedCount = membersList.filter(x => x.mentorId === mentorId).length;
    let confirmMsg = `「${target.name}（${target.teamName}）」を削除しますか？`;
    if (assignedCount > 0) {
      confirmMsg += `\n\n⚠️ 現在この担当者に割り当てられている会員が ${assignedCount} 名います。\n削除すると、該当会員の担当は「未割り当て」に自動変更されます。`;
    }

    if (!confirm(confirmMsg)) return;

    // 該当会員の割り当てを解除
    if (assignedCount > 0) {
      membersList.forEach(m => {
        if (m.mentorId === mentorId) {
          m.mentorId = "unassigned";
        }
      });
      localStorage.setItem(MEMBERS_STORAGE_KEY, JSON.stringify(membersList));
    }

    mentorsList = mentorsList.filter(m => m.id !== mentorId);
    saveMentors();
    alert(`「${target.name}」を削除しました。`);
  };

  // ==================== TAB SWITCHING ====================

  window.switchSuperTab = function (tabName) {
    const tabs = ["mentors", "accounts", "settings"];
    tabs.forEach(t => {
      const btn = document.getElementById(`tab-btn-super-${t}`);
      const content = document.getElementById(`super-tab-content-${t}`);
      if (t === tabName) {
        if (btn) {
          btn.className = "px-4 py-3 border-b-2 border-purple-600 text-purple-700 flex items-center gap-2 whitespace-nowrap transition font-bold";
        }
        if (content) content.classList.remove("hidden");
      } else {
        if (btn) {
          btn.className = "px-4 py-3 border-b-2 border-transparent text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap transition font-bold";
        }
        if (content) content.classList.add("hidden");
      }
    });
  };

  // ==================== CSV EXPORT ====================

  window.exportSuperAdminData = function (type) {
    let csv = "";
    let filename = "";

    if (type === "mentors") {
      filename = `mentors_list_${new Date().toISOString().slice(0, 10)}.csv`;
      csv = "\uFEFF担当者ID,氏名,所属チーム,役職,個別ID/メール,ステータス\n";
      mentorsList.forEach(m => {
        csv += `"${m.id}","${m.name}","${m.teamName || ''}","${m.role || ''}","${m.email || ''}","${m.status || ''}"\n`;
      });
    } else {
      filename = `members_progress_${new Date().toISOString().slice(0, 10)}.csv`;
      csv = "\uFEFF会員ID,担当者ID,担当者名,Zoom参加,定例会参加,相談窓口利用,閲覧コンテンツ数,最終アクセス日時\n";
      membersList.forEach(m => {
        const s = m.onboardingSteps || {};
        const mentor = mentorsList.find(x => x.id === m.mentorId);
        const mentorName = mentor ? `${mentor.name} (${mentor.teamName})` : (m.mentorId === "unassigned" ? "未割り当て" : (m.mentorId || ""));
        const viewedCount = Object.keys(m.viewedContents || {}).length;
        csv += `"${m.memberId}","${m.mentorId || ''}","${mentorName}","${s.zoom ? '済' : '未'}","${s.teireikai ? '済' : '未'}","${s.support ? '済' : '未'}","${viewedCount}","${m.lastActiveAt || ''}"\n`;
      });
    }

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  };

  window.resetSuperAdminDemoData = function () {
    if (confirm("理事長メンバーリストを初期状態（田中/佐藤/鈴木）にリセットしますか？")) {
      mentorsList = getDefaultMentors();
      saveMentors();
      alert("初期データに戻しました。");
    }
  };

  // 初期化
  document.addEventListener("DOMContentLoaded", () => {
    checkSuperAuth();
  });

})();

/**
 * NEO FAMILY & RAYTUS group
 * インタラクティブ・フローチャート (段階展開ノードマップ)
 * 選択肢を1つ選ぶごとに、その下のノードが段階的にアンロック・展開される
 */

(function () {
  'use strict';

  // --- Sound Effects (Disabled as per user request) ---
  let isSoundEnabled = false;

  function playSound(type) {
    // Sound disabled
  }

  window.toggleSound = function () {
    // No-op
  };

  // --- Support & Original Images Visibility Controller ---
  function showSupportAndOriginals(scroll = false) {
    const container = document.getElementById('support-and-originals-container');
    if (!container) return;

    container.classList.remove('hidden');
    // Force reflow for smooth CSS fade-in
    void container.offsetWidth;
    container.classList.remove('opacity-0', 'translate-y-6');
    container.classList.add('opacity-100', 'translate-y-0');

    const label = document.getElementById('label-toggle-support');
    if (label) label.textContent = 'サポート一覧を閉じる';

    if (scroll) {
      setTimeout(() => {
        container.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 150);
    }
  }

  function hideSupportAndOriginals() {
    const container = document.getElementById('support-and-originals-container');
    if (!container) return;

    container.classList.remove('opacity-100', 'translate-y-0');
    container.classList.add('opacity-0', 'translate-y-6');
    setTimeout(() => {
      if (container.classList.contains('opacity-0')) {
        container.classList.add('hidden');
      }
    }, 500);

    const label = document.getElementById('label-toggle-support');
    if (label) label.textContent = 'サポート一覧を表示';
  }

  window.toggleSupportAndOriginals = function () {
    const container = document.getElementById('support-and-originals-container');
    if (!container) return;
    if (container.classList.contains('hidden') || container.classList.contains('opacity-0')) {
      showSupportAndOriginals(true);
    } else {
      hideSupportAndOriginals();
    }
  };

  // --- Support Table Filter & Highlight (Only show highlighted rows on goal reach) ---
  function filterSupportRows(targetRowId) {
    const notice = document.getElementById('support-filter-notice');
    const counselingNotice = document.getElementById('support-counseling-notice');
    const rows = document.querySelectorAll('.support-table-row');

    if (counselingNotice) counselingNotice.classList.add('hidden');

    if (!targetRowId || targetRowId === 'all') {
      // すべて表示
      rows.forEach(r => {
        r.classList.remove('hidden');
        r.classList.remove('bg-amber-50', 'ring-2', 'ring-amber-400', 'animate-pulse');
      });
      if (notice) {
        notice.classList.add('hidden');
        notice.classList.remove('flex');
      }
      return;
    }

    if (targetRowId === 'counseling') {
      // 理事長相談（サポート一覧原本にはないため全件+案内表示）
      rows.forEach(r => {
        r.classList.remove('hidden');
        r.classList.remove('bg-amber-50', 'ring-2', 'ring-amber-400', 'animate-pulse');
      });
      if (notice) {
        notice.classList.add('hidden');
        notice.classList.remove('flex');
      }
      if (counselingNotice) counselingNotice.classList.remove('hidden');
      return;
    }

    // 指定されたサポート行のみを表示（色づけ）
    let matched = false;
    rows.forEach(r => {
      r.classList.remove('bg-amber-50', 'ring-2', 'ring-amber-400', 'animate-pulse');
      if (r.id === targetRowId) {
        r.classList.remove('hidden');
        r.classList.add('bg-amber-50', 'ring-2', 'ring-amber-400');
        matched = true;
      } else {
        r.classList.add('hidden');
      }
    });

    if (notice) {
      if (matched) {
        notice.classList.remove('hidden');
        notice.classList.add('flex');
      } else {
        notice.classList.add('hidden');
        notice.classList.remove('flex');
        rows.forEach(r => r.classList.remove('hidden'));
      }
    }
  }

  // フィルターリセット用グローバル関数
  window.resetSupportTableFilter = function () {
    filterSupportRows('all');
  };

  // --- Flowchart State ---
  const state = {
    step1: null,   // 'clear' | 'unclear'
    step2: null,   // 'not_latest' | 'latest'
    step3: null,   // 'no_iyasaka' | 'has_iyasaka'
    step4a: null,  // 'apply_not_yet' | 'apply_done'
    step5a: null,  // 'profile_not_yet' | 'profile_done'
    step4b: null,  // 'ginger_unknown' | 'ginger_done'
    step5b: null   // 'eeda_intro' | 'eeda_work'
  };

  // --- Helper to toggle buttons visually ---
  function setActiveChoice(groupId, activeBtnId) {
    const group = document.getElementById(groupId);
    if (!group) return;
    group.querySelectorAll('.flow-choice-btn').forEach(btn => {
      btn.classList.remove('border-blue-600', 'bg-blue-600', 'text-white', 'border-purple-600', 'bg-purple-600', 'shadow-md', 'scale-102');
      btn.classList.add('border-slate-300', 'bg-white', 'text-slate-700', 'hover:bg-slate-50');
      const check = btn.querySelector('.choice-check');
      if (check) check.classList.add('hidden');
    });

    const activeBtn = document.getElementById(activeBtnId);
    if (activeBtn) {
      activeBtn.classList.remove('border-slate-300', 'bg-white', 'text-slate-700', 'hover:bg-slate-50');
      activeBtn.classList.add('border-blue-600', 'bg-blue-600', 'text-white', 'shadow-md', 'scale-102');
      const check = activeBtn.querySelector('.choice-check');
      if (check) check.classList.remove('hidden');
    }
  }

  // --- Reach Goal Helper: Show Goal node & reveal filtered support table/originals smoothly ---
  function onReachGoal(goalNodeId, supportRowId) {
    showNode(goalNodeId);
    showSupportAndOriginals(false);
    setTimeout(() => {
      filterSupportRows(supportRowId);
    }, 200);
  }

  // --- Step 1: やることは明確？ ---
  window.chooseStep1 = function (val) {
    state.step1 = val;
    setActiveChoice('step1-choices', val === 'clear' ? 'btn-step1-clear' : 'btn-step1-unclear');

    // Hide all downstream nodes
    hideDownstreamFrom(1);

    if (val === 'unclear') {
      // Show Goal: 理事長に相談（原本一覧にはないため理事長案内を表示）
      onReachGoal('goal-counseling-node', 'counseling');
    } else {
      // Show Step 2: 最新情報に触れてる？
      showNode('step2-node');
    }
  };

  // --- Step 2: 最新情報に触れてる？ ---
  window.chooseStep2 = function (val) {
    state.step2 = val;
    setActiveChoice('step2-choices', val === 'not_latest' ? 'btn-step2-not-latest' : 'btn-step2-latest');

    hideDownstreamFrom(2);

    if (val === 'not_latest') {
      // Show Goal: NEO構想 ぎゅっと勉強会
      onReachGoal('goal-neo-study-node', 'support-row-neo-study');
    } else {
      // Show Step 3: Iyasaka宮に出品してる？
      showNode('step3-node');
    }
  };

  // --- Step 3: Iyasaka宮に出品してる？ ---
  window.chooseStep3 = function (val) {
    state.step3 = val;
    setActiveChoice('step3-choices', val === 'no_iyasaka' ? 'btn-step3-no' : 'btn-step3-yes');

    hideDownstreamFrom(3);

    if (val === 'no_iyasaka') {
      // 出してない ➜ Step 4A: 出店申請は終わってる？
      showNode('step4a-node');
    } else {
      // 出してる ➜ Step 4B: 勉強ジンジャー出品してる？
      showNode('step4b-node');
    }
  };

  // --- Step 4A: 出店申請は終わってる？ ---
  window.chooseStep4a = function (val) {
    state.step4a = val;
    setActiveChoice('step4a-choices', val === 'apply_not_yet' ? 'btn-step4a-no' : 'btn-step4a-yes');

    hideDownstreamFrom(4, 'a');

    if (val === 'apply_not_yet') {
      // まだ ➜ Goal: 出店申請
      onReachGoal('goal-apply-node', 'support-row-iyasaka-work');
    } else {
      // 終わってる ➜ Step 5A: プロフィール設定や出品方法は把握してる？
      showNode('step5a-node');
    }
  };

  // --- Step 5A: プロフィール設定や出品方法は把握してる？ ---
  window.chooseStep5a = function (val) {
    state.step5a = val;
    setActiveChoice('step5a-choices', val === 'profile_not_yet' ? 'btn-step5a-no' : 'btn-step5a-yes');

    hideDownstreamFrom(5, 'a');

    if (val === 'profile_not_yet') {
      // まだ / 把握してない ➜ Goal: Iyasaka宮 作業会
      onReachGoal('goal-iyasaka-work-node', 'support-row-iyasaka-work');
    } else {
      // してる ➜ 勉強ジンジャー (Step 4B) へ合流！
      showNode('step4b-node');
    }
  };

  // --- Step 4B: 勉強ジンジャー出品してる？ ---
  window.chooseStep4b = function (val) {
    state.step4b = val;
    setActiveChoice('step4b-choices', val === 'ginger_unknown' ? 'btn-step4b-unknown' : 'btn-step4b-done');

    hideDownstreamFrom(4, 'b');

    if (val === 'ginger_unknown') {
      // やり方がわからない ➜ Goal: 勉強ジンジャー活用サポート
      onReachGoal('goal-ginger-node', 'support-row-ginger');
    } else {
      // してる / 今はやらない ➜ Step 5B: EEDA動画出してる？
      showNode('step5b-node');
    }
  };

  // --- Step 5B: EEDA動画出してる？ ---
  window.chooseStep5b = function (val) {
    state.step5b = val;
    setActiveChoice('step5b-choices', val === 'eeda_intro' ? 'btn-step5b-intro' : 'btn-step5b-work');

    hideDownstreamFrom(5, 'b');

    if (val === 'eeda_intro') {
      // そもそもを知りたい ➜ Goal: EEDA探検ポチポチ会
      onReachGoal('goal-eeda-pochi-node', 'support-row-eeda-pochi');
    } else {
      // 制作進まない / 質問したい ➜ Goal: EEDA作業会
      onReachGoal('goal-eeda-work-node', 'support-row-eeda-pochi');
    }
  };

  // --- Show Node with smooth scroll ---
  function showNode(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.remove('hidden');
    el.classList.add('flex');
    setTimeout(() => {
      el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
  }

  function hideNode(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.add('hidden');
    el.classList.remove('flex');
  }

  // --- Hide downstream nodes when a previous choice changes ---
  function hideDownstreamFrom(level, branch = '') {
    const allNodes = [
      'goal-counseling-node',
      'step2-node',
      'goal-neo-study-node',
      'step3-node',
      'step4a-node',
      'goal-apply-node',
      'step5a-node',
      'goal-iyasaka-work-node',
      'step4b-node',
      'goal-ginger-node',
      'step5b-node',
      'goal-eeda-pochi-node',
      'goal-eeda-work-node'
    ];

    if (level === 1) {
      allNodes.forEach(hideNode);
      filterSupportRows('all');
    } else if (level === 2) {
      allNodes.slice(2).forEach(hideNode);
      filterSupportRows('all');
    } else if (level === 3) {
      allNodes.slice(4).forEach(hideNode);
      filterSupportRows('all');
    } else if (level === 4) {
      if (branch === 'a') {
        ['goal-apply-node', 'step5a-node', 'goal-iyasaka-work-node'].forEach(hideNode);
      } else {
        ['goal-ginger-node', 'step5b-node', 'goal-eeda-pochi-node', 'goal-eeda-work-node'].forEach(hideNode);
      }
      filterSupportRows('all');
    } else if (level === 5) {
      if (branch === 'a') {
        ['goal-iyasaka-work-node'].forEach(hideNode);
      } else {
        ['goal-eeda-pochi-node', 'goal-eeda-work-node'].forEach(hideNode);
      }
      filterSupportRows('all');
    }

    // Check if any goal node is still visible; if not, collapse support & originals
    const anyGoalVisible = allNodes.some(id => id.startsWith('goal-') && !document.getElementById(id)?.classList.contains('hidden'));
    if (!anyGoalVisible) {
      hideSupportAndOriginals();
      filterSupportRows('all');
    }
  }

  // --- Reset Entire Flowchart ---
  window.resetFlowchart = function () {
    hideSupportAndOriginals();
    filterSupportRows('all');
    Object.keys(state).forEach(k => state[k] = null);
    hideDownstreamFrom(1);

    document.querySelectorAll('.flow-choice-btn').forEach(btn => {
      btn.classList.remove('border-blue-600', 'bg-blue-600', 'text-white', 'border-purple-600', 'bg-purple-600', 'shadow-md', 'scale-102');
      btn.classList.add('border-slate-300', 'bg-white', 'text-slate-700', 'hover:bg-slate-50');
      const check = btn.querySelector('.choice-check');
      if (check) check.classList.add('hidden');
    });

    const root = document.getElementById('step1-node');
    if (root) {
      root.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  // --- Scroll to section helper ---
  window.scrollToSection = function (sectionId) {
    showSupportAndOriginals(false);
    setTimeout(() => {
      const el = document.getElementById(sectionId);
      if (el) {
        const headerOffset = 80;
        const elementPosition = el.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    }, 100);
  };

  // --- Copy Zoom Info Helper ---
  window.copyZoomInfo = function () {
    const text = '【NEO FAMILY 全日共通Zoom】\nミーティングID: 811 1315 2898\nパスコード: 2026\n参加URL: https://us06web.zoom.us/j/81113152898?pwd=rnUDogc0paequYOxCnvXYaSs3WngG3.1';
    navigator.clipboard.writeText(text).then(() => {
      alert('Zoom情報をクリップボードにコピーしました！\nそのままLINEやメモに貼り付けられます。');
    }).catch(() => {
      prompt('以下のZoom情報をコピーしてください:', text);
    });
  };

})();

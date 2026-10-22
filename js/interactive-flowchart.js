/**
 * NEO FAMILY & RAYTUS group
 * インタラクティブ・フローチャート (段階展開ノードマップ)
 * 選択肢を1つ選ぶごとに、その下のノードが段階的にアンロック・展開される
 */

(function () {
  'use strict';

  // --- Sound Effects using Web Audio API ---
  let audioCtx = null;
  let isSoundEnabled = true;

  function initAudio() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) audioCtx = new AudioContext();
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  }

  function playSound(type) {
    if (!isSoundEnabled) return;
    try {
      initAudio();
      if (!audioCtx) return;
      const now = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.connect(gain);
      gain.connect(audioCtx.destination);

      if (type === 'select') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.exponentialRampToValueAtTime(660, now + 0.08);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.08);
        osc.start(now);
        osc.stop(now + 0.08);
      } else if (type === 'goal') {
        const notes = [
          { f: 523.25, d: 0.1, t: 0 },
          { f: 659.25, d: 0.1, t: 0.1 },
          { f: 783.99, d: 0.15, t: 0.2 },
          { f: 1046.50, d: 0.3, t: 0.3 }
        ];
        notes.forEach(n => {
          const o = audioCtx.createOscillator();
          const g = audioCtx.createGain();
          o.type = 'triangle';
          o.frequency.setValueAtTime(n.f, now + n.t);
          g.gain.setValueAtTime(0.12, now + n.t);
          g.gain.exponentialRampToValueAtTime(0.001, now + n.t + n.d);
          o.connect(g);
          g.connect(audioCtx.destination);
          o.start(now + n.t);
          o.stop(now + n.t + n.d);
        });
      }
    } catch (e) {
      // Audio fallback silent
    }
  }

  // --- Sound Toggle ---
  window.toggleSound = function () {
    isSoundEnabled = !isSoundEnabled;
    const icon = document.getElementById('sound-toggle-icon');
    const label = document.getElementById('sound-toggle-label');
    if (icon) {
      icon.className = isSoundEnabled ? 'fa-solid fa-volume-high text-amber-500' : 'fa-solid fa-volume-xmark text-slate-400';
    }
    if (label) {
      label.textContent = isSoundEnabled ? '効果音: ON' : '効果音: OFF';
    }
    if (isSoundEnabled) playSound('select');
  };

  // --- Support Table Highlight ---
  function highlightSupportRow(rowId) {
    document.querySelectorAll('.support-table-row').forEach(r => {
      r.classList.remove('bg-amber-50', 'ring-2', 'ring-amber-400', 'animate-pulse');
    });
    if (!rowId) return;
    const row = document.getElementById(rowId);
    if (row) {
      row.classList.add('bg-amber-50', 'ring-2', 'ring-amber-400', 'animate-pulse');
      setTimeout(() => row.classList.remove('animate-pulse'), 3000);
      row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

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

  // --- Step 1: やることは明確？ ---
  window.chooseStep1 = function (val) {
    playSound('select');
    state.step1 = val;
    setActiveChoice('step1-choices', val === 'clear' ? 'btn-step1-clear' : 'btn-step1-unclear');

    // Hide all downstream nodes
    hideDownstreamFrom(1);

    if (val === 'unclear') {
      // Show Goal: 理事長に相談
      showNode('goal-counseling-node');
      highlightSupportRow('support-row-counseling');
      playSound('goal');
    } else {
      // Show Step 2: 最新情報に触れてる？
      showNode('step2-node');
    }
  };

  // --- Step 2: 最新情報に触れてる？ ---
  window.chooseStep2 = function (val) {
    playSound('select');
    state.step2 = val;
    setActiveChoice('step2-choices', val === 'not_latest' ? 'btn-step2-not-latest' : 'btn-step2-latest');

    hideDownstreamFrom(2);

    if (val === 'not_latest') {
      // Show Goal: NEO構想 ぎゅっと勉強会
      showNode('goal-neo-study-node');
      highlightSupportRow('support-row-neo-study');
      playSound('goal');
    } else {
      // Show Step 3: Iyasaka宮に出品してる？
      showNode('step3-node');
    }
  };

  // --- Step 3: Iyasaka宮に出品してる？ ---
  window.chooseStep3 = function (val) {
    playSound('select');
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
    playSound('select');
    state.step4a = val;
    setActiveChoice('step4a-choices', val === 'apply_not_yet' ? 'btn-step4a-no' : 'btn-step4a-yes');

    hideDownstreamFrom(4, 'a');

    if (val === 'apply_not_yet') {
      // まだ ➜ Goal: 出店申請
      showNode('goal-apply-node');
      highlightSupportRow('support-row-iyasaka-work');
      playSound('goal');
    } else {
      // 終わってる ➜ Step 5A: プロフィール設定や出品方法は把握してる？
      showNode('step5a-node');
    }
  };

  // --- Step 5A: プロフィール設定や出品方法は把握してる？ ---
  window.chooseStep5a = function (val) {
    playSound('select');
    state.step5a = val;
    setActiveChoice('step5a-choices', val === 'profile_not_yet' ? 'btn-step5a-no' : 'btn-step5a-yes');

    hideDownstreamFrom(5, 'a');

    if (val === 'profile_not_yet') {
      // まだ / 把握してない ➜ Goal: Iyasaka宮 作業会
      showNode('goal-iyasaka-work-node');
      highlightSupportRow('support-row-iyasaka-work');
      playSound('goal');
    } else {
      // してる ➜ 勉強ジンジャー (Step 4B) へ合流！
      showNode('step4b-node');
    }
  };

  // --- Step 4B: 勉強ジンジャー出品してる？ ---
  window.chooseStep4b = function (val) {
    playSound('select');
    state.step4b = val;
    setActiveChoice('step4b-choices', val === 'ginger_unknown' ? 'btn-step4b-unknown' : 'btn-step4b-done');

    hideDownstreamFrom(4, 'b');

    if (val === 'ginger_unknown') {
      // やり方がわからない ➜ Goal: 勉強ジンジャー活用サポート
      showNode('goal-ginger-node');
      highlightSupportRow('support-row-ginger');
      playSound('goal');
    } else {
      // してる / 今はやらない ➜ Step 5B: EEDA動画出してる？
      showNode('step5b-node');
    }
  };

  // --- Step 5B: EEDA動画出してる？ ---
  window.chooseStep5b = function (val) {
    playSound('select');
    state.step5b = val;
    setActiveChoice('step5b-choices', val === 'eeda_intro' ? 'btn-step5b-intro' : 'btn-step5b-work');

    hideDownstreamFrom(5, 'b');

    if (val === 'eeda_intro') {
      // そもそもを知りたい ➜ Goal: EEDA探検ポチポチ会
      showNode('goal-eeda-pochi-node');
      highlightSupportRow('support-row-eeda-pochi');
      playSound('goal');
    } else {
      // 制作進まない / 質問したい ➜ Goal: EEDA作業会
      showNode('goal-eeda-work-node');
      highlightSupportRow('support-row-eeda-work');
      playSound('goal');
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
      highlightSupportRow(null);
    } else if (level === 2) {
      allNodes.slice(2).forEach(hideNode);
      highlightSupportRow(null);
    } else if (level === 3) {
      allNodes.slice(4).forEach(hideNode);
      highlightSupportRow(null);
    } else if (level === 4) {
      if (branch === 'a') {
        ['goal-apply-node', 'step5a-node', 'goal-iyasaka-work-node'].forEach(hideNode);
      } else {
        ['goal-ginger-node', 'step5b-node', 'goal-eeda-pochi-node', 'goal-eeda-work-node'].forEach(hideNode);
      }
    } else if (level === 5) {
      if (branch === 'a') {
        ['goal-iyasaka-work-node'].forEach(hideNode);
      } else {
        ['goal-eeda-pochi-node', 'goal-eeda-work-node'].forEach(hideNode);
      }
    }
  }

  // --- Reset Entire Flowchart ---
  window.resetFlowchart = function () {
    playSound('select');
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

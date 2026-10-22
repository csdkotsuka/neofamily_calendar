/**
 * NEO FAMILY & RAYTUS group
 * イベント参加フロー クエスト (Interactive Flowchart Game)
 */

(function () {
  'use strict';

  // --- Sound Effects using Web Audio API (No external sound files required) ---
  let audioCtx = null;
  let isSoundEnabled = true;

  function initAudio() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        audioCtx = new AudioContext();
      }
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
        // Crisp pop/click
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.exponentialRampToValueAtTime(880, now + 0.08);
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.08);
        osc.start(now);
        osc.stop(now + 0.08);
      } else if (type === 'back') {
        // Back note
        osc.type = 'sine';
        osc.frequency.setValueAtTime(520, now);
        osc.frequency.exponentialRampToValueAtTime(260, now + 0.1);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.1);
        osc.start(now);
        osc.stop(now + 0.1);
      } else if (type === 'clear') {
        // Victory Fanfare (Do-Mi-Sol-Do-Mi-Sol High!)
        const notes = [
          { f: 523.25, d: 0.1, t: 0 },       // C5
          { f: 659.25, d: 0.1, t: 0.1 },     // E5
          { f: 783.99, d: 0.1, t: 0.2 },     // G5
          { f: 1046.50, d: 0.35, t: 0.3 }    // C6
        ];
        notes.forEach(n => {
          const o = audioCtx.createOscillator();
          const g = audioCtx.createGain();
          o.type = 'triangle';
          o.frequency.setValueAtTime(n.f, now + n.t);
          g.gain.setValueAtTime(0.15, now + n.t);
          g.gain.exponentialRampToValueAtTime(0.001, now + n.t + n.d);
          o.connect(g);
          g.connect(audioCtx.destination);
          o.start(now + n.t);
          o.stop(now + n.t + n.d);
        });
      }
    } catch (e) {
      console.warn('Audio play error:', e);
    }
  }

  // --- Confetti Animation for Game Clear ---
  function launchConfetti() {
    const canvas = document.getElementById('quest-confetti-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.parentElement.offsetWidth;
    canvas.height = canvas.parentElement.offsetHeight;

    const pieces = [];
    const colors = ['#f43f5e', '#fbbf24', '#3b82f6', '#10b981', '#8b5cf6', '#ec4899'];
    for (let i = 0; i < 70; i++) {
      pieces.push({
        x: Math.random() * canvas.width,
        y: Math.random() * -canvas.height * 0.5,
        w: Math.random() * 8 + 4,
        h: Math.random() * 6 + 4,
        color: colors[Math.floor(Math.random() * colors.length)],
        vy: Math.random() * 3 + 2,
        vx: (Math.random() - 0.5) * 2,
        rot: Math.random() * 360,
        vrot: (Math.random() - 0.5) * 10
      });
    }

    let frame = 0;
    function render() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      pieces.forEach(p => {
        p.y += p.vy;
        p.x += p.vx;
        p.rot += p.vrot;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate((p.rot * Math.PI) / 180);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
        ctx.restore();
      });

      frame++;
      if (frame < 120) {
        requestAnimationFrame(render);
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    }
    render();
  }

  // --- Flowchart Nodes (Questions) ---
  const questNodes = {
    start: {
      id: 'start',
      mapNodeId: 'map-node-clear-target',
      step: 1,
      maxStep: 5,
      level: 'LV.1 冒険の始まり',
      progressPercent: 20,
      badge: 'MISSION 1',
      question: 'やること（活動の目的・方向性）は明確ですか？',
      description: 'NEO FAMILY / RAYTUSで自分が今何に取り組むべきか、方針や目標のイメージを教えてください。',
      options: [
        {
          label: '明確 / なんとなく見えている',
          sub: 'やるべき方向性は掴めている・活動を進めたい',
          icon: 'fa-solid fa-compass',
          next: 'q2_latest',
          theme: 'border-blue-500/30 hover:border-blue-500 bg-blue-50/50 hover:bg-blue-50 text-blue-900',
          badgeColor: 'bg-blue-600 text-white'
        },
        {
          label: 'よく分かってない / もう一度見直したい',
          sub: '何から手をつけて良いか迷っている・一度立ち止まりたい',
          icon: 'fa-solid fa-headset',
          next: 'goal_counseling',
          theme: 'border-purple-500/30 hover:border-purple-500 bg-purple-50/50 hover:bg-purple-50 text-purple-900',
          badgeColor: 'bg-purple-600 text-white'
        }
      ]
    },

    q2_latest: {
      id: 'q2_latest',
      mapNodeId: 'map-node-latest-info',
      step: 2,
      maxStep: 5,
      level: 'LV.2 探求チャレンジャー',
      progressPercent: 40,
      badge: 'MISSION 2',
      question: 'NEO・RAYTUSの最新情報に触れていますか？',
      description: '合同定例会や全体の構想、公式共有情報などを定期的にキャッチアップできていますか？',
      options: [
        {
          label: 'しっかり触れている / キャッチアップ済',
          sub: '全体の動きや最新方針は大体把握できている',
          icon: 'fa-solid fa-check-double',
          next: 'q3_iyasaka',
          theme: 'border-blue-500/30 hover:border-blue-500 bg-blue-50/50 hover:bg-blue-50 text-blue-900',
          badgeColor: 'bg-blue-600 text-white'
        },
        {
          label: '全然触れてない / 最近追えていない',
          sub: '忙しくて追えていない・基本から短時間で整理したい',
          icon: 'fa-solid fa-book-open-reader',
          next: 'goal_neo_study',
          theme: 'border-indigo-500/30 hover:border-indigo-500 bg-indigo-50/50 hover:bg-indigo-50 text-indigo-900',
          badgeColor: 'bg-indigo-600 text-white'
        }
      ]
    },

    q3_iyasaka: {
      id: 'q3_iyasaka',
      mapNodeId: 'map-node-iyasaka',
      step: 3,
      maxStep: 5,
      level: 'LV.3 実践プレイヤー',
      progressPercent: 60,
      badge: 'MISSION 3',
      question: '公式マルシェ「Iyasaka宮」に出品していますか？',
      description: '会員相互の経済循環プラットフォーム「Iyasaka宮」にあなたの商品・サービスを出品したことがありますか？',
      options: [
        {
          label: 'すでに出品している！',
          sub: '出店者アカウントやマイページ・出品商品がある',
          icon: 'fa-solid fa-store',
          next: 'q4b_ginger',
          theme: 'border-emerald-500/30 hover:border-emerald-500 bg-emerald-50/50 hover:bg-emerald-50 text-emerald-900',
          badgeColor: 'bg-emerald-600 text-white'
        },
        {
          label: 'まだ出品していない',
          sub: 'これから出品したい・まだ準備に取り掛かれていない',
          icon: 'fa-solid fa-shop-slash',
          next: 'q4a_apply',
          theme: 'border-amber-500/30 hover:border-amber-500 bg-amber-50/50 hover:bg-amber-50 text-amber-900',
          badgeColor: 'bg-amber-600 text-white'
        }
      ]
    },

    q4a_apply: {
      id: 'q4a_apply',
      mapNodeId: 'map-node-apply',
      step: 4,
      maxStep: 5,
      level: 'LV.4 準備マスター',
      progressPercent: 75,
      badge: 'MISSION 4',
      question: '出店申請は終わっていますか？',
      description: 'Iyasaka宮への出店者としての公式申請手続きはすでに完了していますか？',
      options: [
        {
          label: '出店申請は終わっている',
          sub: '申請は済んでおり、プロフィールや出品準備へ進みたい',
          icon: 'fa-solid fa-file-circle-check',
          next: 'q5a_profile',
          theme: 'border-blue-500/30 hover:border-blue-500 bg-blue-50/50 hover:bg-blue-50 text-blue-900',
          badgeColor: 'bg-blue-600 text-white'
        },
        {
          label: 'まだ出店申請していない',
          sub: '出店申請の手続き自体がまだ完了していない',
          icon: 'fa-solid fa-pen-to-square',
          next: 'goal_apply_shop',
          theme: 'border-rose-500/30 hover:border-rose-500 bg-rose-50/50 hover:bg-rose-50 text-rose-900',
          badgeColor: 'bg-rose-600 text-white'
        }
      ]
    },

    q5a_profile: {
      id: 'q5a_profile',
      mapNodeId: 'map-node-profile',
      step: 5,
      maxStep: 5,
      level: 'LV.5 到達直前！',
      progressPercent: 90,
      badge: 'MISSION 5',
      question: 'プロフィール設定や出品方法は把握していますか？',
      description: '管理画面の操作や、魅力的なプロフィール・商品の登録方法に不安はありませんか？',
      options: [
        {
          label: '把握していて準備バッチリ！',
          sub: '出品方法は理解できているので、次のステップへ進みたい',
          icon: 'fa-solid fa-circle-check',
          next: 'q4b_ginger',
          theme: 'border-emerald-500/30 hover:border-emerald-500 bg-emerald-50/50 hover:bg-emerald-50 text-emerald-900',
          badgeColor: 'bg-emerald-600 text-white'
        },
        {
          label: 'まだよく分からない / 不安がある',
          sub: '一人だと進まない・誰かに教わりながら進めたい',
          icon: 'fa-solid fa-laptop-code',
          next: 'goal_iyasaka_work',
          theme: 'border-amber-500/30 hover:border-amber-500 bg-amber-50/50 hover:bg-amber-50 text-amber-900',
          badgeColor: 'bg-amber-600 text-white'
        }
      ]
    },

    q4b_ginger: {
      id: 'q4b_ginger',
      mapNodeId: 'map-node-ginger',
      step: 4,
      maxStep: 5,
      level: 'LV.4 拡大チャレンジャー',
      progressPercent: 75,
      badge: 'MISSION 4',
      question: '「勉強ジンジャー」に出品・投稿していますか？',
      description: '学びとアウトプットを加速するプラットフォーム「勉強ジンジャー」への参加状況はいかがですか？',
      options: [
        {
          label: 'している / 今はやらない（次へ進む）',
          sub: 'すでに投稿している、または動画や別の展開へ進めたい',
          icon: 'fa-solid fa-forward-step',
          next: 'q5b_eeda',
          theme: 'border-blue-500/30 hover:border-blue-500 bg-blue-50/50 hover:bg-blue-50 text-blue-900',
          badgeColor: 'bg-blue-600 text-white'
        },
        {
          label: 'やり方がわからない / 学びたい',
          sub: '興味はあるが活用方法や投稿の仕方が不明',
          icon: 'fa-solid fa-mortar-pestle',
          next: 'goal_ginger_support',
          theme: 'border-purple-500/30 hover:border-purple-500 bg-purple-50/50 hover:bg-purple-50 text-purple-900',
          badgeColor: 'bg-purple-600 text-white'
        }
      ]
    },

    q5b_eeda: {
      id: 'q5b_eeda',
      mapNodeId: 'map-node-eeda',
      step: 5,
      maxStep: 5,
      level: 'LV.5 フロンティア',
      progressPercent: 90,
      badge: 'MISSION 5',
      question: '「EEDA動画」は出していますか？',
      description: '次世代動画プラットフォームEEDAでの動画公開や制作の状況を教えてください。',
      options: [
        {
          label: 'そもそもEEDAについて知りたい！',
          sub: 'どんな動画やコンテンツがあるか、まずは探検してみたい',
          icon: 'fa-solid fa-compass',
          next: 'goal_eeda_pochi',
          theme: 'border-amber-500/30 hover:border-amber-500 bg-amber-50/50 hover:bg-amber-50 text-amber-900',
          badgeColor: 'bg-amber-600 text-white'
        },
        {
          label: '制作が進まない / 質問したいことがある',
          sub: '動画を作りたいが進まない・制作の悩みを相談したい',
          icon: 'fa-solid fa-clapperboard',
          next: 'goal_eeda_work',
          theme: 'border-rose-500/30 hover:border-rose-500 bg-rose-50/50 hover:bg-rose-50 text-rose-900',
          badgeColor: 'bg-rose-600 text-white'
        }
      ]
    }
  };

  // --- Flowchart Goals (Results) ---
  const questGoals = {
    goal_counseling: {
      id: 'goal_counseling',
      mapNodeId: 'map-goal-counseling',
      title: '理事長に相談',
      badge: '個別サポート / 方針整理',
      frequency: '随時受付（RAYTUS公式LINE）',
      icon: 'fa-solid fa-handshake',
      gradient: 'from-purple-600 via-indigo-600 to-slate-900',
      tagline: 'まずは活動の軸や目標を理事長と一緒に整理しましょう！',
      description: '「やることが明確でない」「一度方針を見直したい」と感じたときは、無理に手を動かすよりも原点に立ち返るのが一番の近道です。RAYTUS公式LINEから理事長への相談をメッセージしてください。親身に次のステップを導いてくれます。',
      highlights: [
        '個別の現状に合わせた無理のない進め方をアドバイス',
        '31事業の中からあなたに最適な分野をマッチング',
        '公式LINEでメッセージを送るだけで相談予約可能'
      ],
      actions: [
        {
          label: 'RAYTUS公式LINEで相談を申し込む',
          url: 'https://line.me/R/ti/p/@raytus',
          icon: 'fa-brands fa-line',
          btnClass: 'bg-emerald-600 hover:bg-emerald-700 text-white'
        },
        {
          label: '総合ポータルへ戻る',
          url: './',
          icon: 'fa-solid fa-compass',
          btnClass: 'bg-slate-100 hover:bg-slate-200 text-slate-800'
        }
      ],
      supportItemId: 'support-row-counseling'
    },

    goal_neo_study: {
      id: 'goal_neo_study',
      mapNodeId: 'map-goal-neo-study',
      title: 'NEO構想 ぎゅっと勉強会',
      badge: '月4回開催（朝・夜各2回）',
      frequency: '月4回（朝夜各2回 / 参加無料 / 全日共通Zoom）',
      icon: 'fa-solid fa-book-open-reader',
      gradient: 'from-blue-600 via-indigo-600 to-slate-900',
      tagline: '短時間で基本と最新ポイントを丸ごと学べる必須勉強会！',
      description: 'NEO FAMILYの全体像と最新動向をぎゅっと凝縮してお届けする勉強会です。最新情報に触れていないときは、まずここに参加するのが最善手！短時間で理解が追いつき、自分が今どこに関わるべきかが見えてきます。',
      subNotice: '💡 さらに深く知りたい方向けに「特別勉強会アーカイブ」（公式LINE）も用意されています！',
      highlights: [
        '短時間（30〜45分程度）で効率よくポイントを吸収',
        '朝の部・夜の部があり、忙しい方でも参加しやすい',
        '全日共通Zoom（ID: 811 1315 2898）からそのまま参加可能'
      ],
      actions: [
        {
          label: 'カレンダーで次回開催日程を見る',
          url: 'calendar.html',
          icon: 'fa-regular fa-calendar-days',
          btnClass: 'bg-slate-900 hover:bg-black text-white'
        },
        {
          label: '全日共通Zoom情報をコピー',
          action: 'copyZoom',
          icon: 'fa-solid fa-copy',
          btnClass: 'bg-blue-600 hover:bg-blue-700 text-white'
        },
        {
          label: '勉強会アーカイブ集を見る',
          url: 'archive.html',
          icon: 'fa-solid fa-graduation-cap',
          btnClass: 'bg-indigo-600 hover:bg-indigo-700 text-white'
        }
      ],
      supportItemId: 'support-row-neo-study'
    },

    goal_apply_shop: {
      id: 'goal_apply_shop',
      mapNodeId: 'map-goal-apply',
      title: 'Iyasaka宮 出店申請',
      badge: '随時受付（簡単3分）',
      frequency: 'オンライン随時受付',
      icon: 'fa-solid fa-torii-gate',
      gradient: 'from-amber-600 via-rose-600 to-slate-900',
      tagline: 'まずは出店申請を完了して、Iyasaka宮の仲間入りをしよう！',
      description: 'Iyasaka宮は、日本古来の精神とテクノロジーを融合した会員相互の経済循環プラットフォームです。出店申請を済ませることで、あなたの商品やスキルを全国のファミリーに向けて販売できるようになります。',
      highlights: [
        'オンライン申請フォームから簡単3分で申請完了',
        '物販だけでなくスキル・サービス・講座も出店可能',
        '出店申請後の設定は「整え作業会」で手厚くサポート'
      ],
      actions: [
        {
          label: 'Iyasaka宮 特設ページをチェック',
          url: 'iyasaka.html',
          icon: 'fa-solid fa-torii-gate',
          btnClass: 'bg-amber-600 hover:bg-amber-700 text-white'
        },
        {
          label: '出店申請フォームを開く',
          url: 'https://community-iyasakagu.jp/application',
          target: '_blank',
          icon: 'fa-solid fa-arrow-up-right-from-square',
          btnClass: 'bg-rose-600 hover:bg-rose-700 text-white'
        }
      ],
      supportItemId: 'support-row-iyasaka-work'
    },

    goal_iyasaka_work: {
      id: 'goal_iyasaka_work',
      mapNodeId: 'map-goal-iyasaka-work',
      title: 'Iyasaka宮 作業会 (整え作業会)',
      badge: '月2回 日中開催 ＆ 毎週火曜21:00〜Zoomライブ',
      frequency: '月2回 日中開催 ＋ 毎週火曜21:00〜',
      icon: 'fa-solid fa-laptop-code',
      gradient: 'from-amber-500 via-orange-600 to-slate-900',
      tagline: 'プロフィール設定や出品準備を、仲間と一緒に進める作業会！',
      description: '「管理画面の操作がよくわからない」「どんな商品写真や文章にすればいいか迷う」という方に最適！みんなで集まって一緒に手を動かすため、一人で悩むことなく出品準備がサクサク進みます。毎週火曜日21:00〜の「Iyasaka宮サポートZoomライブ」も利用できます！',
      highlights: [
        '画面を見ながら質問できる安心のサポート環境',
        '他の出店者の魅力的な見せ方も参考にできる',
        '毎週火曜21:00〜のサポートZoomライブと合わせて万全'
      ],
      actions: [
        {
          label: '次回作業会の日程をカレンダーで確認',
          url: 'calendar.html',
          icon: 'fa-regular fa-calendar-days',
          btnClass: 'bg-slate-900 hover:bg-black text-white'
        },
        {
          label: '火曜21:00 Zoomに参加する',
          url: 'https://us06web.zoom.us/j/81113152898?pwd=rnUDogc0paequYOxCnvXYaSs3WngG3.1',
          target: '_blank',
          icon: 'fa-solid fa-video',
          btnClass: 'bg-blue-600 hover:bg-blue-700 text-white'
        }
      ],
      supportItemId: 'support-row-iyasaka-work'
    },

    goal_ginger_support: {
      id: 'goal_ginger_support',
      mapNodeId: 'map-goal-ginger',
      title: '勉強ジンジャー活用サポート',
      badge: '月2回開催（昼・夜各1回）',
      frequency: '月2回（昼夜各1回開催）',
      icon: 'fa-solid fa-mortar-pestle',
      gradient: 'from-purple-600 via-indigo-700 to-slate-900',
      tagline: '勉強ジンジャーの活用方法や投稿方法をゼロから学べる！',
      description: '勉強ジンジャーへの投稿方法や、出品コンテンツをより多くの人に届けるコツを丁寧にレクチャーします。昼・夜の2部構成なので、お仕事や家事のスケジュールに合わせて参加いただけます。',
      highlights: [
        '投稿の具体的な手順を画面共有でステップバイステップ解説',
        '初心者でもわかりやすい質疑応答タイムあり',
        'RAYTUS公式LINEでも補足サポートを実施'
      ],
      actions: [
        {
          label: 'カレンダーで次回開催を確認',
          url: 'calendar.html',
          icon: 'fa-regular fa-calendar-days',
          btnClass: 'bg-slate-900 hover:bg-black text-white'
        },
        {
          label: 'RAYTUS公式LINEで質問する',
          url: 'https://line.me/R/ti/p/@raytus',
          target: '_blank',
          icon: 'fa-brands fa-line',
          btnClass: 'bg-emerald-600 hover:bg-emerald-700 text-white'
        }
      ],
      supportItemId: 'support-row-ginger'
    },

    goal_eeda_pochi: {
      id: 'goal_eeda_pochi',
      mapNodeId: 'map-goal-eeda-pochi',
      title: 'EEDA探検ポチポチ会',
      badge: '月4〜8回 活発に開催中！',
      frequency: '月4〜8回開催',
      icon: 'fa-solid fa-compass',
      gradient: 'from-amber-500 via-yellow-600 to-slate-900',
      tagline: 'EEDA動画やコンテンツをみんなで探索し、気づきや発見を共有！',
      description: '「EEDAってどんな仕組み？」「どんな動画が出てるの？」という疑問を楽しみながら解決できる大人気イベント！参加者同士でポチポチ操作しながら、新しい発見やお気に入りのコンテンツをシェアし合います。',
      highlights: [
        '肩肘張らずに楽しく参加できるカジュアルな雰囲気',
        '月4〜8回と開催頻度が高く、気軽に参加可能',
        '動画制作のヒントやアイデアがどんどん湧いてくる！'
      ],
      actions: [
        {
          label: 'カレンダーでポチポチ会を探す',
          url: 'calendar.html',
          icon: 'fa-regular fa-calendar-days',
          btnClass: 'bg-amber-600 hover:bg-amber-700 text-white'
        },
        {
          label: '全日共通Zoom情報をコピー',
          action: 'copyZoom',
          icon: 'fa-solid fa-copy',
          btnClass: 'bg-blue-600 hover:bg-blue-700 text-white'
        }
      ],
      supportItemId: 'support-row-eeda-pochi'
    },

    goal_eeda_work: {
      id: 'goal_eeda_work',
      mapNodeId: 'map-goal-eeda-work',
      title: 'EEDA作業会',
      badge: 'リクエスト開催（公式LINE受付中）',
      frequency: '随時リクエスト開催',
      icon: 'fa-solid fa-clapperboard',
      gradient: 'from-rose-600 via-pink-600 to-slate-900',
      tagline: '動画制作を進めたり、疑問や悩みをその場で質問・解決できる作業会！',
      description: '動画の企画・撮影・編集・アップロードなど、制作の手が止まってしまった時に仲間やサポートメンバーと一緒に作業を進められます。開催希望はRAYTUS公式LINEまでお気軽にメッセージをお寄せください！',
      subNotice: '※開催のご要望はRAYTUS group.公式LINEまでお気軽にどうぞ！',
      highlights: [
        '動画制作でつまずいているポイントを直接質問・解決',
        '集中して制作作業に打ち込める「もくもく作業」環境',
        '公式LINEから簡単に開催リクエストが可能'
      ],
      actions: [
        {
          label: 'RAYTUS公式LINEで開催をリクエスト',
          url: 'https://line.me/R/ti/p/@raytus',
          target: '_blank',
          icon: 'fa-brands fa-line',
          btnClass: 'bg-emerald-600 hover:bg-emerald-700 text-white'
        },
        {
          label: '全事業紹介動画を見る',
          url: 'raytus.html',
          icon: 'fa-solid fa-play',
          btnClass: 'bg-slate-900 hover:bg-black text-white'
        }
      ],
      supportItemId: 'support-row-eeda-work'
    }
  };

  // --- Game State ---
  let historyStack = ['start'];
  let currentKey = 'start';

  // --- Sound Toggle ---
  window.toggleQuestSound = function () {
    isSoundEnabled = !isSoundEnabled;
    const icon = document.getElementById('quest-sound-icon');
    const label = document.getElementById('quest-sound-label');
    if (icon) {
      icon.className = isSoundEnabled ? 'fa-solid fa-volume-high text-amber-500' : 'fa-solid fa-volume-xmark text-slate-400';
    }
    if (label) {
      label.textContent = isSoundEnabled ? 'BGM/効果音: ON' : 'BGM/効果音: OFF';
    }
    if (isSoundEnabled) {
      playSound('select');
    }
  };

  // --- Reset Game ---
  window.resetQuest = function () {
    playSound('back');
    historyStack = ['start'];
    currentKey = 'start';
    renderQuest();
    highlightMapNode('map-node-clear-target');
    clearSupportTableHighlight();
  };

  // --- Back to Previous Question ---
  window.prevQuestStep = function () {
    if (historyStack.length > 1) {
      playSound('back');
      historyStack.pop();
      currentKey = historyStack[historyStack.length - 1];
      renderQuest();
      const node = questNodes[currentKey];
      if (node && node.mapNodeId) {
        highlightMapNode(node.mapNodeId);
      }
      clearSupportTableHighlight();
    }
  };

  // --- Choose Option ---
  window.chooseQuestOption = function (nextKey) {
    playSound('select');
    historyStack.push(nextKey);
    currentKey = nextKey;
    renderQuest();
  };

  // --- Highlight Map Node with Player Avatar ---
  function highlightMapNode(mapNodeId) {
    document.querySelectorAll('.quest-map-node').forEach(el => {
      el.classList.remove('ring-4', 'ring-amber-400', 'bg-amber-100', 'scale-105', 'font-black');
      const badge = el.querySelector('.player-avatar-badge');
      if (badge) badge.remove();
    });
    const target = document.getElementById(mapNodeId);
    if (target) {
      target.classList.add('ring-4', 'ring-amber-400', 'bg-amber-100', 'scale-105', 'font-black');
      const avatar = document.createElement('span');
      avatar.className = 'player-avatar-badge absolute -top-3.5 left-1/2 -translate-x-1/2 bg-amber-400 text-slate-950 px-2.5 py-0.5 rounded-full text-[10px] font-black shadow-md flex items-center gap-1 animate-bounce z-20 pointer-events-none whitespace-nowrap';
      avatar.innerHTML = '<i class="fa-solid fa-person-running text-rose-600"></i> あなたの現在地';
      target.style.position = 'relative';
      target.appendChild(avatar);
      if (window.innerWidth < 768) {
        target.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    }
  }

  // --- Highlight Support Table Row ---
  function highlightSupportTableRow(rowId) {
    clearSupportTableHighlight();
    const row = document.getElementById(rowId);
    if (row) {
      row.classList.add('bg-amber-50', 'ring-2', 'ring-amber-400', 'animate-pulse');
      setTimeout(() => {
        row.classList.remove('animate-pulse');
      }, 3000);
      row.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  function clearSupportTableHighlight() {
    document.querySelectorAll('.support-table-row').forEach(r => {
      r.classList.remove('bg-amber-50', 'ring-2', 'ring-amber-400', 'animate-pulse');
    });
  }

  // --- Render Quest UI ---
  function renderQuest() {
    const container = document.getElementById('quest-stage-container');
    if (!container) return;

    // Check if it's a Goal
    if (questGoals[currentKey]) {
      const goal = questGoals[currentKey];
      playSound('clear');
      setTimeout(launchConfetti, 100);

      highlightMapNode(goal.mapNodeId);
      if (goal.supportItemId) {
        highlightSupportTableRow(goal.supportItemId);
      }

      const actionsHtml = goal.actions.map(act => {
        if (act.action === 'copyZoom') {
          return `
            <button onclick="copyZoomInfo()" class="px-5 py-3 rounded-2xl ${act.btnClass} font-bold text-xs sm:text-sm flex items-center justify-center gap-2 transition shadow-md hover:scale-102">
              <i class="${act.icon}"></i>
              <span>${act.label}</span>
            </button>
          `;
        }
        return `
          <a href="${act.url}" ${act.target ? `target="${act.target}"` : ''} class="px-5 py-3 rounded-2xl ${act.btnClass} font-bold text-xs sm:text-sm flex items-center justify-center gap-2 transition shadow-md hover:scale-102">
            <i class="${act.icon}"></i>
            <span>${act.label}</span>
          </a>
        `;
      }).join('');

      const highlightsHtml = goal.highlights.map(h => `
        <li class="flex items-start gap-2 text-xs sm:text-sm text-slate-700">
          <i class="fa-solid fa-circle-check text-emerald-500 mt-1 shrink-0"></i>
          <span>${h}</span>
        </li>
      `).join('');

      container.innerHTML = `
        <div class="animate-in fade-in zoom-in-95 duration-300">
          <!-- Clear Banner -->
          <div class="relative overflow-hidden rounded-3xl bg-gradient-to-r ${goal.gradient} text-white p-6 sm:p-8 shadow-xl">
            <div class="absolute -right-10 -bottom-10 opacity-15 text-9xl">
              <i class="${goal.icon}"></i>
            </div>
            
            <div class="relative z-10 space-y-4">
              <div class="flex items-center justify-between flex-wrap gap-2">
                <span class="px-3 py-1 rounded-full bg-amber-400 text-slate-950 font-black text-xs flex items-center gap-1.5 shadow-sm">
                  <i class="fa-solid fa-trophy"></i>
                  <span>QUEST COMPLETE! 最適な参加先を導き出しました</span>
                </span>
                <span class="text-xs text-slate-200 font-medium">進行度: 100% COMPLETE</span>
              </div>

              <div>
                <span class="inline-block px-2.5 py-0.5 rounded text-[11px] font-bold bg-white/20 text-white backdrop-blur-xs mb-2">
                  ${goal.badge}
                </span>
                <h3 class="text-2xl sm:text-3xl font-black text-white tracking-tight flex items-center gap-3">
                  <i class="${goal.icon} text-amber-300"></i>
                  <span>${goal.title}</span>
                </h3>
                <p class="text-sm sm:text-base text-rose-100 font-bold mt-2">
                  ${goal.tagline}
                </p>
              </div>

              <p class="text-xs sm:text-sm text-white/90 leading-relaxed max-w-2xl">
                ${goal.description}
              </p>

              ${goal.subNotice ? `
                <div class="p-3 rounded-xl bg-white/10 border border-white/20 text-xs text-amber-200">
                  ${goal.subNotice}
                </div>
              ` : ''}

              <!-- Highlights -->
              <div class="bg-white/95 text-slate-900 rounded-2xl p-4 sm:p-5 shadow-sm space-y-2.5">
                <h4 class="font-extrabold text-xs text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
                  <i class="fa-solid fa-sparkles text-amber-500"></i>
                  <span>このサポートの特徴・おすすめ理由</span>
                </h4>
                <ul class="space-y-2">
                  ${highlightsHtml}
                </ul>
              </div>

              <!-- Action Buttons -->
              <div class="pt-2 flex flex-col sm:flex-row flex-wrap items-center gap-3">
                ${actionsHtml}
                <button onclick="resetQuest()" class="px-4 py-3 rounded-2xl bg-white/20 hover:bg-white/30 text-white font-bold text-xs sm:text-sm transition flex items-center gap-2">
                  <i class="fa-solid fa-rotate-left"></i>
                  <span>最初からやり直す</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      `;
      return;
    }

    // Render Question Node
    const node = questNodes[currentKey];
    if (!node) return;

    if (node.mapNodeId) {
      highlightMapNode(node.mapNodeId);
    }

    const optionsHtml = node.options.map(opt => `
      <button onclick="chooseQuestOption('${opt.next}')" class="group w-full p-4 sm:p-5 rounded-2xl border-2 ${opt.theme} transition-all duration-200 hover:scale-101 hover:shadow-md text-left flex items-start gap-4 cursor-pointer relative overflow-hidden">
        <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-2xl ${opt.badgeColor} flex items-center justify-center shrink-0 shadow-sm group-hover:rotate-6 transition-transform">
          <i class="${opt.icon} text-lg sm:text-xl"></i>
        </div>
        <div class="flex-1">
          <div class="flex items-center justify-between">
            <h4 class="font-black text-sm sm:text-base tracking-tight">${opt.label}</h4>
            <i class="fa-solid fa-chevron-right text-xs text-slate-400 group-hover:text-slate-700 group-hover:translate-x-1 transition-transform"></i>
          </div>
          <p class="text-xs text-slate-500 mt-1 leading-relaxed">${opt.sub}</p>
        </div>
      </button>
    `).join('');

    container.innerHTML = `
      <div class="animate-in fade-in slide-in-from-right-4 duration-300 space-y-6">
        
        <!-- Header & Progress -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
          <div class="flex items-center gap-3">
            <span class="px-3 py-1 rounded-xl bg-slate-900 text-white font-black text-xs shadow-xs">
              ${node.badge}
            </span>
            <span class="text-xs font-bold text-amber-600 flex items-center gap-1">
              <i class="fa-solid fa-shield-halved"></i>
              <span>${node.level}</span>
            </span>
          </div>

          <div class="flex items-center gap-3">
            <div class="w-32 sm:w-44 bg-slate-100 rounded-full h-2.5 overflow-hidden">
              <div class="bg-gradient-to-r from-amber-500 to-rose-500 h-full rounded-full transition-all duration-500" style="width: ${node.progressPercent}%"></div>
            </div>
            <span class="text-xs font-bold text-slate-500">${node.step} / ${node.maxStep}</span>
          </div>
        </div>

        <!-- Question Body -->
        <div class="space-y-2">
          <h3 class="text-lg sm:text-xl md:text-2xl font-black text-slate-900 leading-snug">
            ${node.question}
          </h3>
          <p class="text-xs sm:text-sm text-slate-500 leading-relaxed">
            ${node.description}
          </p>
        </div>

        <!-- Options Cards -->
        <div class="grid grid-cols-1 gap-3.5 pt-1">
          ${optionsHtml}
        </div>

        <!-- Navigation Footer -->
        <div class="flex items-center justify-between pt-2">
          ${historyStack.length > 1 ? `
            <button onclick="prevQuestStep()" class="text-xs font-bold text-slate-500 hover:text-slate-800 flex items-center gap-1.5 px-3 py-1.5 rounded-lg hover:bg-slate-100 transition">
              <i class="fa-solid fa-arrow-left"></i>
              <span>前の質問に戻る</span>
            </button>
          ` : `<div></div>`}

          <button onclick="resetQuest()" class="text-xs font-bold text-slate-400 hover:text-slate-600 flex items-center gap-1.5 px-3 py-1.5 rounded-lg hover:bg-slate-100 transition">
            <i class="fa-solid fa-rotate-left"></i>
            <span>最初からやり直す</span>
          </button>
        </div>

      </div>
    `;
  }

  // --- Map Node Click (Direct Inspect) ---
  window.inspectMapNode = function (nodeKey) {
    if (questGoals[nodeKey]) {
      currentKey = nodeKey;
      historyStack.push(nodeKey);
      renderQuest();
      return;
    }
    if (questNodes[nodeKey]) {
      currentKey = nodeKey;
      historyStack.push(nodeKey);
      renderQuest();
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

  // --- Initialize when DOM is ready ---
  document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('quest-stage-container')) {
      renderQuest();
      highlightMapNode('map-node-clear-target');
    }
  });

})();

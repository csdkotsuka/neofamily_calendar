/**
 * NEO FAMILY & RAYTUS 会員IDトラッカー & クラウド進捗同期システム
 * 
 * 1. 会員ID（例: 1234abc）を用いたパスワード不要の識別・ログアウト制御
 * 2. スマホ・PC間のFirestoreクラウド自動同期（同じ会員IDでどこから開いても復元）
 * 3. 初心者ファーストステップ3箇条（Zoom、定例会、サポート窓口）の進捗管理
 * 4. 目的別スタートコンパス（4つの目的診断）
 * 5. 動画・画像・主要コンテンツ閲覧ログの自動記録
 */

const MEMBER_STORAGE_KEY = 'neofamily_member_id';
let currentMemberId = null;
let currentProgressData = {
  memberId: '',
  mentorId: '',
  onboardingSteps: { zoom: false, teireikai: false, support: false },
  viewedContents: {},
  lastActiveAt: null,
  deviceInfo: ''
};

// 初期化
async function initMemberTracker() {
  // 1. URLパラメータから ?uid=... または ?memberId=... をチェック
  const urlParams = new URLSearchParams(window.location.search);
  const paramId = urlParams.get('uid') || urlParams.get('memberId');
  
  if (paramId) {
    await setMemberSession(paramId.trim().toLowerCase());
  } else {
    // 2. localStorage から復元
    const savedId = localStorage.getItem(MEMBER_STORAGE_KEY);
    if (savedId) {
      currentMemberId = savedId;
      updateHeaderMemberUI(savedId);
      await fetchMemberProgressFromCloud(savedId);
    }
  }

  updateHeaderMemberUI(currentMemberId);
  updateOnboardingProgressUI();
}

// 会員IDの設定
async function setMemberSession(id) {
  if (!id) return;
  const cleanId = id.trim().toLowerCase();
  currentMemberId = cleanId;
  localStorage.setItem(MEMBER_STORAGE_KEY, cleanId);
  updateHeaderMemberUI(cleanId);
  await fetchMemberProgressFromCloud(cleanId);
  showToast(`👤 会員ID「${cleanId}」でログインしました`);
}

// ログアウト（記録停止）
function clearMemberSession() {
  const prevId = currentMemberId;
  currentMemberId = null;
  localStorage.removeItem(MEMBER_STORAGE_KEY);
  updateHeaderMemberUI(null);

  // チェックボックスのリセット（ローカル状態をクリア）
  if (document.getElementById('check-step-1')) document.getElementById('check-step-1').checked = false;
  if (document.getElementById('check-step-2')) document.getElementById('check-step-2').checked = false;
  if (document.getElementById('check-step-3')) document.getElementById('check-step-3').checked = false;
  updateOnboardingProgressUI();

  showToast(`ログアウトしました（閲覧ログの記録を停止しました）`);
  closeModal('member-id-modal');
}

// ヘッダーUIの更新
function updateHeaderMemberUI(id) {
  const badge = document.getElementById('member-auth-badge');
  const label = document.getElementById('member-auth-label');
  const loggedInView = document.getElementById('member-logged-in-view');
  const loginForm = document.getElementById('member-id-form');
  const modalCurrentId = document.getElementById('modal-current-member-id');

  if (id) {
    if (label) label.innerHTML = `<span class="text-indigo-600 font-mono font-bold">${id}</span> <span class="text-[10px] text-emerald-600 font-bold bg-emerald-50 px-1.5 py-0.5 rounded">記録中</span>`;
    if (loggedInView) loggedInView.classList.remove('hidden');
    if (loginForm) loginForm.classList.add('hidden');
    if (modalCurrentId) modalCurrentId.textContent = id;
  } else {
    if (label) label.textContent = '会員IDを入力';
    if (loggedInView) loggedInView.classList.add('hidden');
    if (loginForm) loginForm.classList.remove('hidden');
  }
}

// モーダル操作
function openMemberIdModal() {
  updateHeaderMemberUI(currentMemberId);
  openModal('member-id-modal');
}

// ログインフォーム送信
async function handleMemberLogin(e) {
  e.preventDefault();
  const input = document.getElementById('input-member-id');
  if (input && input.value.trim()) {
    await setMemberSession(input.value);
    closeModal('member-id-modal');
  }
}

function logoutMember() {
  clearMemberSession();
}

// クラウド（Firestore）から進捗を取得して画面に反映
async function fetchMemberProgressFromCloud(id) {
  if (!id) return;
  
  try {
    if (typeof firebase !== 'undefined' && firebase.apps.length) {
      const db = firebase.firestore();
      const docRef = db.collection('member_progress').doc(id);
      const doc = await docRef.get();

      if (doc.exists) {
        currentProgressData = doc.data();
        applyProgressToUI(currentProgressData);
        console.log('[Tracker] Cloud progress loaded for:', id, currentProgressData);
      } else {
        // 新規作成
        currentProgressData = {
          memberId: id,
          mentorId: 'unassigned',
          onboardingSteps: { zoom: false, teireikai: false, support: false },
          viewedContents: {},
          firstSeenAt: new Date().toISOString(),
          lastActiveAt: new Date().toISOString(),
          deviceInfo: navigator.userAgent
        };
        await docRef.set(currentProgressData);
        applyProgressToUI(currentProgressData);
      }
    }
  } catch (err) {
    console.warn('[Tracker] Firestore read fallback to local:', err);
  }
}

// UIに進捗を反映
function applyProgressToUI(data) {
  if (!data || !data.onboardingSteps) return;

  const steps = data.onboardingSteps;
  if (document.getElementById('check-step-1')) document.getElementById('check-step-1').checked = !!steps.zoom;
  if (document.getElementById('check-step-2')) document.getElementById('check-step-2').checked = !!steps.teireikai;
  if (document.getElementById('check-step-3')) document.getElementById('check-step-3').checked = !!steps.support;

  updateOnboardingProgressUI();
}

// クラウドへ進捗・アクションを保存
async function saveMemberProgressToCloud(updates) {
  if (!currentMemberId) return; // ログインしていなければ保存しない（仕様通り）

  const now = new Date().toISOString();
  currentProgressData = {
    ...currentProgressData,
    ...updates,
    memberId: currentMemberId,
    lastActiveAt: now,
    deviceInfo: navigator.userAgent
  };

  try {
    if (typeof firebase !== 'undefined' && firebase.apps.length) {
      const db = firebase.firestore();
      await db.collection('member_progress').doc(currentMemberId).set(currentProgressData, { merge: true });
      console.log('[Tracker] Cloud progress saved for:', currentMemberId);
    }
  } catch (err) {
    console.warn('[Tracker] Firestore save error:', err);
  }
}

// チェックボックスの変更イベントハンドラー
function updateOnboardingProgress() {
  const c1 = document.getElementById('check-step-1')?.checked || false;
  const c2 = document.getElementById('check-step-2')?.checked || false;
  const c3 = document.getElementById('check-step-3')?.checked || false;

  updateOnboardingProgressUI();

  if (!currentProgressData.onboardingSteps) {
    currentProgressData.onboardingSteps = {};
  }
  currentProgressData.onboardingSteps.zoom = c1;
  currentProgressData.onboardingSteps.teireikai = c2;
  currentProgressData.onboardingSteps.support = c3;

  saveMemberProgressToCloud({
    onboardingSteps: currentProgressData.onboardingSteps
  });

  if (!currentMemberId) {
    showToast('💡 会員IDを入力すると、この進捗がスマホやPCに保存されます');
  }
}

// プログレスバーUIの更新
function updateOnboardingProgressUI() {
  const c1 = document.getElementById('check-step-1')?.checked || false;
  const c2 = document.getElementById('check-step-2')?.checked || false;
  const c3 = document.getElementById('check-step-3')?.checked || false;
  const total = 3;
  const count = [c1, c2, c3].filter(Boolean).length;
  const percent = Math.round((count / total) * 100);

  const bar = document.getElementById('onboarding-progress-bar');
  const txt = document.getElementById('onboarding-progress-text');

  if (bar) bar.style.width = percent + '%';
  if (txt) {
    if (count === total) {
      txt.innerHTML = '<span class="text-emerald-400 font-bold">🎉 全ステップ完了！</span>';
    } else {
      txt.textContent = `${count} / ${total} 完了 (${percent}%)`;
    }
  }
}

// コンテンツ閲覧ログの記録（動画、フロー、事業紹介など）
function trackContentView(contentId, contentTitle) {
  if (!currentMemberId) return;

  const now = new Date().toISOString();
  if (!currentProgressData.viewedContents) currentProgressData.viewedContents = {};
  currentProgressData.viewedContents[contentId] = {
    title: contentTitle,
    viewedAt: now
  };

  saveMemberProgressToCloud({
    viewedContents: currentProgressData.viewedContents
  });
}

// 目的別スタートコンパスの選択ハンドラー
function selectPurpose(type) {
  const panel = document.getElementById('purpose-result-panel');
  if (!panel) return;

  const cards = document.querySelectorAll('.purpose-card');
  cards.forEach(c => c.classList.remove('ring-4', 'ring-amber-400', 'bg-amber-50/50', 'ring-rose-400', 'bg-rose-50/50', 'ring-blue-400', 'bg-blue-50/50', 'ring-emerald-400', 'bg-emerald-50/50'));

  const selectedCard = document.getElementById(`purpose-card-${type}`);
  if (selectedCard) {
    selectedCard.classList.add('ring-4');
    if (type === 'community') selectedCard.classList.add('ring-amber-400', 'bg-amber-50/50');
    if (type === 'shop') selectedCard.classList.add('ring-rose-400', 'bg-rose-50/50');
    if (type === 'business') selectedCard.classList.add('ring-blue-400', 'bg-blue-50/50');
    if (type === 'study') selectedCard.classList.add('ring-emerald-400', 'bg-emerald-50/50');
  }

  const data = {
    community: {
      title: '🤝 「仲間と交流したい」あなたへのスタートガイド',
      bg: 'bg-amber-50/80 border-amber-300',
      badge: 'bg-amber-200 text-amber-900',
      desc: 'まずは月1回の合同定例会と、毎日の事業説明会Zoomに参加して顔を合わせるのが一番の近道です！',
      steps: [
        { label: 'Step 1: 次回合同定例会（11/2福岡）に参加表明する', desc: '調整さんで【所属会名のみ】入力して送信。リアル会場で同期や先輩と直接話せます。', action: '<a href="https://chouseisan.com/s?h=2733ccd431d846f8bccd9c3061c0bca3" target="_blank" class="px-3 py-1.5 rounded-lg bg-emerald-600 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>調整さんを開く</span><i class="fa-solid fa-pen-to-square"></i></a>' },
        { label: 'Step 2: 全日共通Zoom（ID: 811 1315 2898 / PW: 2026）を保存', desc: '合同事業説明会は毎日開催。まずは耳だけ・画面オフでも大歓迎です。', action: '<button onclick="copyZoomInfo()" class="px-3 py-1.5 rounded-lg bg-indigo-600 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>Zoom情報をコピー</span><i class="fa-solid fa-copy"></i></button>' },
        { label: 'Step 3: イベントカレンダーで今月の交流会をチェック', desc: '懇親会や勉強会など、気軽に参加できる日程をカレンダーから探せます。', action: '<button onclick="switchTab(\'calendar\')" class="px-3 py-1.5 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>カレンダーを見る</span><i class="fa-regular fa-calendar-days"></i></button>' }
      ]
    },
    shop: {
      title: '🛍️ 「商品を出品・販売したい」あなたへのスタートガイド',
      bg: 'bg-rose-50/80 border-rose-300',
      badge: 'bg-rose-200 text-rose-900',
      desc: 'Iyasaka宮マルシェや各地のリアルマルシェで、あなたのオリジナル商品や鑑定・セッションを出品できます。',
      steps: [
        { label: 'Step 1: Iyasaka宮（デモ体験 & 本家マルシェ）を見る', desc: 'どんな商品や価格帯が並んでいるか、ポータル内のIyasaka宮タブでイメージを掴みましょう。', action: '<button onclick="switchTab(\'iyasaka\')" class="px-3 py-1.5 rounded-lg bg-amber-600 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>Iyasaka宮を見る</span><i class="fa-solid fa-torii-gate"></i></button>' },
        { label: 'Step 2: 合同事業説明会でマルシェ出店要項を聞く', desc: '共通Zoomで開催される事業説明会で、出店手続きや出品条件について案内があります。', action: '<button onclick="scrollToSection(\'common-zoom-section\')" class="px-3 py-1.5 rounded-lg bg-blue-600 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>Zoom日程を見る</span><i class="fa-solid fa-video"></i></button>' },
        { label: 'Step 3: サポート一覧の「マルシェ担当」に相談する', desc: '分からないことがあれば、サポート一覧画像に記載のマルシェ窓口に気軽にLINEで相談可能です。', action: '<button onclick="scrollToSection(\'flowchart-section\')" class="px-3 py-1.5 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>サポート窓口を見る</span><i class="fa-solid fa-arrow-down"></i></button>' }
      ]
    },
    business: {
      title: '🏫 「RAYTUS事業・共育に参入したい」あなたへのスタートガイド',
      bg: 'bg-blue-50/80 border-blue-300',
      badge: 'bg-blue-200 text-blue-900',
      desc: 'RAYTUS group.には子育て・食・美容・教育など多種多様な事業があります。あなたの想いに合ったチームに参加しましょう。',
      steps: [
        { label: 'Step 1: 「全事業紹介 & 公式動画アーカイブ」で関心のある事業を探す', desc: '31事業を5大グループ別に整理。各事業の代表者や理念の動画をその場で視聴できます。', action: '<button onclick="switchTab(\'raytus\'); scrollToSection(\'raytus-services-section\');" class="px-3 py-1.5 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>全事業一覧を見る</span><i class="fa-solid fa-shapes"></i></button>' },
        { label: 'Step 2: 寺子屋プロジェクト・バスタ高校プロジェクトをチェック', desc: 'RAYTUSが力を入れる次世代の教育支援プロジェクトの最新状況を確認できます。', action: '<button onclick="switchTab(\'raytus\'); scrollToSection(\'raytus-projects-section\');" class="px-3 py-1.5 rounded-lg bg-amber-500 text-slate-950 font-bold text-xs flex items-center gap-1 shadow-xs"><span>プロジェクトを見る</span><i class="fa-solid fa-arrow-right"></i></button>' },
        { label: 'Step 3: 合同定例会（11/2福岡）で各事業リーダーと直接名刺交換', desc: 'リアルの定例会には全事業の代表・リーダーが集結します。直接相談して参画を決めましょう。', action: '<a href="https://chouseisan.com/s?h=2733ccd431d846f8bccd9c3061c0bca3" target="_blank" class="px-3 py-1.5 rounded-lg bg-emerald-600 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>定例会に参加表明</span><i class="fa-solid fa-pen-to-square"></i></a>' }
      ]
    },
    study: {
      title: '🔥 「起業・稼ぐ力・マインドを学びたい」あなたへのスタートガイド',
      bg: 'bg-emerald-50/80 border-emerald-300',
      badge: 'bg-emerald-200 text-emerald-900',
      desc: '半年で億を稼ぐ思考法、ぶった斬り会長の哲学、特別勉強会のアーカイブで最短距離でビジネスマインドを鍛えましょう。',
      steps: [
        { label: 'Step 1: ぶった斬り会長 公式YouTube（@buttagirichannel）を見る', desc: '夫婦関係からお金の使い方・起業戦略まで、人気動画をポータル内で直接再生できます。', action: '<button onclick="switchTab(\'sns\'); setSnsFilter(\'youtube\');" class="px-3 py-1.5 rounded-lg bg-red-600 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>YouTube動画を見る</span><i class="fa-brands fa-youtube"></i></button>' },
        { label: 'Step 2: ぶった斬り会長 公式TikTok（@buttagiri888）をフォロー', desc: '日常のスキマ時間に見られるショート動画で、毎日マインドセットをアップデート。', action: '<button onclick="switchTab(\'sns\'); setSnsFilter(\'tiktok\');" class="px-3 py-1.5 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>TikTokを見る</span><i class="fa-brands fa-tiktok"></i></button>' },
        { label: 'Step 3: 特別勉強会（アーカイブ集）でビジネス実践を学ぶ', desc: '確定申告、クリエイティブ、協会のノウハウなど過去の勉強会アーカイブを視聴できます。', action: '<button onclick="switchTab(\'archive\')" class="px-3 py-1.5 rounded-lg bg-indigo-600 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>勉強会アーカイブ</span><i class="fa-solid fa-graduation-cap"></i></button>' }
      ]
    }
  };

  const item = data[type];
  if (!item) return;

  panel.className = `p-6 sm:p-8 rounded-3xl border-2 ${item.bg} space-y-4 shadow-sm animate-fadeIn`;
  panel.classList.remove('hidden');

  let stepsHtml = item.steps.map((s, idx) => `
    <div class="bg-white/90 p-4 rounded-2xl border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div class="space-y-1">
        <h5 class="text-sm font-black text-slate-900 flex items-center gap-2">
          <span class="w-6 h-6 rounded-full bg-slate-900 text-white text-xs flex items-center justify-center shrink-0 font-bold">${idx + 1}</span>
          <span>${s.label}</span>
        </h5>
        <p class="text-xs text-slate-600 ml-8">${s.desc}</p>
      </div>
      <div class="ml-8 sm:ml-0 shrink-0">
        ${s.action}
      </div>
    </div>
  `).join('');

  panel.innerHTML = `
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="px-2.5 py-1 rounded-full text-xs font-bold ${item.badge}">あなたへのおすすめ導線</span>
        <h4 class="text-base sm:text-lg font-black text-slate-900">${item.title}</h4>
      </div>
      <button onclick="document.getElementById('purpose-result-panel').classList.add('hidden')" class="text-slate-400 hover:text-slate-700 text-xs px-2 py-1 rounded" title="閉じる">
        <i class="fa-solid fa-xmark text-sm"></i>
      </button>
    </div>
    <p class="text-xs text-slate-700 leading-relaxed">${item.desc}</p>
    <div class="space-y-2.5 pt-2">
      ${stepsHtml}
    </div>
  `;

  panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// openLightbox にも自動トラッキングフック
window.addEventListener('load', () => {
  const origLightbox = window.openLightbox;
  if (typeof origLightbox === 'function') {
    window.openLightbox = function(src, title) {
      origLightbox(src, title);
      trackContentView(src, title);
    };
  }
});

// DOMContentLoaded で初期化
document.addEventListener('DOMContentLoaded', () => {
  initMemberTracker();
});

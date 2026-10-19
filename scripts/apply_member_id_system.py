import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. ヘッダー右側アクションの整理
header_actions_pattern = re.compile(
    r'<!-- ヘッダー右側アクション -->\s*<div class="flex items-center gap-2 sm:gap-3">.*?<!-- 管理者ログイン -->',
    re.DOTALL
)

new_header_actions = '''<!-- ヘッダー右側アクション -->
        <div class="flex items-center gap-2 sm:gap-3">
          
          <!-- 会員ID ステータス & ログイン -->
          <div id="member-auth-badge" class="flex items-center gap-1.5 bg-slate-100 hover:bg-slate-200/80 px-2.5 sm:px-3 py-1.5 rounded-xl border border-slate-200 text-xs font-bold transition cursor-pointer" onclick="openMemberIdModal()" title="会員IDでログインして閲覧ログを同期">
            <i class="fa-solid fa-id-card text-indigo-600"></i>
            <span id="member-auth-label" class="text-slate-700">会員IDを入力</span>
          </div>

          <!-- 管理者ログイン -->'''

html = header_actions_pattern.sub(new_header_actions, html, count=1)
print("1. Header cleaned up: removed beginner/veteran toggle and calendar button, added member ID badge.")

# 2. 会員ID入力モーダルを HTML末尾に追加
member_modal_html = '''  <!-- ========================================== -->
  <!-- 会員ID ログイン / ログアウト モーダル -->
  <!-- ========================================== -->
  <div id="member-id-modal" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm hidden items-center justify-center p-4">
    <div class="bg-white rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl border border-slate-200 relative animate-scaleUp">
      <button onclick="closeModal('member-id-modal')" class="absolute top-4 right-4 text-slate-400 hover:text-slate-700 w-8 h-8 rounded-full flex items-center justify-center bg-slate-100 transition" title="閉じる">
        <i class="fa-solid fa-xmark"></i>
      </button>

      <div class="text-center space-y-2 mb-6">
        <div class="w-14 h-14 mx-auto rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-2xl shadow-sm">
          <i class="fa-solid fa-id-card"></i>
        </div>
        <h3 class="text-xl font-black text-slate-900">会員IDで進捗を記録・同期</h3>
        <p class="text-xs text-slate-500 leading-relaxed">
          会員IDを入力すると、閲覧したコンテンツやチェックリストの達成状況がクラウドに保存され、サポート担当者に共有されます。スマホとPCの間でも自動で同期されます。
        </p>
      </div>

      <!-- ログイン中表示 -->
      <div id="member-logged-in-view" class="hidden space-y-4">
        <div class="p-4 rounded-2xl bg-indigo-50/70 border border-indigo-200 text-center space-y-1">
          <span class="text-[10px] font-bold text-indigo-600 uppercase tracking-wider">現在ログイン中の会員ID</span>
          <div class="text-2xl font-black text-slate-900 font-mono tracking-wider" id="modal-current-member-id">--</div>
          <p class="text-[11px] text-emerald-600 font-bold flex items-center justify-center gap-1">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>閲覧ログをリアルタイム記録中</span>
          </p>
        </div>

        <div class="text-xs text-slate-500 space-y-1 bg-slate-50 p-3 rounded-xl">
          <p>💡 別の端末（スマホ・PC）でも同じ会員IDを入力すると、進捗が引き継がれます。</p>
          <p>⚠️ ログアウトすると、閲覧ログの記録が停止します。</p>
        </div>

        <button onclick="logoutMember()" class="w-full py-2.5 rounded-xl bg-slate-100 hover:bg-rose-50 text-slate-700 hover:text-rose-600 font-bold text-xs transition border border-slate-200 flex items-center justify-center gap-1.5">
          <i class="fa-solid fa-right-from-bracket"></i>
          <span>ログアウト（記録を停止）</span>
        </button>
      </div>

      <!-- 未ログイン入力フォーム -->
      <form id="member-id-form" onsubmit="handleMemberLogin(event)" class="space-y-4">
        <div>
          <label for="input-member-id" class="block text-xs font-bold text-slate-700 mb-1.5">会員ID（半角英数字）</label>
          <div class="relative">
            <input type="text" id="input-member-id" required placeholder="例: 1234abc" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm font-mono font-bold tracking-wider">
          </div>
          <p class="text-[11px] text-slate-400 mt-1">※パスワードは不要です。割り振られた会員IDをご入力ください。</p>
        </div>

        <button type="submit" class="w-full py-3 bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white font-bold rounded-xl shadow-md transition flex items-center justify-center gap-2 text-xs">
          <i class="fa-solid fa-check"></i>
          <span>会員IDを設定して閲覧を開始</span>
        </button>
      </form>

    </div>
  </div>
'''

proposal_modal_target = '  <div id="proposal-modal"'
if proposal_modal_target in html:
    html = html.replace(proposal_modal_target, member_modal_html + '\n\n' + proposal_modal_target)
    print("2. Member ID modal added.")

# 3. js/member-tracker.js スクリプト読み込み
app_script_target = '  <script src="js/app.js"></script>'
tracker_script_tag = '  <script src="js/member-tracker.js"></script>'
if app_script_target in html and tracker_script_tag not in html:
    html = html.replace(app_script_target, tracker_script_tag + '\n' + app_script_target)
    print("3. member-tracker.js script tag added.")

# 4. updateOnboardingProgress の関数更新（trackStepChange と連動）
old_update_fn = '''    function updateOnboardingProgress() {
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

      try {
        localStorage.setItem('neofamily_onboarding', JSON.stringify({ c1, c2, c3 }));
      } catch (e) {}
    }'''

new_update_fn = '''    function updateOnboardingProgress() {
      const c1 = document.getElementById('check-step-1')?.checked || false;
      const c2 = document.getElementById('check-step-2')?.checked || false;
      const c3 = document.getElementById('check-step-3')?.checked || false;
      
      updateOnboardingProgressUI();

      try {
        localStorage.setItem('neofamily_onboarding', JSON.stringify({ c1, c2, c3 }));
      } catch (e) {}

      // クラウド（Firestore）に進捗を同期
      if (typeof trackStepChange === 'function') {
        trackStepChange('zoom', c1);
        trackStepChange('teireikai', c2);
        trackStepChange('support', c3);
      }
    }

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
    }'''

if old_update_fn in html:
    html = html.replace(old_update_fn, new_update_fn)
    print("4. updateOnboardingProgress linked to cloud tracking.")

# 5. 動画再生時に trackContentView を呼び出し
old_video_fn = '''    // 動画モーダル
    function openVideoModal(url, title) {
      document.getElementById('video-modal-title').textContent = title;
      document.getElementById('video-iframe').src = url + '?autoplay=1';
      openModal('video-modal');
    }'''

new_video_fn = '''    // 動画モーダル
    function openVideoModal(url, title) {
      document.getElementById('video-modal-title').textContent = title;
      document.getElementById('video-iframe').src = url + '?autoplay=1';
      openModal('video-modal');

      // 閲覧ログの記録
      if (typeof trackContentView === 'function') {
        trackContentView(url, title);
      }
    }'''

if old_video_fn in html:
    html = html.replace(old_video_fn, new_video_fn)
    print("5. openVideoModal hooked to trackContentView.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html update complete!")

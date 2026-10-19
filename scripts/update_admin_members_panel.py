with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. タブボタン
if 'tab-btn-members' not in html:
    old_btn = '''        <button id="tab-btn-settings" onclick="switchAdminTab('settings')" class="px-4 py-3 text-xs sm:text-sm font-bold border-b-2 border-transparent text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap transition">
          <i class="fa-solid fa-shield-halved"></i>
          <span>設定 & パスコード変更</span>
        </button>'''
    new_btn = '''        <button id="tab-btn-members" onclick="switchAdminTab('members')" class="px-4 py-3 text-xs sm:text-sm font-bold border-b-2 border-transparent text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap transition">
          <i class="fa-solid fa-users-gear text-indigo-600"></i>
          <span>会員進捗 & 担当サポート管理</span>
        </button>\n''' + old_btn
    html = html.replace(old_btn, new_btn)

# 2. 会員タブコンテンツ
member_tab_content = '''    <!-- ==================== TAB: MEMBERS & MENTORS PROGRESS ==================== -->
    <div id="tab-content-members" class="hidden space-y-6">

      <!-- ロール切替 & フィルターバー -->
      <div class="bg-white rounded-3xl p-5 sm:p-6 border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-lg font-bold shrink-0">
            <i class="fa-solid fa-user-shield"></i>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h2 class="text-lg font-black text-slate-900">会員オンボーディング進捗管理</h2>
              <span id="role-badge" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800">総責任者ビュー</span>
            </div>
            <p class="text-xs text-slate-500 mt-0.5">5,000人規模の会員閲覧ログ・Zoom/定例会アクションおよびサポート担当の割り当て状況</p>
          </div>
        </div>

        <div class="flex items-center gap-2.5 flex-wrap">
          <!-- ロール選択 -->
          <div class="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl text-xs font-bold border border-slate-200">
            <button onclick="setAdminRoleView('admin')" id="role-btn-admin" class="px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-2xs transition flex items-center gap-1">
              <i class="fa-solid fa-crown text-amber-500"></i>
              <span>総責任者（全員）</span>
            </button>
            <button onclick="setAdminRoleView('mentor')" id="role-btn-mentor" class="px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition flex items-center gap-1">
              <i class="fa-solid fa-handshake text-indigo-600"></i>
              <span>サポート担当者別</span>
            </button>
          </div>

          <!-- 担当者セレクト（担当者ビュー用） -->
          <select id="mentor-select-filter" onchange="filterMembersByMentor()" class="hidden px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="all">すべての担当者</option>
            <option value="mentor_tanaka">田中 リーダー (担当 18名)</option>
            <option value="mentor_sato">佐藤 リーダー (担当 14名)</option>
            <option value="mentor_suzuki">鈴木 リーダー (担当 12名)</option>
            <option value="unassigned">⚠️ 未割り当て (要対応)</option>
          </select>

          <!-- 新規登録/一括操作 -->
          <button onclick="openAddMemberModal()" class="px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition shadow-xs flex items-center gap-1">
            <i class="fa-solid fa-user-plus"></i>
            <span>会員IDを追加</span>
          </button>
        </div>
      </div>

      <!-- KPI サマリーカード -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white rounded-3xl p-5 border border-slate-200 shadow-xs flex items-center gap-4">
          <div class="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-xl shrink-0">
            <i class="fa-solid fa-users"></i>
          </div>
          <div>
            <span class="text-[11px] font-bold text-slate-400 block uppercase tracking-wider">管理会員数</span>
            <div class="flex items-baseline gap-1 mt-0.5">
              <span id="kpi-members-total" class="text-2xl font-black text-slate-900">0</span>
              <span class="text-xs text-slate-500 font-bold">名</span>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-3xl p-5 border border-slate-200 shadow-xs flex items-center gap-4">
          <div class="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center text-xl shrink-0">
            <i class="fa-solid fa-circle-check"></i>
          </div>
          <div>
            <span class="text-[11px] font-bold text-slate-400 block uppercase tracking-wider">ファーストステップ完了 (3/3)</span>
            <div class="flex items-baseline gap-1 mt-0.5">
              <span id="kpi-members-completed" class="text-2xl font-black text-emerald-600">0</span>
              <span class="text-xs text-slate-500 font-bold">名</span>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-3xl p-5 border border-slate-200 shadow-xs flex items-center gap-4">
          <div class="w-12 h-12 rounded-2xl bg-rose-50 text-rose-600 flex items-center justify-center text-xl shrink-0">
            <i class="fa-solid fa-triangle-exclamation"></i>
          </div>
          <div>
            <span class="text-[11px] font-bold text-slate-400 block uppercase tracking-wider">未着手・フォロー推奨</span>
            <div class="flex items-baseline gap-1 mt-0.5">
              <span id="kpi-members-unstarted" class="text-2xl font-black text-rose-600">0</span>
              <span class="text-xs text-slate-500 font-bold">名</span>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-3xl p-5 border border-slate-200 shadow-xs flex items-center gap-4">
          <div class="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center text-xl shrink-0">
            <i class="fa-solid fa-clock-rotate-left"></i>
          </div>
          <div>
            <span class="text-[11px] font-bold text-slate-400 block uppercase tracking-wider">直近アクティブ (24時間)</span>
            <div class="flex items-baseline gap-1 mt-0.5">
              <span id="kpi-members-active" class="text-2xl font-black text-slate-900">0</span>
              <span class="text-xs text-slate-500 font-bold">名</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 会員進捗一覧テーブル -->
      <div class="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden space-y-4 p-5 sm:p-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div class="relative w-full sm:w-72">
            <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
            <input type="text" id="member-search-input" onkeyup="filterMembersTable()" placeholder="会員IDで検索..." class="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500">
          </div>
          <div class="flex items-center gap-2 text-xs font-bold">
            <span class="text-slate-500">ステータス絞り込み:</span>
            <select id="member-status-filter" onchange="filterMembersTable()" class="px-2.5 py-1.5 rounded-lg bg-slate-50 border border-slate-200 text-xs font-bold text-slate-700">
              <option value="all">すべて</option>
              <option value="completed">全完了 (3/3)</option>
              <option value="inprogress">進行中 (1〜2)</option>
              <option value="unstarted">未着手 (0/3)</option>
            </select>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-slate-50 text-slate-500 font-bold border-y border-slate-200">
              <tr>
                <th class="py-3 px-4">会員ID</th>
                <th class="py-3 px-4">担当サポート者</th>
                <th class="py-3 px-4">ファーストステップ進捗</th>
                <th class="py-3 px-4">閲覧コンテンツ</th>
                <th class="py-3 px-4">最終アクセス</th>
                <th class="py-3 px-4 text-right">操作</th>
              </tr>
            </thead>
            <tbody id="members-table-body" class="divide-y divide-slate-100 font-medium text-slate-700">
            </tbody>
          </table>
        </div>
      </div>

    </div>
'''

target = '    <!-- ==================== TAB 3: SETTINGS ==================== -->'
assert target in html, 'target not found'
html = html.replace(target, member_tab_content + '\n\n' + target)

# 3. モーダル
admin_modals_html = '''  <!-- ========================================== -->
  <!-- 会員 閲覧ログ詳細モーダル -->
  <!-- ========================================== -->
  <div id="member-detail-modal" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm hidden items-center justify-center p-4">
    <div class="bg-white rounded-3xl p-6 sm:p-8 max-w-lg w-full shadow-2xl border border-slate-200 relative animate-scaleUp max-h-[85vh] flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between pb-4 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-lg font-bold">
              <i class="fa-solid fa-id-card"></i>
            </div>
            <div>
              <h3 class="text-lg font-black text-slate-900 font-mono" id="detail-modal-member-id">--</h3>
              <p class="text-xs text-slate-500" id="detail-modal-mentor-name">担当: --</p>
            </div>
          </div>
          <button onclick="closeModal('member-detail-modal')" class="w-8 h-8 rounded-full bg-slate-100 text-slate-400 hover:text-slate-700 flex items-center justify-center">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>

        <div class="py-4 space-y-4 overflow-y-auto max-h-[50vh]">
          <div>
            <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">ファーストステップ達成状況</h4>
            <div id="detail-modal-steps" class="space-y-1.5">
            </div>
          </div>

          <div>
            <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">閲覧ログ履歴（動画・ページ・フロー）</h4>
            <div id="detail-modal-logs" class="space-y-2">
            </div>
          </div>
        </div>
      </div>

      <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
        <button onclick="closeModal('member-detail-modal')" class="px-4 py-2 rounded-xl bg-slate-100 text-slate-700 font-bold text-xs hover:bg-slate-200 transition">
          閉じる
        </button>
      </div>
    </div>
  </div>

  <!-- 新規会員ID追加モーダル -->
  <div id="add-member-modal" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm hidden items-center justify-center p-4">
    <div class="bg-white rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl border border-slate-200 relative animate-scaleUp">
      <button onclick="closeModal('add-member-modal')" class="absolute top-4 right-4 w-8 h-8 rounded-full bg-slate-100 text-slate-400 hover:text-slate-700 flex items-center justify-center">
        <i class="fa-solid fa-xmark"></i>
      </button>

      <div class="text-center space-y-1 mb-5">
        <h3 class="text-lg font-black text-slate-900">会員IDを手動登録・割り当て</h3>
        <p class="text-xs text-slate-500">担当サポート者を指定して会員IDを発行します</p>
      </div>

      <form onsubmit="handleAddMemberSubmit(event)" class="space-y-4">
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">会員ID</label>
          <input type="text" id="new-member-id" required placeholder="例: 1234abc" class="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-xs font-mono font-bold">
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">担当サポート者</label>
          <select id="new-member-mentor" class="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-800">
            <option value="mentor_tanaka">田中 リーダー</option>
            <option value="mentor_sato">佐藤 リーダー</option>
            <option value="mentor_suzuki">鈴木 リーダー</option>
            <option value="unassigned">未割り当て</option>
          </select>
        </div>
        <button type="submit" class="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl text-xs shadow-md transition">
          登録する
        </button>
      </form>
    </div>
  </div>
'''

html = html.replace('</body>', admin_modals_html + '\n</body>')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("admin.html successfully updated!")

import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 新入生ファーストステップ 3箇条 & 目的別スタートコンパスのHTML
starter_and_compass_html = '''      <!-- ========================================== -->
      <!-- 🌱 新入生ファーストステップ 3箇条（やること最小化 & プログレス） -->
      <!-- ========================================== -->
      <section id="onboarding-steps-section" class="bg-gradient-to-br from-indigo-950 via-slate-900 to-slate-950 text-white rounded-3xl p-6 sm:p-8 border border-indigo-800/60 shadow-xl space-y-5">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-indigo-800/40">
          <div class="flex items-center gap-3">
            <span class="w-10 h-10 rounded-2xl bg-amber-400 text-slate-950 flex items-center justify-center font-black text-lg shadow-md shrink-0">
              🌱
            </span>
            <div>
              <h3 class="text-lg sm:text-xl font-black text-white flex items-center gap-2">
                <span>新入生ファーストステップ：最初の1週間はこれだけでOK！</span>
              </h3>
              <p class="text-xs text-indigo-200 mt-0.5">事業やイベントが多くて迷ったら、まずこの3つだけ完了させましょう✨</p>
            </div>
          </div>
          <div class="flex items-center gap-2 bg-indigo-900/60 px-3 py-1.5 rounded-xl border border-indigo-700/50 text-xs font-bold shrink-0">
            <span class="text-indigo-300">達成度:</span>
            <span id="onboarding-progress-text" class="text-amber-300 font-extrabold text-sm">0 / 3 完了</span>
          </div>
        </div>

        <!-- プログレスバー -->
        <div class="w-full bg-slate-800/80 rounded-full h-2.5 overflow-hidden">
          <div id="onboarding-progress-bar" class="bg-gradient-to-r from-amber-400 to-emerald-400 h-2.5 rounded-full transition-all duration-500" style="width: 0%"></div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          <!-- Step 1 -->
          <div class="bg-white/5 border border-white/10 hover:border-amber-400/50 p-4 rounded-2xl transition flex flex-col justify-between space-y-3">
            <label class="flex items-start gap-3 cursor-pointer">
              <input type="checkbox" id="check-step-1" onchange="updateOnboardingProgress()" class="mt-1 w-4 h-4 rounded text-amber-500 focus:ring-amber-400 accent-amber-400 shrink-0">
              <div class="space-y-1">
                <span class="text-[10px] px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 font-bold">STEP 1</span>
                <p class="text-sm font-bold text-white">全日共通Zoom情報をメモ</p>
                <p class="text-xs text-slate-300 leading-relaxed">事業説明会は毎日共通のZoomで開催。IDとパスワードを保存しておきましょう。</p>
              </div>
            </label>
            <div class="pt-2 border-t border-white/10 flex items-center justify-between">
              <button onclick="copyZoomInfo()" class="text-xs text-amber-300 hover:underline font-bold flex items-center gap-1">
                <i class="fa-solid fa-copy text-[10px]"></i> Zoom情報をコピー
              </button>
              <span class="text-[11px] font-mono text-slate-400">ID: 811 1315 2898</span>
            </div>
          </div>

          <!-- Step 2 -->
          <div class="bg-white/5 border border-white/10 hover:border-amber-400/50 p-4 rounded-2xl transition flex flex-col justify-between space-y-3">
            <label class="flex items-start gap-3 cursor-pointer">
              <input type="checkbox" id="check-step-2" onchange="updateOnboardingProgress()" class="mt-1 w-4 h-4 rounded text-amber-500 focus:ring-amber-400 accent-amber-400 shrink-0">
              <div class="space-y-1">
                <span class="text-[10px] px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold">STEP 2</span>
                <p class="text-sm font-bold text-white">次回合同定例会に参加表明</p>
                <p class="text-xs text-slate-300 leading-relaxed">月1回の最重要イベント（11/2福岡）。調整さんで所属会名を入れて送信します。</p>
              </div>
            </label>
            <div class="pt-2 border-t border-white/10 flex items-center justify-between">
              <a href="https://chouseisan.com/s?h=2733ccd431d846f8bccd9c3061c0bca3" target="_blank" class="text-xs text-rose-300 hover:underline font-bold flex items-center gap-1">
                <i class="fa-solid fa-pen-to-square text-[10px]"></i> 調整さんを開く
              </a>
              <span class="text-[11px] text-slate-400">11/2(月) 13:00〜</span>
            </div>
          </div>

          <!-- Step 3 -->
          <div class="bg-white/5 border border-white/10 hover:border-amber-400/50 p-4 rounded-2xl transition flex flex-col justify-between space-y-3">
            <label class="flex items-start gap-3 cursor-pointer">
              <input type="checkbox" id="check-step-3" onchange="updateOnboardingProgress()" class="mt-1 w-4 h-4 rounded text-amber-500 focus:ring-amber-400 accent-amber-400 shrink-0">
              <div class="space-y-1">
                <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">STEP 3</span>
                <p class="text-sm font-bold text-white">困ったときのサポート窓口確認</p>
                <p class="text-xs text-slate-300 leading-relaxed">LINEやZoom、イベント参加で不安なことがあれば専任サポート一覧から相談可能です。</p>
              </div>
            </label>
            <div class="pt-2 border-t border-white/10 flex items-center justify-between">
              <button onclick="scrollToSection('flowchart-section')" class="text-xs text-emerald-300 hover:underline font-bold flex items-center gap-1">
                <i class="fa-solid fa-arrow-down text-[10px]"></i> サポート一覧画像を見る
              </button>
              <span class="text-[11px] text-slate-400">相談無料</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- 🧭 目的別・スタートコンパス（あなたは何がしたい？） -->
      <!-- ========================================== -->
      <section id="purpose-compass-section" class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-5">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-100 text-amber-800 text-xs font-bold mb-1">
              <i class="fa-solid fa-compass text-amber-600"></i> あなたの「やりたいこと」から選ぶ
            </span>
            <h2 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
              目的別・スタートコンパス
            </h2>
            <p class="text-xs sm:text-sm text-slate-500 mt-1">「グループに入ったけれど何から動けばいい？」という方は、気になる目的をタップしてください。最適な最初の一歩をご案内します。</p>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- 目的 1: 仲間づくり・交流 -->
          <div onclick="selectPurpose('community')" id="purpose-card-community" class="purpose-card cursor-pointer p-5 rounded-2xl border-2 border-slate-200 hover:border-amber-400 hover:bg-amber-50/30 transition flex flex-col justify-between group">
            <div>
              <div class="w-12 h-12 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center text-xl mb-3 group-hover:scale-110 transition">
                🤝
              </div>
              <h4 class="font-black text-slate-900 text-base mb-1">仲間と交流したい</h4>
              <p class="text-xs text-slate-500 leading-relaxed">
                まずはグループの雰囲気になじみたい、横のつながりや同期の仲間をつくりたい方。
              </p>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-100 text-xs font-bold text-amber-700 flex items-center justify-between">
              <span>おすすめのアクション</span>
              <i class="fa-solid fa-chevron-right text-[10px]"></i>
            </div>
          </div>

          <!-- 目的 2: 出品・マルシェ出店 -->
          <div onclick="selectPurpose('shop')" id="purpose-card-shop" class="purpose-card cursor-pointer p-5 rounded-2xl border-2 border-slate-200 hover:border-rose-400 hover:bg-rose-50/30 transition flex flex-col justify-between group">
            <div>
              <div class="w-12 h-12 rounded-xl bg-rose-100 text-rose-700 flex items-center justify-center text-xl mb-3 group-hover:scale-110 transition">
                🛍️
              </div>
              <h4 class="font-black text-slate-900 text-base mb-1">商品を出品・販売したい</h4>
              <p class="text-xs text-slate-500 leading-relaxed">
                自分の商品やスキル・鑑定を「Iyasaka宮マルシェ」やリアルマルシェで販売したい方。
              </p>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-100 text-xs font-bold text-rose-700 flex items-center justify-between">
              <span>おすすめのアクション</span>
              <i class="fa-solid fa-chevron-right text-[10px]"></i>
            </div>
          </div>

          <!-- 目的 3: RAYTUS事業・共育参画 -->
          <div onclick="selectPurpose('business')" id="purpose-card-business" class="purpose-card cursor-pointer p-5 rounded-2xl border-2 border-slate-200 hover:border-blue-400 hover:bg-blue-50/30 transition flex flex-col justify-between group">
            <div>
              <div class="w-12 h-12 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center text-xl mb-3 group-hover:scale-110 transition">
                🏫
              </div>
              <h4 class="font-black text-slate-900 text-base mb-1">事業やプロジェクトに参入</h4>
              <p class="text-xs text-slate-500 leading-relaxed">
                寺子屋や子育て・食・美容など、31の公式事業チームに関わって力を発揮したい方。
              </p>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-100 text-xs font-bold text-blue-700 flex items-center justify-between">
              <span>おすすめのアクション</span>
              <i class="fa-solid fa-chevron-right text-[10px]"></i>
            </div>
          </div>

          <!-- 目的 4: ビジネスマインド・稼ぐ力を学ぶ -->
          <div onclick="selectPurpose('study')" id="purpose-card-study" class="purpose-card cursor-pointer p-5 rounded-2xl border-2 border-slate-200 hover:border-emerald-400 hover:bg-emerald-50/30 transition flex flex-col justify-between group">
            <div>
              <div class="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center text-xl mb-3 group-hover:scale-110 transition">
                🔥
              </div>
              <h4 class="font-black text-slate-900 text-base mb-1">起業・稼ぐ力を学びたい</h4>
              <p class="text-xs text-slate-500 leading-relaxed">
                ぶった斬り会長の思考法や特別勉強会を通じて、自立した収入とビジネス力を身につけたい方。
              </p>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-100 text-xs font-bold text-emerald-700 flex items-center justify-between">
              <span>おすすめのアクション</span>
              <i class="fa-solid fa-chevron-right text-[10px]"></i>
            </div>
          </div>
        </div>

        <!-- 診断結果パネル（選択された目的のアクションを表示） -->
        <div id="purpose-result-panel" class="hidden p-6 rounded-2xl border transition duration-300">
        </div>
      </section>
'''

# 挿入位置: </section> (id="beginner-starter-guide" の終わり)
starter_guide_end = '      </section>\n\n      <!-- 主要なポータル機能カードグリッド（各コンテンツへのダイレクト入口） -->'
assert starter_guide_end in html, 'starter_guide_end not found'
html = html.replace(starter_guide_end, '      </section>\n\n' + starter_and_compass_html + '\n\n      <!-- 主要なポータル機能カードグリッド（各コンテンツへのダイレクト入口） -->')
print("1. Starter checklist and Purpose compass added to Hub.")

# 2. tab-content-schedule の内容を抽出し、Hub タブ内に統合
schedule_content_match = re.search(
    r'<div id="tab-content-schedule" class="tab-content space-y-8">(.*?)</div>\s*<!-- ======================================================== -->\s*<!-- TAB 5: 事業紹介 & アーカイブ集',
    html,
    re.DOTALL
)

if schedule_content_match:
    schedule_inner = schedule_content_match.group(1).strip()
    
    # schedule_inner の最上部にラッパー section を付与
    integrated_schedule_block = f'''      <!-- ========================================== -->
      <!-- 📅 直近の重要予定・参加フローチャート・全体スケジュール（旧参加ガイド統合） -->
      <!-- ========================================== -->
      <div id="schedule-section" class="space-y-8 pt-6 border-t border-slate-200">
        <div class="flex items-center justify-between">
          <div>
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-bold mb-1">
              <i class="fa-regular fa-calendar-check text-blue-600"></i> スケジュール & アクション
            </span>
            <h2 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
              直近の定例会・説明会参加フロー & 年間予定
            </h2>
            <p class="text-xs text-slate-500 mt-1">次回定例会への参加表明や共通Zoom、説明会フローチャートをまとめて確認できます</p>
          </div>
        </div>

        {schedule_inner}
      </div>'''

    # Hubタブの末尾（</section> <!-- 迷子になったときの安心ナビ --> の直前か直後）に配置
    hub_qa_target = '      <!-- 迷子になったときの安心ナビ (FAQ / サポート一覧へのリンク) -->'
    assert hub_qa_target in html, 'hub_qa_target not found'
    html = html.replace(hub_qa_target, integrated_schedule_block + '\n\n' + hub_qa_target)
    print("2. Schedule & Flow contents integrated into Hub tab.")

    # 独立した tab-content-schedule を削除
    old_schedule_tab_pattern = re.compile(
        r'    <!-- ======================================================== -->\s*<!-- TAB 4: スケジュール & フロー.*?<div id="tab-content-schedule".*?</div>\s*(?=<!-- ======================================================== -->\s*<!-- TAB 5: 事業紹介 & アーカイブ集)',
        re.DOTALL
    )
    html = old_schedule_tab_pattern.sub('', html)
    print("3. Standalone tab-content-schedule removed.")

# 3. JavaScript ロジックの追加
# switchTab('schedule') のフォールバックと、オンボーディング & 診断ハンドラー
js_additions = '''
    // ==========================================
    // 新入生オンボーディング & 目的別診断ロジック
    // ==========================================

    function updateOnboardingProgress() {
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
    }

    function restoreOnboardingProgress() {
      try {
        const saved = localStorage.getItem('neofamily_onboarding');
        if (saved) {
          const data = JSON.parse(saved);
          if (document.getElementById('check-step-1')) document.getElementById('check-step-1').checked = data.c1;
          if (document.getElementById('check-step-2')) document.getElementById('check-step-2').checked = data.c2;
          if (document.getElementById('check-step-3')) document.getElementById('check-step-3').checked = data.c3;
          updateOnboardingProgress();
        }
      } catch (e) {}
    }

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
            { label: 'Step 3: イベントカレンダーで今月の交流会をチェック', desc: '懇親会や勉強会など、気軽に参加できる日程をカレンダーから探せます。', action: '<button onclick="switchTab(\\'calendar\\')" class="px-3 py-1.5 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>カレンダーを見る</span><i class="fa-regular fa-calendar-days"></i></button>' }
          ]
        },
        shop: {
          title: '🛍️ 「商品を出品・販売したい」あなたへのスタートガイド',
          bg: 'bg-rose-50/80 border-rose-300',
          badge: 'bg-rose-200 text-rose-900',
          desc: 'Iyasaka宮マルシェや各地のリアルマルシェで、あなたのオリジナル商品や鑑定・セッションを出品できます。',
          steps: [
            { label: 'Step 1: Iyasaka宮（デモ体験 & 本家マルシェ）を見る', desc: 'どんな商品や価格帯が並んでいるか、ポータル内のIyasaka宮タブでイメージを掴みましょう。', action: '<button onclick="switchTab(\\'iyasaka\\')" class="px-3 py-1.5 rounded-lg bg-amber-600 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>Iyasaka宮を見る</span><i class="fa-solid fa-torii-gate"></i></button>' },
            { label: 'Step 2: 合同事業説明会でマルシェ出店要項を聞く', desc: '共通Zoomで開催される事業説明会で、出店手続きや出品条件について案内があります。', action: '<button onclick="scrollToSection(\\'common-zoom-section\\')" class="px-3 py-1.5 rounded-lg bg-blue-600 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>Zoom日程を見る</span><i class="fa-solid fa-video"></i></button>' },
            { label: 'Step 3: サポート一覧の「マルシェ担当」に相談する', desc: '分からないことがあれば、サポート一覧画像に記載のマルシェ窓口に気軽にLINEで相談可能です。', action: '<button onclick="scrollToSection(\\'flowchart-section\\')" class="px-3 py-1.5 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>サポート窓口を見る</span><i class="fa-solid fa-arrow-down"></i></button>' }
          ]
        },
        business: {
          title: '🏫 「RAYTUS事業・共育に参入したい」あなたへのスタートガイド',
          bg: 'bg-blue-50/80 border-blue-300',
          badge: 'bg-blue-200 text-blue-900',
          desc: 'RAYTUS group.には子育て・食・美容・教育など多種多様な事業があります。あなたの想いに合ったチームに参加しましょう。',
          steps: [
            { label: 'Step 1: 「全事業紹介 & 公式動画アーカイブ」で関心のある事業を探す', desc: '31事業を5大グループ別に整理。各事業の代表者や理念の動画をその場で視聴できます。', action: '<button onclick="switchTab(\\'raytus\\'); scrollToSection(\\'raytus-services-section\\');" class="px-3 py-1.5 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>全事業一覧を見る</span><i class="fa-solid fa-shapes"></i></button>' },
            { label: 'Step 2: 寺子屋プロジェクト・バスタ高校プロジェクトをチェック', desc: 'RAYTUSが力を入れる次世代の教育支援プロジェクトの最新状況を確認できます。', action: '<button onclick="switchTab(\\'raytus\\'); scrollToSection(\\'raytus-projects-section\\');" class="px-3 py-1.5 rounded-lg bg-amber-500 text-slate-950 font-bold text-xs flex items-center gap-1 shadow-xs"><span>プロジェクトを見る</span><i class="fa-solid fa-arrow-right"></i></button>' },
            { label: 'Step 3: 合同定例会（11/2福岡）で各事業リーダーと直接名刺交換', desc: 'リアルの定例会には全事業の代表・リーダーが集結します。直接相談して参画を決めましょう。', action: '<a href="https://chouseisan.com/s?h=2733ccd431d846f8bccd9c3061c0bca3" target="_blank" class="px-3 py-1.5 rounded-lg bg-emerald-600 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>定例会に参加表明</span><i class="fa-solid fa-pen-to-square"></i></a>' }
          ]
        },
        study: {
          title: '🔥 「起業・稼ぐ力・マインドを学びたい」あなたへのスタートガイド',
          bg: 'bg-emerald-50/80 border-emerald-300',
          badge: 'bg-emerald-200 text-emerald-900',
          desc: '半年で億を稼ぐ思考法、ぶった斬り会長の哲学、特別勉強会のアーカイブで最短距離でビジネスマインドを鍛えましょう。',
          steps: [
            { label: 'Step 1: ぶった斬り会長 公式YouTube（@buttagirichannel）を見る', desc: '夫婦関係からお金の使い方・起業戦略まで、人気動画をポータル内で直接再生できます。', action: '<button onclick="switchTab(\\'sns\\'); setSnsFilter(\\'youtube\\');" class="px-3 py-1.5 rounded-lg bg-red-600 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>YouTube動画を見る</span><i class="fa-brands fa-youtube"></i></button>' },
            { label: 'Step 2: ぶった斬り会長 公式TikTok（@buttagiri888）をフォロー', desc: '日常のスキマ時間に見られるショート動画で、毎日マインドセットをアップデート。', action: '<button onclick="switchTab(\\'sns\\'); setSnsFilter(\\'tiktok\\');" class="px-3 py-1.5 rounded-lg bg-slate-900 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>TikTokを見る</span><i class="fa-brands fa-tiktok"></i></button>' },
            { label: 'Step 3: 特別勉強会（アーカイブ集）でビジネス実践を学ぶ', desc: '確定申告、クリエイティブ、協会のノウハウなど過去の勉強会アーカイブを視聴できます。', action: '<button onclick="switchTab(\\'archive\\')" class="px-3 py-1.5 rounded-lg bg-indigo-600 text-white font-bold text-xs flex items-center gap-1 shadow-xs"><span>勉強会アーカイブ</span><i class="fa-solid fa-graduation-cap"></i></button>' }
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
'''

# switchTab 関数に schedule へのリダイレクトを追加
switch_tab_old = '''    function switchTab(tabId) {
      currentTab = tabId;'''

switch_tab_new = '''    function switchTab(tabId) {
      if (tabId === 'schedule') {
        switchTab('hub');
        scrollToSection('schedule-section');
        return;
      }
      currentTab = tabId;'''

if switch_tab_old in html:
    html = html.replace(switch_tab_old, switch_tab_new)
    print("4. switchTab redirect for schedule added.")

# js_additions を switchTab の直前に挿入
html = html.replace('    // ==========================================\n    // タブ切り替え & ナビゲーション\n    // ==========================================', js_additions + '\n    // ==========================================\n    // タブ切り替え & ナビゲーション\n    // ==========================================')
print("5. Onboarding & Compass JS functions added.")

# 初期化時に restoreOnboardingProgress を呼ぶ
dom_content_loaded_target = "document.addEventListener('DOMContentLoaded', () => {"
assert dom_content_loaded_target in html, 'DOMContentLoaded not found'
html = html.replace(dom_content_loaded_target, dom_content_loaded_target + "\n      restoreOnboardingProgress();")
print("6. restoreOnboardingProgress hooked into DOMContentLoaded.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Part 2 complete! All changes written to index.html.")

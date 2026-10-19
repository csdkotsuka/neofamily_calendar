import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. タブバーの更新: 5つのタブに集約
# 「総合ハブ & ガイド」->「総合スタートガイド」
# 「参加ガイド & フロー」を削除
tab_bar_pattern = re.compile(
    r'<nav class="flex items-center gap-1 overflow-x-auto no-scrollbar py-2 border-t border-slate-100 text-xs font-bold">.*?</nav>',
    re.DOTALL
)

new_tab_bar = '''<nav class="flex items-center gap-1 overflow-x-auto no-scrollbar py-2 border-t border-slate-100 text-xs font-bold">
        <button onclick="switchTab('hub')" id="tab-btn-hub" class="tab-btn whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 bg-slate-900 text-white shadow-xs">
          <i class="fa-solid fa-compass"></i>
          <span>総合スタートガイド</span>
        </button>
        <button onclick="switchTab('raytus')" id="tab-btn-raytus" class="tab-btn whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 text-slate-600 hover:bg-slate-100">
          <i class="fa-solid fa-globe text-slate-400"></i>
          <span>RAYTUS 公式 & 事業紹介</span>
        </button>
        <button onclick="switchTab('iyasaka')" id="tab-btn-iyasaka" class="tab-btn whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 text-slate-600 hover:bg-slate-100">
          <i class="fa-solid fa-torii-gate text-amber-600"></i>
          <span>Iyasaka宮 (配信 & EC)</span>
        </button>
        <button onclick="switchTab('calendar')" id="tab-btn-calendar" class="tab-btn whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 text-slate-600 hover:bg-slate-100">
          <i class="fa-regular fa-calendar-days text-rose-500"></i>
          <span>イベントカレンダー</span>
        </button>
        <button onclick="switchTab('sns')" id="tab-btn-sns" class="tab-btn whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 text-slate-600 hover:bg-slate-100">
          <i class="fa-solid fa-share-nodes text-pink-500"></i>
          <span>公式SNS</span>
        </button>
      </nav>'''

html = tab_bar_pattern.sub(new_tab_bar, html, count=1)
print("1. Tab bar updated.")

# 2. Iyasaka宮: 右上の買い物カゴボタンを削除し、デモ画面注記バナーを追加
old_iyasaka_head = '''    <!-- ======================================================== -->
    <!-- TAB 3: Iyasaka宮 コミュニティ & EC 複製 (IYASAKA) -->
    <!-- ======================================================== -->
    <div id="tab-content-iyasaka" class="tab-content">
      <!-- Iyasaka宮 コンテナ -->'''

cart_button_block = '''            <button onclick="openModal('cart-modal')" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white border border-amber-200 text-amber-800 text-xs font-bold shadow-2xs hover:bg-amber-50 transition">
              <img src="images/hd_cart_icon.png" alt="カゴ" class="w-4 h-4 object-contain">
              <span>買い物カゴ</span>
              <span id="iyasaka-cart-badge" class="px-1.5 py-0.2 rounded-full bg-rose-600 text-white text-[10px]">0</span>
            </button>'''

if cart_button_block in html:
    html = html.replace(cart_button_block, '')
    print("2-a. Iyasaka cart button removed.")

new_iyasaka_demo_banner = '''    <!-- ======================================================== -->
    <!-- TAB 3: Iyasaka宮 コミュニティ & EC 複製 (IYASAKA) -->
    <!-- ======================================================== -->
    <div id="tab-content-iyasaka" class="tab-content space-y-4">
      <!-- 体験用デモ画面・シミュレーション注記 -->
      <div class="bg-amber-500/10 border border-amber-300/40 rounded-2xl p-4 text-xs text-amber-950 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-2xs">
        <div class="flex items-center gap-2.5">
          <span class="inline-flex items-center px-2 py-0.5 rounded-full bg-amber-400 text-slate-950 font-black text-[10px] shrink-0">DEMO</span>
          <span>
            <strong>【体験用シミュレーション画面】</strong> 
            当ページはポータル統合イメージのデモ画面です。掲載内容は本家サイトの再現であり、実際の決済や注文処理は発生しません。
          </span>
        </div>
        <a href="https://community-iyasakagu.jp" target="_blank" class="shrink-0 px-3 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-700 text-white font-bold transition flex items-center gap-1.5 text-xs w-fit">
          <span>本家「Iyasaka宮」を開く</span>
          <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
        </a>
      </div>

      <!-- Iyasaka宮 コンテナ -->'''

if old_iyasaka_head in html:
    html = html.replace(old_iyasaka_head, new_iyasaka_demo_banner)
    print("2-b. Iyasaka demo banner added.")

# 3. SNSタブ: YouTubeフィルターボタン & YouTubeセクション追加
sns_filter_old = '''            <button onclick="setSnsFilter('all')" id="sns-filter-all" class="px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-2xs transition">すべて表示</button>
            <button onclick="setSnsFilter('instagram')" id="sns-filter-instagram" class="px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition flex items-center gap-1">
              <i class="fa-brands fa-instagram text-pink-600"></i>
              <span>Instagram</span>
            </button>
            <button onclick="setSnsFilter('tiktok')" id="sns-filter-tiktok" class="px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition flex items-center gap-1">
              <i class="fa-brands fa-tiktok text-slate-900"></i>
              <span>TikTok (会長)</span>
            </button>'''

sns_filter_new = '''            <button onclick="setSnsFilter('all')" id="sns-filter-all" class="px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-2xs transition">すべて表示</button>
            <button onclick="setSnsFilter('youtube')" id="sns-filter-youtube" class="px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition flex items-center gap-1">
              <i class="fa-brands fa-youtube text-red-600"></i>
              <span>YouTube</span>
            </button>
            <button onclick="setSnsFilter('tiktok')" id="sns-filter-tiktok" class="px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition flex items-center gap-1">
              <i class="fa-brands fa-tiktok text-slate-900"></i>
              <span>TikTok (会長)</span>
            </button>
            <button onclick="setSnsFilter('instagram')" id="sns-filter-instagram" class="px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition flex items-center gap-1">
              <i class="fa-brands fa-instagram text-pink-600"></i>
              <span>Instagram</span>
            </button>'''

if sns_filter_old in html:
    html = html.replace(sns_filter_old, sns_filter_new)
    print("3-a. SNS filter buttons updated with YouTube.")

# YouTubeセクション HTML
youtube_section_html = '''        <!-- ==================== 0. 公式YouTube (ぶった斬りCHANNEL主婦界のヒーロー @buttagirichannel) ==================== -->
        <div id="sns-section-youtube" class="sns-card bg-white rounded-3xl p-6 sm:p-8 border border-red-100 shadow-lg relative overflow-hidden space-y-8">
          <div class="absolute -right-10 -top-10 w-60 h-60 bg-red-500/5 rounded-full blur-3xl pointer-events-none"></div>

          <!-- YouTube チャンネルヘッダー -->
          <div class="flex flex-col sm:flex-row items-center sm:items-start gap-6 pb-6 border-b border-slate-100">
            <!-- アバター -->
            <div class="relative shrink-0">
              <div class="w-24 h-24 sm:w-28 sm:h-28 rounded-full p-1 bg-gradient-to-tr from-red-600 via-rose-500 to-amber-500 shadow-md">
                <img src="images/logo.png" alt="ぶった斬りCHANNEL" class="w-full h-full rounded-full object-contain bg-white p-1">
              </div>
              <span class="absolute bottom-1 right-1 w-7 h-7 rounded-full bg-red-600 text-white flex items-center justify-center text-sm shadow-md">
                <i class="fa-brands fa-youtube"></i>
              </span>
            </div>

            <!-- 情報 -->
            <div class="space-y-3 text-center sm:text-left flex-1">
              <div class="flex flex-col sm:flex-row sm:items-center gap-3">
                <div>
                  <h3 class="text-xl sm:text-2xl font-black text-slate-900 flex items-center justify-center sm:justify-start gap-2">
                    <span>ぶった斬りCHANNEL主婦界のヒーロー</span>
                    <i class="fa-solid fa-circle-check text-red-600 text-base" title="公式チャンネル"></i>
                  </h3>
                  <p class="text-xs font-mono text-slate-500">@buttagirichannel</p>
                </div>
                <div class="flex items-center justify-center sm:justify-start gap-2 sm:ml-auto">
                  <a href="https://www.youtube.com/@buttagirichannel?sub_confirmation=1" target="_blank" class="px-5 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold transition shadow-md flex items-center gap-2">
                    <i class="fa-brands fa-youtube text-base"></i>
                    <span>チャンネル登録</span>
                  </a>
                  <a href="https://www.youtube.com/@buttagirichannel" target="_blank" class="w-9 h-9 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 flex items-center justify-center text-xs transition border border-slate-200" title="YouTubeで開く">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                  </a>
                </div>
              </div>

              <!-- スタッツ -->
              <div class="flex items-center justify-center sm:justify-start gap-6 text-xs sm:text-sm text-slate-700">
                <div><strong class="font-black text-slate-900 text-base">600+</strong> 本の動画</div>
                <div><strong class="font-black text-slate-900 text-base">毎日</strong> 配信中</div>
                <div><span class="px-2 py-0.5 rounded-full bg-red-100 text-red-700 text-[11px] font-bold">主婦層・女性起業家から絶大な支持</span></div>
              </div>

              <!-- 説明文 -->
              <div class="text-xs text-slate-600 leading-relaxed max-w-2xl">
                <p>🔥 夫婦問題・モラハラ・熟年離婚・ワンオペのリアルな悩みを、100億稼ぐ会長が痛快かつ本質からぶった斬る！</p>
                <p class="text-slate-500 mt-1">「傷の舐め合いはいらない、自立して未来を変えたい」すべての女性のための人生変革チャンネル。</p>
              </div>
            </div>
          </div>

          <!-- 最近の注目・人気動画グリッド -->
          <div>
            <div class="flex items-center justify-between mb-4">
              <span class="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
                <i class="fa-brands fa-youtube text-red-600 text-sm"></i> 最近の注目動画（タップでその場で再生）
              </span>
              <a href="https://www.youtube.com/@buttagirichannel/videos" target="_blank" class="text-xs text-red-600 hover:underline flex items-center gap-1 font-bold">
                <span>YouTubeですべて見る</span>
                <i class="fa-solid fa-arrow-right text-[10px]"></i>
              </a>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              
              <!-- Video 1 -->
              <div class="group bg-slate-50 border border-slate-200/80 rounded-2xl overflow-hidden hover:border-red-400 hover:shadow-md transition flex flex-col justify-between">
                <div class="aspect-video relative bg-slate-900 overflow-hidden cursor-pointer" onclick="openVideoModal('https://www.youtube.com/embed/EK-xR3McLHc', '【58歳熟年離婚】を迫られた夫はパンツも洗えん。飯も作れん。｜妻は急に冷めたんじゃない。')">
                  <img src="https://i.ytimg.com/vi/EK-xR3McLHc/hqdefault.jpg" alt="動画サムネイル" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                  <div class="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition flex items-center justify-center">
                    <span class="w-12 h-12 rounded-full bg-red-600/90 text-white flex items-center justify-center text-lg shadow-lg group-hover:scale-110 transition">
                      <i class="fa-solid fa-play ml-0.5"></i>
                    </span>
                  </div>
                  <span class="absolute bottom-2 right-2 px-1.5 py-0.5 rounded bg-black/80 text-white text-[10px] font-mono">YouTube</span>
                </div>
                <div class="p-3.5 space-y-2 flex-1 flex flex-col justify-between">
                  <h4 class="text-xs font-bold text-slate-900 line-clamp-2 group-hover:text-red-600 transition">
                    【58歳熟年離婚】を迫られた夫はパンツも洗えん。飯も作れん。｜妻は急に冷めたんじゃない。
                  </h4>
                  <div class="flex items-center justify-between pt-2 border-t border-slate-200 text-[11px]">
                    <button onclick="openVideoModal('https://www.youtube.com/embed/EK-xR3McLHc', '【58歳熟年離婚】を迫られた夫はパンツも洗えん。飯も作れん。｜妻は急に冷めたんじゃない。')" class="text-red-600 font-bold hover:underline flex items-center gap-1">
                      <i class="fa-solid fa-circle-play text-[10px]"></i> その場で再生
                    </button>
                    <a href="https://www.youtube.com/watch?v=EK-xR3McLHc" target="_blank" class="text-slate-400 hover:text-slate-700" title="YouTubeで開く">
                      <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>
                  </div>
                </div>
              </div>

              <!-- Video 2 -->
              <div class="group bg-slate-50 border border-slate-200/80 rounded-2xl overflow-hidden hover:border-red-400 hover:shadow-md transition flex flex-col justify-between">
                <div class="aspect-video relative bg-slate-900 overflow-hidden cursor-pointer" onclick="openVideoModal('https://www.youtube.com/embed/3sPl_bbEaiE', '【夫の浮気】妻がやるべきことは1つだけ｜100億稼ぐ会長が本音で語る')">
                  <img src="https://i.ytimg.com/vi/3sPl_bbEaiE/hqdefault.jpg" alt="動画サムネイル" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                  <div class="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition flex items-center justify-center">
                    <span class="w-12 h-12 rounded-full bg-red-600/90 text-white flex items-center justify-center text-lg shadow-lg group-hover:scale-110 transition">
                      <i class="fa-solid fa-play ml-0.5"></i>
                    </span>
                  </div>
                  <span class="absolute bottom-2 right-2 px-1.5 py-0.5 rounded bg-black/80 text-white text-[10px] font-mono">YouTube</span>
                </div>
                <div class="p-3.5 space-y-2 flex-1 flex flex-col justify-between">
                  <h4 class="text-xs font-bold text-slate-900 line-clamp-2 group-hover:text-red-600 transition">
                    【夫の浮気】妻がやるべきことは1つだけ｜100億稼ぐ会長が本音で語る
                  </h4>
                  <div class="flex items-center justify-between pt-2 border-t border-slate-200 text-[11px]">
                    <button onclick="openVideoModal('https://www.youtube.com/embed/3sPl_bbEaiE', '【夫の浮気】妻がやるべきことは1つだけ｜100億稼ぐ会長が本音で語る')" class="text-red-600 font-bold hover:underline flex items-center gap-1">
                      <i class="fa-solid fa-circle-play text-[10px]"></i> その場で再生
                    </button>
                    <a href="https://www.youtube.com/watch?v=3sPl_bbEaiE" target="_blank" class="text-slate-400 hover:text-slate-700" title="YouTubeで開く">
                      <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>
                  </div>
                </div>
              </div>

              <!-- Video 3 -->
              <div class="group bg-slate-50 border border-slate-200/80 rounded-2xl overflow-hidden hover:border-red-400 hover:shadow-md transition flex flex-col justify-between">
                <div class="aspect-video relative bg-slate-900 overflow-hidden cursor-pointer" onclick="openVideoModal('https://www.youtube.com/embed/KApFWKM2QEU', '【16年間モラハラ】もう男なんていらない')">
                  <img src="https://i.ytimg.com/vi/KApFWKM2QEU/hqdefault.jpg" alt="動画サムネイル" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                  <div class="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition flex items-center justify-center">
                    <span class="w-12 h-12 rounded-full bg-red-600/90 text-white flex items-center justify-center text-lg shadow-lg group-hover:scale-110 transition">
                      <i class="fa-solid fa-play ml-0.5"></i>
                    </span>
                  </div>
                  <span class="absolute bottom-2 right-2 px-1.5 py-0.5 rounded bg-black/80 text-white text-[10px] font-mono">YouTube</span>
                </div>
                <div class="p-3.5 space-y-2 flex-1 flex flex-col justify-between">
                  <h4 class="text-xs font-bold text-slate-900 line-clamp-2 group-hover:text-red-600 transition">
                    【16年間モラハラ】もう男なんていらない
                  </h4>
                  <div class="flex items-center justify-between pt-2 border-t border-slate-200 text-[11px]">
                    <button onclick="openVideoModal('https://www.youtube.com/embed/KApFWKM2QEU', '【16年間モラハラ】もう男なんていらない')" class="text-red-600 font-bold hover:underline flex items-center gap-1">
                      <i class="fa-solid fa-circle-play text-[10px]"></i> その場で再生
                    </button>
                    <a href="https://www.youtube.com/watch?v=KApFWKM2QEU" target="_blank" class="text-slate-400 hover:text-slate-700" title="YouTubeで開く">
                      <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>
                  </div>
                </div>
              </div>

              <!-- Video 4 -->
              <div class="group bg-slate-50 border border-slate-200/80 rounded-2xl overflow-hidden hover:border-red-400 hover:shadow-md transition flex flex-col justify-between">
                <div class="aspect-video relative bg-slate-900 overflow-hidden cursor-pointer" onclick="openVideoModal('https://www.youtube.com/embed/J7tFe7x3_cs', '【モラハラ夫と離婚】→子連れ再婚したら人生が激変した話')">
                  <img src="https://i.ytimg.com/vi/J7tFe7x3_cs/hqdefault.jpg" alt="動画サムネイル" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                  <div class="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition flex items-center justify-center">
                    <span class="w-12 h-12 rounded-full bg-red-600/90 text-white flex items-center justify-center text-lg shadow-lg group-hover:scale-110 transition">
                      <i class="fa-solid fa-play ml-0.5"></i>
                    </span>
                  </div>
                  <span class="absolute bottom-2 right-2 px-1.5 py-0.5 rounded bg-black/80 text-white text-[10px] font-mono">YouTube</span>
                </div>
                <div class="p-3.5 space-y-2 flex-1 flex flex-col justify-between">
                  <h4 class="text-xs font-bold text-slate-900 line-clamp-2 group-hover:text-red-600 transition">
                    【モラハラ夫と離婚】→子連れ再婚したら人生が激変した話
                  </h4>
                  <div class="flex items-center justify-between pt-2 border-t border-slate-200 text-[11px]">
                    <button onclick="openVideoModal('https://www.youtube.com/embed/J7tFe7x3_cs', '【モラハラ夫と離婚】→子連れ再婚したら人生が激変した話')" class="text-red-600 font-bold hover:underline flex items-center gap-1">
                      <i class="fa-solid fa-circle-play text-[10px]"></i> その場で再生
                    </button>
                    <a href="https://www.youtube.com/watch?v=J7tFe7x3_cs" target="_blank" class="text-slate-400 hover:text-slate-700" title="YouTubeで開く">
                      <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>
                  </div>
                </div>
              </div>

              <!-- Video 5 -->
              <div class="group bg-slate-50 border border-slate-200/80 rounded-2xl overflow-hidden hover:border-red-400 hover:shadow-md transition flex flex-col justify-between">
                <div class="aspect-video relative bg-slate-900 overflow-hidden cursor-pointer" onclick="openVideoModal('https://www.youtube.com/embed/ANth1mJ8YNw', '【我慢の限界突破】ワンオペ地獄｜その家、ブラック家族です')">
                  <img src="https://i.ytimg.com/vi/ANth1mJ8YNw/hqdefault.jpg" alt="動画サムネイル" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                  <div class="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition flex items-center justify-center">
                    <span class="w-12 h-12 rounded-full bg-red-600/90 text-white flex items-center justify-center text-lg shadow-lg group-hover:scale-110 transition">
                      <i class="fa-solid fa-play ml-0.5"></i>
                    </span>
                  </div>
                  <span class="absolute bottom-2 right-2 px-1.5 py-0.5 rounded bg-black/80 text-white text-[10px] font-mono">YouTube</span>
                </div>
                <div class="p-3.5 space-y-2 flex-1 flex flex-col justify-between">
                  <h4 class="text-xs font-bold text-slate-900 line-clamp-2 group-hover:text-red-600 transition">
                    【我慢の限界突破】ワンオペ地獄｜その家、ブラック家族です
                  </h4>
                  <div class="flex items-center justify-between pt-2 border-t border-slate-200 text-[11px]">
                    <button onclick="openVideoModal('https://www.youtube.com/embed/ANth1mJ8YNw', '【我慢の限界突破】ワンオペ地獄｜その家、ブラック家族です')" class="text-red-600 font-bold hover:underline flex items-center gap-1">
                      <i class="fa-solid fa-circle-play text-[10px]"></i> その場で再生
                    </button>
                    <a href="https://www.youtube.com/watch?v=ANth1mJ8YNw" target="_blank" class="text-slate-400 hover:text-slate-700" title="YouTubeで開く">
                      <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>
                  </div>
                </div>
              </div>

              <!-- Video 6 -->
              <div class="group bg-slate-50 border border-slate-200/80 rounded-2xl overflow-hidden hover:border-red-400 hover:shadow-md transition flex flex-col justify-between">
                <div class="aspect-video relative bg-slate-900 overflow-hidden cursor-pointer" onclick="openVideoModal('https://www.youtube.com/embed/fjkadO1_OYs', '【経営者必見】ドブに捨てるお金の使い方と事業拡大するお金の使い方の違い')">
                  <img src="https://i.ytimg.com/vi/fjkadO1_OYs/hqdefault.jpg" alt="動画サムネイル" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                  <div class="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition flex items-center justify-center">
                    <span class="w-12 h-12 rounded-full bg-red-600/90 text-white flex items-center justify-center text-lg shadow-lg group-hover:scale-110 transition">
                      <i class="fa-solid fa-play ml-0.5"></i>
                    </span>
                  </div>
                  <span class="absolute bottom-2 right-2 px-1.5 py-0.5 rounded bg-black/80 text-white text-[10px] font-mono">YouTube</span>
                </div>
                <div class="p-3.5 space-y-2 flex-1 flex flex-col justify-between">
                  <h4 class="text-xs font-bold text-slate-900 line-clamp-2 group-hover:text-red-600 transition">
                    【経営者必見】ドブに捨てるお金の使い方と事業拡大するお金の使い方の違い
                  </h4>
                  <div class="flex items-center justify-between pt-2 border-t border-slate-200 text-[11px]">
                    <button onclick="openVideoModal('https://www.youtube.com/embed/fjkadO1_OYs', '【経営者必見】ドブに捨てるお金の使い方と事業拡大するお金の使い方の違い')" class="text-red-600 font-bold hover:underline flex items-center gap-1">
                      <i class="fa-solid fa-circle-play text-[10px]"></i> その場で再生
                    </button>
                    <a href="https://www.youtube.com/watch?v=fjkadO1_OYs" target="_blank" class="text-slate-400 hover:text-slate-700" title="YouTubeで開く">
                      <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
'''

target_tiktok_section = '        <!-- ==================== 1. 公式TikTok (ぶった斬り会長 @buttagiri888) ==================== -->'
if target_tiktok_section in html:
    html = html.replace(target_tiktok_section, youtube_section_html + '\n\n' + target_tiktok_section)
    print("3-b. YouTube section inserted before TikTok.")

# 4. Hub Card 6 に YouTube の記載追加
hub_card6_title_old = '<span class="text-xs font-bold text-slate-800">OFFICIAL SNS MEDIA</span>'
hub_card6_title_new = '''<i class="fa-brands fa-youtube text-red-600 text-base"></i>
                  <span class="text-xs font-bold text-slate-800">OFFICIAL SNS MEDIA</span>'''

hub_card6_h3_old = '<h3 class="text-lg font-bold text-slate-900 mb-2 group-hover:text-rose-600 transition">\n                公式Instagram & ぶった斬り会長TikTok\n              </h3>'
hub_card6_h3_new = '<h3 class="text-lg font-bold text-slate-900 mb-2 group-hover:text-rose-600 transition">\n                公式YouTube・TikTok・Instagram\n              </h3>'

hub_card6_desc_old = '<p class="text-xs text-slate-600 leading-relaxed mb-4">\n                RAYTUS公式Instagram（活動スナップ・ハイライト）と、大人気のぶった斬り会長公式TikTok（@buttagiri888）をまとめてチェック。\n              </p>'
hub_card6_desc_new = '<p class="text-xs text-slate-600 leading-relaxed mb-4">\n                「ぶった斬りCHANNEL」公式YouTube、TikTok（@buttagiri888）、RAYTUS公式Instagramをワンストップでチェック。\n              </p>'

hub_card6_links_old = '''              <div class="flex items-center gap-2 text-[11px]">
                <a href="https://www.instagram.com/raytus_group.official" target="_blank" class="text-pink-600 hover:underline flex items-center gap-0.5" title="Instagram">
                  <i class="fa-brands fa-instagram"></i>
                </a>
                <span class="text-slate-300">|</span>
                <a href="https://www.tiktok.com/@buttagiri888?_r=1&_t=ZS-9AgCrWXIl6a" target="_blank" class="text-slate-900 hover:underline flex items-center gap-0.5" title="TikTok">
                  <i class="fa-brands fa-tiktok"></i>
                </a>
              </div>'''

hub_card6_links_new = '''              <div class="flex items-center gap-2 text-[11px]">
                <a href="https://www.youtube.com/@buttagirichannel" target="_blank" class="text-red-600 hover:underline flex items-center gap-0.5" title="YouTube">
                  <i class="fa-brands fa-youtube"></i>
                </a>
                <span class="text-slate-300">|</span>
                <a href="https://www.tiktok.com/@buttagiri888?_r=1&_t=ZS-9AgCrWXIl6a" target="_blank" class="text-slate-900 hover:underline flex items-center gap-0.5" title="TikTok">
                  <i class="fa-brands fa-tiktok"></i>
                </a>
                <span class="text-slate-300">|</span>
                <a href="https://www.instagram.com/raytus_group.official" target="_blank" class="text-pink-600 hover:underline flex items-center gap-0.5" title="Instagram">
                  <i class="fa-brands fa-instagram"></i>
                </a>
              </div>'''

if hub_card6_h3_old in html:
    html = html.replace(hub_card6_h3_old, hub_card6_h3_new)
if hub_card6_desc_old in html:
    html = html.replace(hub_card6_desc_old, hub_card6_desc_new)
if hub_card6_links_old in html:
    html = html.replace(hub_card6_links_old, hub_card6_links_new)
print("4. Hub Card 6 updated with YouTube info.")

# 5. setSnsFilter JSの更新
set_sns_filter_old = '''    // SNSフィルター切替
    function setSnsFilter(type) {
      const btnAll = document.getElementById('sns-filter-all');
      const btnInsta = document.getElementById('sns-filter-instagram');
      const btnTiktok = document.getElementById('sns-filter-tiktok');
      const secTiktok = document.getElementById('sns-section-tiktok');
      const secInsta = document.getElementById('sns-section-instagram');

      // リセット
      [btnAll, btnInsta, btnTiktok].forEach(b => {
        b.className = 'px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition flex items-center gap-1';
      });

      if (type === 'all') {
        btnAll.className = 'px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-2xs transition';
        secTiktok.style.display = 'block';
        secInsta.style.display = 'block';
      } else if (type === 'instagram') {
        btnInsta.className = 'px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-2xs transition flex items-center gap-1';
        secTiktok.style.display = 'none';
        secInsta.style.display = 'block';
      } else if (type === 'tiktok') {
        btnTiktok.className = 'px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-2xs transition flex items-center gap-1';
        secTiktok.style.display = 'block';
        secInsta.style.display = 'none';
      }
    }'''

set_sns_filter_new = '''    // SNSフィルター切替
    function setSnsFilter(type) {
      const btnAll = document.getElementById('sns-filter-all');
      const btnYoutube = document.getElementById('sns-filter-youtube');
      const btnTiktok = document.getElementById('sns-filter-tiktok');
      const btnInsta = document.getElementById('sns-filter-instagram');
      const secYoutube = document.getElementById('sns-section-youtube');
      const secTiktok = document.getElementById('sns-section-tiktok');
      const secInsta = document.getElementById('sns-section-instagram');

      // リセット
      [btnAll, btnYoutube, btnTiktok, btnInsta].filter(Boolean).forEach(b => {
        b.className = 'px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition flex items-center gap-1';
      });

      if (type === 'all') {
        if (btnAll) btnAll.className = 'px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-2xs transition';
        if (secYoutube) secYoutube.style.display = 'block';
        if (secTiktok) secTiktok.style.display = 'block';
        if (secInsta) secInsta.style.display = 'block';
      } else if (type === 'youtube') {
        if (btnYoutube) btnYoutube.className = 'px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-2xs transition flex items-center gap-1';
        if (secYoutube) secYoutube.style.display = 'block';
        if (secTiktok) secTiktok.style.display = 'none';
        if (secInsta) secInsta.style.display = 'none';
      } else if (type === 'tiktok') {
        if (btnTiktok) btnTiktok.className = 'px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-2xs transition flex items-center gap-1';
        if (secYoutube) secYoutube.style.display = 'none';
        if (secTiktok) secTiktok.style.display = 'block';
        if (secInsta) secInsta.style.display = 'none';
      } else if (type === 'instagram') {
        if (btnInsta) btnInsta.className = 'px-3 py-1.5 rounded-lg bg-white text-slate-900 shadow-2xs transition flex items-center gap-1';
        if (secYoutube) secYoutube.style.display = 'none';
        if (secTiktok) secTiktok.style.display = 'none';
        if (secInsta) secInsta.style.display = 'block';
      }
    }'''

if set_sns_filter_old in html:
    html = html.replace(set_sns_filter_old, set_sns_filter_new)
    print("5. setSnsFilter JS updated.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Part 1 complete! Saved index.html.")

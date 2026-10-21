# -*- coding: utf-8 -*-
import sys

new_raytus_tab_html = '''    <!-- ======================================================== -->
    <!-- TAB 2: RAYTUS group 公式HP & 全事業紹介・アーカイブ (RAYTUS) -->
    <!-- ======================================================== -->
    <div id="tab-content-raytus" class="tab-content space-y-12">
      
      <!-- RAYTUS 公式ページ コンテナ（本家の公式Webデザイン・世界観を完全再現） -->
      <div class="bg-[#0b0f17] text-white rounded-3xl overflow-hidden border border-slate-800 shadow-2xl relative font-zen">
        
        <!-- ============================================== -->
        <!-- 本家トップ ヒーローセクション（動画背景＋縦書き＋下線ナビ） -->
        <!-- ============================================== -->
        <div class="relative min-h-[580px] lg:min-h-[640px] flex flex-col justify-between p-6 sm:p-10 lg:p-14 overflow-hidden bg-gradient-to-r from-[#0b0f17] via-[#0f172a] to-[#0b0f17]">
          
          <!-- 右側シネマティック背景動画 (本家公式動画) -->
          <div class="absolute right-0 top-0 bottom-0 w-full lg:w-1/2 overflow-hidden pointer-events-none z-0">
            <video class="w-full h-full object-cover opacity-30 lg:opacity-60" playsinline loop autoplay muted src="https://raytus-group.com/wp-content/themes/raytus-theme/video/1130-2.mp4" poster="images/banners-raytus-terakoya.jpg"></video>
            <!-- グラデーションオーバーレイ -->
            <div class="absolute inset-0 bg-gradient-to-r from-[#0b0f17] via-[#0b0f17]/80 to-transparent"></div>
            <div class="absolute inset-0 bg-gradient-to-t from-[#0b0f17] via-transparent to-[#0b0f17]/40"></div>
          </div>

          <!-- 右上 本家固定リンクバー (INSTAGRAM & CONTACT) -->
          <div class="relative z-20 flex justify-end items-center gap-3 mb-6">
            <a href="https://www.instagram.com/raytus_group.official" target="_blank" class="px-5 py-2 rounded-full bg-slate-900/90 hover:bg-black text-white font-zen text-xs tracking-widest border border-slate-700/80 hover:border-amber-400 transition flex items-center gap-2 shadow-lg">
              <i class="fa-brands fa-instagram text-amber-400"></i>
              <span>INSTAGRAM</span>
            </a>
            <a href="https://raytus-group.com/contact/" target="_blank" class="px-5 py-2 rounded-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-zen font-bold text-xs tracking-widest transition shadow-lg shadow-amber-500/20">
              CONTACT
            </a>
          </div>

          <!-- メインコンテンツ（左側ナビ ＆ 中央縦書きコピー） -->
          <div class="relative z-20 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center my-auto">
            
            <!-- 左側: 公式ロゴ & 本家ナビゲーションリスト (7項目) -->
            <div class="lg:col-span-7 space-y-6">
              
              <!-- 公式ロゴ -->
              <div class="max-w-[280px] sm:max-w-[320px]">
                <img src="images/raytus_logo.png" alt="RAYTUS Logo" class="w-full object-contain filter drop-shadow-[0_4px_12px_rgba(0,0,0,0.8)]">
              </div>

              <!-- 本家公式スタイルの下線付きナビゲーション -->
              <nav class="max-w-md space-y-1.5 pt-2">
                <a onclick="scrollToSection('raytus-about-section')" class="raytus-nav-link group">
                  <span class="raytus-nav-en text-white group-hover:text-amber-300">ABOUT</span>
                  <span class="raytus-nav-ja text-slate-400 group-hover:text-amber-200">企業情報</span>
                </a>
                <a onclick="scrollToSection('raytus-services-section')" class="raytus-nav-link group">
                  <span class="raytus-nav-en text-white group-hover:text-amber-300">SERVICE</span>
                  <span class="raytus-nav-ja text-slate-400 group-hover:text-amber-200">事業内容（31事業 & 動画）</span>
                </a>
                <a onclick="scrollToSection('raytus-community-section')" class="raytus-nav-link group">
                  <span class="raytus-nav-en text-white group-hover:text-amber-300">COMMUNITY</span>
                  <span class="raytus-nav-ja text-slate-400 group-hover:text-amber-200">グループコミュニティ</span>
                </a>
                <a onclick="switchTab('iyasaka')" class="raytus-nav-link group" title="Iyasaka宮の加盟店・ショップへ">
                  <span class="raytus-nav-en text-white group-hover:text-amber-300">SHOP</span>
                  <span class="raytus-nav-ja text-slate-400 group-hover:text-amber-200">加盟店紹介（Iyasaka宮）</span>
                </a>
                <a href="https://raytus-group.com/news/" target="_blank" class="raytus-nav-link group">
                  <span class="raytus-nav-en text-white group-hover:text-amber-300">NEWS RELEASE</span>
                  <span class="raytus-nav-ja text-slate-400 group-hover:text-amber-200">お知らせ <i class="fa-solid fa-arrow-up-right-from-square text-[10px] ml-1"></i></span>
                </a>
                <a href="https://raytus-group.com/blog/" target="_blank" class="raytus-nav-link group">
                  <span class="raytus-nav-en text-white group-hover:text-amber-300">BLOG</span>
                  <span class="raytus-nav-ja text-slate-400 group-hover:text-amber-200">ブログ <i class="fa-solid fa-arrow-up-right-from-square text-[10px] ml-1"></i></span>
                </a>
                <a href="https://www.instagram.com/raytus_group.official" target="_blank" class="raytus-nav-link group">
                  <span class="raytus-nav-en text-white group-hover:text-amber-300">INSTAGRAM</span>
                  <span class="raytus-nav-ja text-slate-400 group-hover:text-amber-200">インスタグラム <i class="fa-solid fa-arrow-up-right-from-square text-[10px] ml-1"></i></span>
                </a>
              </nav>

              <!-- 本家公式 2大プロジェクトバナー -->
              <div class="pt-3 max-w-lg grid grid-cols-1 sm:grid-cols-2 gap-3">
                <a href="https://raytus-group.com/news/2026/10/08/terakoya-open-hofu-2027/" target="_blank" class="group block rounded-xl overflow-hidden border border-slate-700/80 hover:border-amber-400 transition shadow-lg bg-slate-900/60">
                  <img src="images/banners-raytus-terakoya.jpg" alt="寺子屋プロジェクト" class="w-full h-auto object-cover group-hover:opacity-85 transition">
                </a>
                <a href="https://raytus-group.com/news/2026/10/08/basta-school-building-construction-project/" target="_blank" class="group block rounded-xl overflow-hidden border border-slate-700/80 hover:border-amber-400 transition shadow-lg bg-slate-900/60">
                  <img src="images/banners-raytus-basta.jpg" alt="バスタ高校 新校舎建設プロジェクト" class="w-full h-auto object-cover group-hover:opacity-85 transition">
                </a>
              </div>

            </div>

            <!-- 右側: 本家そのままの縦書きメインテキスト -->
            <div class="lg:col-span-5 flex justify-center lg:justify-end py-6 lg:py-0">
              <div class="raytus-vertical-text text-xl sm:text-2xl lg:text-3xl font-light text-slate-100 select-none py-6 px-8 rounded-2xl bg-black/40 backdrop-blur-sm border border-white/10 shadow-2xl">
                <p class="tracking-widest">あなたの人生に</p>
                <p class="mt-4 tracking-widest"><span class="text-amber-300 font-normal">光（RAY）</span>を<span class="text-amber-300 font-normal">足す（TUS）</span>。</p>
                <p class="mt-6 text-xs text-slate-400 tracking-normal font-sans" style="writing-mode: horizontal-tb;">仲間の未来の夢をプロデュースするコミュニティ RAYTUS group.</p>
              </div>
            </div>

          </div>

        </div>

        <!-- ============================================== -->
        <!-- SERVICE セクション（本家デザイン完全再現 ＋ 31事業・動画アーカイブ） -->
        <!-- ============================================== -->
        <div id="raytus-services-section" class="p-6 sm:p-10 lg:p-14 border-t border-slate-800 bg-[#0d1118]">
          
          <!-- 本家 sec-head 見出し -->
          <div class="raytus-sec-head">
            <p class="raytus-sec-head__en">SERVICE</p>
            <h3 class="raytus-sec-head__ja">事業内容</h3>
          </div>

          <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-8">
            <p class="text-xs sm:text-sm text-slate-400 font-serif leading-relaxed">
              ※事業名を押すと詳しい内容をご覧いただけます。<br class="hidden sm:inline">
              Notion公式に収録された紹介動画（YouTube）もその場で再生・確認できます。
            </p>
            
            <!-- 検索入力 -->
            <div class="relative w-full md:w-80 shrink-0">
              <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 text-xs"></i>
              <input type="text" id="raytus-service-search" oninput="filterRaytusServices()" placeholder="事業名・責任者・キーワード検索..." class="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-amber-400 transition">
            </div>
          </div>

          <!-- カテゴリ分類 切り替えピルバー (5大グループ) -->
          <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-3 mb-8 text-xs font-bold">
            <button onclick="setRaytusCategory('all')" id="raytus-cat-all" class="raytus-cat-btn px-4 py-2 rounded-xl transition bg-amber-400 text-slate-950 shadow-md whitespace-nowrap font-zen">
              🌟 すべて表示 (<span id="count-all">31</span>)
            </button>
            <button onclick="setRaytusCategory('care')" id="raytus-cat-care" class="raytus-cat-btn px-4 py-2 rounded-xl transition bg-slate-900 text-slate-300 hover:text-white border border-slate-800 hover:border-slate-700 whitespace-nowrap font-zen">
              👶 子育て・女性・ファミリー (<span id="count-care">5</span>)
            </button>
            <button onclick="setRaytusCategory('food')" id="raytus-cat-food" class="raytus-cat-btn px-4 py-2 rounded-xl transition bg-slate-900 text-slate-300 hover:text-white border border-slate-800 hover:border-slate-700 whitespace-nowrap font-zen">
              🍙 食・農業・ウェルネス (<span id="count-food">4</span>)
            </button>
            <button onclick="setRaytusCategory('beauty')" id="raytus-cat-beauty" class="raytus-cat-btn px-4 py-2 rounded-xl transition bg-slate-900 text-slate-300 hover:text-white border border-slate-800 hover:border-slate-700 whitespace-nowrap font-zen">
              💄 美容・ジュエリー・フェムケア (<span id="count-beauty">5</span>)
            </button>
            <button onclick="setRaytusCategory('life')" id="raytus-cat-life" class="raytus-cat-btn px-4 py-2 rounded-xl transition bg-slate-900 text-slate-300 hover:text-white border border-slate-800 hover:border-slate-700 whitespace-nowrap font-zen">
              🤝 暮らし・シニア・パートナー (<span id="count-life">7</span>)
            </button>
            <button onclick="setRaytusCategory('business')" id="raytus-cat-business" class="raytus-cat-btn px-4 py-2 rounded-xl transition bg-slate-900 text-slate-300 hover:text-white border border-slate-800 hover:border-slate-700 whitespace-nowrap font-zen">
              💼 ビジネス・事務・クリエイティブ (<span id="count-business">10</span>)
            </button>
          </div>

          <!-- 事業カード グリッド（JavaScriptで動的生成：本家 sec-service__list-item 仕様） -->
          <div id="raytus-services-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- Injected via renderRaytusServices() -->
          </div>

          <!-- 0件ヒット時のプレースホルダー -->
          <div id="raytus-no-results" class="hidden py-16 text-center border border-slate-800 rounded-3xl bg-slate-900/50">
            <i class="fa-solid fa-shapes text-3xl text-slate-600 mb-3"></i>
            <h4 class="text-sm font-bold text-slate-300 font-zen">該当する事業が見つかりませんでした</h4>
            <p class="text-xs text-slate-500 mt-1 font-zen">検索条件を変更するか、カテゴリーを「すべて表示」に戻してください。</p>
            <button onclick="setRaytusCategory('all'); document.getElementById('raytus-service-search').value = ''; filterRaytusServices();" class="mt-4 px-4 py-2 rounded-xl bg-amber-400 text-slate-950 text-xs font-bold font-zen">
              条件をリセット
            </button>
          </div>

        </div>

        <!-- ============================================== -->
        <!-- ABOUT セクション（本家デザイン完全再現：理念・代表挨拶・概要） -->
        <!-- ============================================== -->
        <div id="raytus-about-section" class="p-6 sm:p-10 lg:p-14 border-t border-slate-800 bg-[#0b0f17]">
          
          <!-- 本家 sec-head 見出し -->
          <div class="raytus-sec-head">
            <p class="raytus-sec-head__en">ABOUT</p>
            <h3 class="raytus-sec-head__ja">私たちの思い</h3>
          </div>

          <!-- 本家 sec-vision 文面 -->
          <div class="max-w-4xl mx-auto my-12 text-center space-y-6">
            <p class="text-base sm:text-lg text-slate-200 font-zen leading-loose">
              一人ひとりの心に秘めた想いや才能を最短で引き出し、<br class="hidden sm:inline">
              あなたのセカンドキャリアをプロデュースいたします。
            </p>
            <p class="text-base sm:text-lg text-slate-200 font-zen leading-loose">
              古き良き時代(アナログ)を大切に、実業は最先端(デジタル)を活用し、<br class="hidden sm:inline">
              活動支援、経済的自立、社会貢献を実現します。
            </p>
            <p class="text-base sm:text-lg text-slate-200 font-zen leading-loose">
              あなたの人生に、<span class="text-amber-300 font-bold">光(RAY)</span>を<span class="text-amber-300 font-bold">足す(TUS)</span>。その光で世界を照らし輝かす。<br class="hidden sm:inline">
              そんな想いで活動する団体です。
            </p>
            <div class="pt-6 flex justify-center">
              <img src="images/raytus_logo.png" alt="RAYTUS ロゴ" class="h-10 opacity-70">
            </div>
          </div>

          <!-- 代表挨拶ブロック（本家 sec-about 完全再現） -->
          <div class="max-w-5xl mx-auto my-16 bg-[#121824] rounded-3xl p-6 sm:p-10 lg:p-12 border border-slate-800 shadow-xl">
            <div class="text-left mb-8 border-b border-slate-800 pb-4">
              <span class="text-xs font-zen font-bold tracking-widest text-amber-400 uppercase">MESSAGE</span>
              <h4 class="text-2xl sm:text-3xl font-zen font-bold text-white mt-1">代表挨拶</h4>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-12 gap-8 lg:gap-12 items-start">
              <!-- 代表写真 -->
              <div class="md:col-span-5 flex flex-col items-center">
                <div class="rounded-2xl overflow-hidden border border-slate-700/80 shadow-2xl max-w-sm w-full bg-slate-900">
                  <img src="images/kusanagi_face.jpg" onerror="this.src='https://raytus-group.com/wp-content/themes/raytus-theme/image/about-image.jpg'" alt="RAYTUS group.代表 草彅亜希" class="w-full h-auto object-cover">
                </div>
                <div class="mt-4 text-center">
                  <p class="text-xs text-slate-400 font-zen">RAYTUS group. 代表理事 / 国連IDIO-DEVNET 理事</p>
                  <p class="text-lg font-zen font-bold text-white mt-0.5 tracking-wider">草彅 亜希 <span class="text-xs text-amber-300 font-normal">Aki Kusanagi</span></p>
                </div>
              </div>

              <!-- 代表メッセージ本文 -->
              <div class="md:col-span-7 space-y-4 text-sm font-zen leading-relaxed text-slate-300">
                <h5 class="text-lg sm:text-xl font-bold text-amber-300 font-zen pb-2">
                  あなたの輝く人生のお手伝い
                </h5>
                <p>
                  長く美容業界に勤めてきましたが、美しさとは、外見だけにとらわれない健康や心のあり方が大切だという信念を持ちました。<br>
                  <strong class="text-white">輝く人生を描いて欲しい。</strong>
                </p>
                <p>
                  私自身女性として、結婚や出産など、そのときのステージで制限がついたり諦めることもあり、そんな経験から、いくつからでも可能性は無限大、人生はどこからでも意思ひとつでリスタートできるのだと、チャレンジ精神に溢れた明るく前向きな人生を描く方を増やしたい思いで起業しました。
                </p>
                <p>
                  皆さまの事業に、人生に、彩りと輝きを足していただけるよう、精一杯活動いたします。
                </p>
                
                <div class="pt-4 border-t border-slate-800 text-right">
                  <p class="text-xs text-slate-400">RAYTUS group.代表理事 国連IDIO-DEVNET 理事</p>
                  <p class="text-xl font-serif tracking-widest text-white mt-1">Aki <span class="text-amber-400 font-normal">K</span>usanagi</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 企業概要（本家 sec-overview 完全再現） -->
          <div class="max-w-4xl mx-auto my-12">
            <h4 class="text-xl font-zen font-bold text-white mb-6 pl-3 border-l-4 border-amber-400">企業概要</h4>
            <div class="bg-[#121824] rounded-2xl border border-slate-800 overflow-hidden text-xs sm:text-sm font-zen">
              <dl class="divide-y divide-slate-800">
                <div class="p-4 sm:grid sm:grid-cols-3 sm:gap-4 bg-slate-900/40">
                  <dt class="font-bold text-amber-300">コミュニティ名</dt>
                  <dd class="mt-1 sm:mt-0 sm:col-span-2 text-white">RAYTUS group.</dd>
                </div>
                <div class="p-4 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="font-bold text-amber-300">設立</dt>
                  <dd class="mt-1 sm:mt-0 sm:col-span-2 text-slate-300">2022年3月24日</dd>
                </div>
                <div class="p-4 sm:grid sm:grid-cols-3 sm:gap-4 bg-slate-900/40">
                  <dt class="font-bold text-amber-300">代表</dt>
                  <dd class="mt-1 sm:mt-0 sm:col-span-2 text-white">草彅 亜希</dd>
                </div>
                <div class="p-4 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="font-bold text-amber-300">事業内容</dt>
                  <dd class="mt-1 sm:mt-0 sm:col-span-2 text-slate-300 space-y-1">
                    <p>1. コミュニティ運営</p>
                    <p>2. コミュニティサイト、EC（電子商取引）サイト、ウェブサイトの企画、制作ならびに運営</p>
                    <p>3. 各種イベント、講習会、セミナー、研修会等の企画、制作ならびに実施 他</p>
                  </dd>
                </div>
                <div class="p-4 sm:grid sm:grid-cols-3 sm:gap-4 bg-slate-900/40">
                  <dt class="font-bold text-amber-300">関連会社</dt>
                  <dd class="mt-1 sm:mt-0 sm:col-span-2 text-slate-300">株式会社K-pays holdings</dd>
                </div>
                <div class="p-4 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="font-bold text-amber-300">公式URL</dt>
                  <dd class="mt-1 sm:mt-0 sm:col-span-2 text-slate-300">
                    <a href="https://raytus-group.com" target="_blank" class="text-amber-400 hover:underline flex items-center gap-1">
                      <span>https://raytus-group.com</span>
                      <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>
                  </dd>
                </div>
              </dl>
            </div>
          </div>

        </div>

        <!-- ============================================== -->
        <!-- COMMUNITY セクション（本家デザイン完全再現：グループコミュニティ一覧） -->
        <!-- ============================================== -->
        <div id="raytus-community-section" class="p-6 sm:p-10 lg:p-14 border-t border-slate-800 bg-[#0d1118]">
          
          <!-- 本家 sec-head 見出し -->
          <div class="raytus-sec-head">
            <p class="raytus-sec-head__en">COMMUNITY</p>
            <h3 class="raytus-sec-head__ja">グループコミュニティ</h3>
          </div>

          <p class="text-xs sm:text-sm text-slate-400 font-serif leading-relaxed mb-8">
            一人ひとりの才能や個性を最短で引き出し、セカンドキャリアを伴走するRAYTUSの多彩なチーム。
          </p>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 font-zen">
            
            <!-- Community 1: RAYTUS -->
            <div class="bg-[#141822] rounded-2xl p-6 border border-slate-800 hover:border-amber-400/60 transition shadow-lg flex flex-col justify-between">
              <div>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-bold">母体・理念</span>
                <h4 class="text-xl font-bold text-white mt-2">RAYTUS</h4>
                <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                  一人ひとりの心に秘めた想いや才能を最短で引き出し、セカンドキャリアをプロデュース。古き良き時代のアナログを大切に、最先端デジタルを活用して経済的自立と社会貢献を実現します。
                </p>
              </div>
              <div class="mt-4 pt-4 border-t border-slate-800 text-xs text-slate-400">
                <span>理事長: <strong class="text-white">草彅 亜希</strong></span>
              </div>
            </div>

            <!-- Community 2: enchant+ -->
            <div class="bg-[#141822] rounded-2xl p-6 border border-slate-800 hover:border-amber-400/60 transition shadow-lg flex flex-col justify-between">
              <div>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-purple-500/20 text-purple-300 font-bold">クリエイティブ</span>
                <h4 class="text-xl font-bold text-white mt-2">enchant+ (アンシャンテ)</h4>
                <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                  「能力を付与する」、そしてフランス語で「出会ってくれてありがとう」。人を喜ばせ、魔法のように人々を魅了し続けていく共創チームです。
                </p>
              </div>
              <div class="mt-4 pt-4 border-t border-slate-800 text-xs text-slate-400">
                <span>代表: <strong class="text-white">川野 弥生</strong></span>
              </div>
            </div>

            <!-- Community 3: yuima-ru -->
            <div class="bg-[#141822] rounded-2xl p-6 border border-slate-800 hover:border-amber-400/60 transition shadow-lg flex flex-col justify-between">
              <div>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-bold">共育・助け合い</span>
                <h4 class="text-xl font-bold text-white mt-2">yuima-ru (ゆいまーる)</h4>
                <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                  沖縄の方言「結い（協働・助け合い）」から名付けられたチーム。教育・共育・暮らしの中で互いに支え合い、誰もが居場所を持てる温かい連帯を創ります。
                </p>
              </div>
              <div class="mt-4 pt-4 border-t border-slate-800 text-xs text-slate-400">
                <span>理事長: <strong class="text-white">畑 ゆかり</strong></span>
              </div>
            </div>

            <!-- Community 4: MAARUKU -->
            <div class="bg-[#141822] rounded-2xl p-6 border border-slate-800 hover:border-amber-400/60 transition shadow-lg flex flex-col justify-between">
              <div>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-300 font-bold">調和・円満</span>
                <h4 class="text-xl font-bold text-white mt-2">MAARUKU (まあるく)</h4>
                <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                  角を立てず、すべての人が丸く円満に繋がり合えるコミュニティ。互いの個性を認め合い、心地よい循環を生み出す場を提供します。
                </p>
              </div>
              <div class="mt-4 pt-4 border-t border-slate-800 text-xs text-slate-400">
                <span>代表: <strong class="text-white">MAARUKU 運営チーム</strong></span>
              </div>
            </div>

            <!-- Community 5: Couleur -->
            <div class="bg-[#141822] rounded-2xl p-6 border border-slate-800 hover:border-amber-400/60 transition shadow-lg flex flex-col justify-between">
              <div>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-rose-500/20 text-rose-300 font-bold">彩り・個性</span>
                <h4 class="text-xl font-bold text-white mt-2">Couleur (クルール)</h4>
                <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                  フランス語で「彩り・色」。一人ひとりが自分だけの色（魅力）を発揮し、カラフルに世界を彩っていく女性・起業家コミュニティです。
                </p>
              </div>
              <div class="mt-4 pt-4 border-t border-slate-800 text-xs text-slate-400">
                <span>代表: <strong class="text-white">Couleur 運営チーム</strong></span>
              </div>
            </div>

            <!-- Community 6: Mimola -->
            <div class="bg-[#141822] rounded-2xl p-6 border border-slate-800 hover:border-amber-400/60 transition shadow-lg flex flex-col justify-between">
              <div>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-bold">サロン・ウェルネス</span>
                <h4 class="text-xl font-bold text-white mt-2">Mimola (ミモラ)</h4>
                <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                  サロン運営やセラピストたちが知恵と技術を持ち寄り、学びと実践を深めるチーム。心身の美と癒やしを社会に届けています。
                </p>
              </div>
              <div class="mt-4 pt-4 border-t border-slate-800 text-xs text-slate-400">
                <span>代表: <strong class="text-white">Mimola 運営チーム</strong></span>
              </div>
            </div>

          </div>

        </div>

        <!-- ============================================== -->
        <!-- PROJECTS セクション（本家デザイン完全再現：公式プロジェクト） -->
        <!-- ============================================== -->
        <div id="raytus-projects-section" class="p-6 sm:p-10 lg:p-14 border-t border-slate-800 bg-[#0b0f17]">
          
          <!-- 本家 sec-head 見出し -->
          <div class="raytus-sec-head">
            <p class="raytus-sec-head__en">PROJECTS</p>
            <h3 class="raytus-sec-head__ja">次世代育成・未来創造プロジェクト</h3>
          </div>

          <p class="text-xs sm:text-sm text-slate-400 font-serif leading-relaxed mb-8">
            RAYTUS groupが全力で取り組む注目の教育・社会支援プロジェクト
          </p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 font-zen">
            <!-- Project 1 -->
            <div class="bg-[#121824] border border-slate-800 rounded-3xl overflow-hidden p-6 sm:p-8 flex flex-col justify-between group hover:border-amber-400/60 transition shadow-xl">
              <div>
                <img src="images/banners-raytus-terakoya.jpg" alt="寺子屋プロジェクト" class="w-full h-52 object-cover rounded-2xl mb-5 group-hover:scale-[1.02] transition duration-300">
                <span class="text-[10px] px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 font-bold">2027年開校予定</span>
                <h4 class="text-xl font-bold text-white mt-3 group-hover:text-amber-300 transition">寺子屋プロジェクト 防府開校 2027</h4>
                <p class="text-xs sm:text-sm text-slate-300 mt-3 leading-relaxed">
                  子供たちが自分の「好き」や「得意」を伸ばし、社会で生き抜く力を育む新たな学びの場。地域社会と連携しながら、山口県防府市に2027年開校を目指して建設・準備が進められています。
                </p>
              </div>
              <div class="mt-8 pt-4 border-t border-slate-800 flex items-center justify-between">
                <a href="https://raytus-group.com/news/2026/10/08/terakoya-open-hofu-2027/" target="_blank" class="text-xs font-bold text-amber-300 hover:text-amber-200 flex items-center gap-1.5">
                  <span>詳細プロジェクト記事を見る</span>
                  <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
                <span class="text-xs text-slate-500">山口県防府市</span>
              </div>
            </div>

            <!-- Project 2 -->
            <div class="bg-[#121824] border border-slate-800 rounded-3xl overflow-hidden p-6 sm:p-8 flex flex-col justify-between group hover:border-blue-400/60 transition shadow-xl">
              <div>
                <img src="images/banners-raytus-basta.jpg" alt="バスタ高校" class="w-full h-52 object-cover rounded-2xl mb-5 group-hover:scale-[1.02] transition duration-300">
                <span class="text-[10px] px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 font-bold">新校舎建設</span>
                <h4 class="text-xl font-bold text-white mt-3 group-hover:text-blue-300 transition">バスタ高校 新校舎建設プロジェクト</h4>
                <p class="text-xs sm:text-sm text-slate-300 mt-3 leading-relaxed">
                  従来の教育の枠にとらわれず、生徒一人ひとりの個性を最大限に生かし自立を支援する学校創り。次世代のリーダーやクリエイターが育つ拠点として新校舎の建設が進んでいます。
                </p>
              </div>
              <div class="mt-8 pt-4 border-t border-slate-800 flex items-center justify-between">
                <a href="https://raytus-group.com/news/2026/10/08/basta-school-building-construction-project/" target="_blank" class="text-xs font-bold text-blue-300 hover:text-blue-200 flex items-center gap-1.5">
                  <span>新校舎建設ニュースを見る</span>
                  <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
                <span class="text-xs text-slate-500">学校創造プロジェクト</span>
              </div>
            </div>
          </div>

        </div>

        <!-- 本家フッター -->
        <div class="p-6 sm:p-8 border-t border-slate-800/80 text-center text-xs text-slate-500 font-zen flex items-center justify-between flex-wrap gap-4 bg-[#080b11]">
          <span>COPYRIGHT. RAYTUS® group. ALL RIGHTS RESERVED.</span>
          <div class="flex items-center gap-6">
            <a href="https://raytus-group.com" target="_blank" class="text-slate-400 hover:text-white transition">raytus-group.com</a>
            <a href="https://raytus-group.com/privacy-policy/" target="_blank" class="text-slate-400 hover:text-white transition">プライバシーポリシー</a>
          </div>
        </div>

      </div>
    </div>
'''

new_card_template = '''      container.innerHTML = filtered.map(item => {
        const originalIndex = RAYTUS_SERVICES.indexOf(item);
        const catLabel = CATEGORY_NAMES[item.category] || '事業';
        const catColor = CATEGORY_COLORS[item.category] || 'bg-slate-800 text-slate-300';
        const hasVideo = !!item.videoId;

        return `
          <div onclick="openRaytusServiceModal(${originalIndex})" class="raytus-card-item group" style="background-image: url('${item.bgImage}');">
            <div class="raytus-card-overlay"></div>
            
            <div class="relative z-10 p-5 sm:p-6 h-full flex flex-col justify-between">
              
              <!-- 上部バッジエリア -->
              <div class="flex items-center justify-between gap-2">
                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold ${catColor}">
                  ${catLabel}
                </span>

                ${hasVideo ? `
                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-600/90 text-white flex items-center gap-1 shadow-md backdrop-blur-xs">
                  <i class="fa-brands fa-youtube"></i> 公式動画あり
                </span>
                ` : `
                <span class="text-[10px] text-slate-400 font-zen">事業詳細</span>
                `}
              </div>

              <!-- 中央〜下部テキスト（本家 sec-service__list-item 完全準拠） -->
              <div class="mt-10">
                <p class="business-name text-[11px] sm:text-xs font-zen text-amber-300/95 tracking-widest font-semibold mb-1">
                  ${item.businessName}
                </p>
                
                <h4 class="company-name text-lg sm:text-xl font-zen font-bold text-white group-hover:text-amber-300 transition duration-300">
                  ${item.companyName}
                </h4>

                <p class="tagline text-xs text-slate-300/90 font-zen mt-2 line-clamp-2 leading-relaxed">
                  ${item.tagline.replace(/\\n/g, ' ')}
                </p>
                
                <div class="mt-3 pt-3 border-t border-white/10 flex items-center justify-between text-xs text-slate-400 font-zen">
                  <span>責任者: <strong class="text-white">${item.manager}</strong></span>
                  <span class="text-amber-300 group-hover:translate-x-1 transition font-bold flex items-center gap-1">
                    <span>詳細を見る</span>
                    <i class="fa-solid fa-arrow-right text-[10px]"></i>
                  </span>
                </div>
              </div>

            </div>
          </div>
        `;
      }).join('');'''

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace tab-content-raytus
    start_marker = "<!-- ======================================================== -->\\n    <!-- TAB 2: RAYTUS group 公式HP & 全事業紹介・アーカイブ (RAYTUS) -->"
    end_marker = "<!-- ======================================================== -->\\n    <!-- TAB 3: Iyasaka宮 コミュニティ & EC 複製 (IYASAKA) -->"
    
    # Try finding markers with various line endings
    s_idx = content.find("<!-- TAB 2: RAYTUS group 公式HP & 全事業紹介・アーカイブ (RAYTUS) -->")
    e_idx = content.find("<!-- TAB 3: Iyasaka宮 コミュニティ & EC 複製 (IYASAKA) -->")
    
    if s_idx == -1 or e_idx == -1:
        print(f"Error: Markers not found in {filename} (s_idx={s_idx}, e_idx={e_idx})")
        return False
        
    # Find preceding line break for s_idx
    line_start = content.rfind("\n", 0, s_idx)
    # Check if there is another line before for the divider comment
    div_idx = content.rfind("<!-- ======================================================== -->", 0, s_idx)
    if div_idx != -1 and div_idx > line_start - 100:
        actual_start = content.rfind("\n", 0, div_idx) + 1
    else:
        actual_start = line_start + 1

    # End position: before the divider of TAB 3
    div3_idx = content.rfind("<!-- ======================================================== -->", 0, e_idx)
    if div3_idx != -1:
        actual_end = content.rfind("\n", 0, div3_idx) + 1
    else:
        actual_end = content.rfind("\n", 0, e_idx) + 1

    content = content[:actual_start] + new_raytus_tab_html + "\n\n\n    " + content[actual_end:]

    # 2. Replace renderRaytusServices card block
    card_start = "container.innerHTML = filtered.map(item => {"
    card_end = "}).join('');"
    
    cs_idx = content.find(card_start)
    if cs_idx != -1:
        ce_idx = content.find(card_end, cs_idx)
        if ce_idx != -1:
            full_card_old = content[cs_idx : ce_idx + len(card_end)]
            content = content[:cs_idx] + new_card_template + content[ce_idx + len(card_end):]
            print(f"Successfully replaced card template in {filename}")
        else:
            print(f"Warning: card_end not found in {filename}")
    else:
        print(f"Warning: card_start not found in {filename}")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated {filename} successfully.")
    return True

update_file("index.html")
update_file("portal.html")

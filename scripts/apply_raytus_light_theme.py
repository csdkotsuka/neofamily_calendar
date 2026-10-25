#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update RAYTUS section to:
1. Simplify 目次 (Table of Contents) by removing:
   - 私たちの思い (ABOUT)
   - お知らせ (NEWS)
   - 公式ブログ・レポート (BLOG)
   - INSTAGRAM
   Keeping only the essential sections: SERVICE, COMMUNITY, PROJECTS, SHOP.
2. Remove the unwanted sections from the page body (私たちの思い, お知らせ, 公式ブログ・レポート).
3. Redesign the entire RAYTUS section with clean light theme (bg-white, elegant borders, amber accents)
   matching calendar.html, caravan.html, flowchart.html, and index.html.
"""

import re

def update_css():
    with open('css/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # Replace .raytus-sec-head rules
    old_sec_head = re.search(r'/\* 本家セクション見出し \(\.sec-head\) \*/.*?\.raytus-card-item \{', css, re.DOTALL)
    if old_sec_head:
        new_sec_head = '''/* 本家セクション見出し (.sec-head) - 明るい洗練されたライトテーマ */
.raytus-sec-head {
  position: relative;
  padding-top: 36px;
  margin-bottom: 24px;
}
.raytus-sec-head__en {
  position: absolute;
  top: 0;
  left: 4px;
  color: rgba(148, 163, 184, 0.18);
  font-family: "Zen Old Mincho", serif;
  font-size: clamp(2.4rem, 6vw, 4.2rem);
  font-weight: 900;
  letter-spacing: 0.15em;
  line-height: 1;
  pointer-events: none;
  z-index: 1;
  user-select: none;
}
.raytus-sec-head__ja {
  position: relative;
  z-index: 2;
  background: linear-gradient(90deg, #fef3c7, #ffffff);
  border-left: 4px solid #f59e0b;
  border-top: 1px solid rgba(251, 191, 36, 0.3);
  border-right: 1px solid rgba(251, 191, 36, 0.3);
  border-bottom: 1px solid rgba(251, 191, 36, 0.3);
  width: fit-content;
  max-width: 90%;
  padding: 8px 20px;
  text-align: left;
  font-family: "Zen Old Mincho", serif;
  font-size: clamp(1.1rem, 2.2vw, 1.4rem);
  font-weight: 700;
  color: #0f172a;
  box-shadow: 0 4px 12px -2px rgba(245, 158, 11, 0.12);
  border-radius: 0 12px 12px 0;
}

/* 本家事業カード (.sec-service__list-item) */
.raytus-card-item {'''
        css = css.replace(old_sec_head.group(0), new_sec_head)
        with open('css/style.css', 'w', encoding='utf-8') as f:
            f.write(css)
        print("Updated css/style.css")

def get_new_raytus_tab_html():
    return '''    <!-- ======================================================== -->
    <!-- TAB 2: RAYTUS group 全31事業紹介 & データベース（ライトテーマ統一） -->
    <!-- ======================================================== -->
    <div id="tab-content-raytus" class="tab-content active space-y-8">

      <div class="relative">

        <!-- ============================================== -->
        <!-- RAYTUS トップヒーロー ＆ 目次（クイックジャンプ） -->
        <!-- ============================================== -->
        <div id="raytus-hero-section" class="relative bg-white/95 backdrop-blur-md rounded-3xl overflow-hidden border border-slate-200/80 shadow-xs p-6 sm:p-10 lg:p-12 mb-8">
          
          <!-- 背景装飾（上品なゴールド・アンバーのグラデーション） -->
          <div class="absolute inset-0 bg-gradient-to-br from-amber-50/70 via-white to-slate-50/80 pointer-events-none"></div>
          <div class="absolute -right-20 -top-20 w-80 h-80 rounded-full bg-amber-200/20 blur-3xl pointer-events-none"></div>

          <!-- メインコンテンツ -->
          <div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            
            <!-- 左側: 公式ロゴ & 洗練された目次ナビゲーション -->
            <div class="lg:col-span-7 space-y-6">
              
              <!-- 公式ロゴ & キャッチコピー -->
              <div class="space-y-2">
                <div class="max-w-[260px] sm:max-w-[300px]">
                  <img src="images/raytus_logo.png" alt="RAYTUS Logo" class="w-full object-contain filter drop-shadow-xs">
                </div>
                <p class="text-xs sm:text-sm font-serif text-amber-800/90 font-medium tracking-wider">
                  仲間の未来の夢をプロデュースするコミュニティ RAYTUS group.
                </p>
              </div>

              <!-- 目次（クイックジャンプ）: 必要な4項目に厳選 -->
              <div class="pt-2">
                <div class="flex items-center gap-2 mb-3">
                  <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                  <span class="text-xs font-bold text-slate-700 tracking-wider font-zen">目次 / クイックジャンプ</span>
                </div>
                
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 max-w-lg">
                  <!-- 1. SERVICE -->
                  <a onclick="scrollToSection('raytus-services-section')" class="flex items-center justify-between p-3.5 rounded-2xl bg-amber-50/50 hover:bg-amber-100/70 border border-amber-200/70 transition shadow-2xs group cursor-pointer">
                    <div class="flex items-center gap-3">
                      <div class="w-9 h-9 rounded-xl bg-amber-500/10 text-amber-700 flex items-center justify-center font-bold text-sm group-hover:scale-105 transition">
                        <i class="fa-solid fa-shapes"></i>
                      </div>
                      <div>
                        <span class="block text-xs font-serif font-bold text-amber-950 group-hover:text-amber-800 transition">SERVICE</span>
                        <span class="block text-[11px] text-slate-600 font-medium">事業内容（31事業 & 動画）</span>
                      </div>
                    </div>
                    <i class="fa-solid fa-arrow-down text-xs text-amber-500 group-hover:translate-y-0.5 transition pr-1"></i>
                  </a>

                  <!-- 2. COMMUNITY -->
                  <a onclick="scrollToSection('raytus-community-section')" class="flex items-center justify-between p-3.5 rounded-2xl bg-amber-50/50 hover:bg-amber-100/70 border border-amber-200/70 transition shadow-2xs group cursor-pointer">
                    <div class="flex items-center gap-3">
                      <div class="w-9 h-9 rounded-xl bg-purple-500/10 text-purple-700 flex items-center justify-center font-bold text-sm group-hover:scale-105 transition">
                        <i class="fa-solid fa-users"></i>
                      </div>
                      <div>
                        <span class="block text-xs font-serif font-bold text-amber-950 group-hover:text-amber-800 transition">COMMUNITY</span>
                        <span class="block text-[11px] text-slate-600 font-medium">グループコミュニティ</span>
                      </div>
                    </div>
                    <i class="fa-solid fa-arrow-down text-xs text-amber-500 group-hover:translate-y-0.5 transition pr-1"></i>
                  </a>

                  <!-- 3. PROJECTS -->
                  <a onclick="scrollToSection('raytus-projects-section')" class="flex items-center justify-between p-3.5 rounded-2xl bg-amber-50/50 hover:bg-amber-100/70 border border-amber-200/70 transition shadow-2xs group cursor-pointer">
                    <div class="flex items-center gap-3">
                      <div class="w-9 h-9 rounded-xl bg-blue-500/10 text-blue-700 flex items-center justify-center font-bold text-sm group-hover:scale-105 transition">
                        <i class="fa-solid fa-graduation-cap"></i>
                      </div>
                      <div>
                        <span class="block text-xs font-serif font-bold text-amber-950 group-hover:text-amber-800 transition">PROJECTS</span>
                        <span class="block text-[11px] text-slate-600 font-medium">2大未来創造プロジェクト</span>
                      </div>
                    </div>
                    <i class="fa-solid fa-arrow-down text-xs text-amber-500 group-hover:translate-y-0.5 transition pr-1"></i>
                  </a>

                  <!-- 4. SHOP -->
                  <a onclick="scrollToSection('raytus-shop-section')" class="flex items-center justify-between p-3.5 rounded-2xl bg-amber-50/50 hover:bg-amber-100/70 border border-amber-200/70 transition shadow-2xs group cursor-pointer">
                    <div class="flex items-center gap-3">
                      <div class="w-9 h-9 rounded-xl bg-emerald-500/10 text-emerald-700 flex items-center justify-center font-bold text-sm group-hover:scale-105 transition">
                        <i class="fa-solid fa-store"></i>
                      </div>
                      <div>
                        <span class="block text-xs font-serif font-bold text-amber-950 group-hover:text-amber-800 transition">SHOP</span>
                        <span class="block text-[11px] text-slate-600 font-medium">加盟店紹介（全85店）</span>
                      </div>
                    </div>
                    <i class="fa-solid fa-arrow-down text-xs text-amber-500 group-hover:translate-y-0.5 transition pr-1"></i>
                  </a>
                </div>
              </div>

              <!-- 2大プロジェクトバナー -->
              <div class="pt-2 max-w-lg grid grid-cols-1 sm:grid-cols-2 gap-3">
                <a href="https://raytus-group.com/news/2026/10/08/terakoya-open-hofu-2027/" target="_blank" class="group block rounded-xl overflow-hidden border border-slate-200 hover:border-amber-400 transition shadow-xs bg-white">
                  <img src="images/banners-raytus-terakoya.jpg" alt="寺子屋プロジェクト" class="w-full h-auto object-cover group-hover:opacity-90 transition">
                </a>
                <a href="https://raytus-group.com/news/2026/10/08/basta-school-building-construction-project/" target="_blank" class="group block rounded-xl overflow-hidden border border-slate-200 hover:border-amber-400 transition shadow-xs bg-white">
                  <img src="images/banners-raytus-basta.jpg" alt="バスタ高校 新校舎建設プロジェクト" class="w-full h-auto object-cover group-hover:opacity-90 transition">
                </a>
              </div>

            </div>

            <!-- 右側: 縦書き理念コピー -->
            <div class="lg:col-span-5 flex justify-center lg:justify-end py-4 lg:py-0">
              <div class="bg-gradient-to-b from-amber-50/90 to-white/90 border border-amber-200/60 rounded-3xl p-6 sm:p-8 shadow-xs flex items-center gap-6">
                <div class="raytus-vertical-text text-xl sm:text-2xl font-light text-slate-800 select-none">
                  <p class="tracking-widest font-serif">あなたの人生に</p>
                  <p class="mt-4 tracking-widest font-serif"><span class="text-amber-600 font-bold">光（RAY）</span>を<span class="text-amber-600 font-bold">足す（TUS）</span>。</p>
                </div>
                <div class="h-44 w-[1px] bg-amber-200/80"></div>
                <div class="text-xs text-slate-600 font-serif space-y-2 max-w-[160px] leading-relaxed">
                  <p class="font-bold text-amber-900">RAYTUS group.</p>
                  <p>一人ひとりの心に秘めた想いや才能を最短で引き出し、セカンドキャリアをプロデュース。</p>
                </div>
              </div>
            </div>

          </div>

        </div>

        <!-- ============================================== -->
        <!-- SERVICE セクション（31事業・動画アーカイブ・ライトテーマ） -->
        <!-- ============================================== -->
        <div id="raytus-services-section" class="bg-white rounded-3xl border border-slate-200/80 shadow-xs p-6 sm:p-10 lg:p-12 mb-8">
          
          <!-- 本家 sec-head 見出し -->
          <div class="raytus-sec-head">
            <p class="raytus-sec-head__en">SERVICE</p>
            <h3 class="raytus-sec-head__ja">事業内容</h3>
          </div>

          <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-8">
            <p class="text-xs sm:text-sm text-slate-500 font-serif leading-relaxed">
              ※事業名を押すと詳しい内容をご覧いただけます。<br class="hidden sm:inline">
              Notion公式に収録された紹介動画（YouTube）もその場で再生・確認できます。
            </p>
            
            <!-- 検索入力 -->
            <div class="relative w-full md:w-80 shrink-0">
              <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
              <input type="text" id="raytus-service-search" oninput="filterRaytusServices()" placeholder="事業名・責任者・キーワード検索..." class="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-amber-500 focus:bg-white transition">
            </div>
          </div>

          <!-- カテゴリ分類 切り替えピルバー (5大グループ) -->
          <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-3 mb-8 text-xs font-bold">
            <button onclick="setRaytusCategory('all')" id="raytus-cat-all" class="raytus-cat-btn px-3.5 sm:px-4 py-2 rounded-xl transition bg-amber-500 text-slate-950 font-black shadow-xs border border-amber-500 whitespace-nowrap font-zen">
              🌟 すべて表示 (<span id="count-all">31</span>)
            </button>
            <button onclick="setRaytusCategory('care')" id="raytus-cat-care" class="raytus-cat-btn px-3.5 sm:px-4 py-2 rounded-xl transition bg-white text-slate-600 hover:text-slate-900 border border-slate-200 hover:bg-slate-50 shadow-2xs whitespace-nowrap font-zen">
              👶 子育て・女性・ファミリー (<span id="count-care">5</span>)
            </button>
            <button onclick="setRaytusCategory('food')" id="raytus-cat-food" class="raytus-cat-btn px-3.5 sm:px-4 py-2 rounded-xl transition bg-white text-slate-600 hover:text-slate-900 border border-slate-200 hover:bg-slate-50 shadow-2xs whitespace-nowrap font-zen">
              🍙 食・農業・ウェルネス (<span id="count-food">4</span>)
            </button>
            <button onclick="setRaytusCategory('beauty')" id="raytus-cat-beauty" class="raytus-cat-btn px-3.5 sm:px-4 py-2 rounded-xl transition bg-white text-slate-600 hover:text-slate-900 border border-slate-200 hover:bg-slate-50 shadow-2xs whitespace-nowrap font-zen">
              💄 美容・ジュエリー・フェムケア (<span id="count-beauty">5</span>)
            </button>
            <button onclick="setRaytusCategory('life')" id="raytus-cat-life" class="raytus-cat-btn px-3.5 sm:px-4 py-2 rounded-xl transition bg-white text-slate-600 hover:text-slate-900 border border-slate-200 hover:bg-slate-50 shadow-2xs whitespace-nowrap font-zen">
              🤝 暮らし・シニア・パートナー (<span id="count-life">7</span>)
            </button>
            <button onclick="setRaytusCategory('business')" id="raytus-cat-business" class="raytus-cat-btn px-3.5 sm:px-4 py-2 rounded-xl transition bg-white text-slate-600 hover:text-slate-900 border border-slate-200 hover:bg-slate-50 shadow-2xs whitespace-nowrap font-zen">
              💼 ビジネス・事務・制作 (<span id="count-business">10</span>)
            </button>
          </div>

          <!-- 31事業 カードグリッド -->
          <div id="raytus-services-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- JavaScriptで動的生成 -->
          </div>

          <!-- 検索該当なしメッセージ -->
          <div id="raytus-no-results" class="hidden py-16 text-center border border-slate-200 rounded-3xl bg-slate-50">
            <i class="fa-solid fa-magnifying-glass text-3xl text-slate-300 mb-3"></i>
            <p class="text-sm font-bold text-slate-600 font-zen">該当する事業が見つかりませんでした</p>
            <p class="text-xs text-slate-400 mt-1 font-zen">キーワードやカテゴリを変更してお試しください</p>
          </div>

        </div>

        <!-- ============================================== -->
        <!-- COMMUNITY セクション（グループコミュニティ一覧・ライトテーマ） -->
        <!-- ============================================== -->
        <div id="raytus-community-section" class="bg-white rounded-3xl border border-slate-200/80 shadow-xs p-6 sm:p-10 lg:p-12 mb-8">
          
          <!-- 本家 sec-head 見出し -->
          <div class="raytus-sec-head">
            <p class="raytus-sec-head__en">COMMUNITY</p>
            <h3 class="raytus-sec-head__ja">グループコミュニティ</h3>
          </div>

          <p class="text-xs sm:text-sm text-slate-500 font-serif leading-relaxed mb-8">
            一人ひとりの才能や個性を最短で引き出し、セカンドキャリアを伴走するRAYTUSの多彩なチーム。
          </p>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 font-zen">
            
            <!-- Community 1: RAYTUS -->
            <div class="bg-slate-50/70 rounded-2xl p-6 border border-slate-200/80 hover:border-amber-400 hover:bg-white hover:shadow-md transition shadow-2xs flex flex-col justify-between">
              <div>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 font-bold border border-amber-200/60">母体・理念</span>
                <h4 class="text-xl font-bold text-slate-900 mt-2">RAYTUS</h4>
                <p class="text-xs text-slate-600 mt-2 leading-relaxed">
                  一人ひとりの心に秘めた想いや才能を最短で引き出し、セカンドキャリアをプロデュース。古き良き時代のアナログを大切に、最先端デジタルを活用して経済的自立と社会貢献を実現します。
                </p>
              </div>
              <div class="mt-4 pt-4 border-t border-slate-200 text-xs text-slate-500">
                <span>理事長: <strong class="text-slate-800">草彅 亜希</strong></span>
              </div>
            </div>

            <!-- Community 2: enchant+ -->
            <div class="bg-slate-50/70 rounded-2xl p-6 border border-slate-200/80 hover:border-purple-400 hover:bg-white hover:shadow-md transition shadow-2xs flex flex-col justify-between">
              <div>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-purple-100 text-purple-800 font-bold border border-purple-200/60">クリエイティブ</span>
                <h4 class="text-xl font-bold text-slate-900 mt-2">enchant+ (アンシャンテ)</h4>
                <p class="text-xs text-slate-600 mt-2 leading-relaxed">
                  「能力を付与する」、そしてフランス語で「出会ってくれてありがとう」。人を喜ばせ、魔法のように人々を魅了し続けていく共創チームです。
                </p>
              </div>
              <div class="mt-4 pt-4 border-t border-slate-200 text-xs text-slate-500">
                <span>代表: <strong class="text-slate-800">川野 弥生</strong></span>
              </div>
            </div>

            <!-- Community 3: yuima-ru -->
            <div class="bg-slate-50/70 rounded-2xl p-6 border border-slate-200/80 hover:border-emerald-400 hover:bg-white hover:shadow-md transition shadow-2xs flex flex-col justify-between">
              <div>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-bold border border-emerald-200/60">共育・助け合い</span>
                <h4 class="text-xl font-bold text-slate-900 mt-2">yuima-ru (ゆいまーる)</h4>
                <p class="text-xs text-slate-600 mt-2 leading-relaxed">
                  沖縄の方言「結い（協働・助け合い）」から名付けられたチーム。教育・共育・暮らしの中で互いに支え合い、誰もが居場所を持てる温かい連帯を創ります。
                </p>
              </div>
              <div class="mt-4 pt-4 border-t border-slate-200 text-xs text-slate-500">
                <span>理事長: <strong class="text-slate-800">畑 ゆかり</strong></span>
              </div>
            </div>

            <!-- Community 4: MAARUKU -->
            <div class="bg-slate-50/70 rounded-2xl p-6 border border-slate-200/80 hover:border-rose-400 hover:bg-white hover:shadow-md transition shadow-2xs flex flex-col justify-between">
              <div>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-800 font-bold border border-rose-200/60">共創</span>
                <h4 class="text-xl font-bold text-slate-900 mt-2">MAARUKU (まあるく)</h4>
                <p class="text-xs text-slate-600 mt-2 leading-relaxed">
                  人と人、事業と事業が丸くつながり、調和と発展を生み出すコミュニティ。多様なバックグラウンドを持つ仲間が集い、新たなシナジーを生み出します。
                </p>
              </div>
              <div class="mt-4 pt-4 border-t border-slate-200 text-xs text-slate-500">
                <span>理事長: <strong class="text-slate-800">田上 順子</strong></span>
              </div>
            </div>

            <!-- Community 5: はるいろ -->
            <div class="bg-slate-50/70 rounded-2xl p-6 border border-slate-200/80 hover:border-pink-400 hover:bg-white hover:shadow-md transition shadow-2xs flex flex-col justify-between">
              <div>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-pink-100 text-pink-800 font-bold border border-pink-200/60">ぬくもり</span>
                <h4 class="text-xl font-bold text-slate-900 mt-2">はるいろ</h4>
                <p class="text-xs text-slate-600 mt-2 leading-relaxed">
                  春のような温もりと優しさで、誰もが安心して自分の想いを表現できる場を提供。個々の歩みに寄り添いながら、彩り豊かな未来を育みます。
                </p>
              </div>
              <div class="mt-4 pt-4 border-t border-slate-200 text-xs text-slate-500">
                <span>代表: <strong class="text-slate-800">長沼 ひとみ</strong></span>
              </div>
            </div>

            <!-- Community 6: Mimola -->
            <div class="bg-slate-50/70 rounded-2xl p-6 border border-slate-200/80 hover:border-blue-400 hover:bg-white hover:shadow-md transition shadow-2xs flex flex-col justify-between">
              <div>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-800 font-bold border border-blue-200/60">未来創生</span>
                <h4 class="text-xl font-bold text-slate-900 mt-2">Mimola (ミモラ)</h4>
                <p class="text-xs text-slate-600 mt-2 leading-relaxed">
                  新しい価値を創造し、次世代へとつなぐイノベーションコミュニティ。一人ひとりの可能性を解き放ち、持続可能な未来への挑戦を後押しします。
                </p>
              </div>
              <div class="mt-4 pt-4 border-t border-slate-200 text-xs text-slate-500">
                <span>理事長: <strong class="text-slate-800">岩崎 由夏</strong></span>
              </div>
            </div>

          </div>

        </div>

        <!-- ============================================== -->
        <!-- PROJECTS セクション（公式プロジェクト・ライトテーマ） -->
        <!-- ============================================== -->
        <div id="raytus-projects-section" class="bg-white rounded-3xl border border-slate-200/80 shadow-xs p-6 sm:p-10 lg:p-12 mb-8">
          
          <!-- 本家 sec-head 見出し -->
          <div class="raytus-sec-head">
            <p class="raytus-sec-head__en">PROJECTS</p>
            <h3 class="raytus-sec-head__ja">次世代育成・未来創造プロジェクト</h3>
          </div>

          <p class="text-xs sm:text-sm text-slate-500 font-serif leading-relaxed mb-8">
            RAYTUS groupが全力で取り組む注目の教育・社会支援プロジェクト
          </p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 font-zen">
            <!-- Project 1 -->
            <div class="bg-slate-50/70 border border-slate-200/80 rounded-3xl overflow-hidden p-6 sm:p-8 flex flex-col justify-between group hover:border-amber-400 hover:bg-white hover:shadow-md transition shadow-2xs">
              <div>
                <div class="overflow-hidden rounded-2xl mb-5 bg-slate-100">
                  <img src="images/banners-raytus-terakoya.jpg" alt="寺子屋プロジェクト" class="w-full h-52 object-cover group-hover:scale-[1.02] transition duration-300">
                </div>
                <span class="text-[10px] px-3 py-1 rounded-full bg-amber-100 text-amber-800 font-bold border border-amber-200/60">2027年開校予定</span>
                <h4 class="text-xl font-bold text-slate-900 mt-3 group-hover:text-amber-700 transition">寺子屋プロジェクト 防府開校 2027</h4>
                <p class="text-xs sm:text-sm text-slate-600 mt-3 leading-relaxed">
                  子供たちが自分の「好き」や「得意」を伸ばし、社会で生き抜く力を育む新たな学びの場。地域社会と連携しながら、山口県防府市に2027年開校を目指して建設・準備が進められています。
                </p>
              </div>
              <div class="mt-8 pt-4 border-t border-slate-200 flex items-center justify-between">
                <a href="https://raytus-group.com/news/2026/10/08/terakoya-open-hofu-2027/" target="_blank" class="text-xs font-bold text-amber-700 hover:text-amber-800 flex items-center gap-1.5">
                  <span>詳細プロジェクト記事を見る</span>
                  <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
                <span class="text-xs text-slate-400">山口県防府市</span>
              </div>
            </div>

            <!-- Project 2 -->
            <div class="bg-slate-50/70 border border-slate-200/80 rounded-3xl overflow-hidden p-6 sm:p-8 flex flex-col justify-between group hover:border-blue-400 hover:bg-white hover:shadow-md transition shadow-2xs">
              <div>
                <div class="overflow-hidden rounded-2xl mb-5 bg-slate-100">
                  <img src="images/banners-raytus-basta.jpg" alt="バスタ高校" class="w-full h-52 object-cover group-hover:scale-[1.02] transition duration-300">
                </div>
                <span class="text-[10px] px-3 py-1 rounded-full bg-blue-100 text-blue-800 font-bold border border-blue-200/60">新校舎建設</span>
                <h4 class="text-xl font-bold text-slate-900 mt-3 group-hover:text-blue-700 transition">バスタ高校 新校舎建設プロジェクト</h4>
                <p class="text-xs sm:text-sm text-slate-600 mt-3 leading-relaxed">
                  従来の教育の枠にとらわれず、生徒一人ひとりの個性を最大限に生かし自立を支援する学校創り。次世代のリーダーやクリエイターが育つ拠点として新校舎の建設が進んでいます。
                </p>
              </div>
              <div class="mt-8 pt-4 border-t border-slate-200 flex items-center justify-between">
                <a href="https://raytus-group.com/news/2026/10/08/basta-school-building-construction-project/" target="_blank" class="text-xs font-bold text-blue-700 hover:text-blue-800 flex items-center gap-1.5">
                  <span>新校舎建設ニュースを見る</span>
                  <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
                <span class="text-xs text-slate-400">学校創造プロジェクト</span>
              </div>
            </div>
          </div>

        </div>

        <!-- ============================================== -->
        <!-- SHOP セクション（加盟店紹介・全85店・ライトテーマ） -->
        <!-- ============================================== -->
        <div id="raytus-shop-section" class="bg-white rounded-3xl border border-slate-200/80 shadow-xs p-6 sm:p-10 lg:p-12 mb-8">
          
          <!-- 本家 sec-head 見出し -->
          <div class="raytus-sec-head">
            <p class="raytus-sec-head__en">SHOP</p>
            <h3 class="raytus-sec-head__ja">加盟店紹介</h3>
          </div>

          <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-6">
            <div>
              <p class="text-xs sm:text-sm text-slate-500 font-serif leading-relaxed">
                RAYTUS group.に加盟している全国の店舗・サービス一覧（全<span id="raytus-shop-count" class="text-amber-600 font-bold font-mono">85</span>件）。<br class="hidden sm:inline">
                横にスクロールが可能です。行をタップすると各店舗の商品・詳細ページが開きます。
              </p>
            </div>
            
            <!-- 加盟店検索入力 -->
            <div class="relative w-full md:w-80 shrink-0">
              <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
              <input type="text" id="raytus-shop-search" oninput="renderRaytusShops()" placeholder="店舗名・代表者・商品・地域で検索..." class="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-amber-500 focus:bg-white transition font-zen">
            </div>
          </div>

          <!-- 加盟店テーブル wrap -->
          <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-2xs">
            <div class="overflow-x-auto max-h-[520px] overflow-y-auto">
              <table class="w-full text-left border-collapse text-xs sm:text-sm font-zen">
                <thead class="bg-slate-50 text-slate-700 font-bold sticky top-0 z-10 border-b border-slate-200 shadow-2xs">
                  <tr>
                    <th class="p-3.5 sm:p-4 font-bold whitespace-nowrap">店舗名・会社名</th>
                    <th class="p-3.5 sm:p-4 font-bold whitespace-nowrap">代表者名</th>
                    <th class="p-3.5 sm:p-4 font-bold">提供商品・サービス</th>
                    <th class="p-3.5 sm:p-4 font-bold whitespace-nowrap">所在地・エリア</th>
                  </tr>
                </thead>
                <tbody id="raytus-shop-tbody" class="divide-y divide-slate-100">
                  <!-- Injected via renderRaytusShops() -->
                </tbody>
              </table>
            </div>
          </div>

          <div class="mt-4 flex items-center justify-between text-xs text-slate-500 font-zen">
            <span>※各加盟店へのご注文・お問い合わせはリンク先の商品ページより承ります</span>
            <a href="https://raytus-group.com/shop/" target="_blank" class="text-amber-700 hover:text-amber-800 font-bold flex items-center gap-1">
              <span>本家サイトで確認</span>
              <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
            </a>
          </div>

        </div>

      </div>

    </div>
'''

def get_new_raytus_js():
    return '''    // ============================================
    // RAYTUS Services Logic (Grouping, Filter, Modal) - Light Theme
    // ============================================
    let currentRaytusCategory = 'all';

    const CATEGORY_NAMES = {
      care: '子育て・女性・ファミリー',
      food: '食・農業・ウェルネス',
      beauty: '美容・ジュエリー・フェムケア',
      life: '暮らし・シニア・パートナー',
      business: 'ビジネス・事務・クリエイティブ'
    };

    const CATEGORY_COLORS = {
      care: 'bg-rose-50 text-rose-700 border border-rose-200',
      food: 'bg-amber-50 text-amber-800 border border-amber-200',
      beauty: 'bg-pink-50 text-pink-700 border border-pink-200',
      life: 'bg-emerald-50 text-emerald-700 border border-emerald-200',
      business: 'bg-blue-50 text-blue-700 border border-blue-200'
    };

    // 加盟店一覧 (SHOP) の描画（ライトテーマ対応）
    function renderRaytusShops() {
      const container = document.getElementById('raytus-shop-tbody');
      if (!container || typeof RAYTUS_SHOPS === 'undefined') return;
      const q = (document.getElementById('raytus-shop-search')?.value || '').toLowerCase().trim();
      const countEl = document.getElementById('raytus-shop-count');

      const filtered = RAYTUS_SHOPS.filter(s => {
        if (!q) return true;
        return `${s.name} ${s.rep} ${s.product} ${s.area}`.toLowerCase().includes(q);
      });

      if (countEl) countEl.textContent = filtered.length;

      container.innerHTML = filtered.map(s => `
        <tr class="hover:bg-amber-50/50 transition border-b border-slate-100 cursor-pointer" onclick="window.open('${s.link}', '_blank')">
          <td class="p-3.5 sm:p-4 font-bold text-slate-900 whitespace-nowrap">
            <div class="flex items-center gap-1.5">
              <span class="hover:text-amber-600 transition">${s.name}</span>
              <i class="fa-solid fa-arrow-up-right-from-square text-[10px] text-slate-400"></i>
            </div>
          </td>
          <td class="p-3.5 sm:p-4 text-slate-700 whitespace-nowrap font-medium">${s.rep}</td>
          <td class="p-3.5 sm:p-4 text-slate-600 min-w-[220px] leading-relaxed text-xs">${s.product}</td>
          <td class="p-3.5 sm:p-4 text-slate-500 whitespace-pre-line text-xs">${s.area}</td>
        </tr>
      `).join('');
    }

    // 31事業 (SERVICE) の描画（ライトテーマ対応カード）
    function renderRaytusServices() {
      const container = document.getElementById('raytus-services-grid');
      if (!container || typeof RAYTUS_SERVICES === 'undefined') return;

      const searchVal = (document.getElementById('raytus-service-search')?.value || '').toLowerCase().trim();
      const noResults = document.getElementById('raytus-no-results');

      const filtered = RAYTUS_SERVICES.filter((item) => {
        if (currentRaytusCategory !== 'all' && item.category !== currentRaytusCategory) {
          return false;
        }
        if (searchVal) {
          const matchText = `${item.businessName} ${item.companyName} ${item.manager} ${item.tagline} ${item.target}`.toLowerCase();
          if (!matchText.includes(searchVal)) return false;
        }
        return true;
      });

      if (filtered.length === 0) {
        container.innerHTML = '';
        if (noResults) noResults.classList.remove('hidden');
        return;
      }

      if (noResults) noResults.classList.add('hidden');

      container.innerHTML = filtered.map(item => {
        const originalIndex = RAYTUS_SERVICES.indexOf(item);
        const catLabel = CATEGORY_NAMES[item.category] || '事業';
        const catColor = CATEGORY_COLORS[item.category] || 'bg-slate-100 text-slate-700 border border-slate-200';
        const hasVideo = !!item.videoId;

        return `
          <div onclick="openRaytusServiceModal(${originalIndex})" class="bg-white rounded-2xl overflow-hidden border border-slate-200 shadow-2xs hover:shadow-md hover:border-amber-400 transition cursor-pointer flex flex-col justify-between group">
            <div>
              <!-- サムネイル画像 -->
              <div class="aspect-video w-full overflow-hidden bg-slate-100 relative">
                <img src="${item.bgImage}" alt="${item.businessName}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy">
                <div class="absolute top-2.5 left-2.5 flex items-center gap-1.5">
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold ${catColor} shadow-2xs backdrop-blur-xs">
                    ${catLabel}
                  </span>
                </div>
                ${hasVideo ? `
                <span class="absolute top-2.5 right-2.5 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-600 text-white flex items-center gap-1 shadow-md">
                  <i class="fa-brands fa-youtube"></i> 動画あり
                </span>
                ` : ''}
              </div>

              <!-- カード本文 -->
              <div class="p-5">
                <p class="text-[11px] font-serif font-bold text-amber-700 tracking-wider mb-1 line-clamp-1">
                  ${item.businessName}
                </p>
                <h4 class="text-base sm:text-lg font-serif font-bold text-slate-900 group-hover:text-amber-700 transition leading-snug">
                  ${item.companyName}
                </h4>
                <p class="text-xs text-slate-500 font-serif mt-2 line-clamp-2 leading-relaxed">
                  ${item.tagline.replace(/\\n/g, ' ')}
                </p>
              </div>
            </div>

            <!-- カードフッター -->
            <div class="px-5 pb-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
              <span>責任者: <strong class="text-slate-800 font-bold">${item.manager}</strong></span>
              <span class="text-amber-600 font-bold flex items-center gap-1 group-hover:translate-x-0.5 transition">
                <span>詳細を見る</span>
                <i class="fa-solid fa-chevron-right text-[10px]"></i>
              </span>
            </div>
          </div>
        `;
      }).join('');
    }

    function setRaytusCategory(cat) {
      currentRaytusCategory = cat;
      document.querySelectorAll('.raytus-cat-btn').forEach(btn => {
        btn.className = 'raytus-cat-btn px-3.5 sm:px-4 py-2 rounded-xl transition bg-white text-slate-600 hover:text-slate-900 border border-slate-200 hover:bg-slate-50 shadow-2xs whitespace-nowrap text-xs font-bold';
      });
      const activeBtn = document.getElementById(`raytus-cat-${cat}`);
      if (activeBtn) {
        activeBtn.className = 'raytus-cat-btn px-3.5 sm:px-4 py-2 rounded-xl transition bg-amber-500 text-slate-950 font-black shadow-xs border border-amber-500 whitespace-nowrap text-xs';
      }
      renderRaytusServices();
    }

    function filterRaytusServices() {
      renderRaytusServices();
    }

    function openRaytusServiceModal(index) {
      if (typeof RAYTUS_SERVICES === 'undefined' || !RAYTUS_SERVICES[index]) return;
      const item = RAYTUS_SERVICES[index];
      const catLabel = CATEGORY_NAMES[item.category] || '事業';
      const catColor = CATEGORY_COLORS[item.category] || 'bg-slate-100 text-slate-700 border border-slate-200';

      const content = document.getElementById('raytus-service-modal-content');
      if (!content) return;

      content.innerHTML = `
        <div class="flex items-start justify-between gap-4 mb-4 pr-8">
          <div>
            <div class="flex items-center gap-2 mb-1.5">
              <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold ${catColor}">${catLabel}</span>
              <span class="text-xs font-serif text-amber-700 font-bold tracking-wider">${item.companyName}</span>
            </div>
            <h3 class="text-xl sm:text-2xl font-serif font-bold text-slate-900">${item.businessName}</h3>
            <p class="text-xs text-slate-500 mt-1 flex items-center gap-1.5">
              <i class="fa-solid fa-user-tie text-amber-600"></i>
              <span>事業責任者: <strong class="text-slate-800">${item.manager}</strong></span>
            </p>
          </div>
        </div>

        ${item.videoId ? `
        <div class="aspect-video w-full rounded-2xl overflow-hidden shadow-md bg-black mb-5 border border-slate-200">
          <iframe src="https://www.youtube.com/embed/${item.videoId}?autoplay=1" title="${item.businessName}" class="w-full h-full border-0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        ` : `
        <div class="aspect-video w-full rounded-2xl overflow-hidden shadow-sm bg-slate-100 mb-5 relative border border-slate-200">
          <img src="${item.bgImage}" alt="${item.businessName}" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent flex items-end p-4">
            <span class="text-xs text-white font-medium">${item.companyName} 公式紹介</span>
          </div>
        </div>
        `}

        <div class="space-y-4 text-xs text-slate-700">
          <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200">
            <h4 class="text-xs font-serif font-bold text-amber-800 mb-1 flex items-center gap-1.5">
              <i class="fa-solid fa-quote-left"></i> 理念・コンセプト
            </h4>
            <div class="leading-relaxed whitespace-pre-line text-slate-600 text-xs sm:text-sm">
              ${item.tagline}
            </div>
          </div>

          <div class="p-4 rounded-2xl bg-amber-50/70 border border-amber-200/80">
            <h4 class="text-xs font-serif font-bold text-amber-900 mb-1 flex items-center gap-1.5">
              <i class="fa-solid fa-bullseye"></i> こんな方へ / 参画対象
            </h4>
            <div class="leading-relaxed whitespace-pre-line text-slate-700">
              ${item.target}
            </div>
          </div>

          <div class="pt-2 flex flex-wrap items-center justify-between gap-3">
            <div class="flex items-center gap-2">
              ${item.videoId ? `
              <a href="https://youtu.be/${item.videoId}" target="_blank" class="px-3.5 py-2 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-bold transition flex items-center gap-1.5 text-xs shadow-xs">
                <i class="fa-brands fa-youtube"></i> YouTubeで開く
              </a>
              ` : ''}
              <a href="https://raytus-group.com/service/" target="_blank" class="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-serif transition flex items-center gap-1.5 text-xs border border-slate-300">
                <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i> 公式HPで確認
              </a>
            </div>
            <button onclick="closeRaytusServiceModal(); switchTab('hub'); scrollToSection('schedule-section');" class="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold transition flex items-center gap-1.5 text-xs shadow-xs">
              <i class="fa-regular fa-calendar-check"></i> 定例会・説明会に参加する
            </button>
          </div>
        </div>
      `;

      openModal('raytus-service-modal');
      if (item.videoId && typeof trackContentView === 'function') {
        trackContentView('https://www.youtube.com/embed/' + item.videoId, item.businessName + '：' + item.companyName);
      }
    }

    function closeRaytusServiceModal() {
      const content = document.getElementById('raytus-service-modal-content');
      if (content) content.innerHTML = '';
      closeModal('raytus-service-modal');
    }
'''

def update_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace TAB 2 HTML
    tab_pattern = re.compile(r'<!-- ======================================================== -->\s*<!-- TAB 2: RAYTUS group.*?<!-- ======================================================== -->\s*<!-- TAB 3: Iyasaka宮', re.DOTALL)
    
    # If in raytus.html where TAB 3 might not be next, check for </main>
    if not tab_pattern.search(content):
        tab_pattern = re.compile(r'<!-- ======================================================== -->\s*<!-- TAB 2: RAYTUS group.*?</main>', re.DOTALL)
        new_tab_block = get_new_raytus_tab_html() + '\n  </main>'
    else:
        new_tab_block = get_new_raytus_tab_html() + '\n    <!-- ======================================================== -->\n    <!-- TAB 3: Iyasaka宮'

    content = tab_pattern.sub(new_tab_block, content, count=1)

    # 2. Update modal container if dark
    modal_dark = '''  <div id="raytus-service-modal" class="fixed inset-0 z-50 bg-black/85 backdrop-blur-md hidden items-center justify-center p-4" onclick="if(event.target === this) closeRaytusServiceModal()">
    <div class="bg-[#121824] rounded-3xl p-6 sm:p-8 max-w-2xl w-full border border-slate-700 shadow-2xl relative max-h-[90vh] overflow-y-auto animate-scaleUp">
      <button onclick="closeRaytusServiceModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white w-8 h-8 rounded-full flex items-center justify-center bg-white/10 hover:bg-white/20 transition">
        <i class="fa-solid fa-xmark"></i>
      </button>
      <div id="raytus-service-modal-content">
        <!-- JSで動的生成 -->
      </div>
    </div>
  </div>'''

    modal_light = '''  <div id="raytus-service-modal" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm hidden items-center justify-center p-4" onclick="if(event.target === this) closeRaytusServiceModal()">
    <div class="bg-white rounded-3xl p-6 sm:p-8 max-w-2xl w-full border border-slate-200 shadow-2xl relative max-h-[90vh] overflow-y-auto animate-scaleUp">
      <button onclick="closeRaytusServiceModal()" class="absolute top-4 right-4 text-slate-400 hover:text-slate-700 w-8 h-8 rounded-full flex items-center justify-center bg-slate-100 hover:bg-slate-200 transition">
        <i class="fa-solid fa-xmark"></i>
      </button>
      <div id="raytus-service-modal-content">
        <!-- JSで動的生成 -->
      </div>
    </div>
  </div>'''
    content = content.replace(modal_dark, modal_light)

    # 3. Replace RAYTUS JS logic
    js_pattern = re.compile(r'// ============================================\s*// RAYTUS Services Logic.*?function closeRaytusServiceModal\(\) \{.*?closeModal\(\'raytus-service-modal\'\);\s*\}', re.DOTALL)
    if js_pattern.search(content):
        content = js_pattern.sub(get_new_raytus_js().strip(), content, count=1)
    else:
        print(f"Warning: JS pattern not matched in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

if __name__ == '__main__':
    update_css()
    update_html_file('raytus.html')
    update_html_file('index.html')
    update_html_file('portal.html')

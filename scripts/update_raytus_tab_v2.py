# -*- coding: utf-8 -*-
import sys

def run():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove the Instagram & Contact buttons in the hero section
    btn_target = '''          <!-- 右上 本家固定リンクバー (INSTAGRAM & CONTACT) -->
          <div class="relative z-20 flex justify-end items-center gap-3 mb-4">
            <a href="https://www.instagram.com/raytus_group.official" target="_blank" class="px-5 py-2 rounded-full bg-black/80 hover:bg-black text-white font-zen text-xs tracking-widest border border-slate-700/80 hover:border-amber-400 transition flex items-center gap-2 shadow-lg backdrop-blur-xs">
              <i class="fa-brands fa-instagram text-amber-400"></i>
              <span>INSTAGRAM</span>
            </a>
            <a href="https://raytus-group.com/contact/" target="_blank" class="px-5 py-2 rounded-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-zen font-bold text-xs tracking-widest transition shadow-lg shadow-amber-500/20">
              CONTACT
            </a>
          </div>'''
    
    if btn_target in content:
        content = content.replace(btn_target, "")
        print("Removed Instagram & Contact buttons successfully.")
    else:
        print("Warning: btn_target not found.")

    # 2. Update navigation links for SHOP, NEWS, BLOG
    nav_old = '''                <a onclick="switchTab('iyasaka')" class="raytus-nav-link group" title="Iyasaka宮の加盟店・ショップへ">
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
                </a>'''

    nav_new = '''                <a onclick="scrollToSection('raytus-shop-section')" class="raytus-nav-link group">
                  <span class="raytus-nav-en text-white group-hover:text-amber-300">SHOP</span>
                  <span class="raytus-nav-ja text-slate-400 group-hover:text-amber-200">加盟店紹介（全85店）</span>
                </a>
                <a onclick="scrollToSection('raytus-news-section')" class="raytus-nav-link group">
                  <span class="raytus-nav-en text-white group-hover:text-amber-300">NEWS RELEASE</span>
                  <span class="raytus-nav-ja text-slate-400 group-hover:text-amber-200">お知らせ</span>
                </a>
                <a onclick="scrollToSection('raytus-blog-section')" class="raytus-nav-link group">
                  <span class="raytus-nav-en text-white group-hover:text-amber-300">BLOG</span>
                  <span class="raytus-nav-ja text-slate-400 group-hover:text-amber-200">ブログ・活動レポート</span>
                </a>'''

    if nav_old in content:
        content = content.replace(nav_old, nav_new)
        print("Updated navigation links successfully.")
    else:
        print("Warning: nav_old not found.")

    # 3. Add SHOP, NEWS, and BLOG sections before the footer in tab-content-raytus
    footer_old = '''        <!-- 本家フッター -->
        <div class="p-6 sm:p-8 border-t border-slate-800/80 text-center text-xs text-slate-500 font-zen flex items-center justify-between flex-wrap gap-4 bg-[#080b11]">'''

    sections_new = '''        <!-- ============================================== -->
        <!-- SHOP セクション（本家 加盟店紹介・全85店データベース） -->
        <!-- ============================================== -->
        <div id="raytus-shop-section" class="p-6 sm:p-10 lg:p-14 border-t border-slate-800 bg-[#0d1118]">
          
          <!-- 本家 sec-head 見出し -->
          <div class="raytus-sec-head">
            <p class="raytus-sec-head__en">SHOP</p>
            <h3 class="raytus-sec-head__ja">加盟店紹介</h3>
          </div>

          <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-6">
            <div>
              <p class="text-xs sm:text-sm text-slate-400 font-serif leading-relaxed">
                RAYTUS group.に加盟している全国の店舗・サービス一覧（全<span id="raytus-shop-count" class="text-amber-400 font-bold font-mono">85</span>件）。<br class="hidden sm:inline">
                横にスクロールが可能です。行をタップすると各店舗の商品・詳細ページが開きます。
              </p>
            </div>
            
            <!-- 加盟店検索入力 -->
            <div class="relative w-full md:w-80 shrink-0">
              <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 text-xs"></i>
              <input type="text" id="raytus-shop-search" oninput="renderRaytusShops()" placeholder="店舗名・代表者・商品・地域で検索..." class="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-amber-400 transition font-zen">
            </div>
          </div>

          <!-- 加盟店テーブル wrap -->
          <div class="bg-[#121824] rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
            <div class="overflow-x-auto max-h-[520px] overflow-y-auto">
              <table class="w-full text-left border-collapse text-xs sm:text-sm font-zen">
                <thead class="bg-slate-900 text-amber-300 sticky top-0 z-10 border-b border-slate-800 shadow-xs">
                  <tr>
                    <th class="p-3.5 sm:p-4 font-bold whitespace-nowrap">店舗名・会社名</th>
                    <th class="p-3.5 sm:p-4 font-bold whitespace-nowrap">代表者名</th>
                    <th class="p-3.5 sm:p-4 font-bold">提供商品・サービス</th>
                    <th class="p-3.5 sm:p-4 font-bold whitespace-nowrap">所在地・エリア</th>
                  </tr>
                </thead>
                <tbody id="raytus-shop-tbody" class="divide-y divide-slate-800/60">
                  <!-- Injected via renderRaytusShops() -->
                </tbody>
              </table>
            </div>
          </div>

          <div class="mt-4 flex items-center justify-between text-xs text-slate-500 font-zen">
            <span>※各加盟店へのご注文・お問い合わせはリンク先の商品ページより承ります</span>
            <a href="https://raytus-group.com/shop/" target="_blank" class="text-amber-400 hover:underline flex items-center gap-1">
              <span>本家サイトで確認</span>
              <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
            </a>
          </div>

        </div>

        <!-- ============================================== -->
        <!-- NEWS RELEASE セクション（本家 公式お知らせ一覧） -->
        <!-- ============================================== -->
        <div id="raytus-news-section" class="p-6 sm:p-10 lg:p-14 border-t border-slate-800 bg-[#0b0f17]">
          
          <!-- 本家 sec-head 見出し -->
          <div class="raytus-sec-head">
            <p class="raytus-sec-head__en">NEWS</p>
            <h3 class="raytus-sec-head__ja">お知らせ</h3>
          </div>

          <p class="text-xs sm:text-sm text-slate-400 font-serif leading-relaxed mb-8">
            RAYTUS group.の最新リリースやプロジェクト進行状況のご案内
          </p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 font-zen">
            
            <!-- News 1 -->
            <a href="https://raytus-group.com/news/2026/10/08/terakoya-open-hofu-2027/" target="_blank" class="group bg-[#121824] rounded-2xl p-6 border border-slate-800 hover:border-amber-400/60 transition shadow-lg flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between text-xs mb-3">
                  <span class="px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-bold text-[10px]">プロジェクト開校</span>
                  <span class="text-slate-400 font-mono">2026.10.08</span>
                </div>
                <h4 class="text-base sm:text-lg font-bold text-white group-hover:text-amber-300 transition leading-snug">
                  2027年春、山口県防府市台道に「寺子屋」がオープンします。
                </h4>
                <p class="text-xs text-slate-400 mt-2.5 leading-relaxed line-clamp-3">
                  子供たちが自分の「好き」や「得意」を伸ばし、社会で生き抜く力を育む新たな学びの場。地域社会と連携しながら建設・準備が進められています。
                </p>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs font-bold text-amber-400">
                <span>詳細記事を見る</span>
                <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
              </div>
            </a>

            <!-- News 2 -->
            <a href="https://raytus-group.com/news/2026/10/08/basta-school-building-construction-project/" target="_blank" class="group bg-[#121824] rounded-2xl p-6 border border-slate-800 hover:border-blue-400/60 transition shadow-lg flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between text-xs mb-3">
                  <span class="px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-300 font-bold text-[10px]">国際支援・学校建設</span>
                  <span class="text-slate-400 font-mono">2026.10.08</span>
                </div>
                <h4 class="text-base sm:text-lg font-bold text-white group-hover:text-blue-300 transition leading-snug">
                  バングラデシュに学校を建てます。バスタ高校 新校舎建設プロジェクト
                </h4>
                <p class="text-xs text-slate-400 mt-2.5 leading-relaxed line-clamp-3">
                  従来の教育の枠にとらわれず、生徒一人ひとりの個性を最大限に生かし自立を支援する学校創り。次世代のリーダーやクリエイターが育つ拠点として建設が進んでいます。
                </p>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs font-bold text-blue-400">
                <span>詳細記事を見る</span>
                <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
              </div>
            </a>

          </div>

        </div>

        <!-- ============================================== -->
        <!-- BLOG セクション（本家 公式ブログ・イベントレポート） -->
        <!-- ============================================== -->
        <div id="raytus-blog-section" class="p-6 sm:p-10 lg:p-14 border-t border-slate-800 bg-[#0d1118]">
          
          <!-- 本家 sec-head 見出し -->
          <div class="raytus-sec-head">
            <p class="raytus-sec-head__en">BLOG</p>
            <h3 class="raytus-sec-head__ja">公式ブログ・レポート</h3>
          </div>

          <p class="text-xs sm:text-sm text-slate-400 font-serif leading-relaxed mb-8">
            コミュニティの熱気あふれるイベントレポートや、メンバーの挑戦のストーリーをお届けします。
          </p>

          <div id="raytus-blog-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 font-zen">
            <!-- Injected via renderRaytusBlogs() -->
          </div>

        </div>

        <!-- 本家フッター -->
        <div class="p-6 sm:p-8 border-t border-slate-800/80 text-center text-xs text-slate-500 font-zen flex items-center justify-between flex-wrap gap-4 bg-[#080b11]">'''

    if footer_old in content:
        content = content.replace(footer_old, sections_new)
        print("Added SHOP, NEWS, and BLOG sections successfully.")
    else:
        print("Warning: footer_old not found.")

    # 4. Add script tag for raytus-shop-data.js
    script_target = '<script src="js/raytus-services-data.js?v=20261020_12"></script>'
    script_replacement = '<script src="js/raytus-shop-data.js?v=20261021_1"></script>\n  <script src="js/raytus-services-data.js?v=20261020_12"></script>'
    if script_target in content:
        content = content.replace(script_target, script_replacement)
        print("Added script tag for raytus-shop-data.js.")
    else:
        print("Warning: script_target not found.")

    # 5. Add renderRaytusShops and renderRaytusBlogs JS logic
    js_target = '    function renderRaytusServices() {'
    js_new = '''    // 加盟店一覧 (SHOP) の描画
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
        <tr class="hover:bg-slate-800/60 transition border-b border-slate-800/80 cursor-pointer" onclick="window.open('${s.link}', '_blank')">
          <td class="p-3.5 sm:p-4 font-bold text-white whitespace-nowrap">
            <div class="flex items-center gap-1.5">
              <span class="hover:text-amber-300 transition">${s.name}</span>
              <i class="fa-solid fa-arrow-up-right-from-square text-[10px] text-slate-500"></i>
            </div>
          </td>
          <td class="p-3.5 sm:p-4 text-slate-300 whitespace-nowrap">${s.rep}</td>
          <td class="p-3.5 sm:p-4 text-slate-300 min-w-[220px] leading-relaxed text-xs">${s.product}</td>
          <td class="p-3.5 sm:p-4 text-slate-400 whitespace-pre-line text-xs">${s.area}</td>
        </tr>
      `).join('');
    }

    // 公式ブログ (BLOG) の描画
    function renderRaytusBlogs() {
      const container = document.getElementById('raytus-blog-grid');
      if (!container || typeof RAYTUS_BLOGS === 'undefined') return;

      container.innerHTML = RAYTUS_BLOGS.map(b => `
        <a href="${b.link}" target="_blank" class="group bg-[#121824] rounded-2xl overflow-hidden border border-slate-800 hover:border-amber-400/60 transition shadow-lg flex flex-col justify-between">
          <div>
            <div class="aspect-video w-full overflow-hidden bg-slate-900 relative">
              <img src="${b.image}" alt="${b.title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy">
              <span class="absolute top-2.5 left-2.5 px-2 py-0.5 rounded bg-black/70 text-amber-300 font-bold text-[10px] backdrop-blur-xs font-zen">
                REPORT
              </span>
            </div>
            <div class="p-4 sm:p-5">
              <span class="text-[11px] text-slate-400 font-mono">${b.date}</span>
              <h4 class="text-sm sm:text-base font-zen font-bold text-white group-hover:text-amber-300 transition mt-1.5 line-clamp-2 leading-snug">
                ${b.title}
              </h4>
            </div>
          </div>
          <div class="px-4 pb-4 pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs font-bold text-amber-400">
            <span>記事を読む</span>
            <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
          </div>
        </a>
      `).join('');
    }

    function renderRaytusServices() {'''

    if js_target in content:
        content = content.replace(js_target, js_new)
        print("Added JS functions renderRaytusShops and renderRaytusBlogs.")
    else:
        print("Warning: js_target not found.")

    # 6. Ensure renderRaytusShops and renderRaytusBlogs are called on tab switch / init
    init_target = 'if (typeof renderRaytusServices === \'function\') renderRaytusServices();'
    init_replacement = '''if (typeof renderRaytusServices === 'function') renderRaytusServices();
      if (typeof renderRaytusShops === 'function') renderRaytusShops();
      if (typeof renderRaytusBlogs === 'function') renderRaytusBlogs();'''
    if init_target in content:
        content = content.replace(init_target, init_replacement)
        print("Added init calls.")

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    with open("portal.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated index.html and portal.html successfully.")

run()

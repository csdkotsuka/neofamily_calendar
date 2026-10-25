#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restore category filter pill buttons, badges, and filtering logic for 加盟店紹介 (SHOP)
in index.html, portal.html, and standalone pages (raytus.html).
"""

import subprocess

def update_index_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update HTML Markup of SHOP Section
    start_str = '<div id="raytus-shop-section"'
    wrap_str = '<!-- 加盟店テーブル wrap -->'
    idx_start = content.find(start_str)
    idx_wrap = content.find(wrap_str, idx_start)

    if idx_start == -1 or idx_wrap == -1:
        print("ERROR: could not find shop section markup bounds")
        return False

    new_shop_markup = '''<div id="raytus-shop-section" class="bg-white rounded-3xl border border-slate-200/80 shadow-xs p-6 sm:p-10 lg:p-12 mb-8">
          
          <!-- 本家 sec-head 見出し -->
          <div class="raytus-sec-head">
            <p class="raytus-sec-head__en">SHOP</p>
            <h3 class="raytus-sec-head__ja">加盟店紹介</h3>
          </div>

          <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-6">
            <div>
              <p class="text-xs sm:text-sm text-slate-500 font-serif leading-relaxed">
                RAYTUS group.に加盟している全国の店舗・サービス一覧（全<span id="raytus-shop-count" class="text-amber-600 font-bold font-mono">85</span>件）。<br class="hidden sm:inline">
                提供商品のジャンル別ボタンやキーワードで絞り込みが可能です。行をタップすると各店舗の商品・詳細ページが開きます。
              </p>
            </div>
            
            <!-- 加盟店検索入力 -->
            <div class="relative w-full md:w-80 shrink-0">
              <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
              <input type="text" id="raytus-shop-search" oninput="renderRaytusShops()" placeholder="店舗名・代表者・商品・地域で検索..." class="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-amber-500 focus:bg-white transition font-zen">
            </div>
          </div>

          <!-- 提供商品 カテゴリ分類 切り替えピルバー (5大グループ) -->
          <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-3 mb-6 text-xs">
            <button onclick="setRaytusShopCategory('all')" id="shop-cat-all" class="shop-cat-btn px-4 py-2 rounded-xl transition bg-amber-500 text-slate-950 shadow-xs border border-amber-500 whitespace-nowrap font-zen font-bold cursor-pointer">
              🌟 すべて表示 (<span id="shop-count-all">85</span>)
            </button>
            <button onclick="setRaytusShopCategory('food')" id="shop-cat-food" class="shop-cat-btn px-4 py-2 rounded-xl transition bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900 border border-slate-200/80 whitespace-nowrap font-zen font-medium cursor-pointer">
              🍙 食・グルメ・スイーツ (<span id="shop-count-food">10</span>)
            </button>
            <button onclick="setRaytusShopCategory('beauty-health')" id="shop-cat-beauty-health" class="shop-cat-btn px-4 py-2 rounded-xl transition bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900 border border-slate-200/80 whitespace-nowrap font-zen font-medium cursor-pointer">
              💆‍♀️ 美容・健康・ボディケア (<span id="shop-count-beauty-health">24</span>)
            </button>
            <button onclick="setRaytusShopCategory('handmade-fashion')" id="shop-cat-handmade-fashion" class="shop-cat-btn px-4 py-2 rounded-xl transition bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900 border border-slate-200/80 whitespace-nowrap font-zen font-medium cursor-pointer">
              👗 ハンドメイド・服・雑貨 (<span id="shop-count-handmade-fashion">15</span>)
            </button>
            <button onclick="setRaytusShopCategory('fortune-healing')" id="shop-cat-fortune-healing" class="shop-cat-btn px-4 py-2 rounded-xl transition bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900 border border-slate-200/80 whitespace-nowrap font-zen font-medium cursor-pointer">
              🔮 占い・鑑定・心のケア (<span id="shop-count-fortune-healing">13</span>)
            </button>
            <button onclick="setRaytusShopCategory('education-business')" id="shop-cat-education-business" class="shop-cat-btn px-4 py-2 rounded-xl transition bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900 border border-slate-200/80 whitespace-nowrap font-zen font-medium cursor-pointer">
              💼 学び・ビジネス・制作 (<span id="shop-count-education-business">23</span>)
            </button>
          </div>

          '''

    content = content[:idx_start] + new_shop_markup + content[idx_wrap:]

    # 2. Update JavaScript logic for SHOP in index.html
    js_start_str = '// 加盟店一覧 (SHOP) の描画（ライトテーマ対応）'
    js_end_str = '// 31事業 (SERVICE) の描画（ライトテーマ対応カード）'
    idx_js_start = content.find(js_start_str)
    idx_js_end = content.find(js_end_str)

    if idx_js_start == -1 or idx_js_end == -1:
        print("ERROR: could not find shop js bounds")
        return False

    new_shop_js = '''// ============================================
    // 加盟店一覧 (SHOP) の絞り込み & 描画（ライトテーマ対応）
    // ============================================
    let currentShopCategory = 'all';

    const SHOP_CATEGORY_BADGES = {
      'food': '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-200">🍙 食・グルメ</span>',
      'beauty-health': '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-bold bg-pink-50 text-pink-700 border border-pink-200">💆‍♀️ 美容・健康</span>',
      'handmade-fashion': '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-bold bg-purple-50 text-purple-700 border border-purple-200">👗 ハンドメイド</span>',
      'fortune-healing': '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">🔮 占い・心のケア</span>',
      'education-business': '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-bold bg-blue-50 text-blue-700 border border-blue-200">💼 学び・ビジネス</span>'
    };

    function setRaytusShopCategory(cat) {
      currentShopCategory = cat;
      document.querySelectorAll('.shop-cat-btn').forEach(btn => {
        btn.className = 'shop-cat-btn px-4 py-2 rounded-xl transition bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900 border border-slate-200/80 whitespace-nowrap font-zen font-medium cursor-pointer';
      });
      const activeBtn = document.getElementById(`shop-cat-${cat}`);
      if (activeBtn) {
        activeBtn.className = 'shop-cat-btn px-4 py-2 rounded-xl transition bg-amber-500 text-slate-950 shadow-xs border border-amber-500 whitespace-nowrap font-zen font-bold cursor-pointer';
      }
      renderRaytusShops();
    }

    function renderRaytusShops() {
      const container = document.getElementById('raytus-shop-tbody');
      if (!container || typeof RAYTUS_SHOPS === 'undefined') return;
      const q = (document.getElementById('raytus-shop-search')?.value || '').toLowerCase().trim();
      const countEl = document.getElementById('raytus-shop-count');

      // 各カテゴリの件数カウント更新
      const counts = { all: RAYTUS_SHOPS.length, food: 0, 'beauty-health': 0, 'handmade-fashion': 0, 'fortune-healing': 0, 'education-business': 0 };
      RAYTUS_SHOPS.forEach(s => {
        if (s.category && counts[s.category] !== undefined) {
          counts[s.category]++;
        }
      });
      Object.keys(counts).forEach(k => {
        const el = document.getElementById(`shop-count-${k}`);
        if (el) el.textContent = counts[k];
      });

      const filtered = RAYTUS_SHOPS.filter(s => {
        if (currentShopCategory !== 'all' && s.category !== currentShopCategory) {
          return false;
        }
        if (!q) return true;
        return `${s.name} ${s.rep} ${s.product} ${s.area}`.toLowerCase().includes(q);
      });

      if (countEl) countEl.textContent = filtered.length;

      if (filtered.length === 0) {
        container.innerHTML = `
          <tr>
            <td colspan="4" class="p-10 text-center text-slate-400">
              <i class="fa-solid fa-store-slash text-2xl text-slate-300 mb-2 block"></i>
              <p class="text-xs font-medium text-slate-500">該当する加盟店は見つかりませんでした。</p>
              <button onclick="setRaytusShopCategory('all'); document.getElementById('raytus-shop-search').value = ''; renderRaytusShops();" class="mt-2.5 px-3 py-1 rounded-lg bg-amber-50 text-amber-700 text-xs font-bold border border-amber-200 hover:bg-amber-100 transition cursor-pointer">
                条件をリセット
              </button>
            </td>
          </tr>
        `;
        return;
      }

      container.innerHTML = filtered.map(s => {
        const catBadge = SHOP_CATEGORY_BADGES[s.category] || '';
        return `
        <tr class="hover:bg-amber-50/50 transition border-b border-slate-100 cursor-pointer group" onclick="window.open('${s.link}', '_blank')">
          <td class="p-3.5 sm:p-4 font-bold text-slate-900 break-words">
            <div class="space-y-1.5">
              ${catBadge}
              <div class="flex items-center gap-1.5 flex-wrap">
                <span class="group-hover:text-amber-700 transition leading-snug">${s.name}</span>
                <i class="fa-solid fa-arrow-up-right-from-square text-[10px] text-slate-400 group-hover:text-amber-600 transition shrink-0"></i>
              </div>
            </div>
          </td>
          <td class="p-3.5 sm:p-4 text-slate-700 break-words whitespace-nowrap font-medium leading-snug">${s.rep}</td>
          <td class="p-3.5 sm:p-4 text-slate-600 leading-relaxed text-xs break-words">${s.product}</td>
          <td class="p-3.5 sm:p-4 text-slate-500 whitespace-pre-line text-xs break-words leading-snug">${s.area}</td>
        </tr>
      `;
      }).join('');
    }

    '''

    content = content[:idx_js_start] + new_shop_js + content[idx_js_end:]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated index.html")

    with open('portal.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated portal.html")

    return True

if __name__ == '__main__':
    if update_index_html():
        subprocess.run(['python3', 'scripts/generate_standalone_pages.py'], check=True)
        print("Regenerated all standalone pages!")

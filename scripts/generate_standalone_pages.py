#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate standalone HTML pages from index.html
Separates the single-page tab container into dedicated, independent pages:
1. raytus.html
2. iyasaka.html
3. archive.html
4. sns.html
Updates calendar.html and index.html to have consistent unified navigation.
"""

import os
import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        src = f.read()

    # Common Head template
    head_match = re.search(r'(<!DOCTYPE html>.*?<body[^>]*>)', src, re.DOTALL)
    if not head_match:
        print("Failed to find header!")
        return

    # Navigation bar generator
    def get_navbar(active_page):
        items = [
            ('hub', './', 'fa-solid fa-compass', '総合ポータル', ''),
            ('flowchart', 'flowchart.html', 'fa-solid fa-gamepad text-amber-500', '参加フロー診断', '<span class="px-1.5 py-0.2 text-[9px] font-black rounded bg-rose-500 text-white animate-pulse">GAME</span>'),
            ('raytus', 'raytus.html', 'fa-solid fa-globe text-slate-400', 'RAYTUS 全事業', ''),
            ('iyasaka', 'iyasaka.html', 'fa-solid fa-torii-gate text-amber-600', 'Iyasaka宮', ''),
            ('calendar', 'calendar.html', 'fa-regular fa-calendar-days text-rose-500', 'イベントカレンダー', ''),
            ('archive', 'archive.html', 'fa-solid fa-graduation-cap text-indigo-500', '勉強会アーカイブ', ''),
            ('sns', 'sns.html', 'fa-solid fa-share-nodes text-pink-500', '公式SNS', '')
        ]

        nav_html = '      <nav class="flex items-center gap-1 overflow-x-auto no-scrollbar py-2 border-t border-slate-100 text-xs font-bold">\n'
        for key, url, icon, label, badge in items:
            if key == active_page:
                cls = "nav-item whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 bg-slate-900 text-white shadow-xs"
            else:
                cls = "nav-item whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 text-slate-600 hover:bg-slate-100"
            badge_html = f" {badge}" if badge else ""
            nav_html += f'        <a href="{url}" id="nav-item-{key}" class="{cls}">\n          <i class="{icon}"></i>\n          <span>{label}</span>{badge_html}\n        </a>\n'
        nav_html += '      </nav>\n'
        return nav_html

    # Header generator
    def get_header(active_page, page_title_sub="総合ポータル & 参加ナビゲーション"):
        return f'''  <!-- ========================================== -->
  <!-- メイン グローバルヘッダー -->
  <!-- ========================================== -->
  <header class="sticky top-0 z-40 glass-nav border-b border-slate-200/80 shadow-xs transition-all">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 md:h-18">
        
        <!-- ブランドロゴ & タイトル -->
        <a href="./" class="flex items-center gap-3 cursor-pointer group">
          <img src="images/logo.png" alt="NEO FAMILY Logo" class="w-10 h-10 md:w-11 md:h-11 rounded-full object-contain shadow-xs border border-amber-200/60 bg-white group-hover:scale-105 transition-transform">
          <div>
            <div class="flex items-center gap-2">
              <span class="font-display font-black text-base md:text-lg tracking-tight text-slate-900">NEO FAMILY</span>
              <span class="text-slate-300">×</span>
              <span class="font-serif font-bold text-sm md:text-base text-slate-800 tracking-wider">RAYTUS</span>
              <span class="px-1.5 py-0.5 text-[9px] font-black rounded-sm bg-amber-500/10 text-amber-700 border border-amber-300/40">PORTAL</span>
            </div>
            <p class="text-[11px] text-slate-500 font-medium hidden sm:block">{page_title_sub}</p>
          </div>
        </a>

        <!-- ヘッダー右側アクション -->
        <div class="flex items-center gap-2 sm:gap-3">
          <button onclick="copyZoomInfo()" class="hidden md:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-blue-50 text-blue-700 border border-blue-200/60 hover:bg-blue-100 transition shadow-2xs">
            <i class="fa-solid fa-video text-blue-500"></i>
            <span>全日共通Zoom</span>
          </button>
          <a href="flowchart.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-amber-50 text-amber-800 border border-amber-300/60 hover:bg-amber-100 transition shadow-2xs">
            <i class="fa-solid fa-gamepad text-amber-600"></i>
            <span>診断ゲーム</span>
          </a>
          <a href="admin.html" class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-xl text-xs font-bold text-slate-500 hover:text-slate-800 transition">
            <i class="fa-solid fa-lock text-[10px]"></i>
            <span class="hidden sm:inline">管理</span>
          </a>
        </div>
      </div>

{get_navbar(active_page)}
    </div>
  </header>

  <!-- ========================================== -->
  <!-- ⚡️ ベテラン向け クイックアクセス HUD -->
  <!-- ========================================== -->
  <section class="bg-white border-b border-slate-200 py-3.5 px-4 sm:px-6 shadow-2xs">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3 text-xs">
      <div class="flex items-center gap-2.5 w-full md:w-auto flex-wrap">
        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-amber-100 text-amber-900 font-extrabold text-[11px] shrink-0">
          <i class="fa-solid fa-bolt text-amber-600"></i> 直近の最重要予定
        </span>
        <div class="text-slate-700 flex flex-wrap items-center gap-1.5">
          <span class="font-bold">次回合同定例会:</span> <span class="bg-rose-50 text-rose-700 px-2 py-0.5 rounded-md font-bold">11/2(月) 13:00〜 福岡</span>
          <span class="hidden sm:inline text-slate-300">|</span>
          <span class="text-slate-600">合同事業説明会: 全日共通Zoom ID: <strong class="text-slate-900">811 1315 2898</strong> (PW: 2026)</span>
        </div>
      </div>
      <div class="flex items-center gap-2 shrink-0 w-full md:w-auto justify-start md:justify-end">
        <button onclick="copyZoomInfo()" class="px-3 py-1.5 rounded-lg bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold border border-indigo-200 transition flex items-center gap-1 text-xs">
          <i class="fa-solid fa-copy"></i>
          <span>Zoomコピー</span>
        </button>
        <a href="https://us06web.zoom.us/j/81113152898?pwd=rnUDogc0paequYOxCnvXYaSs3WngG3.1" target="_blank" class="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-bold transition flex items-center gap-1 text-xs">
          <i class="fa-solid fa-video"></i>
          <span>Zoom参加</span>
        </a>
        <a href="https://chouseisan.com/s?h=2733ccd431d846f8bccd9c3061c0bca3" target="_blank" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold transition flex items-center gap-1 text-xs">
          <i class="fa-solid fa-pen-to-square"></i>
          <span>参加表明</span>
        </a>
      </div>
    </div>
  </section>
'''

    # Modals, Footer and Scripts
    idx_footer = src.find('<!-- フッター -->')
    idx_main_close = src.find('</main>')
    
    footer_modals_scripts = src[idx_footer:]

    # HTML Head without title
    raw_head = src[:src.find('<title>')]
    raw_head_rest = src[src.find('</title>')+8:src.find('</head>')]

    def build_page_html(page_key, title, desc, main_content, init_scripts=''):
        page_head = f'''{raw_head}<title>{title}</title>
  <meta name="description" content="{desc}">{raw_head_rest}</head>
<body class="bg-slate-50 text-slate-800 antialiased selection:bg-rose-500 selection:text-white pb-20">

{get_header(page_key)}

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
{main_content}
  </main>

{footer_modals_scripts}
'''
        # Ensure tab-content has 'active' class so it displays
        page_head = page_head.replace('class="tab-content space-y-12"', 'class="tab-content active space-y-12"')
        page_head = page_head.replace('class="tab-content space-y-4"', 'class="tab-content active space-y-4"')
        page_head = page_head.replace('class="tab-content space-y-6"', 'class="tab-content active space-y-6"')
        page_head = page_head.replace('class="tab-content space-y-8"', 'class="tab-content active space-y-8"')

        return page_head

    # Extract TAB 2 (RAYTUS)
    t2_start = src.find('<!-- TAB 2: RAYTUS group')
    t3_start = src.find('<!-- TAB 3: Iyasaka宮')
    t2_content = src[t2_start:t3_start]
    raytus_html = build_page_html(
        'raytus',
        'RAYTUS group 公式HP & 全31事業紹介・動画アーカイブ | NEO FAMILY × RAYTUS',
        'RAYTUS groupの理念、全31事業の詳細・想い・公式YouTube紹介動画、教育支援プロジェクトを完全集約。',
        t2_content
    )
    with open('raytus.html', 'w', encoding='utf-8') as f:
        f.write(raytus_html)
    print("Wrote raytus.html")

    # Extract TAB 3 (IYASAKA)
    t4_start = src.find('<!-- TAB 4: イベントカレンダー')
    t3_content = src[t3_start:t4_start]
    iyasaka_html = build_page_html(
        'iyasaka',
        'Iyasaka宮 特設ページ & マルシェEC体験 | NEO FAMILY × RAYTUS',
        '日本古来の精神とテクノロジーが融合したIyasaka宮。ライブ配信・会員限定マルシェEC体験・出店者サポート。',
        t3_content
    )
    with open('iyasaka.html', 'w', encoding='utf-8') as f:
        f.write(iyasaka_html)
    print("Wrote iyasaka.html")

    # Extract TAB 5 (ARCHIVE)
    t5_start = src.find('<!-- TAB 5: 事業紹介 & アーカイブ集')
    t6_start = src.find('<!-- TAB 6: 公式SNSメディア')
    t5_content = src[t5_start:t6_start]
    archive_html = build_page_html(
        'archive',
        '特別勉強会 & 定例会 動画アーカイブ集 | NEO FAMILY × RAYTUS',
        'NEO FAMILYの過去の特別勉強会・合同定例会・実践講義動画をカテゴリ別に整理した完全アーカイブ集。',
        t5_content
    )
    with open('archive.html', 'w', encoding='utf-8') as f:
        f.write(archive_html)
    print("Wrote archive.html")

    # Extract TAB 6 (SNS)
    t6_content = src[t6_start:idx_main_close]
    sns_html = build_page_html(
        'sns',
        '公式SNS・Instagram最新投稿・ぶった斬り会長チャンネル | NEO FAMILY × RAYTUS',
        'ぶった斬り会長 公式YouTube・TikTok、RAYTUS group公式Instagramの最新投稿・メディア情報を一堂に集約。',
        t6_content
    )
    with open('sns.html', 'w', encoding='utf-8') as f:
        f.write(sns_html)
    print("Wrote sns.html")

if __name__ == '__main__':
    main()

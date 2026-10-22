#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update navigation bar in header
old_nav = '''      <!-- ========================================== -->
      <!-- メインタブバー（各複製コンテンツへの切り替え） -->
      <!-- ========================================== -->
      <nav class="flex items-center gap-1 overflow-x-auto no-scrollbar py-2 border-t border-slate-100 text-xs font-bold">
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

new_nav = '''      <!-- ========================================== -->
      <!-- 統一グローバルナビゲーション（個別ページ遷移） -->
      <!-- ========================================== -->
      <nav class="flex items-center gap-1 overflow-x-auto no-scrollbar py-2 border-t border-slate-100 text-xs font-bold">
        <a href="./" id="nav-item-hub" class="nav-item whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 bg-slate-900 text-white shadow-xs">
          <i class="fa-solid fa-compass"></i>
          <span>総合ポータル</span>
        </a>
        <a href="flowchart.html" id="nav-item-flowchart" class="nav-item whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 text-slate-600 hover:bg-slate-100">
          <i class="fa-solid fa-gamepad text-amber-500"></i>
          <span>参加フロー診断</span> <span class="px-1.5 py-0.2 text-[9px] font-black rounded bg-rose-500 text-white animate-pulse">GAME</span>
        </a>
        <a href="raytus.html" id="nav-item-raytus" class="nav-item whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 text-slate-600 hover:bg-slate-100">
          <i class="fa-solid fa-globe text-slate-400"></i>
          <span>RAYTUS 全事業</span>
        </a>
        <a href="iyasaka.html" id="nav-item-iyasaka" class="nav-item whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 text-slate-600 hover:bg-slate-100">
          <i class="fa-solid fa-torii-gate text-amber-600"></i>
          <span>Iyasaka宮</span>
        </a>
        <a href="calendar.html" id="nav-item-calendar" class="nav-item whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 text-slate-600 hover:bg-slate-100">
          <i class="fa-regular fa-calendar-days text-rose-500"></i>
          <span>イベントカレンダー</span>
        </a>
        <a href="archive.html" id="nav-item-archive" class="nav-item whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 text-slate-600 hover:bg-slate-100">
          <i class="fa-solid fa-graduation-cap text-indigo-500"></i>
          <span>勉強会アーカイブ</span>
        </a>
        <a href="sns.html" id="nav-item-sns" class="nav-item whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 text-slate-600 hover:bg-slate-100">
          <i class="fa-solid fa-share-nodes text-pink-500"></i>
          <span>公式SNS</span>
        </a>
      </nav>'''

if old_nav in text:
    text = text.replace(old_nav, new_nav, 1)
    print("Nav replaced in index.html")
else:
    print("old_nav not found")

# 2. Update Step 2 button to link to flowchart.html
old_step2_btn = '''              <button onclick="scrollToSection('flowchart-section')" class="mt-3.5 text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1.5 px-3 py-2 rounded-lg bg-blue-50 hover:bg-blue-100 transition w-full sm:w-auto justify-center sm:justify-start">
                <i class="fa-solid fa-diagram-project"></i>
                <span>フローチャートで診断</span>
                <i class="fa-solid fa-arrow-right text-[10px] ml-1"></i>
              </button>'''

new_step2_btn = '''              <a href="flowchart.html" class="mt-3.5 text-xs font-bold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 flex items-center gap-2 px-4 py-2.5 rounded-xl shadow-xs transition w-full sm:w-auto justify-center sm:justify-start group">
                <i class="fa-solid fa-gamepad text-amber-300"></i>
                <span>実際に動かせる診断ゲームをプレイ</span>
                <i class="fa-solid fa-arrow-right text-[10px] ml-1 group-hover:translate-x-1 transition-transform"></i>
              </a>'''

if old_step2_btn in text:
    text = text.replace(old_step2_btn, new_step2_btn, 1)
    print("Step 2 button updated to link to flowchart.html")

# 3. Update Flowchart Section in index.html to feature the interactive game prominently
old_flowchart_sec = '''      <!-- フローチャート セクション -->
      <section id="flowchart-section" class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
        <div>
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-bold mb-2">
            <i class="fa-solid fa-arrows-split-up-and-left"></i> 迷ったらまずここ！
          </span>
          <h3 class="text-xl font-black text-slate-900">
            🏹 説明会 / 作業会 参加フローチャート & サポート一覧
          </h3>
          <p class="text-xs text-slate-500 mt-1">※画像をタップすると全画面で拡大表示されます</p>
        </div>'''

new_flowchart_sec = '''      <!-- フローチャート セクション（ゲーム感覚診断 & サポート一覧） -->
      <section id="flowchart-section" class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-bold mb-2">
              <i class="fa-solid fa-arrows-split-up-and-left"></i> 迷ったらまずここ！
            </span>
            <h3 class="text-xl sm:text-2xl font-black text-slate-900">
              🏹 説明会 / 作業会 参加フローチャート & サポート一覧
            </h3>
            <p class="text-xs text-slate-500 mt-1">
              今の自分のフェーズにぴったりの説明会・作業会・Zoomを楽しくゲーム感覚で判定！
            </p>
          </div>
          <a href="flowchart.html" class="px-5 py-3 rounded-2xl bg-gradient-to-r from-amber-500 via-rose-500 to-indigo-600 text-white font-black text-xs sm:text-sm shadow-md hover:scale-102 transition flex items-center justify-center gap-2 shrink-0">
            <i class="fa-solid fa-gamepad text-amber-200"></i>
            <span>診断ゲームを開く (専用ページ)</span>
            <i class="fa-solid fa-chevron-right text-xs"></i>
          </a>
        </div>

        <!-- 🎮 特設ゲーム案内バナー -->
        <div class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-6 sm:p-7 shadow-md">
          <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="space-y-2 max-w-xl">
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-full bg-amber-400 text-slate-950 font-black text-[11px]">NEW! 動かせる体験</span>
                <span class="text-xs text-rose-300 font-bold">NEO QUEST: イベント参加診断</span>
              </div>
              <h4 class="text-lg sm:text-xl font-black text-white">
                質問にポチポチ答えるだけ！今のあなたにピッタリの会を自動判定！
              </h4>
              <p class="text-xs text-slate-300 leading-relaxed">
                「出店したいけど準備は何から？」「最新情報に追いつくには？」をゲーム感覚で楽しくナビゲート。通ったルートが光る全体マップや、サポート一覧表との連動ハイライトも搭載！
              </p>
            </div>
            <a href="flowchart.html" class="px-6 py-3.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-sm transition shadow-lg flex items-center justify-center gap-2 shrink-0">
              <i class="fa-solid fa-play"></i>
              <span>クエストをスタートする</span>
            </a>
          </div>
        </div>'''

if old_flowchart_sec in text:
    text = text.replace(old_flowchart_sec, new_flowchart_sec, 1)
    print("Flowchart section updated in index.html")

# 4. Fallback in switchTab to navigate to separate pages if user triggers it
old_switch_tab = '''    // タブ切替
    function switchTab(tabId) {'''

new_switch_tab = '''    // タブ切替（個別ページへのフォールバック対応）
    function switchTab(tabId) {
      const pageMap = {
        'hub': './',
        'flowchart': 'flowchart.html',
        'raytus': 'raytus.html',
        'iyasaka': 'iyasaka.html',
        'calendar': 'calendar.html',
        'archive': 'archive.html',
        'sns': 'sns.html'
      };
      // If separate page exists and target is not hub, redirect for clean independent pages
      if (pageMap[tabId] && tabId !== 'hub') {
        window.location.href = pageMap[tabId];
        return;
      }'''

if old_switch_tab in text:
    text = text.replace(old_switch_tab, new_switch_tab, 1)
    print("switchTab updated to redirect to standalone pages")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

# Also update portal.html to match index.html
with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated index.html and portal.html successfully")

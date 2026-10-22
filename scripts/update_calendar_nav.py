#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('calendar.html', 'r', encoding='utf-8') as f:
    text = f.read()

calendar_nav = """      <!-- ========================================== -->
      <!-- 統一グローバルナビゲーション（個別ページ遷移） -->
      <!-- ========================================== -->
      <nav class="flex items-center gap-1 overflow-x-auto no-scrollbar py-2 border-t border-slate-100 text-xs font-bold">
        <a href="./" id="nav-item-hub" class="nav-item whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 text-slate-600 hover:bg-slate-100">
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
        <a href="calendar.html" id="nav-item-calendar" class="nav-item whitespace-nowrap px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 bg-slate-900 text-white shadow-xs">
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
      </nav>
    </div>
  </header>"""

old_header_end = '    </div>\n  </header>'
if old_header_end in text:
    text = text.replace(old_header_end, calendar_nav, 1)
    with open('calendar.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Successfully updated calendar.html')
else:
    print('Target string not found')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

files = ['raytus.html', 'iyasaka.html', 'archive.html', 'sns.html']

smart_switch_tab = """    // タブ切替（個別ページ間のシームレス遷移）
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
      const currentPage = window.location.pathname.split('/').pop() || 'index.html';
      const targetPage = pageMap[tabId];
      if (targetPage && !currentPage.includes(targetPage.replace('.html', ''))) {
        window.location.href = targetPage;
        return;
      }
"""

for fn in files:
    with open(fn, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Replace the beginning of switchTab
    c = c.replace("    // タブ切替\n    function switchTab(tabId) {\n", smart_switch_tab)
    c = c.replace("    function switchTab(tabId) {\n", smart_switch_tab)
    
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Updated switchTab in {fn}")

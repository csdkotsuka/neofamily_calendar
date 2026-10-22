#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob

files = ['archive.html', 'sns.html', 'raytus.html', 'iyasaka.html', 'index.html', 'portal.html']

single_switch_tab = """    // タブ切替（個別ページ間のシームレス遷移）
    function switchTab(tabId) {
      const pageMap = {
        'hub': './',
        'flowchart': 'flowchart',
        'raytus': 'raytus',
        'iyasaka': 'iyasaka',
        'calendar': 'calendar',
        'archive': 'archive',
        'sns': 'sns'
      };
      const currentPage = window.location.pathname.split('/').pop() || 'index.html';
      const targetPage = pageMap[tabId];
      if (targetPage && !currentPage.includes(targetPage.replace('.html', ''))) {
        window.location.href = targetPage;
        return;
      }
      if (tabId === 'schedule') {
        tabId = 'hub';
        setTimeout(() => scrollToSection('schedule-section'), 150);
      }
      if (tabId === 'archive') {
        tabId = 'raytus';
        setTimeout(() => scrollToSection('raytus-services-section'), 150);
      }
"""

duplicate_block_marker = """    // タブ切替（個別ページ間のシームレス遷移）
    // タブ切替（個別ページ間のシームレス遷移）
    function switchTab(tabId) {
      const pageMap = {
        'hub': './',
        'flowchart': 'flowchart',
        'raytus': 'raytus',
        'iyasaka': 'iyasaka',
        'calendar': 'calendar',
        'archive': 'archive',
        'sns': 'sns'
      };
      const currentPage = window.location.pathname.split('/').pop() || 'index.html';
      const targetPage = pageMap[tabId];
      if (targetPage && !currentPage.includes(targetPage.replace('.html', ''))) {
        window.location.href = targetPage;
        return;
      }
      const pageMap = {
        'hub': './',
        'flowchart': 'flowchart',
        'raytus': 'raytus',
        'iyasaka': 'iyasaka',
        'calendar': 'calendar',
        'archive': 'archive',
        'sns': 'sns'
      };
      const currentPage = window.location.pathname.split('/').pop() || 'index.html';
      const targetPage = pageMap[tabId];
      if (targetPage && !currentPage.includes(targetPage.replace('.html', ''))) {
        window.location.href = targetPage;
        return;
      }
      if (tabId === 'schedule') {
        tabId = 'hub';
        setTimeout(() => scrollToSection('schedule-section'), 150);
      }
      if (tabId === 'archive') {
        tabId = 'raytus';
        setTimeout(() => scrollToSection('raytus-services-section'), 150);
      }
"""

for fn in files:
    with open(fn, 'r', encoding='utf-8') as f:
        c = f.read()
    
    if duplicate_block_marker in c:
        c = c.replace(duplicate_block_marker, single_switch_tab)
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Fixed duplicate switchTab in {fn}")
    else:
        # Check if there are other duplicate patterns
        count = c.count("const pageMap = {")
        if count > 1:
            print(f"Warning: {fn} has {count} occurrences of pageMap")

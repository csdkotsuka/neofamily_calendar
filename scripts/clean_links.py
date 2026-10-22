#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import re

html_files = glob.glob('*.html')

# Update links in all HTML files
for fn in html_files:
    with open(fn, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Replace href="xxx.html" with href="xxx" (excluding index.html and admin.html)
    c = c.replace('href="flowchart.html"', 'href="flowchart"')
    c = c.replace('href="./flowchart.html"', 'href="flowchart"')
    c = c.replace('href="raytus.html"', 'href="raytus"')
    c = c.replace('href="./raytus.html"', 'href="raytus"')
    c = c.replace('href="iyasaka.html"', 'href="iyasaka"')
    c = c.replace('href="./iyasaka.html"', 'href="iyasaka"')
    c = c.replace('href="calendar.html"', 'href="calendar"')
    c = c.replace('href="./calendar.html"', 'href="calendar"')
    c = c.replace('href="archive.html"', 'href="archive"')
    c = c.replace('href="./archive.html"', 'href="archive"')
    c = c.replace('href="sns.html"', 'href="sns"')
    c = c.replace('href="./sns.html"', 'href="sns"')

    # Replace switchTab target mappings if any
    c = c.replace("'flowchart.html'", "'flowchart'")
    c = c.replace("'raytus.html'", "'raytus'")
    c = c.replace("'iyasaka.html'", "'iyasaka'")
    c = c.replace("'calendar.html'", "'calendar'")
    c = c.replace("'archive.html'", "'archive'")
    c = c.replace("'sns.html'", "'sns'")

    with open(fn, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Cleaned URLs in {fn}")

# Also update js/flowchart-game.js
with open('js/flowchart-game.js', 'r', encoding='utf-8') as f:
    fg = f.read()
fg = fg.replace('calendar.html', 'calendar')
fg = fg.replace('archive.html', 'archive')
fg = fg.replace('raytus.html', 'raytus')
fg = fg.replace('iyasaka.html', 'iyasaka')
with open('js/flowchart-game.js', 'w', encoding='utf-8') as f:
    f.write(fg)
print("Updated js/flowchart-game.js")

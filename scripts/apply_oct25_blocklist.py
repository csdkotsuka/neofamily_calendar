import json
import re

# 1. Load current blocklist JSON
with open('js/blocklist-data.json', 'r', encoding='utf-8') as f:
    blocklist = json.load(f)

print(f"Current count: {len(blocklist)}")
assert len(blocklist) == 770, f"Expected 770 items, found {len(blocklist)}"

# 2. Update blk_085 with Threads secondary_url and merged reason
updated_085 = False
for item in blocklist:
    if item['id'] == 'blk_085':
        item['secondary_url'] = "https://www.threads.com/@kodomo_mirai_ouentai"
        item['platform'] = "Instagram / Threads"
        new_reason = "【2026-10-25 中嶋初美（glowell / 大阪）報告】腹が立ちました。コメントは、恐らくお仲間の方かと思いますが、投稿主はブロックで良いかと思います！"
        if item.get('reason'):
            item['reason'] = item['reason'] + "\n" + new_reason
        else:
            item['reason'] = new_reason
        updated_085 = True
        print(f"Updated blk_085: secondary_url set, platform={item['platform']}")
        break
assert updated_085, "blk_085 not found!"

# 3. New entries to add
new_entries = [
  {
    "date": "2026-10-24 16:21",
    "reporter": "服部達典（MURA）",
    "name": "黒原めいな｜ケルベロスDr. (@meina_clo)",
    "url": "https://www.instagram.com/meina_clo?dlrf=MTBzc2x6eXlyejh1OA==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-25 at 20.34.35.png",
    "id": "blk_771",
    "serialNo": 771
  },
  {
    "date": "2026-10-24 16:48",
    "reporter": "井峯明香奈（shAdow）",
    "name": "ひらち (@hirachi_ceo)",
    "url": "https://www.threads.com/@hirachi_ceo?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-25 at 20.34.35.png",
    "id": "blk_772",
    "serialNo": 772
  },
  {
    "date": "2026-10-24 16:49",
    "reporter": "井峯明香奈（shAdow）",
    "name": "RIVER (@river_cangoxina)",
    "url": "https://www.threads.com/@river_cangoxina?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-25 at 20.34.35.png",
    "id": "blk_773",
    "serialNo": 773
  },
  {
    "date": "2026-10-24 21:35",
    "reporter": "坂本有莉菜（Mimola）",
    "name": "りくまま⌇多忙看護師ママの辞める道 (@riku_nurse.mama)",
    "url": "https://www.instagram.com/riku_nurse.mama?srtk=MWNkOTBuYjM2MGdjbA==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "聞いたことある〜から根掘り葉掘り聞いてきます。自分の人生たのし〜なのでおせっかい不用です。",
    "image": "Screenshot 2026-10-25 at 20.34.35.png",
    "id": "blk_774",
    "serialNo": 774
  },
  {
    "date": "2026-10-24 23:17",
    "reporter": "岸部千夏（Couleur）",
    "name": "Azusa｜HSP専門キャリアコーチ&カウンセラー (@life_dorm.azusa)",
    "url": "https://www.threads.com/@life_dorm.azusa",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-25 at 20.34.35.png",
    "id": "blk_775",
    "serialNo": 775
  },
  {
    "date": "2026-10-25 06:34",
    "reporter": "長野さとみ（Ablaze）",
    "name": "Camila Valentina（会長偽アカウント）",
    "url": "https://www.instagram.com/camila812583?cplk=ZWJvYzc1dXI5dXN6",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "会長の偽アカです",
    "image": "Screenshot 2026-10-25 at 20.34.29.png",
    "id": "blk_776",
    "serialNo": 776
  },
  {
    "date": "2026-10-25 08:34",
    "reporter": "服部達典（MURA）",
    "name": "ゆん🌈34歳で大学病院勤務を退職してフリーランス看護師に転身した3児のママ (@yunyun.kazamaura)",
    "url": "https://www.instagram.com/yunyun.kazamaura?psln=MWRIdjBiaWl5bXluYg==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "ネットワークに集中したいとのことです。",
    "image": "Screenshot 2026-10-25 at 20.34.29.png",
    "id": "blk_777",
    "serialNo": 777
  },
  {
    "date": "2026-10-25 16:34",
    "reporter": "いわやともみ（Blooming / 東京）",
    "name": "Rin★🐱 (@rinrin_neko)",
    "url": "https://www.instagram.com/rinrin_neko?cplk=MXFjYmUzczVtNHo2Mg==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-25 at 20.34.29.png",
    "id": "blk_778",
    "serialNo": 778
  },
  {
    "date": "2026-10-25 16:34",
    "reporter": "小西みゆき（Mimola）",
    "name": "会長なりすまし（TikTok Lite）",
    "url": "https://lite.tiktok.com/t/ZS9ydKNtKv7xS-8wliv/",
    "secondary_url": "",
    "platform": "TikTok",
    "url_warning": "",
    "reason": "会長のなりすましです",
    "image": "Screenshot 2026-10-25 at 20.34.29.png",
    "id": "blk_779",
    "serialNo": 779
  },
  {
    "date": "2026-10-25 20:26",
    "reporter": "畠山尚美",
    "name": "momikaemasa (@momikaemasa)",
    "url": "https://www.threads.com/@momikaemasa?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "何度もネオファミリーの話しは聞いてる\nネクストエイドが1番とやってるそう。\nネオに入る気全くなく時間の無駄です",
    "image": "Screenshot 2026-10-25 at 20.34.29.png",
    "id": "blk_780",
    "serialNo": 780
  }
]

print(f"Adding {len(new_entries)} new entries...")
blocklist.extend(new_entries)
print(f"New total: {len(blocklist)}")

# 4. Save JSON
with open('js/blocklist-data.json', 'w', encoding='utf-8') as f:
    json.dump(blocklist, f, ensure_ascii=False, indent=2)

# 5. Save JS
with open('js/blocklist-data.js', 'w', encoding='utf-8') as f:
    f.write("/**\n * NEO FAMILY Calendar - Blocklist Data (v5 Enriched Profile Names)\n")
    f.write(f" * Total items: {len(blocklist)}\n */\n")
    f.write("var INITIAL_BLOCKLIST = " + json.dumps(blocklist, ensure_ascii=False, indent=2) + ";\n")

print("Updated js/blocklist-data.json and js/blocklist-data.js successfully!")

# 6. Update blocklist_raw_transcription.md
with open('blocklist_raw_transcription.md', 'r', encoding='utf-8') as f:
    md = f.read()

md = re.sub(r'# LINE Note ブロックリスト スクリーンショット純粋文字起こし（全\d+枚）', '# LINE Note ブロックリスト スクリーンショット純粋文字起こし（全119枚）', md)
md = re.sub(r'提供いただいた全\d+枚のスクリーンショット', '提供いただいた全119枚のスクリーンショット', md)

new_transcriptions = '''
## [115/119] `Screenshot 2026-10-25 at 20.34.58.png`
```text
服部達典/MURA
https://www.instagram.com/kosodatemama0524?rpxt=YmxrZ2RpcDMxbjc1
https://www.instagram.com/cherilu_yn?maxt=bGlqMDhmbjJOczRu
https://www.instagram.com/herb_nemokoro?rpxt=ZzImaWpucHFqMHEx
https://www.instagram.com/romy.yade?exln=ajdhcnYxYmx5Nmsx
Two days ago at 5:08 AM

森崎江里／愛知県/RAYTUS
誰かのやりとり、スクショで晒されてますい。
コメントのやつも報告とブロックお願いします
Two days ago at 8:22 AM

齊藤唯/Mimola
https://www.threads.com/@magier_2023?igshid=NTc4MTIwNjQ2YQ==
Two days ago at 8:49 AM

森崎江里／愛知県/RAYTUS
https://www.threads.com/@rina.s0527
Two days ago at 9:28 AM

相良沙織/Meguria理事長
@森崎江里／愛知県/RAYTUS さんのいう方のリンクはこちら
通報もよろしくお願い申し上げます。
https://www.threads.com/@rina.s0527
Two days ago at 9:46 AM

坂本有莉菜/Mimola
https://www.threads.com/@tomopooh1113?igshid=NTc4MTIwNjQ2YQ==
Two days ago at 11:19 AM
```

## [116/119] `Screenshot 2026-10-25 at 20.34.49.png`
```text
井峯明香奈/shAdow
https://www.threads.com/@shimosonet?igshid=NTc4MTIwNjQ2YQ==
Two days ago at 2:27 PM

畑ゆかり/yuima-ru理事長
ぶった斬り会長・・名指しでした
https://www.threads.com/@matsunaga_haruna?igshid=NTc4MTIwNjQ2YQ==
Two days ago at 3:09 PM

井峯明香奈/shAdow
https://www.threads.com/@yokoyama_ibaraki?igshid=NTc4MTIwNjQ2YQ==
Two days ago at 5:43 PM

城間千聖/enLIGHT
https://www.instagram.com/artmake_momoka?exln=b29zenRzcjUybThs
Two days ago at 7:54 PM

石崎七菜子/tEaM_S.
ファーストして興味あるフリして、なんの断りもなくブロック＆zoom来ずでした
https://www.threads.com/@holitaku_pickleball
Two days ago at 8:42 PM

ロジャーズ優衣\\enchant+
https://www.threads.com/@poochan5676?igshid=NTc4MTIwNjQ2YQ==
Two days ago at 10:37 PM
```

## [117/119] `Screenshot 2026-10-25 at 20.34.41.png`
```text
Two days ago at 10:37 PM

ロジャーズ優衣\\enchant+
https://www.instagram.com/ayumi.reborn?xtok=MXRkZzUwaWlwdm5leA==
Two days ago at 10:57 PM

小野八音/yaShine
何度も声かけいただき
ZOOMもしてお断りしました、とのことです！
https://www.instagram.com/tomo.ninkatsueiyou?srtk=MWxtYjJ4aWM3bXlodg==
Two days ago at 11:34 PM

桝田和裕/AMATERAS
https://www.threads.com/@nobu491004?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 12:16 AM

南藍/tidy.shin代表
言っていることに信ぴょう性がなく、マウント取ってくる。
https://www.threads.com/@mochi_creative123?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 12:43 AM

城間千聖/enLIGHT
https://www.instagram.com/sato_aoi_photo?psln=MWp5bGtncmZpYTE4OA==
何度も声かけしているようです。Zoom面談をした上でお断りしたそう。
Yesterday at 9:44 AM

ロジャーズ優衣\\enchant+
https://www.threads.com/@nijirosinkyu?igshid=NTc4MTIwNjQ2YQ==
https://www.instagram.com/nijirosinkyu?vrfl=MWg3M2oyM25uN2xtYg==
向こうからメッセージをいただきましたが、NEOに会うのは3回目だったそうです🙏
Yesterday at 10:10 AM
```

## [118/119] `Screenshot 2026-10-25 at 20.34.35.png`
```text
だったそうです🙏
Yesterday at 10:10 AM

服部達典/MURA
https://www.instagram.com/mayu_coach.mama?psln=MThpd2lycW5jamo5Mw==
Yesterday at 12:51 PM

服部達典/MURA
https://www.instagram.com/meina_clo?dlrf=MTBzc2x6eXlyejh1OA==
Yesterday at 4:21 PM

井峯明香奈/shAdow
https://www.threads.com/@naomi_futoukoukids_mama?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 4:45 PM

井峯明香奈/shAdow
https://www.threads.com/@hiroshi_yamauchi_55?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 4:47 PM

井峯明香奈/shAdow
https://www.threads.com/@hirachi_ceo?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 4:48 PM

井峯明香奈/shAdow
https://www.threads.com/@river_cangoxina?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 4:49 PM

坂本有莉菜/Mimola
聞いたことある〜から
根掘り葉掘り聞いてきます。
自分の人生たのし〜なので
おせっかい不用です。
https://www.instagram.com/riku_nurse.mama?srtk=MWNkOTBuYjM2MGdjbA==
Yesterday at 9:35 PM

岸部千夏/Couleur
https://www.threads.com/@life_dorm.azusa
Yesterday at 11:17 PM
```

## [119/119] `Screenshot 2026-10-25 at 20.34.29.png`
```text
長野さとみ/Ablaze
会長の偽アカです
https://www.instagram.com/camila812583?cplk=ZWJvYzc1dXI5dXN6
14 hours ago

服部達典/MURA
https://www.instagram.com/yunyun.kazamaura?psln=MWRIdjBiaWl5bXluYg==
ネットワークに集中したいとのことです。
12 hours ago

いわやともみ/Blooming/東京
https://www.instagram.com/rinrin_neko?cplk=MXFjYmUzczVtNHo2Mg==
4 hours ago

小西みゆき/Mimola
会長のなりすましです
https://lite.tiktok.com/t/ZS9ydKNtKv7xS-8wliv/
4 hours ago

中嶋初美/glowell/大阪
腹が立ちました。
コメントは、恐らくお仲間の方かと思いますが、投稿主はブロック
で良いかと思います！
https://www.threads.com/@kodomo_mirai_ouentai
53 minutes ago

畠山尚美
https://www.threads.com/@momikaemasa?igshid=NTc4MTIwNjQ2YQ==
何度もネオファミリーの話しは聞いてる

ネクストエイドが1番とやってるそう。
ネオに入る気全くなく時間の無駄です
8 minutes ago
```
'''

md = md.strip() + "\n" + new_transcriptions

with open('blocklist_raw_transcription.md', 'w', encoding='utf-8') as f:
    f.write(md)

print("Updated blocklist_raw_transcription.md successfully!")

# 7. Update cache buster in admin.html
with open('admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

admin_html = re.sub(r'blocklist-data\.js\?v=[^"]+', 'blocklist-data.js?v=20261025_1', admin_html)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("Updated admin.html cache buster to 20261025_1")

# 8. Update sw.js cache name
with open('sw.js', 'r', encoding='utf-8') as f:
    sw_js = f.read()

sw_js = re.sub(r'neofamily-cache-v[^\"]+', 'neofamily-cache-v20261025_1', sw_js)

with open('sw.js', 'w', encoding='utf-8') as f:
    f.write(sw_js)

print("Updated sw.js CACHE_NAME to neofamily-cache-v20261025_1")

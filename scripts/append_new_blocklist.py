import json
import re

# Load existing JSON
with open('js/blocklist-data.json', 'r', encoding='utf-8') as f:
    blocklist = json.load(f)

print(f"Current count: {len(blocklist)}")
assert len(blocklist) == 722

new_entries = [
  {
    "date": "2026-10-20 22:45",
    "reporter": "望月真美（yaShine）",
    "name": "マタニティ整体│訪問施術│札幌",
    "url": "https://www.instagram.com/chaba_sapporo_seitai?psln=MTR6YWp6exVjcHpzNg==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "3回ここの話を聞いてます。興味ありません！との事です",
    "image": "Screenshot 2026-10-22 at 10.55.55.png",
    "id": "blk_723",
    "serialNo": 723
  },
  {
    "date": "2026-10-21 04:06",
    "reporter": "服部達典（MURA）",
    "name": "あゆ｜21時からのノンアル晩酌",
    "url": "https://www.instagram.com/ayu_otsumami_?xtok=bGtxcGt2MijdvMjli",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.55.png",
    "id": "blk_724",
    "serialNo": 724
  },
  {
    "date": "2026-10-21 08:53",
    "reporter": "服部達典（MURA）",
    "name": "cafe すわろう",
    "url": "https://www.instagram.com/cafe.swallow?exln=YzM2Zno4d2FrdWpo",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.55.png",
    "id": "blk_725",
    "serialNo": 725
  },
  {
    "date": "2026-10-21 11:21",
    "reporter": "服部達典（MURA）",
    "name": "itoeri_",
    "url": "https://www.instagram.com/itoeri_?dlrf=N213aTN5YzlaNzl=",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.55.png",
    "id": "blk_726",
    "serialNo": 726
  },
  {
    "date": "2026-10-21 13:19",
    "reporter": "大森幸子（tidy.shin / 兵庫県加古川）",
    "name": "稚菜",
    "url": "https://www.instagram.com/lc5rots7?rpxt=aTIweTFqdGMxZINi",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.55.png",
    "id": "blk_727",
    "serialNo": 727
  },
  {
    "date": "2026-10-21 13:21",
    "reporter": "大森幸子（tidy.shin / 兵庫県加古川）",
    "name": "yumi_hogushi",
    "url": "https://www.instagram.com/yumi_hogushi?rpxt=MiVmZjUyMDZldmhz",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.55.png",
    "id": "blk_728",
    "serialNo": 728
  },
  {
    "date": "2026-10-21 14:13",
    "reporter": "雨宮ありさ（yaShine）",
    "name": "Buddy Home 湘南｜保護犬活動",
    "url": "https://www.threads.com/@kajik.awa?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.41.png",
    "id": "blk_729",
    "serialNo": 729
  },
  {
    "date": "2026-10-21 14:22",
    "reporter": "小松由衣（Mimola）",
    "name": "青森県　弘前市　FULFILL Dog Saron",
    "url": "https://www.instagram.com/fulfill.dog.training?xtok=ZDJWM2psaTh4YnUw",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.41.png",
    "id": "blk_730",
    "serialNo": 730
  },
  {
    "date": "2026-10-21 14:35",
    "reporter": "大野紗弥加（MURA）",
    "name": "kotoko irie",
    "url": "https://www.instagram.com/kotoko.i?vrfl=MXEzYjJ10G950HhxcQ==",
    "secondary_url": "https://www.threads.com/@kOtOko.i",
    "platform": "Instagram / Threads",
    "url_warning": "",
    "reason": "アンチのコメントに乗っかってコメントしていた方。本日のアポもドタキャンでした。他の何人かとも話すって書いてあったので、気をつけてください。",
    "image": "Screenshot 2026-10-22 at 10.55.41.png",
    "id": "blk_731",
    "serialNo": 731
  },
  {
    "date": "2026-10-21 15:11",
    "reporter": "草間真衣（MURA）",
    "name": "【公式】料理研究家　指宿さゆり",
    "url": "https://www.threads.com/@sayuri.ibusuki?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.41.png",
    "id": "blk_732",
    "serialNo": 732
  },
  {
    "date": "2026-10-21 15:31",
    "reporter": "井峯明香奈（shAdow）",
    "name": "📱スマホ社長📱 (@ilabo_official)",
    "url": "https://www.threads.com/share/BAbv9GPaVM/",
    "secondary_url": "https://www.threads.com/@ilabo_official",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.41.png",
    "id": "blk_733",
    "serialNo": 733
  },
  {
    "date": "2026-10-21 15:32",
    "reporter": "船坂洋子（Blooming）",
    "name": "坂本愛",
    "url": "https://www.instagram.com/aiaideko67?psIn=bDRrcWoObHU3NWVi",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.41.png",
    "id": "blk_734",
    "serialNo": 734
  },
  {
    "date": "2026-10-21 16:07",
    "reporter": "小野八音（yaShine）",
    "name": "花らぼ  クリスマスリースご予約受付中🎄",
    "url": "https://www.instagram.com/artemis_labo_flower?exIn=MTION2FxMWRycjJzaw==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "居場所作りはしたいですが、コミュニティ参加はしません、とのことです！",
    "image": "Screenshot 2026-10-22 at 10.55.41.png",
    "id": "blk_735",
    "serialNo": 735
  },
  {
    "date": "2026-10-21 17:14",
    "reporter": "菅野美穂（Couleur理事長）",
    "name": "Ai Sato",
    "url": "https://www.threads.com/@bloomy65820",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "自分で、企業の力を借りて大きくします！との事です（",
    "image": "Screenshot 2026-10-22 at 10.55.41.png",
    "id": "blk_736",
    "serialNo": 736
  },
  {
    "date": "2026-10-21 17:31",
    "reporter": "小松由衣（Mimola）",
    "name": "きよちん|食事による体質改善、産前産後整体、優しいお手当、アロマ",
    "url": "https://www.instagram.com/kiyothin?cplk=MTasazRqbW5jahonbA==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "コミュニティのお誘いはお断りしているそうです。",
    "image": "Screenshot 2026-10-22 at 10.55.21.png",
    "id": "blk_737",
    "serialNo": 737
  },
  {
    "date": "2026-10-21 19:43",
    "reporter": "黒川みさと（SORiA）",
    "name": "Haru",
    "url": "https://www.threads.com/@relaxation_macaron.milk?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.21.png",
    "id": "blk_738",
    "serialNo": 738
  },
  {
    "date": "2026-10-21 20:53",
    "reporter": "宮川亜希子（Meguria）",
    "name": "うじいえふぁーむ",
    "url": "https://www.instagram.com/ujiie_farm_takatsuki?srtk=MTYZcm5na2560TMINA==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "忙しく、手いっぱいだそうです",
    "image": "Screenshot 2026-10-22 at 10.55.21.png",
    "id": "blk_739",
    "serialNo": 739
  },
  {
    "date": "2026-10-21 21:03",
    "reporter": "上野美寿々（ensemble）",
    "name": "埼玉県／看護師/膣ケア講師養成講師/下着アドバイザー",
    "url": "https://www.instagram.com/eriko_aroma_?obrf=MXBsOWc2aGhtZXBleA==",
    "secondary_url": "https://www.threads.com/@eriko_aroma_",
    "platform": "Instagram / Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.21.png",
    "id": "blk_740",
    "serialNo": 740
  },
  {
    "date": "2026-10-21 22:14",
    "reporter": "北御門祥子（Ablaze）",
    "name": "（名称未記載）",
    "url": "https://www.threads.com/share/_6blrqK-E/",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.21.png",
    "id": "blk_741",
    "serialNo": 741
  },
  {
    "date": "2026-10-21 22:21",
    "reporter": "北御門祥子（Ablaze）",
    "name": "（名称未記載）",
    "url": "https://www.threads.com/share/_OlhJZ2JG/",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-22 at 10.55.21.png",
    "id": "blk_742",
    "serialNo": 742
  },
  {
    "date": "2026-10-22 00:55",
    "reporter": "甲賀花穂（tidy.shin）",
    "name": "ななえ｜赤ちゃんの頭の形ケア｜富士市",
    "url": "https://www.instagram.com/babycare_nanae?mdxt=MWVwCHB4M3ZnZWIwcg==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "有料の団体の話は聞くつもりないそうです",
    "image": "Screenshot 2026-10-22 at 10.55.21.png",
    "id": "blk_743",
    "serialNo": 743
  }
]

blocklist.extend(new_entries)
print(f"New total: {len(blocklist)}")

# Save JSON
with open('js/blocklist-data.json', 'w', encoding='utf-8') as f:
    json.dump(blocklist, f, ensure_ascii=False, indent=2)

# Save JS
with open('js/blocklist-data.js', 'w', encoding='utf-8') as f:
    f.write("/**\n * NEO FAMILY Calendar - Blocklist Data (v5 Enriched Profile Names)\n")
    f.write(f" * Total items: {len(blocklist)}\n */\n")
    f.write("var INITIAL_BLOCKLIST = " + json.dumps(blocklist, ensure_ascii=False, indent=2) + ";\n")

print("Updated js/blocklist-data.json and js/blocklist-data.js successfully!")

# Update blocklist_raw_transcription.md
with open('blocklist_raw_transcription.md', 'r', encoding='utf-8') as f:
    md = f.read()

md = re.sub(r'# LINE Note ブロックリスト スクリーンショット純粋文字起こし（全\d+枚）', '# LINE Note ブロックリスト スクリーンショット純粋文字起こし（全108枚）', md)
md = re.sub(r'提供いただいた全\d+枚のスクリーンショット', '提供いただいた全108枚のスクリーンショット', md)

new_transcriptions = '''
## [105/108] `Screenshot 2026-10-22 at 10.56.04.png`
```text
本多栞/RAYTUS/秘書課
ブロックリスト
過去談したりでお声がけしてほしくない方をこのノートのコメントにてまとめていきます。
Jun 5 11:25 AM

See previous comments

中村駿/碧春/福岡県
https://www.threads.com/@kazuyan.1986?igshid=NTc4MTIwNjQ2YQ==
Two days ago at 6:47 PM

小林菜津子/tEaM_S.
https://www.threads.com/@masahiko8020
Two days ago at 7:49 PM

澤木優里/RAYTUS
https://www.instagram.com/kazenonouen_101?vrfl=bDlqaDQ1NDh6ajVr
Two days ago at 8:04 PM

いわやともみ/Blooming/東京
今は育児と活動に集中したいそうです。
https://www.instagram.com/kirafuldays_handmade?mdxt=MXBjcnVubjFnNXlhMg==
Two days ago at 8:24 PM

桝田和裕/AMATERAS
https://www.instagram.com/megkometani?dlrf=NTJiN3loczNsOHNj
Two days ago at 8:53 PM

服部達典/MURA
https://www.instagram.com/uichan_1213?rpxt=MWY3bmR4bjNoZXpsMg==

https://www.instagram.com/nakami.recipe?exln=MWJiOXdqN2hvNjlkYw==
Two days ago at 9:47 PM

浜野圭/ROOTIA
Two days ago at 9:51 PM
```

## [106/108] `Screenshot 2026-10-22 at 10.55.55.png`
```text
浜野圭/ROOTIA
Two days ago at 9:51 PM

浜野圭/ROOTIA
https://www.threads.com/share/BAal5-OlKo/
Two days ago at 9:52 PM

岸部千夏/Couleur
嫌味を言ってきます
https://www.threads.com/@komame743
Two days ago at 10:22 PM

望月真美/yaShine
3回ここの話を聞いてます。興味ありません！との事です
https://www.instagram.com/chaba_sapporo_seitai?psln=MTR6YWp6exVjcHpzNg==
Two days ago at 10:45 PM

服部達典/MURA
https://www.instagram.com/ayu_otsumami_?xtok=bGtxcGt2MijdvMjli
Yesterday at 4:06 AM

服部達典/MURA
https://www.instagram.com/cafe.swallow?exln=YzM2Zno4d2FrdWpo
Yesterday at 8:53 AM

服部達典/MURA
https://www.instagram.com/itoeri_?dlrf=N213aTN5YzlaNzl=
Yesterday at 11:21 AM

大森幸子/tidy.shin兵庫県加古川
https://www.instagram.com/lc5rots7?rpxt=aTIweTFqdGMxZINi
Yesterday at 1:19 PM

大森幸子/tidy.shin兵庫県加古川
https://www.instagram.com/yumi_hogushi?rpxt=MiVmZjUyMDZldmhz
Yesterday at 1:21 PM

雨宮ありさ/yaShine
https://www.threads.com/@kajik.awa?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 2:13 PM
```

## [107/108] `Screenshot 2026-10-22 at 10.55.41.png`
```text
雨宮ありさ/yaShine
https://www.threads.com/@kajik.awa?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 2:13 PM

小松由衣/Mimola
https://www.instagram.com/fulfill.dog.training?xtok=ZDJWM2psaTh4YnUw
Yesterday at 2:22 PM

大野紗弥加/MURA
アンチのコメントに乗っかってコメントしていた方。
本日のアポもドタキャンでした。
他の何人かとも話すって書いてあったので、気をつけてください。
https://www.instagram.com/kotoko.i?vrfl=MXEzYjJ10G950HhxcQ==
https://www.threads.com/@kOtOko.i?1gShid=NTC4MTIWNQ2YQ==
Yesterday at 2:35 PM

草間真衣/MURA
https://www.threads.com/@sayuri.ibusuki?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 3:11 PM

井峯明香奈/shAdow
https://www.threads.com/share/BAbv9GPaVM/
Yesterday at 3:31 PM

船坂洋子/Blooming
https://www.instagram.com/aiaideko67?psIn=bDRrcWoObHU3NWVi
Yesterday at 3:32 PM

小野八音/yaShine
居場所作りはしたいですが、コミュニティ参加はしません、とのことです！
https://www.instagram.com/artemis_labo_flower?exIn=MTION2FxMWRycjJzaw==
Yesterday at 4:07 PM

菅野美穂/Couleur理事長
自分で、企業の力を借りて大きくします！との事です（
https://www.threads.com/@bloomy65820
Yesterday at 5:14 PM
```

## [108/108] `Screenshot 2026-10-22 at 10.55.21.png`
```text
小松由衣/Mimola
コミュニティのお誘いはお断りしているそうです。
https://www.instagram.com/kiyothin?cplk=MTasazRqbW5jahonbA==
Yesterday at 5:31 PM

黒川みさと/SORiA
https://www.threads.com/@relaxation_macaron.milk?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 7:43 PM

宮川亜希子/Meguria
忙しく、手いっぱいだそうです
https://www.instagram.com/ujiie_farm_takatsuki?srtk=MTYZcm5na2560TMINA==
Yesterday at 8:53 PM

上野美寿々/ensemble
https://www.instagram.com/eriko_aroma_?obrf=MXBsOWc2aGhtZXBleA==
https://www.threads.com/@eriko_aroma_?igshid=NTC4MTIwNjQ2YQ==
Yesterday at 9:03 PM

北御門祥子/Ablaze
https://www.threads.com/share/_6blrqK-E/
Yesterday at 10:14 PM

北御門祥子/Ablaze
https://www.threads.com/share/_OlhJZ2JG/
Yesterday at 10:21 PM

甲賀花穂/tidy.shin
有料の団体の話は聞くつもりないそうです
https://www.instagram.com/babycare_nanae?mdxt=MWVwCHB4M3ZnZWIwcg==
10 hours ago
```
'''

md = md.strip() + "\n" + new_transcriptions

with open('blocklist_raw_transcription.md', 'w', encoding='utf-8') as f:
    f.write(md)

print("Updated blocklist_raw_transcription.md successfully!")

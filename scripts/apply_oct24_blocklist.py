import json
import re

# Load current blocklist JSON
with open('js/blocklist-data.json', 'r', encoding='utf-8') as f:
    blocklist = json.load(f)

print(f"Current count: {len(blocklist)}")
assert len(blocklist) == 743, f"Expected 743 items, found {len(blocklist)}"

new_entries = [
  {
    "date": "2026-10-22 12:55",
    "reporter": "小野八音（yaShine）",
    "name": "Me+(ミタス)|-15kg朝ごはん記録|管理栄養士",
    "url": "https://www.instagram.com/kanrieiyoushi_metas?obrf=MXd0NXk3Y214Nzk1OQ==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.12.15.png",
    "id": "blk_744",
    "serialNo": 744
  },
  {
    "date": "2026-10-22 15:52",
    "reporter": "後藤広代（Lumiere.）",
    "name": "@kk_kasuga",
    "url": "https://www.threads.com/share/BBsMFS1cFy/",
    "secondary_url": "https://www.threads.com/@kk_kasuga",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.12.15.png",
    "id": "blk_745",
    "serialNo": 745
  },
  {
    "date": "2026-10-22 15:53",
    "reporter": "後藤広代（Lumiere.）",
    "name": "ゆうな (@yu.chuzai.mama)",
    "url": "https://www.threads.com/share/BAa9M0zjs6/",
    "secondary_url": "https://www.threads.com/@yu.chuzai.mama",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.12.15.png",
    "id": "blk_746",
    "serialNo": 746
  },
  {
    "date": "2026-10-22 16:26",
    "reporter": "小西みゆき（Mimola）",
    "name": "baby growth/赤ちゃん整体&脳・心の発達",
    "url": "https://www.instagram.com/baby_growth_japan?cplk=MnVqMWRmYjFydzlw",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "自分でコミュニティ作ってるので大丈夫だそうです",
    "image": "Screenshot 2026-10-24 at 15.12.08.png",
    "id": "blk_747",
    "serialNo": 747
  },
  {
    "date": "2026-10-22 17:17",
    "reporter": "服部達典（MURA）",
    "name": "ねもころ暮らしの舎|大西歩美",
    "url": "https://www.instagram.com/herb_nemokoro?cplk=ZzImaWpucHFqMHEx",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.12.08.png",
    "id": "blk_748",
    "serialNo": 748
  },
  {
    "date": "2026-10-22 17:24",
    "reporter": "井峯明香奈（shAdow）",
    "name": "高嶺の花子",
    "url": "https://www.threads.com/@1123.love.1123?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.12.08.png",
    "id": "blk_749",
    "serialNo": 749
  },
  {
    "date": "2026-10-22 17:49",
    "reporter": "後藤広代（Lumiere.）",
    "name": "坂口健人",
    "url": "https://www.threads.com/@kento12ap",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.12.08.png",
    "id": "blk_750",
    "serialNo": 750
  },
  {
    "date": "2026-10-22 18:52",
    "reporter": "菅野美穂（Couleur理事長）",
    "name": "chie",
    "url": "https://www.threads.com/@chi_e_biyou",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.12.08.png",
    "id": "blk_751",
    "serialNo": 751
  },
  {
    "date": "2026-10-22 21:56",
    "reporter": "小西みゆき（Mimola）",
    "name": "大原かこ|不登校ママの作戦会議室",
    "url": "https://www.instagram.com/caco.kosodate",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.12.08.png",
    "id": "blk_752",
    "serialNo": 752
  },
  {
    "date": "2026-10-22 21:57",
    "reporter": "小西みゆき（Mimola）",
    "name": "【柳川市】ベビーマッサージ×フォト/子育て支援サークル活動🌻なかお みか",
    "url": "https://www.instagram.com/m.baby_mama.23",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "DM送ったら非公開になりました",
    "image": "Screenshot 2026-10-24 at 15.12.08.png",
    "id": "blk_753",
    "serialNo": 753
  },
  {
    "date": "2026-10-23 05:08",
    "reporter": "服部達典（MURA）",
    "name": "春野 杏",
    "url": "https://www.instagram.com/kosodatemama0524?rpxt=YmxrZ2RpcDMxbjc1",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.12.02.png",
    "id": "blk_754",
    "serialNo": 754
  },
  {
    "date": "2026-10-23 05:08",
    "reporter": "服部達典（MURA）",
    "name": "izumi /シミ.肝斑.たるみ専門/愛知県高浜市",
    "url": "https://www.instagram.com/cherilu_yn?mdxt=bGlqMDhmbjJ0czRu",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.12.02.png",
    "id": "blk_755",
    "serialNo": 755
  },
  {
    "date": "2026-10-23 05:08",
    "reporter": "服部達典（MURA）",
    "name": "ろみ(〜)",
    "url": "https://www.instagram.com/romy.yade?exln=ajdhcnYxYmx5Nmsx",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.12.02.png",
    "id": "blk_756",
    "serialNo": 756
  },
  {
    "date": "2026-10-23 08:49",
    "reporter": "齊藤唯（Mimola）",
    "name": "川野友美 元美容看護師|Magier代表",
    "url": "https://www.threads.com/@magier_2023?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.12.02.png",
    "id": "blk_757",
    "serialNo": 757
  },
  {
    "date": "2026-10-23 09:28",
    "reporter": "森崎江里（愛知県 / RAYTUS）",
    "name": "rina",
    "url": "https://www.threads.com/@rina.s0527",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "誰かのやりとり、スクショで晒されてます💦 コメントのやつも報告とブロックお願いします",
    "image": "Screenshot 2026-10-24 at 15.12.02.png",
    "id": "blk_758",
    "serialNo": 758
  },
  {
    "date": "2026-10-23 15:09",
    "reporter": "畑ゆかり（yuima-ru理事長）",
    "name": "はるな / アダルトチルドレン克服カウンセラー",
    "url": "https://www.threads.com/@matsunaga__haruna?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "ぶった斬り会長・・・名指しでした",
    "image": "Screenshot 2026-10-24 at 15.11.56.png",
    "id": "blk_759",
    "serialNo": 759
  },
  {
    "date": "2026-10-23 17:43",
    "reporter": "井峯明香奈（shAdow）",
    "name": "発達支援【栄養✖️運動で発達をサポート】横山佳奈",
    "url": "https://www.threads.com/@yokoyama_ibaraki?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.11.56.png",
    "id": "blk_760",
    "serialNo": 760
  },
  {
    "date": "2026-10-23 19:54",
    "reporter": "城間千聖（enLIGHT）",
    "name": "モモカ|アートメイク|沖縄|看護師",
    "url": "https://www.instagram.com/artmake_momoka?exln=b29zenR2cjUyYXB1bHs=",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.11.56.png",
    "id": "blk_761",
    "serialNo": 761
  },
  {
    "date": "2026-10-23 20:42",
    "reporter": "岩﨑七菜子（tEaM_S.）",
    "name": "堀井 拓也",
    "url": "https://www.threads.com/@holitaku_pickleball",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "ファーストして興味あるフリして、なんの断りもなくブロック＆zoom来ずでした",
    "image": "Screenshot 2026-10-24 at 15.11.56.png",
    "id": "blk_762",
    "serialNo": 762
  },
  {
    "date": "2026-10-23 22:37",
    "reporter": "ロジャーズ優衣（enchant+）",
    "name": "テニスコーディネーター川又お悩み解決教室",
    "url": "https://www.threads.com/@poochan5676?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.11.56.png",
    "id": "blk_763",
    "serialNo": 763
  },
  {
    "date": "2026-10-23 22:57",
    "reporter": "ロジャーズ優衣（enchant+）",
    "name": "あゆみ|自分を好きになるセルフメイク伴走者",
    "url": "https://www.instagram.com/ayumi.reborn?xtok=MXRkZzUwaWIwam5leA==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.11.48.png",
    "id": "blk_764",
    "serialNo": 764
  },
  {
    "date": "2026-10-23 23:34",
    "reporter": "小野八音（yaShine）",
    "name": "tomo_\"妊娠を叶える体\"に整える栄養メソッド",
    "url": "https://www.instagram.com/tomo.ninkatsueiyou?srtk=MWxtYjJ4aWM3bXlodg==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "何度もお声かけいただき ZOOMもしてお断りしました、とのことです！",
    "image": "Screenshot 2026-10-24 at 15.11.48.png",
    "id": "blk_765",
    "serialNo": 765
  },
  {
    "date": "2026-10-24 01:14",
    "reporter": "桝田和裕（AMATERAS）",
    "name": "Nobuyuki Hori",
    "url": "https://www.threads.com/@nobu491004?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.11.48.png",
    "id": "blk_766",
    "serialNo": 766
  },
  {
    "date": "2026-10-24 01:14",
    "reporter": "南藍（tidy.shin代表）",
    "name": "もっちー | Web・広告×動画制作",
    "url": "https://www.threads.com/@mochi_creative123?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "",
    "platform": "Threads",
    "url_warning": "",
    "reason": "言っていることに信ぴょう性がなく、マウント取ってくる。",
    "image": "Screenshot 2026-10-24 at 15.11.48.png",
    "id": "blk_767",
    "serialNo": 767
  },
  {
    "date": "2026-10-24 10:11",
    "reporter": "城間千聖（enLIGHT）",
    "name": "𝕤𝕒𝕥𝕠𝕞𝕚 ｜こどもとかめら",
    "url": "https://www.instagram.com/sato_aoi_photo?psln=MWp5bGtncmZpYTE4OA==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "何度もお声かけしているようです。Zoom面談をした上でお断りしたそう。",
    "image": "Screenshot 2026-10-24 at 15.11.48.png",
    "id": "blk_768",
    "serialNo": 768
  },
  {
    "date": "2026-10-24 10:11",
    "reporter": "ロジャーズ優衣（enchant+）",
    "name": "にじいろ鍼灸 (@nijirosinkyu)",
    "url": "https://www.threads.com/@nijirosinkyu?igshid=NTc4MTIwNjQ2YQ==",
    "secondary_url": "https://www.instagram.com/nijirosinkyu?vrfl=MWg3M2oyM25uN2xtYg==",
    "platform": "Threads / Instagram",
    "url_warning": "",
    "reason": "向こうからメッセージをいただきましたが、NEOに会うのは3回目だったそうです🙏",
    "image": "Screenshot 2026-10-24 at 15.11.48.png",
    "id": "blk_769",
    "serialNo": 769
  },
  {
    "date": "2026-10-24 13:11",
    "reporter": "服部達典（MURA）",
    "name": "まゆ｜親子ではぐくむ子育てコーチ🧸",
    "url": "https://www.instagram.com/mayu_coach.mama?psln=MThpd2lycW5jamo5Mw==",
    "secondary_url": "",
    "platform": "Instagram",
    "url_warning": "",
    "reason": "",
    "image": "Screenshot 2026-10-24 at 15.11.48.png",
    "id": "blk_770",
    "serialNo": 770
  }
]

print(f"Adding {len(new_entries)} new entries...")
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

md = re.sub(r'# LINE Note ブロックリスト スクリーンショット純粋文字起こし（全\d+枚）', '# LINE Note ブロックリスト スクリーンショット純粋文字起こし（全114枚）', md)
md = re.sub(r'提供いただいた全\d+枚のスクリーンショット', '提供いただいた全114枚のスクリーンショット', md)

new_transcriptions = '''
## [109/114] `Screenshot 2026-10-24 at 15.12.21.png`
```text
Oct 21 3:31 PM

船坂洋子/Blooming
https://www.instagram.com/aiaideko67?psIn=bDRrcWoObHU3NWVi
Oct 21 3:32 PM

小野八音/yaShine
居場所作りはしたいですが、コミュニティ参加はしません、とのことです！
https://www.instagram.com/artemis_labo_flower?exIn=MTION2FxMWRycjJzaw==
Oct 21 4:07 PM

菅野美穂/Couleur理事長
自分で、企業の力を借りて大きくします！との事です😊
https://www.threads.com/@bloomy65820
Oct 21 5:14 PM

小松由衣/Mimola
コミュニティのお誘いはお断りしているそうです。
https://www.instagram.com/kiyothin?cplk=MTdsazRqbW5jdHJhbA==
Oct 21 5:31 PM

黒川みさと/SORiA
https://www.threads.com/@relaxation_macaron.milk?igshid=NTc4MTIwNjQ2YQ==
Oct 21 7:43 PM

宮川亜希子/Meguria
https://www.instagram.com/ujiie_farm_takatsuki?srtk=MTYzczm5na256OTM1NA==
忙しく、手いっぱいだそうです
Oct 21 8:53 PM

上野美寿々/ensemble
https://www.instagram.com/eriko_aroma_?obrf=MXBsOWc2aGhtZXBleA==
https://www.threads.com/@eriko_aroma_?igshid=NTc4MTIwNjQ2YQ==
Oct 21 9:03 PM
```

## [110/114] `Screenshot 2026-10-24 at 15.12.15.png`
```text
https://www.threads.com/@eriko_aroma_?igshid=NTc4MTIwNjQ2YQ==
Oct 21 9:03 PM

北御門祥子 / Ablaze
https://www.threads.com/share/_6b1rqK-E/
Oct 21 10:14 PM

北御門祥子 / Ablaze
https://www.threads.com/share/_0lhJZ2JG/
Oct 21 10:21 PM

甲賀花穂tidy.shin
有料の団体の話は聞くつもりないそうです
https://www.instagram.com/babycare_nanae?mdxt=MWVwCHB4M3ZnZWIwcg==
Two days ago at 12:45 AM

小野八音/yaShine
https://www.instagram.com/kanrieiyoushi_metas?obrf=MXd0NXk3Y214Nzk1OQ==
Two days ago at 12:55 PM

後藤広代/Lumiere.
https://www.threads.com/share/BBsMFS1cFy/
Two days ago at 3:52 PM

後藤広代/Lumiere.
https://www.threads.com/share/BAa9M0zjs6/
Two days ago at 3:53 PM
```

## [111/114] `Screenshot 2026-10-24 at 15.12.08.png`
```text
Two days ago at 3:53 PM

小西みゆき/Mimola
自分でコミュニティ作ってるので大丈夫だそうです
https://www.instagram.com/baby_growth_japan?cplk=MnVqMWRmYjFydzlw
Two days ago at 4:26 PM

服部達典/MURA
https://www.instagram.com/herb_nemokoro?cplk=ZzImaWpucHFqMHEx
Two days ago at 5:17 PM

井峯明香奈/shAdow
https://www.threads.com/@1123.love.1123?igshid=NTc4MTIwNjQ2YQ==
Two days ago at 5:24 PM

後藤広代/Lumiere.
https://www.threads.com/@kento12ap
Two days ago at 5:49 PM

菅野美穂/Couleur理事長
https://www.threads.com/@chi_e_biyou
Two days ago at 6:52 PM

北御門祥子 / Ablaze
https://www.threads.com/share/BAt2rEETHn/
Two days ago at 9:25 PM

小西みゆき/Mimola
https://www.instagram.com/caco.kosodate
Two days ago at 9:56 PM

小西みゆき/Mimola
DM送ったら非公開になりました
https://www.instagram.com/m.baby_mama.23
Two days ago at 9:57 PM
```

## [112/114] `Screenshot 2026-10-24 at 15.12.02.png`
```text
服部達典/MURA
https://www.instagram.com/kosodatemama0524?rpxt=YmxrZ2RpcDMxbjc1
https://www.instagram.com/cherilu_yn?mdxt=bGlqMDhmbjJ0czRu
https://www.instagram.com/herb_nemokoro?rpxt=ZzImaWpucHFqMHEx
https://www.instagram.com/romy.yade?exln=ajdhcnYxYmx5Nmsx
Yesterday at 5:08 AM

森崎江里／愛知県/RAYTUS
誰かのやりとり、スクショで晒されてます💦
コメントのやつも報告とブロックお願いします
Yesterday at 8:22 AM

齊藤唯/Mimola
https://www.threads.com/@magier_2023?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 8:49 AM

森崎江里／愛知県/RAYTUS
https://www.threads.com/@rina.s0527
Yesterday at 9:28 AM

相良沙織/Meguria理事長
@森崎江里／愛知県/RAYTUS さんのいう方のリンクはこちら
通報もよろしくお願い申し上げます。
https://www.threads.com/@rina.s0527
Yesterday at 9:46 AM

坂本有莉菜/Mimola
https://www.threads.com/@tomopooh1113?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 11:19 AM
```

## [113/114] `Screenshot 2026-10-24 at 15.11.56.png`
```text
井峯明香奈/shAdow
https://www.threads.com/@shimosonet?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 2:27 PM

畑ゆかり/yuima-ru理事長
ぶった斬り会長・・・名指しでした
https://www.threads.com/@matsunaga__haruna?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 3:09 PM

井峯明香奈/shAdow
https://www.threads.com/@yokoyama_ibaraki?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 5:43 PM

城間千聖/enLIGHT
https://www.instagram.com/artmake_momoka?exln=b29zenR2cjUyYXB1bHs=
Yesterday at 7:54 PM

岩﨑七菜子/tEaM_S.
ファーストして興味あるフリして、なんの断りもなくブロック＆zoom来ずでした
https://www.threads.com/@holitaku_pickleball
Yesterday at 8:42 PM

ロジャーズ優衣\enchant+
https://www.threads.com/@poochan5676?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 10:37 PM
```

## [114/114] `Screenshot 2026-10-24 at 15.11.48.png`
```text
Yesterday at 10:37 PM

ロジャーズ優衣\enchant+
https://www.instagram.com/ayumi.reborn?xtok=MXRkZzUwaWIwam5leA==
Yesterday at 10:57 PM

小野八音/yaShine
何度もお声かけいただき
ZOOMもしてお断りしました、とのことです！
https://www.instagram.com/tomo.ninkatsueiyou?srtk=MWxtYjJ4aWM3bXlodg==
Yesterday at 11:34 PM

桝田和裕/AMATERAS
https://www.threads.com/@nobu491004?igshid=NTc4MTIwNjQ2YQ==
14 hours ago

南藍/tidy.shin代表
言っていることに信ぴょう性がなく、マウント取ってくる。
https://www.threads.com/@mochi_creative123?igshid=NTc4MTIwNjQ2YQ==
14 hours ago

城間千聖/enLIGHT
https://www.instagram.com/sato_aoi_photo?psln=MWp5bGtncmZpYTE4OA==
何度もお声かけしているようです。Zoom面談をした上でお断りしたそう。
5 hours ago

ロジャーズ優衣\enchant+
https://www.threads.com/@nijirosinkyu?igshid=NTc4MTIwNjQ2YQ==
https://www.instagram.com/nijirosinkyu?vrfl=MWg3M2oyM25uN2xtYg==
向こうからメッセージをいただきましたが、NEOに会うのは3回目だったそうです🙏
5 hours ago

服部達典/MURA
https://www.instagram.com/mayu_coach.mama?psln=MThpd2lycW5jamo5Mw==
2 hours ago
```
'''

md = md.strip() + "\n" + new_transcriptions

with open('blocklist_raw_transcription.md', 'w', encoding='utf-8') as f:
    f.write(md)

print("Updated blocklist_raw_transcription.md successfully!")

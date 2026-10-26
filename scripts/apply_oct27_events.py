# -*- coding: utf-8 -*-
"""
apply_oct27_events.py

Applies the 261027 event updates and flyer images to:
1. images/
2. events.json
3. js/events-data.js
4. neofamily_all_events.ics
5. HTML files cache-busting version parameter
"""

import os
import shutil
import json
from datetime import datetime

WORKSPACE = "/Users/kotsuka/Documents/systemDev/neo_family_calendar"
PRVIDED_DIR = os.path.join(WORKSPACE, "prvided data")
IMAGES_DIR = os.path.join(WORKSPACE, "images")

# 1. Copy flyer images
flyer_mappings = [
    ("S__42025005.jpg", "event-20261026-bengyo-ginger-nakajima-manami.jpg"),
    ("S__6881310.jpg", "event-20261027-liver-namikky.jpg"),
    ("S__281092149.jpg", "event-20261030-bengyo-ginger-shiraki-yuki-takashi.jpg"),
]

for src_name, dst_name in flyer_mappings:
    src_path = os.path.join(PRVIDED_DIR, src_name)
    dst_path = os.path.join(IMAGES_DIR, dst_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"✅ Copied flyer: {src_name} -> images/{dst_name}")
    else:
        print(f"⚠️ Source flyer not found: {src_path}")

# 2. Load existing events from events.json
events_json_path = os.path.join(WORKSPACE, "events.json")
with open(events_json_path, "r", encoding="utf-8") as f:
    events = json.load(f)

print(f"Loaded {len(events)} existing events from events.json")
event_map = {e["id"]: e for e in events}

# 3. Update existing event: event-20261030-livecommerce
if "event-20261030-livecommerce" in event_map:
    e = event_map["event-20261030-livecommerce"]
    e["title"] = "✨🎤 ライブコマーサー無料セミナー「あなたの伝える力が仕事になるかも！」"
    e["subtitle"] = "テレビ通販・ライブコマースの現場で活躍するプロ 相本さち子登壇（参加費無料🎁）"
    e["category"] = "セミナー・勉強会"
    e["categoryColor"] = "#d97706"
    e["startDate"] = "2026-10-30"
    e["startTime"] = "20:00"
    e["endDate"] = "2026-10-30"
    e["endTime"] = "21:30"
    e["location"] = "Zoom（オンライン）"
    e["locationType"] = "online"
    e["fee"] = "無料🎁"
    e["presenter"] = "相本さち子（テレビ通販・ライブコマーサー）"
    e["zoomUrl"] = "https://us06web.zoom.us/j/81838613264?pwd=UTmQD3bKAJBtd5onNUoiox0ZRRRBsm.1"
    e["zoomMeetingId"] = "818 3861 3264"
    e["zoomPasscode"] = "UTmQD3bKAJBtd5onNUoiox0ZRRRBsm.1"
    e["registrationUrl"] = "https://us06web.zoom.us/j/81838613264?pwd=UTmQD3bKAJBtd5onNUoiox0ZRRRBsm.1"
    e["description"] = (
        "✨🎤 あなたの「伝える力」が仕事になるかも！🎤✨\n"
        "＼10月30日 20時 ライブコマーサー無料セミナー開催／\n\n"
        "今、TikTokなどで注目を集めている「ライブコマース」をご存じですか？😳\n"
        "ライブ配信をしながら商品の魅力を伝え、視聴者とのコミュニケーションを通して購入につなげていく、新しい販売のカタチです✨\n\n"
        "今回の無料セミナーでは、テレビ通販・ライブコマースの現場で活躍する相本さち子が、\n"
        "🔥 ライブコマースとは？\n"
        "🔥 ライブで商品を売るために必要なこと\n"
        "🔥 商品の魅力を引き出す伝え方\n"
        "🔥 視聴者の「欲しい！」を生み出す販売の基礎\n"
        "🔥 ライブコマーサーという新しい働き方\n"
        "などを、初心者の方にも分かりやすくお伝えします☺️\n\n"
        "⭐️開催日時：10月30日（金）20:00～\n"
        "⭐️参加費：無料🎁\n\n"
        "【こんな方におすすめです💁‍♀️】\n"
        "・自分の商品やサービスをもっと売りたい\n"
        "・ライブコマーサーオーディションを受ける前に予備知識がほしい\n"
        "・人前で話すことや商品を紹介することが好き\n"
        "・在宅でもできる新しい仕事に興味がある\n"
        "・自分に向いているか、まず話を聞いてみたい\n\n"
        "そして「ライブコマーサーオーディション」も来月開催予定です🎉 すでにたくさんのエントリーをいただいています！\n"
        "オーディションへの参加を決めていない方も、無料セミナーだけのご参加で大歓迎です🙌\n"
        "商品を売る方にも、誰かの商品を紹介する方にも役立つ内容です✨ ライブコマースの世界を一緒にのぞいてみませんか？☺️\n\n"
        "🔻Zoom ミーティングに参加する🔻\n"
        "https://us06web.zoom.us/j/81838613264?pwd=UTmQD3bKAJBtd5onNUoiox0ZRRRBsm.1"
    )
    print("✅ Updated event-20261030-livecommerce")

# 4. New events to add
new_events = [
    {
        "id": "event-20261026-raytus-godo-setsumeikai",
        "title": "📢 RAYTUS group. 合同事業説明会",
        "subtitle": "ノワナスクール・Ligare・ままゆね・Re.Co Lab 合同登壇（耳だけ参加も大歓迎！）",
        "category": "事業説明会・相談会",
        "categoryColor": "#0284c7",
        "startDate": "2026-10-26",
        "startTime": "13:00",
        "endDate": "2026-10-26",
        "endTime": "14:30",
        "isAllDay": False,
        "location": "Zoom（オンライン）",
        "locationType": "online",
        "fee": "無料",
        "capacity": "",
        "presenter": "RAYTUS group.（4事業代表登壇）",
        "image": "",
        "images": [],
        "description": (
            "📢 RAYTUS group.合同事業説明会のお知らせ📢\n\n"
            "本日は下記4事業が登壇します✨\n\n"
            "--------------------\n"
            "【26日（月）13:00～】\n"
            "・韓国コミュニティ事業：ノワナスクール\n"
            "・総合美容事業：Ligare\n"
            "・ママ支援事業：ままゆね\n"
            "・スポーツリカバリー事業：Re.Co Lab\n"
            "--------------------\n\n"
            "耳だけ参加も大歓迎です💡\n"
            "リアルタイムでのみなさんのご参加お待ちしております✨\n\n"
            "🔻Zoom ID（全日共通）🔻\n"
            "https://us06web.zoom.us/j/81113152898?pwd=rnUDogc0paequYOxCnvXYaSs3WngG3.1\n\n"
            "ミーティング ID: 811 1315 2898\n"
            "パスコード: 2026"
        ),
        "registrationUrl": "https://us06web.zoom.us/j/81113152898?pwd=rnUDogc0paequYOxCnvXYaSs3WngG3.1",
        "zoomUrl": "https://us06web.zoom.us/j/81113152898?pwd=rnUDogc0paequYOxCnvXYaSs3WngG3.1",
        "zoomMeetingId": "811 1315 2898",
        "zoomPasscode": "2026",
        "archive": {
            "hasArchive": False,
            "archiveUrl": "",
            "password": "",
            "notes": ""
        }
    },
    {
        "id": "event-20261026-bengyo-ginger-nakajima-manami",
        "title": "⛩️ 勉強ジンジャー「私の本音、どこ行った!? 😂」",
        "subtitle": "人の目を気にして言いたいことも言えなかった私が、人前で話せるようになるまで（参加費：会場費充当）",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-26",
        "startTime": "19:00",
        "endDate": "2026-10-26",
        "endTime": "20:00",
        "isAllDay": False,
        "location": "⛩️ 勉強ジンジャー（オンライン）",
        "locationType": "online",
        "fee": "視聴権購入（売上全額定例会会場費充当）",
        "capacity": "",
        "presenter": "中嶋愛美（MURA理事長）、櫻井香菜子（MURA理事 / マシンガントークKANAKO）",
        "image": "images/event-20261026-bengyo-ginger-nakajima-manami.jpg",
        "images": [
            "images/event-20261026-bengyo-ginger-nakajima-manami.jpg"
        ],
        "description": (
            "＼ 私の本音、どこ行った!? 😂 ／\n\n"
            "10月26日（月）19:00～\n"
            "話すのに💥コンプレックス💥ある人あつまれ〜！\n\n"
            "𓇠𓇠𓇠𓇠𓇠𓇠𓇠𓇠𓇠𓇠𓇠\n"
            "🎤 MURA理事長 中嶋愛美\n"
            "🎤 MURA理事 櫻井香菜子\n"
            "𓇠𓇠𓇠𓇠𓇠𓇠𓇠𓇠𓇠𓇠𓇠\n\n"
            "人の目を気にして、嫌われるのが怖くて、言いたいことも言えない人間でした😂\n"
            "「こんなこと言ったらどう思われる？」「嫌われたらどうしよう…」\n"
            "そんなことばっかり考えて、自分の本音はどこへやら🤣\n\n"
            "話す機会も増えましたが、最初からこんな私だったわけじゃありません！（※嘘ではありません⚠️）\n"
            "じゃあ、どうやって変わったのか🤔\n"
            "今回は、そんな私の過去から今に至るまでを、包み隠さず赤裸々にお話しします🔥\n\n"
            "そして今回は‼️ スペシャルゲストにMURA理事 マシンガントークKANAKO📣こと、櫻井香菜子さんをお迎えします✨\n\n"
            "✔ 人の目が気になってしまう\n"
            "✔ 嫌われるのが怖い\n"
            "✔ 自分の意見をなかなか言えない\n\n"
            "そんな方にこそ聞いてほしい内容です🙌\n"
            "笑いあり、NGなし‼️ 楽しい時間をお届けします💃\n\n"
            "ぜひ遊びに来てください❤️\n"
            "話すの苦手でも、変わりたい‼️と思っているそこのあなた🙌 お待ちしています💓\n\n"
            "･･━━･･━━･･━━･･━━･･\n"
            "購入していただいた売上は全て定例会の会場費になります💙\n"
            "･･━━･･━━･･━━･･━━･･\n"
            "🛒 視聴権の購入はこちら：\n"
            "https://community-iyasakagu.jp/subschool/course/school_course1268/"
        ),
        "registrationUrl": "https://community-iyasakagu.jp/subschool/course/school_course1268/",
        "zoomUrl": "",
        "zoomMeetingId": "",
        "zoomPasscode": "",
        "archive": {
            "hasArchive": False,
            "archiveUrl": "",
            "password": "",
            "notes": ""
        }
    },
    {
        "id": "event-20261027-liver-namikky",
        "title": "📲 NEO FAMILY ライバー事業説明会＆特別番組",
        "subtitle": "ゲスト：幼児性教育の先生 🌺なみっきー🌺（ライバー名なっちゃん）1周年記念！",
        "category": "事業説明会・相談会",
        "categoryColor": "#0284c7",
        "startDate": "2026-10-27",
        "startTime": "14:00",
        "endDate": "2026-10-27",
        "endTime": "15:00",
        "isAllDay": False,
        "location": "LIVEPARK（オンライン生配信）",
        "locationType": "online",
        "fee": "無料（顔出しなし・ラジオ感覚参加OK）",
        "capacity": "",
        "presenter": "NEO FAMILY ライバー事業部 / ゲスト：なみっきー（なっちゃん）",
        "image": "images/event-20261027-liver-namikky.jpg",
        "images": [
            "images/event-20261027-liver-namikky.jpg"
        ],
        "description": (
            "📲 ライバー事業説明会 📲\n\n"
            "昨年8月にスタートしたこの事業🎙\n\n"
            "今回のゲストは、ついにライバー1周年❣️❣️\n"
            "幼児性教育の先生 🌺なみっきー🌺（ライバーネームはなっちゃん）\n"
            "3歳と1歳の男子を育てながら、どうやって続けたのー⁉️\n"
            "率直な気持ちを聞いてみましょう🩷\n\n"
            "📅 10月27日(火) 14時～15時\n\n"
            "ライバーって何してるの？ どんな人がいるの？ どんな配信なの？\n"
            "《ライバー》って言葉だけ聞いても正直よくわからなくないですか？\n"
            "そういう時は、まず✨体感✨\n\n"
            "ライブパークを使用して、ポコチャ仕様の特別な説明会を行ないます♪\n"
            "顔出しなし、ラジオ感覚で参加できます📻 スタンプ機能も特別なものがあるかも…⁉️\n\n"
            "ライバーってなんだろう🤔 その疑問を解決しに、ぜひお気軽に見に来てください😍\n\n"
            "前半はポコチャで活躍中の現役ライバーさんをゲストにライバー特別番組を📺\n"
            "後半はライバー事業説明会を行います✍️\n\n"
            "推しがいる人もいない人も、ポコチャを見たことがある人もない人も、覗いてみてね～🙌✨🥰\n\n"
            "🎬 ご視聴はこちら：\n"
            "https://events.livepark.jp/videos/HYFD7eGXFFV"
        ),
        "registrationUrl": "https://events.livepark.jp/videos/HYFD7eGXFFV",
        "zoomUrl": "",
        "zoomMeetingId": "",
        "zoomPasscode": "",
        "archive": {
            "hasArchive": False,
            "archiveUrl": "",
            "password": "",
            "notes": ""
        }
    },
    {
        "id": "event-20261030-bengyo-ginger-shiraki-yuki-takashi",
        "title": "📚⛩️ 勉強ジンジャー「真面目な夫と、自由すぎる妻。夫婦で人生大冒険！」",
        "subtitle": "enCORE 理事長 白木悠希・隆司 登壇！性格真逆の2人が夫婦そろって理事長に！？（参加費1,000円）",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-30",
        "startTime": "21:30",
        "endDate": "2026-10-30",
        "endTime": "22:30",
        "isAllDay": False,
        "location": "⛩️ 勉強ジンジャー（オンライン）",
        "locationType": "online",
        "fee": "1,000円（売上全額定例会会場費充当）",
        "capacity": "",
        "presenter": "白木悠希・白木隆司（enCORE 理事長夫婦）",
        "image": "images/event-20261030-bengyo-ginger-shiraki-yuki-takashi.jpg",
        "images": [
            "images/event-20261030-bengyo-ginger-shiraki-yuki-takashi.jpg"
        ],
        "description": (
            "📚⛩️ 勉強ジンジャー開催 ⛩️📚\n\n"
            "enCORE 理事長 白木悠希、隆司です☺️\n\n"
            "📅 10月30日(金) 21:30～22:30\n"
            "参加費: 1,000円\n\n"
            "＼真面目な夫と、自由すぎる妻。／\n"
            "そんな2人が、夫婦で人生大冒険！ 🤣💕\n"
            "enCORE理事長の白木夫婦がお届けします♡\n\n"
            "👨 白木隆司（A×Ｂ＝AB型）：真面目で慎重派の夫。\n"
            "👩 白木悠希（O×Ｂ＝B型）：好奇心旺盛！楽しいこと大好き！自由すぎる妻。\n\n"
            "性格も考え方も違う2人が、夫婦で同じ環境に飛び込み、まさかの2人そろって理事長に！！😳✨\n"
            "しかも、わが家には小学1年生と0歳の子どもがいます👧👶\n"
            "仕事に家事に育児。時間がたっぷりあるわけじゃない。\n"
            "それでも、夫婦で挑戦することを選びました🔥\n\n"
            "今回お話しするのは…\n"
            "🌈 夫婦で活動するって実際どうなの？\n"
            "🌈 性格が真逆の2人がどうやって協力している？\n"
            "🌈 小さな子どもがいても挑戦できた、リアルな時間の使い方\n"
            "🌈 コツコツ続けた先に見えた景色\n"
            "🌈 理事長になって変わったこと、そしてこれから叶えたい夢\n\n"
            "もちろん、うまくいった話ばかりじゃありません🤣\n"
            "夫婦だからこその本音や、普段は見せない裏側もお話しできたらと思っています♡\n"
            "人生、予定通りじゃつまらない！\n"
            "大人になっても、親になっても、まだまだ夢を追いかけていい。夫婦そろって、まだまだ青春！！😆🔥\n"
            "笑いあり、リアルな話ありの勉強ジンジャー♡ ぜひ気軽に遊びに来てください🥰💕\n\n"
            "※この度の売上は、全額定例会の会場費の補填になります！\n\n"
            "🛒 視聴チケットはこちら：\n"
            "https://shopping.community-iyasakagu.jp/product/school_course1293/"
        ),
        "registrationUrl": "https://shopping.community-iyasakagu.jp/product/school_course1293/",
        "zoomUrl": "",
        "zoomMeetingId": "",
        "zoomPasscode": "",
        "archive": {
            "hasArchive": False,
            "archiveUrl": "",
            "password": "",
            "notes": ""
        }
    }
]

for ne in new_events:
    if ne["id"] in event_map:
        event_map[ne["id"]].update(ne)
        print(f"🔄 Overwrote existing event: {ne['id']}")
    else:
        events.append(ne)
        event_map[ne["id"]] = ne
        print(f"➕ Added new event: {ne['id']}")

# 5. Sort events chronologically: startDate, startTime
events.sort(key=lambda x: (x.get("startDate", ""), x.get("startTime", "")))
print(f"Total events now: {len(events)}")

# 6. Save events.json
with open(events_json_path, "w", encoding="utf-8") as f:
    json.dump(events, f, ensure_ascii=False, indent=2)
print("✅ Saved events.json")

# 7. Save js/events-data.js
js_events_data_path = os.path.join(WORKSPACE, "js", "events-data.js")
js_content = f"// Automatically generated from events.json on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
js_content += "const INITIAL_EVENTS = " + json.dumps(events, ensure_ascii=False, indent=2) + ";\n"

with open(js_events_data_path, "w", encoding="utf-8") as f:
    f.write(js_content)
print("✅ Saved js/events-data.js")

# 8. Generate neofamily_all_events.ics
ics_lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//NEO FAMILY//Events Calendar//JA",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "X-WR-CALNAME:NEO FAMILY イベントカレンダー",
    "X-WR-TIMEZONE:Asia/Tokyo"
]

for e in events:
    s_date = e.get('startDate', '').replace('-', '')
    s_time = e.get('startTime', '00:00').replace(':', '') + '00'
    e_date = e.get('endDate', e.get('startDate', '')).replace('-', '')
    e_time = e.get('endTime', '23:59').replace(':', '') + '00'
    
    dtstart = f"{s_date}T{s_time}"
    dtend = f"{e_date}T{e_time}"
    
    summary = e.get('title', '').replace('\n', ' ')
    desc = e.get('description', '').replace('\n', '\\n')
    loc = e.get('location', '').replace('\n', ' ')
    url = e.get('registrationUrl') or e.get('zoomUrl') or ''
    uid = f"{e['id']}@neofamily.jp"
    
    ics_lines.extend([
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
        f"DTSTART;TZID=Asia/Tokyo:{dtstart}",
        f"DTEND;TZID=Asia/Tokyo:{dtend}",
        f"SUMMARY:{summary}",
        f"DESCRIPTION:{desc}",
        f"LOCATION:{loc}",
        f"URL:{url}" if url else "",
        "END:VEVENT"
    ])

ics_lines = [line for line in ics_lines if line]
ics_lines.append("END:VCALENDAR\n")

ics_path = os.path.join(WORKSPACE, "neofamily_all_events.ics")
with open(ics_path, "w", encoding="utf-8") as f:
    f.write("\r\n".join(ics_lines))
print("✅ Saved neofamily_all_events.ics")

# 9. Update cachebuster ?v=20261024_1 -> ?v=20261027_1 in HTML files
html_files = [
    "index.html", "portal.html", "calendar.html", "sns.html",
    "iyasaka.html", "admin.html", "raytus.html", "archive.html"
]

for hf in html_files:
    hp = os.path.join(WORKSPACE, hf)
    if os.path.exists(hp):
        with open(hp, "r", encoding="utf-8") as f:
            content = f.read()
        if "js/events-data.js?v=20261024_1" in content:
            content = content.replace("js/events-data.js?v=20261024_1", "js/events-data.js?v=20261027_1")
            with open(hp, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"🔄 Bumped cachebuster in {hf}")

print("🎉 All event updates applied successfully!")

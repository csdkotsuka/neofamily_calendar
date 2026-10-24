# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

# Load existing events from events.json
with open('events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

print(f"Loaded {len(events)} existing events from events.json")
event_map = {e['id']: e for e in events}

# 1. Update event-20261026-sanpun-cooking (会長勉強ジンジャー)
if 'event-20261026-sanpun-cooking' in event_map:
    e = event_map['event-20261026-sanpun-cooking']
    e['presenter'] = "会長"
    e['subtitle'] = "10/26(月) 21:00〜 会長直伝！成功って、3分クッキング⁉️億を生み出す🔥成功のレシピ🔥"
    e['fee'] = "視聴権購入（売上全額定例会会場費充当）"
    e['registrationUrl'] = "https://community-iyasakagu.jp/subschool/course/school_course1266/"
    e['image'] = "images/event-20261026-sanpun-cooking.jpg"
    e['images'] = ["images/event-20261026-sanpun-cooking.jpg"]
    e['description'] = "10/26は何の日でしょうか⁉️\n会長勉強ジンジャー開催日‼️\n※最低200人以上で開催❤️‍🔥\n\n今回のテーマは…\n【簡単に稼ぐポイント💡】\n\n10/26（月）21:00〜\n説得力の塊❗️会長から直伝のチャンス💰✨✨\nご夫婦やご家族でzoomに集合してもよし⭕️💻\n周りの人もみーんなで稼いでいこう😎❤️‍🔥❤️‍🔥❤️‍🔥\n\nリアル参加できなくてもアーカイブあります‼️\nとにかく視聴権の購入お願いします‼️\n\n※購入リンクはこちら👇\nhttps://community-iyasakagu.jp/subschool/course/school_course1266/"
    print("Updated event-20261026-sanpun-cooking")

# 2. Update event-20261104-mohatsu-2 (ようへい先生 無料オンラインセミナー 第2回)
if 'event-20261104-mohatsu-2' in event_map:
    e = event_map['event-20261104-mohatsu-2']
    e['title'] = "ムダに毛の多いようへい先生プレゼンツ【発毛・脱毛】知ると変わる、毎日のヘアケア。"
    e['subtitle'] = "会長お墨付き！Q-more.・エイジングショット代理店の皆さまも必見の無料セミナー第2回"
    e['image'] = "images/event-20261104-hatsumou-datsumou-yohei.jpg"
    e['images'] = ["images/event-20261104-hatsumou-datsumou-yohei.jpg"]
    e['description'] = "会長お墨付き👀 ムダに毛の多いようへい先生プレゼンツ👨‍🏫\n今回のテーマは【発毛・脱毛】✨\n\n生える毛、抜ける毛、その違い、気になりませんか？👀\n髪にとって、めちゃくちゃ大事な今回のお話！！\n知っているだけで普段のヘアケアが変わるかも🤭\n\nそして！Q-more.・エイジングショットの代理店の皆さまも必見です✨\nお客様へのご提案に「なんとなくおすすめ」から「理由も伝えておすすめ」できる知識を！！\nその毛量も説得力のひとつ👏 Q-more.開発者のようへい先生から直接学べる大チャンスです！ぜひ一緒に学びましょう🙌\n\n【今後のスケジュール】\n第2回：11/4（水）21:00～22:00\n第3回：12/4（金）21:00～22:00"
    print("Updated event-20261104-mohatsu-2")

# 3. Update event-20261023-snack-aki (スナック亜希 22時開店チラシ反映)
if 'event-20261023-snack-aki' in event_map:
    e = event_map['event-20261023-snack-aki']
    e['startTime'] = "22:00"
    e['endTime'] = "23:00"
    e['subtitle'] = "また来ちゃった♡ 22時開店！人生に光を足すかもしれない特別な部屋へようこそ❤️"
    e['image'] = "images/event-20261023-snack-aki-22h.jpg"
    e['images'] = ["images/event-20261023-snack-aki-22h.jpg"]
    print("Updated event-20261023-snack-aki")

# New events to add
new_events = [
    {
        "id": "event-20261024-zubari-aging-shot-2",
        "title": "🔥📸 第2回！ズバリ言うわよ！ present by エイジングショットFC事業",
        "subtitle": "顔が長く見える！特に顎の長さが気になる！エイジングショット×再生美容（ヒト臍帯由来幹細胞培養上清液）",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-24",
        "startTime": "21:00",
        "endDate": "2026-10-24",
        "endTime": "21:30",
        "isAllDay": False,
        "location": "LIVEPARK（オンライン生配信）",
        "locationType": "online",
        "fee": "無料",
        "capacity": "",
        "presenter": "エイジングショットFC事業",
        "image": "",
        "images": [],
        "description": "ねぇ、ちょっと待って…🤣‼️ あなたは、自分の顔に隠れたクセに気づいてる？😳\n\n顔の写真を見てみると、自分では当たり前だと思っていた表情や身体の使い方のクセに気づくきっかけがあるかもしれません👀✨\n今回も実際のお写真をもとにお顔のお悩みをズバリ解説します‼️🔥\n\n【今回のお悩み】\n😳 「顔が長く見える！特に顎の長さが気になる！」\nなぜそう見えるのか？普段の何気ないクセが関係しているのか？\nご本人からは「めちゃくちゃ変わった！」「ありえないぐらい楽！！」という感想も😍✨\n\n✨ エイジングショット × 再生美容 ✨\nエイジングショットで取り扱うのは、ヒト臍帯由来の幹細胞培養上清液。\n美容の現場で新たな選択肢として取り入れられている再生美容の可能性をお伝えします！\n\n💎 美容の可能性を広げたい方\n💎 お客様に新しい美容の選択肢を届けたい方\n💎 エイジングショットを導入しているけれど理解を深めたい方\nぜひチェックしてください🔥\n\n🎬 ご視聴はこちら：\nhttps://events.livepark.jp/videos/8lBRwHGTCrd",
        "registrationUrl": "https://events.livepark.jp/videos/8lBRwHGTCrd",
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
        "id": "event-20261029-bengyo-ginger-komi-ria",
        "title": "🦍 勉強ジンジャー「“お利口さん”の檻から、一歩外へ」",
        "subtitle": "人に合わせる私から、やりたいことを選ぶ私へ（参加費1,000円）",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-29",
        "startTime": "20:00",
        "endDate": "2026-10-29",
        "endTime": "21:00",
        "isAllDay": False,
        "location": "⛩️ 勉強ジンジャー（オンライン）",
        "locationType": "online",
        "fee": "1,000円（売上全額定例会会場費充当）",
        "capacity": "",
        "presenter": "古見梨亜（enLIGHT 理事長）",
        "image": "images/event-20261029-bengyo-ginger-komi-ria.jpg",
        "images": [
            "images/event-20261029-bengyo-ginger-komi-ria.jpg"
        ],
        "description": "父も母も私もB型！\n「純粋ゴリラ」の私ですが、以前は人の目を気にして、周りに合わせてばかりでした😂\n\n看護師として働きながら、気づけば会話は不満や愚痴ばかり🌀\n私自身も、それが当たり前になっていました😭\n\nそんな私が、環境や仲間との出会いを通して、自分の「やりたい」に向かって動き始めるまでの経験をお話しします✨️\n\n●こんな方へおすすめ\n🍀人の目を気にせず、自分らしく動きたい！\n🍀周りに合わせて、自分の気持ちを後回しにしがち\n🍀「ママだから」「今さら」と挑戦をためらっている\n🍀やりたいことはあるけど、一歩が踏み出せない\n🍀環境や考え方を変えて、ステージアップしたい！\n\n私もまだ挑戦の途中ですが、皆さんが自分の「やりたい」に向き合い、一歩踏み出すヒントになれば嬉しいです☺️✨\n※売上げは、定例会の会場費に充てさせていただきます✨\n\nB型さんも、そうでない方も大歓迎🦍♪ たくさんのお仲間のご参加、お待ちしています🌸",
        "registrationUrl": "https://shopping.community-iyasakagu.jp/product/school_course1289/",
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
        "id": "event-20261030-hoken-money-seminar",
        "title": "💡 フリーランス自衛術＆成長戦略 ～会社は守ってくれない！病気・ケガ・借入リスクに備える完全ガイド～",
        "subtitle": "保険事業プレゼンツ！フリーランス・個人事業主必見の無料マネーセミナー",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-30",
        "startTime": "20:00",
        "endDate": "2026-10-30",
        "endTime": "21:00",
        "isAllDay": False,
        "location": "Zoom オンライン",
        "locationType": "online",
        "fee": "無料（参加者限定・無料個別相談あり）",
        "capacity": "",
        "presenter": "NEO FAMILY 保険事業",
        "image": "",
        "images": [],
        "description": "フリーランス・個人事業主の方必見！無料マネーセミナー開催のお知らせ💡\n\nフリーランス自衛術＆成長戦略\n～会社は守ってくれない！病気・ケガ・借入リスクに備える完全ガイド～\n\n「もし明日、病気やケガで仕事ができなくなったら？」\n「売上はあるのに、なぜかお金が手元に残らない…」\n「将来の年金や老後資金、このままで大丈夫？」\n「事業を大きくしたいけれど、借入や万が一のリスクが不安…」\nフリーランスや個人事業主は、自由に働ける一方で、会社員なら受けられる保障や福利厚生を自分で準備しなければなりません。\n自分と家族、そして大切な事業を守りながら、将来の成長につなげるお金の戦略をわかりやすくお伝えします！\n\n📚 セミナーで学べること\n✅ 病気・ケガで働けなくなったときの収入減少への備え\n✅ 医療費や生活費に困らないための資金準備\n✅ フリーランスが知っておきたい年金・老後資金の考え方\n✅ 節税制度を活用しながら、手元にお金を残す方法\n✅ 事業拡大に伴う借入リスクと、万が一に備える考え方\n✅ 将来の法人化も見据えた資産形成のステップ\n\n🎁 参加者限定・無料個別相談もご用意！\n\n参加をご希望の方は調整さんよりお申込みください：\nhttps://chouseisan.com/s?h=4fa29be4f6844f8ab5d6afb881d151d5",
        "registrationUrl": "https://chouseisan.com/s?h=4fa29be4f6844f8ab5d6afb881d151d5",
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
        "id": "event-20261031-bengyo-ginger-furuichi-mika",
        "title": "🌈 勉強ジンジャー「ゲイ夫×ストレート妻の、新しい家族のカタチ♡」～シリーズ第1回“出会い編”～",
        "subtitle": "家族って、こうじゃなきゃいけないの？ハロウィンの夜はみんなここに集まれ！",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-31",
        "startTime": "21:00",
        "endDate": "2026-10-31",
        "endTime": "22:00",
        "isAllDay": False,
        "location": "⛩️ 勉強ジンジャー（オンライン）",
        "locationType": "online",
        "fee": "売上全額定例会会場費充当",
        "capacity": "",
        "presenter": "古市美香（常勝会・Harmony支部理事長）",
        "image": "images/event-20261031-bengyo-ginger-furuichi-mika.jpg",
        "images": [
            "images/event-20261031-bengyo-ginger-furuichi-mika.jpg"
        ],
        "description": "皆さんこんにちは！\n常勝会・Harmony支部理事長のみかりんこと古市美香です😊\n\n実は私……世間では一風変わった結婚をしています！！！\nそれは……旦那さんがゲイであること！！\n\nえ？？どゆこと！？いつ知ったの？初めから知ってたの？子どもはどうやって？\n皆さんの疑問質問にもお答えしながら、世の中の「当たり前」や「常識」をぶっ壊しにいく1時間✨\nハロウィンの夜は、みんなここに集まれーーー！🙌\n\n_________________________\n🌈 ちょっと聞いてほしい、我が家の話🤣❤️\nゲイの夫×ストレート妻の、新しい家族のカタチ。～シリーズ第1回“出会い編”～\n\n出会いも、恋愛も、家族のカタチも、我が家はちょっと個性的！？\n笑いありのお話をしながら、「家族・愛・幸せに正解ってあるの？」をゆるっと考えてみませんか？🥰\n\n⚠️重要⚠️\n売上は全て、NEO FAMILY. 定例会の会場費に充てられます‼️\nみんなで創るNEO FAMILY. ❣️是非、多くの方のご参加をお待ちしております💓",
        "registrationUrl": "https://community-iyasakagu.jp/subschool/course/school_course1267/",
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
    if ne['id'] not in event_map:
        events.append(ne)
        event_map[ne['id']] = ne
        print(f"Added new event: {ne['id']} ({ne['title']})")
    else:
        print(f"Skipping duplicate event id: {ne['id']}")

# Sort events chronologically by startDate then startTime
events.sort(key=lambda x: (x.get('startDate', ''), x.get('startTime', '')))
print(f"Total events now: {len(events)}")

# Write events.json
with open('events.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, ensure_ascii=False, indent=2)
print("Updated events.json")

# Write js/events-data.js
js_output = "/**\n * NEO FAMILY Events Dataset\n * Generated from LINE Group Chat Notices & Provided Data\n * Total events: " + str(len(events)) + "\n */\n\nconst INITIAL_EVENTS = " + json.dumps(events, ensure_ascii=False, indent=2) + ";\n"
with open('js/events-data.js', 'w', encoding='utf-8') as f:
    f.write(js_output)
print("Updated js/events-data.js")

# Generate updated neofamily_all_events.ics
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

with open('neofamily_all_events.ics', 'w', encoding='utf-8') as f:
    f.write("\r\n".join(ics_lines))
print("Updated neofamily_all_events.ics")

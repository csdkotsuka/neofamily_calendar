# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

# Load existing events from js/events-data.js (which has 47 items)
with open('js/events-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract json
marker = 'const INITIAL_EVENTS = '
start = content.find(marker)
if start == -1:
    raise ValueError("Could not find INITIAL_EVENTS in js/events-data.js")

json_str = content[start + len(marker):].rstrip().rstrip(';')
events = json.loads(json_str)
print(f"Loaded {len(events)} events from js/events-data.js")

# Map of existing event by ID
event_map = {e['id']: e for e in events}

# 1. Update existing event-20261023-kaicho-online
if 'event-20261023-kaicho-online' in event_map:
    e = event_map['event-20261023-kaicho-online']
    e['image'] = 'images/event-20261023-kaicho-online.jpg'
    e['images'] = ['images/event-20261023-kaicho-online.jpg']
    e['registrationUrl'] = 'https://forms.gle/iKhKs7iBC9qxxnZU9'
    print("Updated event-20261023-kaicho-online")

# 2. Update existing event-20261022-osakana
if 'event-20261022-osakana' in event_map:
    e = event_map['event-20261022-osakana']
    e['zoomUrl'] = 'https://us06web.zoom.us/j/86984245385?pwd=g0Sn20DCizVZ7ViHwhavyK57U6dBg8.1'
    e['zoomMeetingId'] = '869 8424 5385'
    e['zoomPasscode'] = '1111'
    print("Updated event-20261022-osakana")

# New events to append
new_events = [
    {
        "id": "event-20261021-kaicho-gurokon",
        "title": "📢 ぶった斬り会長 合同グルコン「主婦の方が稼げる根拠とは⁉️」",
        "subtitle": "個人事業主より何も知らない「主婦」の方が稼げる🔥 コミュニケーション会員・運営会員 合同Zoom",
        "category": "定例会",
        "categoryColor": "#e11d48",
        "startDate": "2026-10-21",
        "startTime": "21:00",
        "endDate": "2026-10-21",
        "endTime": "22:00",
        "isAllDay": False,
        "location": "Zoom オンライン",
        "locationType": "online",
        "fee": "無料（会員限定）",
        "capacity": "",
        "presenter": "ぶった斬り会長",
        "image": "",
        "images": [],
        "description": "📢 こんや！ 10/21 21時〜\nぶった斬り会長合同グルコンです✨\n\nさて‼️今日のテーマは…\n個人事業主より何も知らない「主婦」の方が稼げる🔥\nとはどういうことなのか⁉️\n\n会長はいつも『主婦は大丈夫じゃ！』というのですが…その根拠とは⁉️\nみなさん気になりませんかー⁉️ 会長自ら解説してくれます🙌✨\n\n▶︎コミュニケーション会員\n▶︎運営会員　合同\n\n会長から無料で直接学べる月に一度の貴重なチャンス‼️✨\n皆さま積極的にご参加ください⭐️",
        "registrationUrl": "",
        "zoomUrl": "https://us06web.zoom.us/j/88257025834?pwd=UCD7vXd4Wb2tSchrokwBGcgU5q6bam.1",
        "zoomMeetingId": "882 5702 5834",
        "zoomPasscode": "2026",
        "archive": {
            "hasArchive": False,
            "archiveUrl": "",
            "password": "",
            "notes": ""
        }
    },
    {
        "id": "event-20261022-seitai-balm",
        "title": "✨「バカ売れ整体バーム」TheraMove Balm 特別説明会",
        "subtitle": "たった9ヶ月で累計4000個突破！ぶった斬り会長コラボ新ラベル『ファミリーバーム』Ver新登場‼️",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-22",
        "startTime": "22:00",
        "endDate": "2026-10-22",
        "endTime": "23:00",
        "isAllDay": False,
        "location": "Zoom オンライン",
        "locationType": "online",
        "fee": "参加無料",
        "capacity": "",
        "presenter": "整体バーム TheraMove チーム / ぶった斬り会長",
        "image": "",
        "images": [],
        "description": "10/22（木）22:00〜\n\nみんな使ってる❕\n「バカ売れ整体バーム」\nたったの9ヶ月で全国で累計4,000個突破‼️\n\n「えっ⁉️なんで⁉️」\nあまりの即効性と万能性に驚きの声リピーターが続出❕\n整体バーム『TheraMove Balm』\n\n✅天然由来成分で超安心❕\n✅1gで1,000円する成分も❕\n✅奇跡の配合であらゆる痛みに❕\n\nさらに今回は…ぶった斬り会長とのコラボ❣️\n新ラベルの『ファミリーバーム』Verも新登場しました‼️\n\n【今回の説明会では】\n✅ 天然成分だけで整体を受けたあとのような感覚になる理由\n✅ 人気の秘密\n✅ 小顔、皮膚のトラブルにも！？\n✅ 超お得意なお金のお話し\nを一挙公開します‼️\n\n・スポーツの疲労 / 肩こりや腰痛 / 怪我や皮膚トラブル\nなどのお悩みをお抱えのあなた❕今日からその痛みとおさらばです👋\n\n驚きの動画の数々はこちら：\nhttps://www.instagram.com/nekturn_dance_seitai/",
        "registrationUrl": "https://www.instagram.com/nekturn_dance_seitai/",
        "zoomUrl": "https://us06web.zoom.us/j/81758041069?pwd=AQIjvXDvQjuc9m3HK5i0bvfupDMFFa.1",
        "zoomMeetingId": "817 5804 1069",
        "zoomPasscode": "375996",
        "archive": {
            "hasArchive": False,
            "archiveUrl": "",
            "password": "",
            "notes": ""
        }
    },
    {
        "id": "event-20261025-remiko-taiwa",
        "title": "精神科専門医 れみこ先生が教える！『人の心に届く、対話の心理学』",
        "subtitle": "NEO FAMILY.限定❣️特別無料講座 精神科専門医の視点から人間関係・恋愛・ビジネスの対話を解き明かす✨",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-25",
        "startTime": "21:00",
        "endDate": "2026-10-25",
        "endTime": "22:00",
        "isAllDay": False,
        "location": "Zoom オンライン",
        "locationType": "online",
        "fee": "無料（NEO FAMILY限定）",
        "capacity": "",
        "presenter": "精神科専門医 れみこ先生",
        "image": "",
        "images": [],
        "description": "NEO FAMILY.限定❣️特別無料講座\n精神科専門医 れみこ先生が教える！『人の心に届く、対話の心理学』\n\n💭「良かれと思って言ったのに、伝わらない…」\n💭「あの人、本当は何を考えているの？」\n💭「どうすれば、もっと人間関係がうまくいく？」\nそんな疑問を、精神科専門医の視点から楽しく解き明かします！😆✨\n\n❤️ 恋愛・夫婦関係に！\n🤝 職場・人間関係に！\n💎 営業・ビジネスに！\n\n大学病院や精神科救急、企業研修や有料のカウンセリング講座も手がけるれみこ先生‼️\nその専門知識を、NEO FAMILY.限定で無料でお届けします🎉\n講座では、メンバーだけの🌸特別情報もご案内予定🌸🎁",
        "registrationUrl": "",
        "zoomUrl": "https://us06web.zoom.us/j/85864096749?pwd=yiknu6hYRqwVeIbM1NbbjOiJbVwnBH.1",
        "zoomMeetingId": "858 6409 6749",
        "zoomPasscode": "102521",
        "archive": {
            "hasArchive": False,
            "archiveUrl": "",
            "password": "",
            "notes": ""
        }
    },
    {
        "id": "event-20261026-bengyo-ginger-nanako-yuko",
        "title": "⛩️ 勉強ジンジャー「引き寄せ力強化 〜あなたの成功への道しるべ〜」",
        "subtitle": "色で現在地を知り、星からのエネルギーチャージで引き寄せ力UP！色の専門家 七菜子 ＆ 星を読み解く伴走者 ゆこ",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-26",
        "startTime": "14:00",
        "endDate": "2026-10-26",
        "endTime": "15:00",
        "isAllDay": False,
        "location": "オンライン配信（勉強ジンジャー）",
        "locationType": "online",
        "fee": "定例会会場費補填チケット",
        "capacity": "",
        "presenter": "七菜子（色の専門家） / ゆこ（星を読み解く伴走者）",
        "image": "images/event-20261026-bengyo-ginger-nanako-yuko.png",
        "images": ["images/event-20261026-bengyo-ginger-nanako-yuko.png"],
        "description": "⛩️ 勉強ジンジャー 配信\n\n引き寄せ力強化 〜あなたの成功への道しるべ〜\n色で現在地を知り、星からのエネルギーチャージで引き寄せ力UP！\n\n🗓️ 10月26日（月）14:00〜15:00\n💻 勉強ジンジャーにて配信\n\n登壇：\n🎨 色の専門家 七菜子\n⭐ 星を読み解く伴走者 ゆこ\n\n※みなさんのご参加が【全額定例会会場費】の補填になります！",
        "registrationUrl": "https://community-iyasakagu.jp/",
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
        "id": "event-20261026-sanpun-cooking",
        "title": "🍳 億稼ぐのは「3分クッキング」？！成功する簡単なポイント",
        "subtitle": "10/26（月）21:00〜22:00 誰でも実践できる成功への簡単ステップを大公開！",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-26",
        "startTime": "21:00",
        "endDate": "2026-10-26",
        "endTime": "22:00",
        "isAllDay": False,
        "location": "Zoom オンライン",
        "locationType": "online",
        "fee": "無料",
        "capacity": "",
        "presenter": "NEO FAMILY",
        "image": "images/event-20261026-sanpun-cooking.jpg",
        "images": ["images/event-20261026-sanpun-cooking.jpg"],
        "description": "10/26（月）21:00〜22:00\n\n億稼ぐのは「3分クッキング」？！\n成功する簡単なポイント✨\n\nビジネスや収益化を難しく考えすぎていませんか？\nシンプルでわかりやすい成功のエッセンスを凝縮してお届けします！",
        "registrationUrl": "",
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
        "id": "event-20261027-bengyo-ginger-shiori",
        "title": "🚒🔥 勉強ジンジャー「かつて消防車と言われた女がRAYTUS No.2と呼ばれるようになるまで」",
        "subtitle": "enchant+理事長 青山しおり登壇！泣き虫・ネガティブ・モラハラ離婚を乗り越えて人生を変えた秘密を大公開👑",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-27",
        "startTime": "21:00",
        "endDate": "2026-10-27",
        "endTime": "22:00",
        "isAllDay": False,
        "location": "オンライン配信（勉強ジンジャー）",
        "locationType": "online",
        "fee": "定例会会場費補填チケット",
        "capacity": "",
        "presenter": "enchant+理事長 青山しおり",
        "image": "images/event-20261027-bengyo-ginger-shiori.jpg",
        "images": ["images/event-20261027-bengyo-ginger-shiori.jpg"],
        "description": "🚒🔥 勉強ジンジャー開催🔥🚒\nenchant+理事長🩵青山しおりです☺️\n\n10/27(火) 21:00～\n\n＼かつて消防車🚒と言われた女が／\nRAYTUS No.2と呼ばれるようになるまで✨\n\nhttps://community-iyasakagu.jp/subschool/course/school_course1284/\n\n2022年5月、会長との出会い\n当時の私は、とにかく泣き虫！！\nネガティブ全開！メンタル弱子！🤣\nそんな私に会長がつけたあだ名は…なんと「消防車🚒」笑\n\nそんな私が会長からマインドを学び、たった1年でネガティブを克服！！\n✔️ 人の目を気にして言えなかったことも言えるように！\n✔️ 我慢ばかりの自分から卒業！\n✔️ モラハラ旦那との離婚も決断！\n\nそして今では、なんと…\n👑 「RAYTUS No.2」 と呼ばれるまでに！！✨\n\n人は何歳からでも変われる！！\n昔の私みたいに「変わりたいのに変われない」「すぐネガティブになっちゃう」そんな人にこそ聞いてほしい！！\n🚒消防車からRAYTUS No.2へ👑 その秘密、全部お話ししちゃいます😆❤️\n\n※この度の売上は、全額定例会の会場費の補填になります！",
        "registrationUrl": "https://community-iyasakagu.jp/subschool/course/school_course1284/",
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
        "id": "event-20261028-bengyo-ginger-doubutsu",
        "title": "⛩️ 勉強ジンジャー「動物を守る、その先へ。」🐶🐱",
        "subtitle": "🐕犬派の美穂（菅野美穂）✖️猫派の美穂（大葉美穂）ダブル美穂がお届けする人と動物が輝ける社会を考える60分",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-28",
        "startTime": "22:00",
        "endDate": "2026-10-28",
        "endTime": "23:00",
        "isAllDay": False,
        "location": "オンライン配信（勉強ジンジャー）",
        "locationType": "online",
        "fee": "定例会会場費補填チケット",
        "capacity": "",
        "presenter": "Couleur理事長 菅野美穂 ＆ CHOICE理事長 大葉美穂",
        "image": "images/event-20261028-bengyo-ginger-doubutsu.jpg",
        "images": ["images/event-20261028-bengyo-ginger-doubutsu.jpg"],
        "description": "⛩️勉強ジンジャーのお知らせ📢\n\n【Couleur理事長 菅野美穂】\n【CHOICE理事長 大葉美穂】\n\n🗓 10/28(水) ⏰ 22:00〜23:00\n🐶🐱 動物を守る、その先へ。\n\n🐕犬派の美穂 ✖️ 猫派の美穂🐈‍⬛\n✨ダブル美穂がお届けする✨\n人も動物も、自分らしく輝ける社会を考える60分🌈\n\n動物大好きな2人が、それぞれの視点から「動物保護」と「これからの未来」について語ります🌈\n動物を守ることは、命を救うことだけじゃない🐕\n動物たちが幸せに暮らせること、そして関わる人たちも笑顔で自分らしく生きられること🐈‍⬛\n人が動物を助けるだけでなく、動物たちが人の心を支えることもある🐎\n\n難しい勉強会ではなく、未来について楽しくお話しする時間です☺️\n\n＊みなさんのご参加が【全額定例会会場費】の補填になります💕\nhttps://community-iyasakagu.jp/subschool/course/school_course1273/",
        "registrationUrl": "https://community-iyasakagu.jp/subschool/course/school_course1273/",
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
        "id": "event-20261029-diet-qa",
        "title": "まるっと解決 ダイエットQ&A（食事・運動・習慣・リバウンドなど）",
        "subtitle": "気になることなんでも聞いてね！食べ痩せダイエットコーチ中岡真沙美 ＆ ファシリテーター坂井照子",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-29",
        "startTime": "21:00",
        "endDate": "2026-10-29",
        "endTime": "22:00",
        "isAllDay": False,
        "location": "Zoom オンライン",
        "locationType": "online",
        "fee": "無料",
        "capacity": "",
        "presenter": "食べ痩せダイエットコーチ 中岡真沙美 / ファシリテーター 坂井照子",
        "image": "images/event-20261029-diet-qa.jpg",
        "images": ["images/event-20261029-diet-qa.jpg"],
        "description": "気になることなんでも聞いてね！\nまるっと解決 ダイエットQ&A\n\n🗓️ 10/29（木）21:00〜22:00\n\n・食事のコツは？\n・効率よくやせる方法は？\n・リバウンドしない秘訣は？\n食事・運動・習慣・モチベーションなど、ダイエットのお悩みをまるごと解決！\n\n登壇：\n🥗 食べ痩せダイエットコーチ 中岡真沙美\n🎤 ファシリテーター 坂井照子",
        "registrationUrl": "",
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
        "id": "event-20261030-rijicho-ginger-nagoya",
        "title": "⛩️ 理事長ジンジャー「それ、どうやっとるの？あなたにもなれる！美容の秘訣教えてあげる♥」",
        "subtitle": "キレイも元気も年齢に負けない。今よりもっと好きな私へ！いくえとまゆみの美と健康の名古屋弁トーク",
        "category": "セミナー・勉強会",
        "categoryColor": "#d97706",
        "startDate": "2026-10-30",
        "startTime": "20:00",
        "endDate": "2026-10-30",
        "endTime": "21:00",
        "isAllDay": False,
        "location": "オンライン配信（理事長ジンジャー）",
        "locationType": "online",
        "fee": "定例会会場費補填チケット",
        "capacity": "",
        "presenter": "いくえ ＆ まゆみ",
        "image": "images/event-20261030-rijicho-ginger-nagoya.jpg",
        "images": ["images/event-20261030-rijicho-ginger-nagoya.jpg"],
        "description": "⛩️ 理事長ジンジャー 配信\n\nそれ、どうやっとるの？あなたにもなれる！美容の秘訣教えてあげる♥\nキレイも元気も年齢に負けない。今よりもっと、好きな私へ。\n\n🗓️ 10月30日（金）20:00〜21:00\nいくえとまゆみの美と健康の名古屋弁トーク✨",
        "registrationUrl": "https://community-iyasakagu.jp/",
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
        "id": "event-20261102-machihoke-fukuoka",
        "title": "出張！まちのほけんしつ in 福岡（聞ける・話せる・体験できる！）",
        "subtitle": "定例会当日の午前開催！子育ての相談やお話し会＆ママのセルフケア体験（博多駅徒歩1分）",
        "category": "リアルイベント",
        "categoryColor": "#059669",
        "startDate": "2026-11-02",
        "startTime": "10:00",
        "endDate": "2026-11-02",
        "endTime": "11:30",
        "isAllDay": False,
        "location": "ふれあい貸し会議室 博多東（博多駅 徒歩1分）",
        "locationType": "offline",
        "fee": "参加無料・子連れOK",
        "capacity": "",
        "presenter": "まちのほけんしつ専門家チーム（みか、松田かなめ、えりな、ありさ、ももか、ゆうこ、みさき、美川浩一郎、FUMI）",
        "image": "images/event-20261102-machihoke-fukuoka-1.jpg",
        "images": [
            "images/event-20261102-machihoke-fukuoka-1.jpg",
            "images/event-20261102-machihoke-fukuoka-2.jpg"
        ],
        "description": "聞ける・話せる・体験できる！\n出張！まちのほけんしつ in 福岡\n\n🗓️ 11月2日（月）10:00〜11:30（11月福岡定例会の当日午前開催！）\n📍 会場：ふれあい貸し会議室 博多東（博多駅 徒歩1分）\n🎁 参加無料・子連れOK\n\n【10:10～10:40｜聞ける・話せるお話し会】\n子育ての「こんなとき、どうしたら？」を専門家と一緒に。\n・ブース①：マインドリセットナース みか / 管理栄養士 松田かなめ\n「家族のこと、自分のこと。誰に相談したらいい？子育てから介護まで、日々の不安を専門職と考える30分」\n・ブース②：発達育児を支える看護師 えりな / 管理栄養士 ありさ\n「栄養が心配。でも、無理には食べさせたくない。わが子に合う食事を考えるお話し会」\n\n【10:50～11:20｜ママのセルフケア体験】\n心身共にリラックスして、自分をいたわる時間に。\n・ブース①：柔道整復師 ももか / セラピスト ゆうこ / ハンドケア みさき\n「足・手・心から自分をいたわる3人の専門家によるセルフケア体験」\n・ブース②：整体師 美川浩一郎 / イーマ・サウンドセラピスト＆コーチ FUMI\n「自分を大切にする時間 イーマ・サウンドセラピー体験 / テラヘルツかっさ体験」",
        "registrationUrl": "",
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

# Append only new ones
for ne in new_events:
    if ne['id'] not in event_map:
        events.append(ne)
        event_map[ne['id']] = ne
        print(f"Added new event: {ne['id']} - {ne['title']}")
    else:
        print(f"Already exists: {ne['id']}")

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

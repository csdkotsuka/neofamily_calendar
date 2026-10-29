import json
import re

# 1. Load current blocklist JSON
with open('js/blocklist-data.json', 'r', encoding='utf-8') as f:
    blocklist = json.load(f)

print(f"Current count: {len(blocklist)}")
assert len(blocklist) == 780, f"Expected 780 items, found {len(blocklist)}"

# 2. Update blk_560 with Threads secondary_url and merged reason
updated_560 = False
for item in blocklist:
    if item['id'] == 'blk_560':
        item['secondary_url'] = "https://www.threads.com/@merci422y?igshid=NTc4MTIwNjQ2YQ=="
        item['platform'] = "Instagram / Threads"
        new_reason = "【2026-10-29 齋藤深雪（RAYTUS）報告】お友達がネオの方でご本人はやる気ないとの事です。"
        if item.get('reason'):
            item['reason'] = item['reason'] + "\n" + new_reason
        else:
            item['reason'] = new_reason
        updated_560 = True
        print(f"Updated blk_560: secondary_url set, platform={item['platform']}")
        break
assert updated_560, "blk_560 not found!"

# 3. Load candidate titles
with open('scripts/candidate_titles_oct30.json') as f:
    candidates = json.load(f)

# Build new entries
new_entries = []
start_no = 781

for c in candidates:
    if c.get("is_dup") or c.get("merge_target"):
        continue
    
    cand_id = c["cand_id"]
    u = c["raw_url"]
    username = c["username"]
    platform = c["platform"]
    fetched_title = c.get("fetched_title") or ""
    secondary_url = ""

    # Clean display name
    if cand_id == "c_11":
        name = "会長偽アカウント（TikTok）"
    elif cand_id == "c_14":
        name = "Aya (@therapist_aya24)"
        secondary_url = "https://www.threads.com/@therapist_aya24"
    elif fetched_title:
        # e.g., "はるな｜身体がよろこぶヨガ講師(@be_haruna_18)"
        if f"@{username}" not in fetched_title:
            name = f"{fetched_title} (@{username})"
        else:
            name = fetched_title
    else:
        name = f"@{username}"
    
    # Ensure standard parentheses
    name = name.replace("（@", " (@").strip()

    serial_no = start_no + len(new_entries)
    entry = {
        "date": c["date"],
        "reporter": c["reporter"],
        "name": name,
        "url": u,
        "secondary_url": secondary_url,
        "platform": platform,
        "url_warning": "",
        "reason": c.get("reason", ""),
        "image": c["image"],
        "id": f"blk_{serial_no}",
        "serialNo": serial_no
    }
    new_entries.append(entry)

print(f"Generated {len(new_entries)} new entries (blk_781 to blk_{start_no + len(new_entries) - 1})")
assert len(new_entries) == 54, f"Expected 54 new entries, got {len(new_entries)}"

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

md = re.sub(r'# LINE Note ブロックリスト スクリーンショット純粋文字起こし（全\d+枚）', '# LINE Note ブロックリスト スクリーンショット純粋文字起こし（全129枚）', md)
md = re.sub(r'提供いただいた全\d+枚のスクリーンショット', '提供いただいた全129枚のスクリーンショット', md)

new_transcriptions = '''
## [120/129] `Screenshot 2026-10-30 at 8.04.10.png`
```text
井峯明香奈/shAdow
https://www.threads.com/@hirachi_ceo?igshid=NTc4MTIwNjQ2YQ==
Oct 24 4:48 PM

井峯明香奈/shAdow
https://www.threads.com/@river_cangoxina?igshid=NTc4MTIwNjQ2YQ==
Oct 24 4:49 PM

坂本有莉菜/Mimola
聞いたことある～から
根掘り葉掘り聞いてきます。
自分の人生たのし～なので
おせっかい不用です。
https://www.instagram.com/riku_nurse.mama?srtk=MWNKOTBuYjM2MGdjbA==
Oct 24 9:35 PM

岸部千夏/Couleur
https://www.threads.com/@life_dorm.azusa
Oct 24 11:17 PM

長野さとみ/Ablaze
会長の偽アカです
https://www.instagram.com/camila812583?cplk=ZWJvYzc1dXI5dXN6
Oct 25 6:12 AM

服部達典/MURA
https://www.instagram.com/yunyun.kazamaura?psln=MWRIdjBiaW15bXluYg==
ネットワークに集中したいとのことです。
Oct 25 8:26 AM

いわやともみ/Blooming/東京
https://www.instagram.com/rinrin_neko?cplk=MXFjYmUzzVtNHo2Mg==
Oct 25 4:24 PM

小西みゆき/Mimola
会長のなりすましです
https://lite.tiktok.com/t/ZS9ydkNtkv7xs-8wliv/
Oct 25 4:28 PM
```

## [121/129] `Screenshot 2026-10-30 at 8.03.53.png`
```text
Oct 25 4:24 PM

小西みゆき/Mimola
会長のなりすましです
https://lite.tiktok.com/t/ZS9ydkNtkv7xs-8wliv/
Oct 25 4:28 PM

中嶋初美/glowell/大阪
腹が立ちました。
コメントは、恐らくお仲間の方かと思いますが、投稿主はブロック
で良いかと思います！
https://www.threads.com/@kodomo_mirai_ouentai
Oct 25 7:40 PM

畠山尚美
https://www.threads.com/@momikaemasa?igshid=NTc4MTIwNjQ2YQ==
何度もネオファミリーの話しは聞いてる
ネクストエイドが1番とやってるそう。
ネオに入る気全くなく時間の無駄です
Oct 25 8:25 PM

飯田晃/碧春
https://www.instagram.com/be_haruna_18?xtok=MXR2aDQ5MnF5azVxMw==
3回ほど声をかけられて断っているそうです。
Oct 25 9:37 PM

服部達典/MURA
https://www.instagram.com/nanairokoubou.k?srtk=MXAzc25yNDhucjkONA==
Oct 25 10:29 PM

ロジャーズ優衣\\enchant+
https://www.instagram.com/mai.bitoreppi?psln=MWgxb21yOHakN3U1ZA==
先日お話聞いたばかりだそうです♪
Oct 25 11:07 PM
```

## [122/129] `Screenshot 2026-10-30 at 8.03.48.png`
```text
先日お話聞いたばかりだそうです♪
Oct 25 11:07 PM

城間千聖/enLIGHT
https://www.instagram.com/omochi.ehon?obrf=YzaiYmk3anIwaGwo
コミュニティーに属する気はないそうです
Oct 25 11:22 PM

ロジャーズ優衣\\enchant+
https://www.instagram.com/arona_keana._.maki?vrfl=MxNnZwgnemhrY280Ng==
Oct 25 11:32 PM

井峯明香奈/shAdow
https://www.threads.com/@earthforest1257?igshid=NTc4MTIwNjQ2YQ==
4回もDM来てるそうなので、送らないであげてください！
Oct 26 1:35 PM

井峯明香奈/shAdow
https://www.threads.com/@a_mori0820?igshid=NTc4MTIwNjQ2YQ==
Oct 26 1:35 PM

井峯明香奈/shAdow
https://www.threads.com/@atsumama0412?igshid=NTc4MTIwNjQ2YQ==
Oct 26 3:52 PM

井峯明香奈/shAdow
https://www.threads.com/@mia_mia0725?igshid=NTc4MTIwNjQ2YQ==
Oct 26 3:53 PM

桝田和裕/AMATERAS
https://www.instagram.com/nao.on?rpxt=MXdoZTV6ZGFmMmM2pg==
Oct 26 4:39 PM

小西みゆき/Mimola
会長の偽アカです
https://lite.tiktok.com/t/ZS9yFaW83nuvF-8euZi/
Oct 26 5:07 PM
```

## [123/129] `Screenshot 2026-10-30 at 8.03.21.png`
```text
小西みゆき/Mimola
会長の偽アカです
https://lite.tiktok.com/t/ZS9yFaW83nuvF-8euZi/
Oct 26 5:07 PM

小西みゆき/Mimola
こちらも会長の偽アカです
https://lite.tiktok.com/t/ZS9yFaW83nuvF-8euZi/
Oct 26 5:10 PM

森崎江里／愛知県/RAYTUS
https://www.instagram.com/fleur.n0708?mdxt=YnRmbHI3d3FoMWNy
https://www.instagram.com/turtle.1626272?dirf=MWRvcGRiajlpdDc5cg==
Oct 26 7:04 PM

北御門祥子 ／ Ablaze
https://www.threads.com/share/BAEHSrbqw5/
Oct 26 7:27 PM

後藤広代/Lumiere.
https://www.threads.com/@vitamare0314
Oct 26 11:10 PM

後藤広代/Lumiere.
https://www.threads.com/@gghl4255
Oct 26 11:14 PM

坂井照子/AMATERAS
https://www.threads.com/@nisitatuya?igshid=NTc4MTIwNjQ2YQ==
Oct 26 11:34 PM

内本ちはる（ensemble）
みやすいように（人
Oct 27 12:17 AM
```

## [124/129] `Screenshot 2026-10-30 at 8.03.14.png`
```text
みやすいように（人
Oct 27 12:17 AM

井峯明香奈/shAdow
https://www.threads.com/@haruetokito?igshid=NTc4MTIwNjQ2YQ==
警戒されたのかな？
Oct 27 10:26 AM

岡本祐果/ROOTIA
ネットワーカーでした
https://www.threads.com/@mirai_creation.55
Oct 27 1:10 PM

小野八音/yaShine
コミュニティ参加、ビジネスのお話は不用とのことです！
https://www.instagram.com/artemis_labo_flower?xtok=MTION2FxMWRycjJzaw==
Oct 27 2:55 PM

桝田和裕/AMATERAS
アポで話してバリバリのネットワーカーでした
https://www.threads.com/@sachi_yo.yo?igshid=NTc4MTIwNjQ2YQ==
Oct 27 5:25 PM

桝田和裕/AMATERAS
https://www.threads.com/@sumiko__artmake?igshid=NTc4MTIwNjQ2YQ==
Oct 27 7:37 PM

服部達典/MURA
https://www.instagram.com/umi07_08?cplk=NGVhNGVyeiZqaGpo
https://www.instagram.com/shino_soh_uma?vrfl=dTZ6czlhdTB4c2wy
https://www.instagram.com/masabuu.inst?psln=MWJibzR10XBicHgyeg==
Oct 27 11:32 PM
```

## [125/129] `Screenshot 2026-10-30 at 8.03.09.png`
```text
https://www.instagram.com/umi07_08?cplk=NGVhNGVyeiZqaGpo
https://www.instagram.com/shino_soh_uma?vrfl=dTZ6czlhdTB4c2wy
https://www.instagram.com/masabuu.inst?psln=MWJibzR10XBicHgyeg==
Oct 27 11:32 PM

桝田和裕/AMATERAS
https://www.instagram.com/mul_886?srtk=MWx0OWR2enJseGdvbA==
Oct 27 11:50 PM

服部達典/MURA
https://www.instagram.com/yui.yuinowa0o?srtk=b3UyaHQ2MGUxM214
Two days ago at 5:42 AM

畑ゆかり/yuima-ru理事長
https://www.threads.com/@hiroko.9531527?igshid=NTc4MTIwNjQ2YQ==
Two days ago at 7:53 AM

菅野美穂/Couleur理事長
https://www.threads.com/@akiko.lihiro.dog?igshid=NTc4MTIwNjQ2YQ==
立ち上げには興味ないとの事です
Two days ago at 10:02 AM

太田千鶴子/Couleur
https://www.threads.com/@maaru.kurasi.no.kango
https://www.threads.com/@haruetokito
https://www.threads.com/@naoko.kuma_healthsupport
結構前の投稿ですが、まちのほけんしつのこと書かれていました！
Two days ago at 11:10 AM
```

## [126/129] `Screenshot 2026-10-30 at 8.03.03.png`
```text
Two days ago at 11:10 AM

澤木優里/RAYTUS
https://www.instagram.com/kitohmidori67
Two days ago at 11:16 AM

服部達典/MURA
https://www.instagram.com/shino_soh_uma?vrfl=dTZ6czlhdTB4c2wy
他の事もあるので、見送りますとのことです
Two days ago at 12:24 PM

服部達典/MURA
https://www.instagram.com/meguri.kaori?dirf=MW4xY2hydTklanZxCW==
Two days ago at 12:29 PM

服部達典/MURA
https://www.instagram.com/haruko.relax00?rpxt=NGdnbDJudnIxNGJ5
すでに自分の会社で町の保健室を立ち上げてるから大丈夫とのことでした
Two days ago at 9:04 PM

服部達典/MURA
https://www.instagram.com/yukosensei_kosodate_sos?exln=MWExYTE3ZXJIN25pag==
三回ほど受け取ってます。しかし、私には響かないとのことでした
Two days ago at 10:39 PM

桝田和裕/AMATERAS
https://www.threads.com/@ayaka_monolog?igshid=NTc4MTIwNjQ2YQ==
https://www.threads.com/@manami.diet?igshid=NTc4MTIwNjQ2YQ==
Two days ago at 11:08 PM
```

## [127/129] `Screenshot 2026-10-30 at 8.02.59.png`
```text
Two days ago at 11:08 PM

桝田和裕/AMATERAS
https://www.instagram.com/yukirg?obrf=MWO2dDlxYzlycnloeg==
Two days ago at 11:11 PM

澤木優里/RAYTUS
https://www.instagram.com/yuko_acj?dlrf=MWZweGFseGtnb3c3Mw==
Two days ago at 11:40 PM

後藤広代/Lumiere.
https://www.threads.com/@youko_toriumi
こじらせタイプです
Two days ago at 11:43 PM

大森幸子/tidy.shin兵庫県加古川
https://www.instagram.com/sorasaku.6?cplk=MWwzaDahZ3Axamg5aQ==
Yesterday at 12:52 AM

服部達典/MURA
https://www.instagram.com/iyashisaron_mimosa?rpxt=MWlaNmZvMzFxazBpdA==
Yesterday at 11:08 AM

小野八音/yaShine
https://www.instagram.com/yuka.rikon?obrf=MWFkbGdtMIndzZGNIbw==
ご自分の仲間と活動中とのことです（^^）
Yesterday at 11:51 AM

小野八音/yaShine
https://www.instagram.com/ayabe_non_?exln=MXZpYnAxeWvgzNnVrcA==
それぞれの場所で頑張りましょうと！のことです
Yesterday at 11:52 AM

澤木優里/RAYTUS
https://www.instagram.com/chi_yutori_life?xtok=MXEOGjl5Z3k2b3NrYQ==
自分も大きな団体持っている・ビジネスモデルがアメリカ起源で〜とよくわからない長文の丁寧なお断りの返信が来ました。
Yesterday at 12:01 PM
```

## [128/129] `Screenshot 2026-10-30 at 8.02.53.png`
```text
自分も大きな団体持っている・ビジネスモデルがアメリカ起源で〜とよくわからない長文の丁寧なお断りの返信が来ました。
Yesterday at 12:01 PM

齋藤深雪/RAYTUS
https://www.threads.com/@merci422y?igshid=NTc4MTIwNjQ2YQ==
お友達がネオの方でご本人はやる気ないとの事です。
https://www.threads.com/@otani_colortype?igshid=NTc4MTIwNjQ2YQ==
何度も話聞いてるみたいなのでおせっかい不用です。
Yesterday at 12:05 PM

大森幸子/tidy.shin兵庫県加古川
https://www.threads.com/@traverermini.0520?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 12:14 PM

桝田和裕/AMATERAS
https://www.threads.com/@ptr_natsumi?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 1:08 PM

桝田和裕/AMATERAS
https://www.instagram.com/hiromi_note.and_?vrfl=MTNIdjZzenVhYWt4aw==
Yesterday at 1:11 PM

服部達典/MURA
https://www.instagram.com/raterate728?cplk=MWtlYnVubHZzb2huNQ==
Zoomとしては2回目で、入会金や活動実態に対して、あまり良く思われていないようでした。
Yesterday at 1:34 PM
```

## [129/129] `Screenshot 2026-10-30 at 8.02.48.png`
```text
Yesterday at 1:34 PM

森田由香利/yaShine
https://www.threads.com/@hsgdjdjsh.95?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 4:35 PM

服部達典/MURA
https://www.instagram.com/yoga_yokohama_erika?psln=MWinc2g5ciNSNjiNmaw==
Yesterday at 5:06 PM

井峯明香奈/shAdow
https://www.threads.com/@snn2789?igshid=NTc4MTIwNjQ2YQ==
Yesterday at 7:01 PM

服部達典/MURA
https://www.instagram.com/aki_ko_1027?vrfl=MmxkaDlhdzNwdHA1
集客、認知には興味がないそうです
Yesterday at 8:47 PM

服部達典/MURA
https://www.instagram.com/yoshioka_pedilist?psln=MXFsNHJnamJkM2ZIbA==
3 hours ago

桝田和裕/AMATERAS
https://www.threads.com/@meru13022?igshid=NTc4MTIwNjQ2YQ==
1 hour ago

服部達典/MURA
https://www.instagram.com/pilatesstudio_lunae?exln=MXindGVucXJ4MxVONg==
1 hour ago

藤田萌/Blooming
https://www.threads.com/@relaxation_macaron.milk?igshid=NTc4MTIwNjQ2YQ==
精神に大変です
55 minutes ago
```
'''

md = md.strip() + "\n" + new_transcriptions

with open('blocklist_raw_transcription.md', 'w', encoding='utf-8') as f:
    f.write(md)

print("Updated blocklist_raw_transcription.md successfully!")

# 7. Update cache busters
with open('admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

admin_html = re.sub(r'blocklist-data\.js\?v=[^"]+', 'blocklist-data.js?v=20261030_1', admin_html)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("Updated admin.html cache buster to 20261030_1")

with open('sw.js', 'r', encoding='utf-8') as f:
    sw_js = f.read()

sw_js = re.sub(r'neofamily-cache-v[^\"]+', 'neofamily-cache-v20261030_1', sw_js)

with open('sw.js', 'w', encoding='utf-8') as f:
    f.write(sw_js)

print("Updated sw.js CACHE_NAME to neofamily-cache-v20261030_1")

import json, urllib.request, re, html, time
from urllib.parse import urlparse

# Candidate raw items from OCR
candidates_raw = [
    # Oct 25
    {
        "cand_id": "c_01",
        "date": "2026-10-25 21:37",
        "reporter": "飯田晃（碧春）",
        "raw_url": "https://www.instagram.com/be_haruna_18?xtok=MXR2aDQ5MnF5azVxMw==",
        "username": "be_haruna_18",
        "platform": "Instagram",
        "reason": "3回ほど声をかけられて断っているそうです。",
        "image": "Screenshot 2026-10-30 at 8.03.53.png"
    },
    {
        "cand_id": "c_02",
        "date": "2026-10-25 22:29",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/nanairokoubou.k?srtk=MXAzc25yNDhucjkONA==",
        "username": "nanairokoubou.k",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.53.png"
    },
    {
        "cand_id": "c_03",
        "date": "2026-10-25 23:07",
        "reporter": "ロジャーズ優衣（enchant+）",
        "raw_url": "https://www.instagram.com/mai.bitoreppi?psln=MWgxb21yOHakN3U1ZA==",
        "username": "mai.bitoreppi",
        "platform": "Instagram",
        "reason": "先日お話聞いたばかりだそうです♪",
        "image": "Screenshot 2026-10-30 at 8.03.53.png"
    },
    {
        "cand_id": "c_04",
        "date": "2026-10-25 23:22",
        "reporter": "城間千聖（enLIGHT）",
        "raw_url": "https://www.instagram.com/omochi.ehon?obrf=YzaiYmk3anIwaGwo",
        "username": "omochi.ehon",
        "platform": "Instagram",
        "reason": "コミュニティーに属する気はないそうです",
        "image": "Screenshot 2026-10-30 at 8.03.48.png"
    },
    {
        "cand_id": "c_05",
        "date": "2026-10-25 23:32",
        "reporter": "ロジャーズ優衣（enchant+）",
        "raw_url": "https://www.instagram.com/arona_keana._.maki?vrfl=MxNnZwgnemhrY280Ng==",
        "username": "arona_keana._.maki",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.48.png"
    },
    # Oct 26
    {
        "cand_id": "c_06",
        "date": "2026-10-26 13:35",
        "reporter": "井峯明香奈（shAdow）",
        "raw_url": "https://www.threads.com/@earthforest1257?igshid=NTc4MTIwNjQ2YQ==",
        "username": "earthforest1257",
        "platform": "Threads",
        "reason": "4回もDM来てるそうなので、送らないであげてください！",
        "image": "Screenshot 2026-10-30 at 8.03.48.png"
    },
    {
        "cand_id": "c_07",
        "date": "2026-10-26 13:35",
        "reporter": "井峯明香奈（shAdow）",
        "raw_url": "https://www.threads.com/@a_mori0820?igshid=NTc4MTIwNjQ2YQ==",
        "username": "a_mori0820",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.48.png"
    },
    {
        "cand_id": "c_08",
        "date": "2026-10-26 15:52",
        "reporter": "井峯明香奈（shAdow）",
        "raw_url": "https://www.threads.com/@atsumama0412?igshid=NTc4MTIwNjQ2YQ==",
        "username": "atsumama0412",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.48.png"
    },
    {
        "cand_id": "c_09",
        "date": "2026-10-26 15:53",
        "reporter": "井峯明香奈（shAdow）",
        "raw_url": "https://www.threads.com/@mia_mia0725?igshid=NTc4MTIwNjQ2YQ==",
        "username": "mia_mia0725",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.48.png"
    },
    {
        "cand_id": "c_10",
        "date": "2026-10-26 16:39",
        "reporter": "桝田和裕（AMATERAS）",
        "raw_url": "https://www.instagram.com/nao.on?rpxt=MXdoZTV6ZGFmMmM2pg==",
        "username": "nao.on",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.48.png"
    },
    {
        "cand_id": "c_11",
        "date": "2026-10-26 17:07",
        "reporter": "小西みゆき（Mimola）",
        "raw_url": "https://lite.tiktok.com/t/ZS9yFaW83nuvF-8euZi/",
        "username": "ZS9yFaW83nuvF-8euZi",
        "platform": "TikTok",
        "reason": "会長の偽アカです",
        "image": "Screenshot 2026-10-30 at 8.03.48.png"
    },
    {
        "cand_id": "c_12",
        "date": "2026-10-26 19:04",
        "reporter": "森崎江里（愛知県 / RAYTUS）",
        "raw_url": "https://www.instagram.com/fleur.n0708?mdxt=YnRmbHI3d3FoMWNy",
        "username": "fleur.n0708",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.21.png"
    },
    {
        "cand_id": "c_13",
        "date": "2026-10-26 19:04",
        "reporter": "森崎江里（愛知県 / RAYTUS）",
        "raw_url": "https://www.instagram.com/turtle.1626272?dirf=MWRvcGRiajlpdDc5cg==",
        "username": "turtle.1626272",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.21.png"
    },
    {
        "cand_id": "c_14",
        "date": "2026-10-26 19:27",
        "reporter": "北御門祥子（Ablaze）",
        "raw_url": "https://www.threads.com/share/BAEHSrbqw5/",
        "username": "share_BAEHSrbqw5",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.21.png"
    },
    {
        "cand_id": "c_15",
        "date": "2026-10-26 23:10",
        "reporter": "後藤広代（Lumiere.）",
        "raw_url": "https://www.threads.com/@vitamare0314",
        "username": "vitamare0314",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.21.png"
    },
    {
        "cand_id": "c_16",
        "date": "2026-10-26 23:14",
        "reporter": "後藤広代（Lumiere.）",
        "raw_url": "https://www.threads.com/@gghl4255",
        "username": "gghl4255",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.21.png"
    },
    {
        "cand_id": "c_17",
        "date": "2026-10-26 23:34",
        "reporter": "坂井照子（AMATERAS）",
        "raw_url": "https://www.threads.com/@nisitatuya?igshid=NTc4MTIwNjQ2YQ==",
        "username": "nisitatuya",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.21.png"
    },
    # Oct 27
    {
        "cand_id": "c_18_dup",
        "date": "2026-10-27 10:26",
        "reporter": "井峯明香奈（shAdow）",
        "raw_url": "https://www.threads.com/@haruetokito?igshid=NTc4MTIwNjQ2YQ==",
        "username": "haruetokito",
        "platform": "Threads",
        "reason": "警戒されたのかな？",
        "image": "Screenshot 2026-10-30 at 8.03.14.png",
        "is_dup": True,
        "dup_target": "blk_329"
    },
    {
        "cand_id": "c_19",
        "date": "2026-10-27 13:10",
        "reporter": "岡本祐果（ROOTIA）",
        "raw_url": "https://www.threads.com/@mirai_creation.55",
        "username": "mirai_creation.55",
        "platform": "Threads",
        "reason": "ネットワーカーでした",
        "image": "Screenshot 2026-10-30 at 8.03.14.png"
    },
    {
        "cand_id": "c_20_dup",
        "date": "2026-10-27 14:55",
        "reporter": "小野八音（yaShine）",
        "raw_url": "https://www.instagram.com/artemis_labo_flower?xtok=MTION2FxMWRycjJzaw==",
        "username": "artemis_labo_flower",
        "platform": "Instagram",
        "reason": "コミュニティ参加、ビジネスのお話は不用とのことです！",
        "image": "Screenshot 2026-10-30 at 8.03.14.png",
        "is_dup": True,
        "dup_target": "blk_735"
    },
    {
        "cand_id": "c_21",
        "date": "2026-10-27 17:25",
        "reporter": "桝田和裕（AMATERAS）",
        "raw_url": "https://www.threads.com/@sachi_yo.yo?igshid=NTc4MTIwNjQ2YQ==",
        "username": "sachi_yo.yo",
        "platform": "Threads",
        "reason": "アポで話してバリバリのネットワーカーでした",
        "image": "Screenshot 2026-10-30 at 8.03.14.png"
    },
    {
        "cand_id": "c_22",
        "date": "2026-10-27 19:37",
        "reporter": "桝田和裕（AMATERAS）",
        "raw_url": "https://www.threads.com/@sumiko__artmake?igshid=NTc4MTIwNjQ2YQ==",
        "username": "sumiko__artmake",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.14.png"
    },
    {
        "cand_id": "c_23",
        "date": "2026-10-27 23:32",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/umi07_08?cplk=NGVhNGVyeiZqaGpo",
        "username": "umi07_08",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.14.png"
    },
    {
        "cand_id": "c_24",
        "date": "2026-10-27 23:32",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/shino_soh_uma?vrfl=dTZ6czlhdTB4c2wy",
        "username": "shino_soh_uma",
        "platform": "Instagram",
        "reason": "他の事もあるので、見送りますとのことです", # merged from Oct 28
        "image": "Screenshot 2026-10-30 at 8.03.14.png"
    },
    {
        "cand_id": "c_25",
        "date": "2026-10-27 23:32",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/masabuu.inst?psln=MWJibzR10XBicHgyeg==",
        "username": "masabuu.inst",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.14.png"
    },
    {
        "cand_id": "c_26",
        "date": "2026-10-27 23:50",
        "reporter": "桝田和裕（AMATERAS）",
        "raw_url": "https://www.instagram.com/mul_886?srtk=MWx0OWR2enJseGdvbA==",
        "username": "mul_886",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.09.png"
    },
    # Oct 28
    {
        "cand_id": "c_27",
        "date": "2026-10-28 05:42",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/yui.yuinowa0o?srtk=b3UyaHQ2MGUxM214",
        "username": "yui.yuinowa0o",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.09.png"
    },
    {
        "cand_id": "c_28",
        "date": "2026-10-28 07:53",
        "reporter": "畑ゆかり（yuima-ru理事長）",
        "raw_url": "https://www.threads.com/@hiroko.9531527?igshid=NTc4MTIwNjQ2YQ==",
        "username": "hiroko.9531527",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.09.png"
    },
    {
        "cand_id": "c_29",
        "date": "2026-10-28 10:02",
        "reporter": "菅野美穂（Couleur理事長）",
        "raw_url": "https://www.threads.com/@akiko.lihiro.dog?igshid=NTc4MTIwNjQ2YQ==",
        "username": "akiko.lihiro.dog",
        "platform": "Threads",
        "reason": "立ち上げには興味ないとの事です",
        "image": "Screenshot 2026-10-30 at 8.03.09.png"
    },
    {
        "cand_id": "c_30",
        "date": "2026-10-28 11:10",
        "reporter": "太田千鶴子（Couleur）",
        "raw_url": "https://www.threads.com/@maaru.kurasi.no.kango",
        "username": "maaru.kurasi.no.kango",
        "platform": "Threads",
        "reason": "結構前の投稿ですが、まちのほけんしつのこと書かれていました！",
        "image": "Screenshot 2026-10-30 at 8.03.09.png"
    },
    {
        "cand_id": "c_31",
        "date": "2026-10-28 11:10",
        "reporter": "太田千鶴子（Couleur）",
        "raw_url": "https://www.threads.com/@naoko.kuma_healthsupport",
        "username": "naoko.kuma_healthsupport",
        "platform": "Threads",
        "reason": "結構前の投稿ですが、まちのほけんしつのこと書かれていました！",
        "image": "Screenshot 2026-10-30 at 8.03.09.png"
    },
    {
        "cand_id": "c_32",
        "date": "2026-10-28 11:16",
        "reporter": "澤木優里（RAYTUS）",
        "raw_url": "https://www.instagram.com/kitohmidori67",
        "username": "kitohmidori67",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.03.png"
    },
    {
        "cand_id": "c_33",
        "date": "2026-10-28 12:29",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/meguri.kaori?dirf=MW4xY2hydTklanZxCW==",
        "username": "meguri.kaori",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.03.png"
    },
    {
        "cand_id": "c_34",
        "date": "2026-10-28 21:04",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/haruko.relax00?rpxt=NGdnbDJudnIxNGJ5",
        "username": "haruko.relax00",
        "platform": "Instagram",
        "reason": "すでに自分の会社で町の保健室を立ち上げてるから大丈夫とのことでした",
        "image": "Screenshot 2026-10-30 at 8.03.03.png"
    },
    {
        "cand_id": "c_35",
        "date": "2026-10-28 22:39",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/yukosensei_kosodate_sos?exln=MWExYTE3ZXJIN25pag==",
        "username": "yukosensei_kosodate_sos",
        "platform": "Instagram",
        "reason": "三回ほど受け取ってます。しかし、私には響かないとのことでした",
        "image": "Screenshot 2026-10-30 at 8.03.03.png"
    },
    {
        "cand_id": "c_36",
        "date": "2026-10-28 23:08",
        "reporter": "桝田和裕（AMATERAS）",
        "raw_url": "https://www.threads.com/@ayaka_monolog?igshid=NTc4MTIwNjQ2YQ==",
        "username": "ayaka_monolog",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.03.png"
    },
    {
        "cand_id": "c_37",
        "date": "2026-10-28 23:08",
        "reporter": "桝田和裕（AMATERAS）",
        "raw_url": "https://www.threads.com/@manami.diet?igshid=NTc4MTIwNjQ2YQ==",
        "username": "manami.diet",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.03.03.png"
    },
    {
        "cand_id": "c_38",
        "date": "2026-10-28 23:11",
        "reporter": "桝田和裕（AMATERAS）",
        "raw_url": "https://www.instagram.com/yukirg?obrf=MWO2dDlxYzlycnloeg==",
        "username": "yukirg",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.02.59.png"
    },
    {
        "cand_id": "c_39",
        "date": "2026-10-28 23:40",
        "reporter": "澤木優里（RAYTUS）",
        "raw_url": "https://www.instagram.com/yuko_acj?dlrf=MWZweGFseGtnb3c3Mw==",
        "username": "yuko_acj",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.02.59.png"
    },
    {
        "cand_id": "c_40",
        "date": "2026-10-28 23:43",
        "reporter": "後藤広代（Lumiere.）",
        "raw_url": "https://www.threads.com/@youko_toriumi",
        "username": "youko_toriumi",
        "platform": "Threads",
        "reason": "こじらせタイプです",
        "image": "Screenshot 2026-10-30 at 8.02.59.png"
    },
    # Oct 29
    {
        "cand_id": "c_41",
        "date": "2026-10-29 00:52",
        "reporter": "大森幸子（tidy.shin / 兵庫県加古川）",
        "raw_url": "https://www.instagram.com/sorasaku.6?cplk=MWwzaDahZ3Axamg5aQ==",
        "username": "sorasaku.6",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.02.59.png"
    },
    {
        "cand_id": "c_42",
        "date": "2026-10-29 11:08",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/iyashisaron_mimosa?rpxt=MWlaNmZvMzFxazBpdA==",
        "username": "iyashisaron_mimosa",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.02.59.png"
    },
    {
        "cand_id": "c_43",
        "date": "2026-10-29 11:51",
        "reporter": "小野八音（yaShine）",
        "raw_url": "https://www.instagram.com/yuka.rikon?obrf=MWFkbGdtMIndzZGNIbw==",
        "username": "yuka.rikon",
        "platform": "Instagram",
        "reason": "ご自分の仲間と活動中とのことです（^^）",
        "image": "Screenshot 2026-10-30 at 8.02.59.png"
    },
    {
        "cand_id": "c_44",
        "date": "2026-10-29 11:52",
        "reporter": "小野八音（yaShine）",
        "raw_url": "https://www.instagram.com/ayabe_non_?exln=MXZpYnAxeWvgzNnVrcA==",
        "username": "ayabe_non_",
        "platform": "Instagram",
        "reason": "それぞれの場所で頑張りましょうと！のことです",
        "image": "Screenshot 2026-10-30 at 8.02.59.png"
    },
    {
        "cand_id": "c_45",
        "date": "2026-10-29 12:01",
        "reporter": "澤木優里（RAYTUS）",
        "raw_url": "https://www.instagram.com/chi_yutori_life?xtok=MXEOGjl5Z3k2b3NrYQ==",
        "username": "chi_yutori_life",
        "platform": "Instagram",
        "reason": "自分も大きな団体持っている・ビジネスモデルがアメリカ起源で〜とよくわからない長文の丁寧なお断りの返信が来ました。",
        "image": "Screenshot 2026-10-30 at 8.02.59.png"
    },
    {
        "cand_id": "c_46_merge",
        "date": "2026-10-29 12:05",
        "reporter": "齋藤深雪（RAYTUS）",
        "raw_url": "https://www.threads.com/@merci422y?igshid=NTc4MTIwNjQ2YQ==",
        "username": "merci422y",
        "platform": "Threads",
        "reason": "お友達がネオの方でご本人はやる気ないとの事です。",
        "image": "Screenshot 2026-10-30 at 8.02.53.png",
        "merge_target": "blk_560"
    },
    {
        "cand_id": "c_47_dup",
        "date": "2026-10-29 12:05",
        "reporter": "齋藤深雪（RAYTUS）",
        "raw_url": "https://www.threads.com/@otani_colortype?igshid=NTc4MTIwNjQ2YQ==",
        "username": "otani_colortype",
        "platform": "Threads",
        "reason": "何度も話聞いてるみたいなのでおせっかい不用です。",
        "image": "Screenshot 2026-10-30 at 8.02.53.png",
        "is_dup": True,
        "dup_target": "blk_290"
    },
    {
        "cand_id": "c_48",
        "date": "2026-10-29 12:14",
        "reporter": "大森幸子（tidy.shin / 兵庫県加古川）",
        "raw_url": "https://www.threads.com/@traverermini.0520?igshid=NTc4MTIwNjQ2YQ==",
        "username": "traverermini.0520",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.02.53.png"
    },
    {
        "cand_id": "c_49",
        "date": "2026-10-29 13:08",
        "reporter": "桝田和裕（AMATERAS）",
        "raw_url": "https://www.threads.com/@ptr_natsumi?igshid=NTc4MTIwNjQ2YQ==",
        "username": "ptr_natsumi",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.02.53.png"
    },
    {
        "cand_id": "c_50",
        "date": "2026-10-29 13:11",
        "reporter": "桝田和裕（AMATERAS）",
        "raw_url": "https://www.instagram.com/hiromi_note.and_?vrfl=MTNIdjZzenVhYWt4aw==",
        "username": "hiromi_note.and_",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.02.53.png"
    },
    {
        "cand_id": "c_51",
        "date": "2026-10-29 13:34",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/raterate728?cplk=MWtlYnVubHZzb2huNQ==",
        "username": "raterate728",
        "platform": "Instagram",
        "reason": "Zoomとしては2回目で、入会金や活動実態に対して、あまり良く思われていないようでした。",
        "image": "Screenshot 2026-10-30 at 8.02.53.png"
    },
    {
        "cand_id": "c_52",
        "date": "2026-10-29 16:35",
        "reporter": "森田由香利（yaShine）",
        "raw_url": "https://www.threads.com/@hsgdjdjsh.95?igshid=NTc4MTIwNjQ2YQ==",
        "username": "hsgdjdjsh.95",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.02.48.png"
    },
    {
        "cand_id": "c_53",
        "date": "2026-10-29 17:06",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/yoga_yokohama_erika?psln=MWinc2g5ciNSNjiNmaw==",
        "username": "yoga_yokohama_erika",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.02.48.png"
    },
    {
        "cand_id": "c_54",
        "date": "2026-10-29 19:01",
        "reporter": "井峯明香奈（shAdow）",
        "raw_url": "https://www.threads.com/@snn2789?igshid=NTc4MTIwNjQ2YQ==",
        "username": "snn2789",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.02.48.png"
    },
    {
        "cand_id": "c_55",
        "date": "2026-10-29 20:47",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/aki_ko_1027?vrfl=MmxkaDlhdzNwdHA1",
        "username": "aki_ko_1027",
        "platform": "Instagram",
        "reason": "集客、認知には興味がないそうです",
        "image": "Screenshot 2026-10-30 at 8.02.48.png"
    },
    # Oct 30
    {
        "cand_id": "c_56",
        "date": "2026-10-30 05:00",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/yoshioka_pedilist?psln=MXFsNHJnamJkM2ZIbA==",
        "username": "yoshioka_pedilist",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.02.48.png"
    },
    {
        "cand_id": "c_57",
        "date": "2026-10-30 07:00",
        "reporter": "桝田和裕（AMATERAS）",
        "raw_url": "https://www.threads.com/@meru13022?igshid=NTc4MTIwNjQ2YQ==",
        "username": "meru13022",
        "platform": "Threads",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.02.48.png"
    },
    {
        "cand_id": "c_58",
        "date": "2026-10-30 07:00",
        "reporter": "服部達典（MURA）",
        "raw_url": "https://www.instagram.com/pilatesstudio_lunae?exln=MXindGVucXJ4MxVONg==",
        "username": "pilatesstudio_lunae",
        "platform": "Instagram",
        "reason": "",
        "image": "Screenshot 2026-10-30 at 8.02.48.png"
    },
    {
        "cand_id": "c_59_dup",
        "date": "2026-10-30 07:05",
        "reporter": "藤田萌（Blooming）",
        "raw_url": "https://www.threads.com/@relaxation_macaron.milk?igshid=NTc4MTIwNjQ2YQ==",
        "username": "relaxation_macaron.milk",
        "platform": "Threads",
        "reason": "精神に大変です",
        "image": "Screenshot 2026-10-30 at 8.02.48.png",
        "is_dup": True,
        "dup_target": "blk_738"
    }
]

def fetch_url_info(u):
    if not u or not u.startswith("http"):
        return None, None
    for ua in ["facebookexternalhit/1.1", "Twitterbot/1.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"]:
        try:
            req = urllib.request.Request(u, headers={
                "User-Agent": ua,
                "Accept-Language": "ja,en-US;q=0.9,en;q=0.8"
            })
            with urllib.request.urlopen(req, timeout=5) as r:
                final_url = r.geturl()
                body = r.read(98304).decode("utf-8", errors="ignore")
                og = re.search(r'property=["\']og:title["\']\s+content=["\'](.*?)["\']', body, re.I) or \
                     re.search(r'content=["\'](.*?)["\']\s+property=["\']og:title["\']', body, re.I) or \
                     re.search(r'name=["\']twitter:title["\']\s+content=["\'](.*?)["\']', body, re.I)
                t = re.search(r'<title[^>]*>(.*?)</title>', body, re.S | re.I)
                raw = og.group(1) if og else (t.group(1) if t else None)
                if raw:
                    raw = html.unescape(raw).strip()
                    raw = re.sub(r'\s*[\|｜•·-]\s*(?:Instagram|Threads|TikTok).*$', '', raw, flags=re.I).strip()
                return raw, final_url
        except Exception:
            pass
    return None, None

print(f"Total candidates to evaluate: {len(candidates_raw)}")

results = []
for idx, c in enumerate(candidates_raw):
    u = c["raw_url"]
    t, f_url = fetch_url_info(u)
    if not t and c["platform"] in ["Instagram", "Threads"] and not c.get("username", "").startswith("share_"):
        alt = f"https://www.threads.net/@{c['username']}" if c["platform"] == "Instagram" else f"https://www.instagram.com/{c['username']}/"
        alt_t, alt_f_url = fetch_url_info(alt)
        if alt_t:
            t = alt_t
            if not f_url:
                f_url = alt_f_url
    c["fetched_title"] = t
    c["final_url"] = f_url
    print(f"[{idx+1}/{len(candidates_raw)}] {c['cand_id']} {c['username']} -> {t}")
    results.append(c)

with open("scripts/candidate_titles_oct30.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved results to scripts/candidate_titles_oct30.json")

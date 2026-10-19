# NEO FAMILY イベントカレンダー & アーカイブポータル

ネオファミリーのグループLINEや公式アナウンスで共有されたイベント情報を一覧・カレンダー表示し、ワンクリックでGoogleカレンダーやiPhone/スマホカレンダーに登録できるWebポータルです。  
また、一部のイベントでは限定Zoom録画アーカイブをパスワード保護付きで安全に閲覧・管理できます。

---

## 🌟 主な機能

### 0. 🌐 NEO FAMILY × RAYTUS 総合ポータルハブ (`portal.html`) 【NEW】
- **初心者とベテランの両立**:
  - **初心者向け**: 「どこで何ができる？」「何から始めればいい？」を解決する4ステップ・スタートガイド、グループ全体構造図、参加フローチャート、おすすめ事業診断。
  - **ベテラン向け**: 今日のZoom（全日共通Zoom ID/PW、ワンクリックコピー）、次回定例会（11/2福岡）の調整さん参加表明へのショートカットHUD。
- **5つのオフィシャルリソースの完全統合＆テイスト再現**:
  1. **RAYTUS group 公式HP**: シネマティック動画背景、ロゴ、哲学、寺子屋・バスタ高校プロジェクト。
  2. **Iyasaka宮（配信 & EC）**: イヤサカスタジオ・こころチャンネル配信情報、イヤスタ限定ショップ（カート＆注文シミュレーション）、出店者検索。
  3. **スケジュール & 参加ガイド (Notion 1)**: 年間・月間予定、参加フローチャート、サポート一覧（タップで拡大表示）、クリスマスパーティー2026特設。
  4. **公式事業 & アーカイブ集 (Notion 2)**: 全18事業（ensemble、おむすび、ジュエリー等）＋特別勉強会（第1〜第6夜）のYouTube動画をページ内モーダル再生。
  5. **公式Instagram**: プロフィール、フォロワー数、ハイライト、投稿グリッドのUI再現。
- **上層部へのUI/UX改善提案バナー**: 各リソースの統合理由と効果をワンクリックでプレゼンできる説明モーダルを搭載。

### 1. 📅 2つのビュー切り替え
- **カード一覧ビュー**: フライヤー画像、日時、会場/Zoom情報、参加費、定員、詳細をスタイリッシュにカード表示。
- **月間カレンダービュー**: 2026年10月・11月・12月の月別カレンダー。
  - **イベントをクリック（またはダブルクリック）すると直接イベント詳細モーダルが開きます。**
  - 日付セルをクリックしても画面が勝手にスクロールしたりジャンプすることなく、その場で選択日の予定を確認できます。

### 2. 📲 スマホカレンダー登録＆ダウンロード
- **Googleカレンダーに追加**: タイトル、日時、場所、Zoomリンク、パスコードが自動入力されたGoogleカレンダー登録画面が開きます。
- **スマホに登録 (.ics)**: iPhone、Mac、Android、Outlookで即取り込めるiCalendar形式（.ics）をダウンロード。

### 3. 🔒 パスワード保護付き Zoomアーカイブ閲覧機能
- 開催済みの定例会や各種事業説明会、トークショーなどの録画アーカイブを保護付きで掲載。
- 「**パスワードを入力して視聴**」をクリックし、暗証コードを入力することでアンロックされ、動画リンクや視聴ノートが表示されます。
- **モーダルは「ESCキー」または「外側（背景）をクリック」で即座に閉じられます。**
- **管理者モード（設定機能）**:
  - 各イベントカード詳細右上の歯車アイコン（管理ボタン）から、ブラウザ上で新しいアーカイブURLや閲覧パスワードを追加・更新・保存（LocalStorage）できます。

### 4. 🔍 検索＆カテゴリフィルター
- **キーワード検索**: タイトル、登壇者（ぶった斬り会長、ようへい先生など）、会場名などでリアルタイム検索。
- **カテゴリフィルター**:
  - 🍜 定例会
  - 🎤 会長トークショー
  - 📢 事業説明会
  - ⛩️ 勉強会・セミナー
  - 🌿 リアル・マルシェ・体験

---

## ❓ Googleカレンダーに予定が表示されない理由と登録手順

指定いただいたカレンダーID（`c_5a885f7923e2170ff9b443b58c3612f4ff58809d0287730da1c1d6680bd8fa20@group.calendar.google.com`）は、まだGoogleカレンダー本体側に予定データが投入されていないため空の表示になっています。

### Googleカレンダーに全予定を一発で登録（インポート）する手順:
1. PCのブラウザで [Google カレンダー](https://calendar.google.com/) を開きます。
2. 右上の **歯車マーク（設定）** ＞ **「設定」** をクリック。
3. 左メニューの **「インポート / エクスポート」** をクリック。
4. 「パソコンからファイルを選択」で、リポジトリ内にある **`neofamily_all_events.ics`** を選択。
5. **「カレンダーに追加」** のプルダウンで、ネオファミリー用のカレンダーを選択。
6. **「インポート」** ボタンをクリック。
   👉 これで、全39件のイベントが一瞬で該当Googleカレンダーに登録され、共有している全メンバーのカレンダーにも反映されます！

---

## 🔥 Firebase（Firestore & Storage）登録とCloudflareでの連携手順

Webアプリは **Cloudflare（Cloudflare Pagesなど）** でホストしたまま、イベントのテキストや画像を **Firebase（Firestore & Firebase Storage）** で管理できます。

### 1. Firebase プロジェクトの作成
1. [Firebase Console](https://console.firebase.google.com/) を開きます。
2. 「プロジェクトを追加」をクリック（例: `neofamily-calendar`）。
3. プロジェクト概要の画面で「**ウェブ（</> アイコン）**」をクリックし、Webアプリを登録します。
4. 表示された `firebaseConfig`（以下の7項目）をコピーします:
   ```javascript
   const firebaseConfig = {
     apiKey: "AIzaSy...",
     authDomain: "neofamily-calendar.firebaseapp.com",
     projectId: "neofamily-calendar",
     storageBucket: "neofamily-calendar.appspot.com",
     messagingSenderId: "123456789012",
     appId: "1:123456789012:web:abcdef..."
   };
   ```
5. 本プロジェクトの `js/firebase-config.js` の `FIREBASE_CONFIG` に貼り付けます。

### 2. Firestore Database の有効化
1. Firebase Console 左メニュー > **構築** > **Firestore Database** を選択。
2. 「データベースの作成」をクリック（ロケーションは `asia-northeast1 (東京)` 推奨）。
3. 「テストモード」または以下のルールを設定:
   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /events/{eventId} {
         allow read: if true; // Web閲覧者は誰でも読み取り可能
         allow write: if request.auth != null; // 管理者のみ書き込み可能
       }
     }
   }
   ```

### 3. Firebase Storage の有効化（画像用）
1. 左メニュー > **構築** > **Storage** を選択。
2. 「使ってみる」をクリックし、バケットを作成。
3. ルール設定:
   ```javascript
   rules_version = '2';
   service firebase.storage {
     match /b/{bucket}/o {
       match /{allPaths=**} {
         allow read: if true;
         allow write: if request.auth != null;
       }
     }
   }
   ```

### 4. 既存データの一括流し込み（シード実行）
作成したスクリプトを使えば、全39件のデータを一撃でFirestoreに登録できます。

1. Firebase Console > **プロジェクトの設定** > **サービスアカウント** タブを開く。
2. **「新しい秘密鍵の生成」** をクリックし、ダウンロードされたJSONファイルを本リポジトリのルートに `serviceAccountKey.json` というファイル名で配置。
3. 以下のいずれかを実行:
   ```bash
   # Pythonの場合
   pip install firebase-admin
   python3 scripts/seed_to_firebase.py

   # Node.jsの場合
   npm install firebase-admin
   node scripts/seed_to_firebase.js
   ```
4. これでFirestoreの `events` コレクションに全データが登録され、Webアプリを開くとFirestoreから自動的にイベント一覧が取得されるようになります！

### 5. Cloudflare Pages へのデプロイ
1. Cloudflare Dashboard > **Workers & Pages** > **Create application** > **Pages**。
2. GitHubリポジトリ（`csdkotsuka/neofamily_calendar`）を連携。
3. ビルド設定:
   - **Framework preset**: None
   - **Build command**: (空のままでOK)
   - **Build output directory**: `/` (ルートのままでOK)
4. 「Save and Deploy」をクリックするだけで、Cloudflareの爆速CDN経由で世界中に配信されます。

---

## 📁 ディレクトリ構成
```text
├── index.html                  # メインページ（Tailwind CSS / 2ビュー切り替え / モーダル）
├── css/
│   └── style.css              # カスタムスタイル
├── js/
│   ├── firebase-config.js     # Firebase連携モジュール（Firestore非同期ローダー）
│   ├── events-data.js         # ローカル抽出済みイベントデータ（フォールバック用 39件）
│   └── app.js                 # アプリケーションロジック（カレンダー描画、ics生成、アーカイブ認証）
├── scripts/
│   ├── seed_to_firebase.py    # Firestore一括登録スクリプト (Python)
│   └── seed_to_firebase.js    # Firestore一括登録スクリプト (Node.js)
├── images/                    # イベントチラシ・フライヤー画像
├── neofamily_all_events.ics   # Googleカレンダー / スマホ一括インポート用.icsファイル
├── events.json                # 生JSONデータ
├── generate_events.py         # イベントデータ生成スクリプト
└── prvided data/              # LINEチャット元テキスト & 画像元データ
```

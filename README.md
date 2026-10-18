# NEO FAMILY イベントカレンダー & アーカイブポータル

ネオファミリーのグループLINEや公式アナウンスで共有されたイベント情報を一覧・カレンダー表示し、ワンクリックでGoogleカレンダーやiPhone/スマホカレンダーに登録できるWebアプリケーションです。  
また、一部のイベントでは限定Zoom録画アーカイブをパスワード保護付きで安全に閲覧・管理できます。

---

## 🌟 主な機能

### 1. 📅 3つのビュー切り替え
- **カード一覧ビュー**: フライヤー画像、日時、会場/Zoom情報、参加費、定員、詳細をスタイリッシュにカード表示。
- **月間カレンダービュー**: 2026年10月・11月・12月の月別カレンダー。日付セルをタップすると、その日の予定へスムーズにフォーカス。
- **公式Googleカレンダー埋め込み**: ネオファミリー公式Googleカレンダーをiframeでリアルタイム埋め込み表示。

### 2. 📲 スマホカレンダー登録＆ダウンロード
- **個別の予定登録**:
  - **Googleカレンダーに追加**: タイトル、日時、場所、Zoomリンク、パスコードが自動入力されたGoogleカレンダー登録画面が開きます。
  - **スマホに登録 (.ics)**: iPhone、Mac、Android、Outlookで即取り込めるiCalendar形式（.ics）をダウンロード。
- **全件一括登録**:
  - ヘッダーの「**一括登録 (.ics)**」ボタンから、全イベントを一括でスマホやPCのカレンダーにインポート可能。
  - 「**Googleカレンダー登録**」ボタンから、Googleアカウントに公式カレンダーをワンクリックで追加・購読可能。

### 3. 🔒 パスワード保護付き Zoomアーカイブ閲覧機能
- 開催済みの定例会や各種事業説明会、トークショーなどの録画アーカイブを保護付きで掲載。
- 「**パスワードを入力して視聴**」をクリックし、暗証コードを入力することでアンロックされ、動画リンクや視聴ノートが表示されます。
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

## 📌 カレンダーID
```text
c_5a885f7923e2170ff9b443b58c3612f4ff58809d0287730da1c1d6680bd8fa20@group.calendar.google.com
```

- **Googleカレンダー登録URL**:
  [Googleカレンダーに追加する](https://calendar.google.com/calendar/r?cid=c_5a885f7923e2170ff9b443b58c3612f4ff58809d0287730da1c1d6680bd8fa20@group.calendar.google.com)
- **Googleカレンダー埋め込みURL**:
  `https://calendar.google.com/calendar/embed?src=c_5a885f7923e2170ff9b443b58c3612f4ff58809d0287730da1c1d6680bd8fa20%40group.calendar.google.com&ctz=Asia%2FTokyo`

---

## 🚀 GitHub Pagesでの公開手順
このリポジトリはHTML/CSS/JavaScriptのみの静的サイト構成のため、GitHub Pagesですぐに全世界・会員向けに公開できます。

1. GitHubリポジトリの設定（Settings）を開きます。
2. 左メニューの **Pages** を選択します。
3. **Build and deployment** の Source で **Deploy from a branch** を選択。
4. Branch に **main**（または master）、Folder に **/ (root)** を指定して **Save** をクリック。
5. 数分後に公開URL（例: `https://csdkotsuka.github.io/neofamily_calendar/`）が発行されます。

---

## 📁 ディレクトリ構成
```text
├── index.html                  # メインページ
├── css/
│   └── style.css              # カスタムスタイル
├── js/
│   ├── events-data.js         # 抽出済みイベントデータ（39件）
│   └── app.js                 # アプリケーションロジック（カレンダー描画、ics生成、アーカイブ認証）
├── images/                    # イベントチラシ・フライヤー画像
├── neofamily_all_events.ics   # 全イベント入りiCalendarファイル
├── events.json                # 生JSONデータ
├── generate_events.py         # イベントデータ生成スクリプト
└── prvided data/              # 元データ（LINEテキスト・画像）
```

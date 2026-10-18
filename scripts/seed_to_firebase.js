/**
 * Firebase Firestore へのイベント一括アップロードスクリプト
 * 
 * 使い方:
 * 1. Firebase Console > プロジェクト設定 > サービス アカウント から
 *    「新しい秘密鍵の生成」をクリックし、ダウンロードしたJSONファイルを
 *    本ディレクトリに `serviceAccountKey.json` という名前で配置します。
 * 2. ターミナルで実行:
 *    npm install firebase-admin
 *    node scripts/seed_to_firebase.js
 */

const admin = require("firebase-admin");
const fs = require("fs");
const path = require("path");

const serviceAccountPath = path.join(__dirname, "../serviceAccountKey.json");

if (!fs.existsSync(serviceAccountPath)) {
  console.error("❌ エラー: serviceAccountKey.json が見つかりません。");
  console.log("Firebase Console > プロジェクト設定 > サービスアカウント より秘密鍵JSONを取得し、ルートディレクトリに配置してください。");
  process.exit(1);
}

const serviceAccount = require(serviceAccountPath);

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();
const eventsData = JSON.parse(fs.readFileSync(path.join(__dirname, "../events.json"), "utf8"));

async function seedData() {
  console.log(`🚀 ${eventsData.length} 件のイベントを Firestore の 'events' コレクションに登録開始...`);
  
  const batch = db.batch();
  
  for (const ev of eventsData) {
    const docRef = db.collection("events").doc(ev.id);
    batch.set(docRef, ev, { merge: true });
  }

  await batch.commit();
  console.log("✅ 全イベントの Firestore への登録が完了しました！");
}

seedData().catch(console.error);

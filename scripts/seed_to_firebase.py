# -*- coding: utf-8 -*-
"""
Firebase Firestore へのイベント一括アップロードスクリプト (Python版)

使い方:
1. Firebase Console > プロジェクト設定 > サービスアカウント より
   「新しい秘密鍵の生成」をクリックし、ダウンロードしたJSONを
   ルートに `serviceAccountKey.json` として配置。
2. 実行:
   pip install firebase-admin
   python3 scripts/seed_to_firebase.py
"""

import json
import os
import sys

SERVICE_KEY_PATH = "serviceAccountKey.json"

if not os.path.exists(SERVICE_KEY_PATH):
    print("❌ serviceAccountKey.json が見つかりません。")
    print("Firebase Console > プロジェクト設定 > サービスアカウント より秘密鍵を取得し配置してください。")
    sys.exit(1)

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    print("❌ firebase-admin がインストールされていません。")
    print("pip install firebase-admin を実行してください。")
    sys.exit(1)

cred = credentials.Certificate(SERVICE_KEY_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

with open("events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

print(f"🚀 {len(events)} 件のイベントを Firestore の 'events' コレクションに登録します...")

batch = db.batch()
for ev in events:
    doc_ref = db.collection("events").document(ev["id"])
    batch.set(doc_ref, ev, merge=True)

batch.commit()
print("✅ Firestore への登録が完了しました！")

# -*- coding: utf-8 -*-
"""
Google Calendar API を使って caravan-events.json の全イベント（ぶった斬り会長 全国キャラバン）を
指定のGoogleカレンダーに直接自動同期（作成）するスクリプト

カレンダーID:
c_1518f8a0d81830bb6be2a84b4ee3c865b33db3e46ca58d12d91443101f9fb611@group.calendar.google.com

前提条件:
1. Google Cloud Console で「Google Calendar API」を有効化
2. サービスアカウントを作成し、キーJSONをダウンロードして `google_service_account.json` として配置
3. 対象のGoogleカレンダーの設定で、サービスアカウントのメールアドレス（xxx@xxx.iam.gserviceaccount.com）に
   「予定の変更権限」を付与して共有
4. 実行:
   pip install google-api-python-client google-auth
   python3 scripts/sync_caravan_to_google_calendar.py
"""

import json
import os
import sys

CALENDAR_ID = "c_1518f8a0d81830bb6be2a84b4ee3c865b33db3e46ca58d12d91443101f9fb611@group.calendar.google.com"
SERVICE_ACCOUNT_FILE = "google_service_account.json"
EVENTS_FILE = "caravan-events.json"

if not os.path.exists(SERVICE_ACCOUNT_FILE):
    print("❌ google_service_account.json が見つかりません。")
    print("Google Cloud Console のサービスアカウント鍵をプロジェクトルートに配置してください。")
    print(f"対象カレンダーID: {CALENDAR_ID}")
    print("\n💡 サービスアカウントを使わない場合:")
    print("Googleカレンダーの「設定」＞「インポート/エクスポート」から `caravan_events.ics` をインポートすることで、一括登録が可能です！")
    sys.exit(1)

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except ImportError:
    print("❌ 必要なライブラリが不足しています。")
    print("pip install google-api-python-client google-auth を実行してください。")
    sys.exit(1)

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('calendar', 'v3', credentials=creds)

with open(EVENTS_FILE, "r", encoding="utf-8") as f:
    events = json.load(f)

print(f"🚀 {len(events)} 件のぶった斬り会長キャラバンイベントを Google カレンダー ({CALENDAR_ID}) に登録・同期します...")

for ev in events:
    s_dt = f"{ev['startDate']}T{ev['startTime']}:00+09:00"
    e_dt = f"{ev['endDate']}T{ev['endTime']}:00+09:00"

    desc = f"{ev.get('subtitle', '')}\n\n{ev.get('description', '')}"
    if ev.get("fee"):
        desc += f"\n\n参加費: {ev['fee']}"
    if ev.get("capacity"):
        desc += f"\n定員: {ev['capacity']}"
    if ev.get("organizer"):
        desc += f"\n{ev['organizer']}"

    body = {
        'summary': ev['title'],
        'description': desc,
        'location': ev.get('location', '現地会場'),
        'start': {'dateTime': s_dt, 'timeZone': 'Asia/Tokyo'},
        'end': {'dateTime': e_dt, 'timeZone': 'Asia/Tokyo'},
    }

    try:
        created_event = service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
        print(f"✅ 追加完了: {ev['startDate']} {ev['title']}")
    except Exception as e:
        print(f"⚠️ エラー ({ev['title']}): {e}")

print("🎉 会長キャラバン全イベントの同期処理が完了しました！")

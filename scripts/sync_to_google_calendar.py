# -*- coding: utf-8 -*-
"""
Google Calendar API を使って events.json の全イベントを
指定のGoogleカレンダーに直接自動同期（作成）するスクリプト

前提条件:
1. Google Cloud Console で「Google Calendar API」を有効化
2. サービスアカウントを作成し、キーJSONをダウンロードして `google_service_account.json` として配置
3. 対象のGoogleカレンダーの設定で、サービスアカウントのメールアドレス（xxx@xxx.iam.gserviceaccount.com）に
   「予定の変更権限」を付与して共有
4. 実行:
   pip install google-api-python-client google-auth
   python3 scripts/sync_to_google_calendar.py
"""

import json
import os
import sys

CALENDAR_ID = "c_5a885f7923e2170ff9b443b58c3612f4ff58809d0287730da1c1d6680bd8fa20@group.calendar.google.com"
SERVICE_ACCOUNT_FILE = "google_service_account.json"

if not os.path.exists(SERVICE_ACCOUNT_FILE):
    print("❌ google_service_account.json が見つかりません。")
    print("Google Cloud Console のサービスアカウント鍵を本ディレクトリに配置してください。")
    print(f"カレンダーID: {CALENDAR_ID}")
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

with open("events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

print(f"🚀 {len(events)} 件のイベントを Google カレンダー ({CALENDAR_ID}) に登録・同期します...")

for ev in events:
    s_dt = f"{ev['startDate']}T{ev['startTime']}:00+09:00"
    e_dt = f"{ev['endDate']}T{ev['endTime']}:00+09:00"

    desc = f"{ev.get('subtitle', '')}\n\n{ev.get('description', '')}"
    if ev.get("zoomUrl"):
        desc += f"\n\nZoom参加URL: {ev['zoomUrl']}"
        if ev.get("zoomMeetingId"): desc += f"\nミーティングID: {ev['zoomMeetingId']}"
        if ev.get("zoomPasscode"): desc += f"\nパスコード: {ev['zoomPasscode']}"

    body = {
        'summary': ev['title'],
        'description': desc,
        'location': ev.get('location', 'オンライン'),
        'start': {'dateTime': s_dt, 'timeZone': 'Asia/Tokyo'},
        'end': {'dateTime': e_dt, 'timeZone': 'Asia/Tokyo'},
    }

    try:
        created_event = service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
        print(f"✅ 追加完了: {ev['startDate']} {ev['title']}")
    except Exception as e:
        print(f"⚠️ エラー ({ev['title']}): {e}")

print("🎉 全イベントの同期処理が完了しました！")

/**
 * Cloudflare Pages Function: /api/config
 * Cloudflare Dashboard の「Settings」>「Environment Variables」に登録した
 * Firebase設定をフロントエンドへ安全に受け渡すエンドポイント
 */
export async function onRequestGet(context) {
  const env = context.env || {};

  const config = {
    apiKey: env.FIREBASE_API_KEY || "",
    authDomain: env.FIREBASE_AUTH_DOMAIN || "",
    projectId: env.FIREBASE_PROJECT_ID || "",
    storageBucket: env.FIREBASE_STORAGE_BUCKET || "",
    messagingSenderId: env.FIREBASE_MESSAGING_SENDER_ID || "",
    appId: env.FIREBASE_APP_ID || "",
    googleCalendarId: env.GOOGLE_CALENDAR_ID || "c_5a885f7923e2170ff9b443b58c3612f4ff58809d0287730da1c1d6680bd8fa20@group.calendar.google.com"
  };

  return new Response(JSON.stringify(config), {
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "public, max-age=300"
    }
  });
}

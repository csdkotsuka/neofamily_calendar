/**
 * Cloudflare Pages Functions: _middleware.js
 * ルート (/) が総合ポータル（index.html）のエントリーポイント
 * /portal へのアクセスは ルート (/) へリダイレクト
 */
export async function onRequest(context) {
  const url = new URL(context.request.url);

  // /portal へのアクセスは ルート (/) へリダイレクトして正規化
  if (url.pathname === '/portal' || url.pathname === '/portal.html') {
    return Response.redirect(`${url.origin}/`, 301);
  }

  return context.next();
}


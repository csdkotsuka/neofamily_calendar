/**
 * Cloudflare Pages Functions: _middleware.js
 * ルート (/) へのアクセスを /portal へリダイレクト
 * /portal へのアクセスは portal.html のコンテンツを返却
 */
export async function onRequest(context) {
  const url = new URL(context.request.url);

  // ルートへのアクセスを /portal へリダイレクト
  if (url.pathname === '/' || url.pathname === '') {
    return Response.redirect(`${url.origin}/portal`, 302);
  }

  // /portal へのアクセスは /portal.html を読み込んで返す
  if (url.pathname === '/portal') {
    const portalUrl = new URL(context.request.url);
    portalUrl.pathname = '/portal.html';
    return context.env.ASSETS ? context.env.ASSETS.fetch(portalUrl) : context.next();
  }

  return context.next();
}

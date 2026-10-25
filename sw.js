/**
 * NEO FAMILY Calendar - Service Worker
 * Handles PWA lifecycle, notifications, and offline caching.
 */

const CACHE_NAME = "neofamily-cache-v20261025_8";
const ASSETS_TO_CACHE = [
  "./",
  "./index.html",
  "./flowchart",
  "./raytus",
  "./iyasaka",
  "./calendar",
  "./caravan",
  "./caravan.html",
  "./archive",
  "./sns",
  "./admin.html",
  "./super-admin.html",
  "./css/style.css",
  "./js/events-data.js",
  "./js/caravan-events-data.js",
  "./js/caravan-app.js",
  "./images/kaicho_face.jpg",
  "./images/caravan/S__15892572.jpg",
  "./images/kusanagi_face.jpg",
  "./js/interactive-flowchart.js",
  "./js/admin.js",
  "./js/super-admin.js",
  "./js/raytus-services-data.js",
  "./js/raytus-shop-data.js",
  "./js/app.js",
  "./images/logo.png",
  "./images/icon-192.png",
  "./images/icon-512.png",
  "./images/apple-touch-icon.png",
  "./manifest.json"
];

// Install: Cache core assets and activate immediately
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE).catch((err) => {
        console.warn("[SW] Cache prefetch error:", err);
      });
    }).then(() => self.skipWaiting())
  );
});

// Activate: Clean up old caches
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME) {
            return caches.delete(name);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Network first, fallback to cache
self.addEventListener("fetch", (event) => {
  // Only handle GET requests for our origin
  if (event.request.method !== "GET" || !event.request.url.startsWith(self.location.origin)) {
    return;
  }

  // Never cache admin console or blocklist data — always fetch fresh from network
  if (
    event.request.url.includes("admin") ||
    event.request.url.includes("blocklist")
  ) {
    event.respondWith(fetch(event.request, { cache: "no-store" }).catch(() => fetch(event.request)));
    return;
  }

  // Network-first strategy for data freshness
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        return caches.match(event.request);
      })
  );
});

// ==================== NOTIFICATIONS & PUSH ====================

// Receive Push Notification from Web Push Server
self.addEventListener("push", (event) => {
  let data = {
    title: "【NEO FAMILY】新着イベントのお知らせ",
    body: "カレンダーに新しいイベントが追加されました！",
    icon: "images/apple-touch-icon.png",
    badge: "images/icon-192.png",
    url: "./index.html"
  };

  if (event.data) {
    try {
      const payload = event.data.json();
      data = { ...data, ...payload };
    } catch (e) {
      data.body = event.data.text();
    }
  }

  const options = {
    body: data.body,
    icon: data.icon || "images/apple-touch-icon.png",
    badge: data.badge || "images/icon-192.png",
    vibrate: [200, 100, 200],
    data: { url: data.url || "./index.html" },
    tag: "neofamily-event-notice",
    renotify: true
  };

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

// Handle Message from Client Window to trigger Local ServiceWorker Notification
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SHOW_NOTIFICATION") {
    const { title, body, icon, url, eventId } = event.data;
    const options = {
      body: body || "カレンダーに新しいイベントが追加されました！",
      icon: icon || "images/apple-touch-icon.png",
      badge: "images/icon-192.png",
      vibrate: [200, 100, 200],
      data: {
        url: url || "./index.html",
        eventId: eventId || null
      },
      tag: "neofamily-new-event",
      renotify: true
    };
    event.waitUntil(
      self.registration.showNotification(title || "【NEO FAMILY】新着イベント！", options)
    );
  }
});

// Notification Click -> Focus or open window
self.addEventListener("notificationclick", (event) => {
  event.notification.close();

  const targetUrl = (event.notification.data && event.notification.data.url) || "./index.html";
  const eventId = event.notification.data && event.notification.data.eventId;

  event.waitUntil(
    clients.matchAll({ type: "window", includeUncontrolled: true }).then((windowClients) => {
      // If a window is already open, focus it
      for (let client of windowClients) {
        if (client.url.includes("index.html") && "focus" in client) {
          if (eventId && "postMessage" in client) {
            client.postMessage({ type: "OPEN_EVENT_DETAIL", eventId: eventId });
          }
          return client.focus();
        }
      }
      // Otherwise open a new window
      if (clients.openWindow) {
        const fullUrl = eventId ? `${targetUrl}#event-${eventId}` : targetUrl;
        return clients.openWindow(fullUrl);
      }
    })
  );
});

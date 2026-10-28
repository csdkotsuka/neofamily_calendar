/**
 * NEO FAMILY Calendar - Service Worker
 * Handles PWA lifecycle, notifications, and offline caching.
 */

const CACHE_NAME = "neofamily-cache-v20261028_1";
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
  "./favicon.ico",
  "./manifest.json"
];

// Install Event
self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      // Best-effort cache: don't let one 404 abort caching the whole app
      for (const url of ASSETS_TO_CACHE) {
        try {
          await cache.add(url);
        } catch (err) {
          console.warn("[SW] Failed to precache asset:", url, err);
        }
      }
    }).then(() => self.skipWaiting())
  );
});

// Activate Event
self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((k) => {
          if (k !== CACHE_NAME) {
            console.log("[SW] Deleting old cache:", k);
            return caches.delete(k);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event (Stale-while-revalidate for critical files, Network-first for dynamic data)
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);

  // Skip non-GET requests and non-http/https
  if (e.request.method !== "GET" || !url.protocol.startsWith("http")) {
    return;
  }

  // API or external calls: network only
  if (url.pathname.startsWith("/api/") || url.hostname.includes("firestore.googleapis.com") || url.hostname.includes("googleapis.com")) {
    return;
  }

  // Network First with Cache Fallback for dynamic JSON and html
  if (url.pathname.endsWith(".json") || url.pathname.endsWith(".html") || url.pathname === "/" || url.pathname === "/calendar" || url.pathname === "/caravan" || url.pathname === "/portal" || url.pathname === "/flowchart" || url.pathname === "/raytus" || url.pathname === "/iyasaka" || url.pathname === "/archive" || url.pathname === "/sns") {
    e.respondWith(
      fetch(e.request)
        .then((res) => {
          if (res.ok) {
            const clone = res.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(e.request, clone));
          }
          return res;
        })
        .catch(async () => {
          const cached = await caches.match(e.request);
          if (cached) return cached;
          if (e.request.mode === "navigate") {
            return caches.match("./index.html");
          }
        })
    );
    return;
  }

  // Stale-While-Revalidate for JS, CSS, and Images
  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {
      const fetchPromise = fetch(e.request)
        .then((networkResponse) => {
          if (networkResponse.ok) {
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(e.request, networkResponse.clone());
            });
          }
          return networkResponse;
        })
        .catch(() => cachedResponse);

      return cachedResponse || fetchPromise;
    })
  );
});

// Push Notification Event
self.addEventListener("push", (e) => {
  let data = { title: "NEO FAMILY カレンダー", body: "新しいイベント情報があります！", url: "/" };
  
  if (e.data) {
    try {
      data = e.data.json();
    } catch (err) {
      data.body = e.data.text();
    }
  }

  const options = {
    body: data.body,
    icon: "./images/icon-192.png",
    badge: "./images/icon-192.png",
    vibrate: [100, 50, 100],
    data: {
      url: data.url || "/"
    },
    actions: [
      { action: "open", title: "カレンダーを見る" }
    ]
  };

  e.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

// Notification Click Event
self.addEventListener("notificationclick", (e) => {
  e.notification.close();

  const targetUrl = e.notification.data?.url || "/";

  e.waitUntil(
    clients.matchAll({ type: "window", includeUncontrolled: true }).then((clientList) => {
      // Focus if already open
      for (const client of clientList) {
        if (client.url.includes(self.location.origin) && "focus" in client) {
          client.navigate(targetUrl);
          return client.focus();
        }
      }
      // Otherwise open new window
      if (clients.openWindow) {
        return clients.openWindow(targetUrl);
      }
    })
  );
});

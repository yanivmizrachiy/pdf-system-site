const CACHE = "pwa-a4-stable"; // לא לשנות — זה נותן יציבות
const CORE = [
  "/pdf-system-site/",
  "/pdf-system-site/print.css",
  "/pdf-system-site/pages/page-1.html",
  "/pdf-system-site/pages/page-2.html",
  "/pdf-system-site/manifest.webmanifest",
  "/pdf-system-site/icons/icon-192.png",
  "/pdf-system-site/icons/icon-512.png"
];

self.addEventListener("install", (e) => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    await c.addAll(CORE);
    self.skipWaiting();
  })());
});

self.addEventListener("activate", (e) => {
  e.waitUntil((async () => {
    await self.clients.claim();
  })());
});

self.addEventListener("message", (e) => {
  if (e.data === "SKIP_WAITING") self.skipWaiting();
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  const url = new URL(req.url);

  // only our site
  if (!url.pathname.startsWith("/pdf-system-site/")) return;

  const isHTML = req.mode === "navigate" || (req.headers.get("accept") || "").includes("text/html");

  e.respondWith((async () => {
    const cache = await caches.open(CACHE);

    if (isHTML) {
      // network-first for pages so updates show up
      try {
        const fresh = await fetch(req);
        cache.put(req, fresh.clone());
        return fresh;
      } catch {
        const cached = await cache.match(req, { ignoreSearch: true });
        return cached || (await cache.match("/pdf-system-site/pages/page-1.html"));
      }
    }

    // assets: cache-first
    const cached = await cache.match(req, { ignoreSearch: true });
    if (cached) return cached;

    try {
      const fresh = await fetch(req);
      cache.put(req, fresh.clone());
      return fresh;
    } catch {
      return Response.error();
    }
  })());
});

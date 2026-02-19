const CACHE="quad-a4-pwa-v1";
const CORE=[
  "./",
  "./pages/page-1.html",
  "./pages/page-2.html",
  "./style.css",
  "./manifest.webmanifest",
  "./assets/icons/icon-192.png",
  "./assets/icons/icon-512.png"
];
self.addEventListener("install",(e)=>{e.waitUntil((async()=>{const c=await caches.open(CACHE);await c.addAll(CORE);await self.skipWaiting();})());});
self.addEventListener("activate",(e)=>{e.waitUntil((async()=>{const ks=await caches.keys();await Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)));await self.clients.claim();})());});
self.addEventListener("fetch",(e)=>{e.respondWith((async()=>{const cached=await caches.match(e.request,{ignoreSearch:true});if(cached) return cached;try{return await fetch(e.request);}catch{if(e.request.mode==="navigate"){const fb=await caches.match("./pages/page-1.html");if(fb) return fb;}return cached||Response.error();}})());});

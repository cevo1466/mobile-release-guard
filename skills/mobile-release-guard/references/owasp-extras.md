# Ek denetimler (EXT-xx) ve AI / abonelik profili

Standartlar: OWASP MASVS/MASTG/MASWE, API Security Top 10, ASVS (backend), CWE, Apple Platform Security, Android Security Best Practices. Yalnızca koşulu sağlanan EXT kontrolünü çalıştır; yalnızca gerçekten tespit edilen önemli bulguları rapor bölüm G'ye yaz.

| ID | Konu | Koşul | Ara |
|---|---|---|---|
| EXT-01 | SQL/NoSQL injection | SQL/Mongo/Firestore sorgusu kullanıcı girdisiyle kuruluyor | String birleştirme, parametresiz sorgu, `$where` |
| EXT-02 | XSS | WebView/web içerik var | `loadHTMLString`, `evaluateJavascript`, `innerHTML` |
| EXT-03 | CSRF | Çerez tabanlı web oturumu var | CSRF token/SameSite yokluğu |
| EXT-04 | Authorization bypass / broken auth | Yetkili uçlar var | Auth middleware eksik rota, istemci-tarafı rol kontrolü, auth durum tutarsızlığı |
| EXT-05 | Güvensiz deserialization | Backend/istemci nesne deserialize ediyor | `pickle.loads`, `ObjectInputStream`, `NSKeyedUnarchiver` (secure coding yok) |
| EXT-06 | Insecure WebView | WebView var | `javaScriptEnabled` + `addJavascriptInterface`, `allowFileAccess`, URL allowlist yokluğu |
| EXT-07 | TLS doğrulama hataları | (SEC-19 ile birleştir) | Trust-all |
| EXT-08 | Hardcoded credentials | (SEC-14 ile birleştir) | Gömülü kullanıcı/parola |
| EXT-09 | Güvensiz loglama / PII sızıntısı | Log/crash/analytics var | `print`, `Log.d`, `console.log` ile token/e-posta/PII |
| EXT-10 | 3. parti SDK riskleri | Analytics/reklam/crash SDK'ları | Toplanan veri, izin, gizlilik beyanıyla uyum |
| EXT-11 | Veri silme / saklama politikası | Kullanıcı verisi tutuluyor | Silme akışı, saklama süresi |
| EXT-12 | Transaction doğrulama, race, replay | Ödeme/kredi/kota var | Çift harcama, idempotency anahtarı, nonce, tekrar oynatma |
| EXT-13 | Güvensiz dosya yükleme | Yükleme var | Tür/boyut/yol doğrulaması, herkese açık bucket |
| EXT-14 | Abuse prevention | Kayıt/OTP/pahalı uç | Hız sınırı, bot/kötüye kullanım koruması |
| EXT-15 | Production debug özellikleri | Release build | Debug menüsü, test endpoint'i, `DEBUG` bayrakları, `debuggable=true` |
| EXT-16 | Release build konfigürasyon hataları | Release build | Staging URL'si, test anahtarı, açık loglama |

## AI ve abonelikli uygulamalar profili

Yalnızca AI veya ücretli abonelik varsa çalıştır; yoksa tümü NOT_APPLICABLE.

**AI:** LLM API anahtarı istemcide mi (FAIL); istemciden doğrudan AI API çağrısı; token/bütçe sınırı ve kullanıcı bazlı rate limit; prompt injection savunması (SEC-25); tool-calling yetkisi (SEC-26); model çıktısı doğrulama; uygunsuz içerik riski; hassas verinin prompt'a taşınması; AI kesintisinde davranış; maliyet patlaması koruması.

**Abonelik (sunucu tarafı doğrulama esastır):** Plus/Pro yetkisi sunucuda doğrulanıyor mu; iptal/bitişte entitlement güncellemesi; restore purchases; duplicate transaction işleme (idempotency); webhook / server notification imza doğrulaması (App Store Server Notifications, Google RTDN, RevenueCat webhook); ödeme başarısızlığı ve grace period; cihazlar arası durum eşitleme. Sunucu kodu yoksa UNVERIFIED; "istemcide premium bayrağı" tek başına FAIL kanıtı değil, sunucu enforcement'ı doğrulanamayan güven sınırıdır.

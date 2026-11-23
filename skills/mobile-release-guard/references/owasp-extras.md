# Ek denetimler (EXT-01 … EXT-21) ve AI / abonelik profili (AI-01 … AI-19)

Kaynak standartlar: OWASP MASVS/MASTG/MASWE, API Security Top 10, ASVS (backend bölümleri), CWE, Apple Platform Security, Android Security Best Practices. Standart eşleşmeleri resmî sayfalardan canlı doğrulanmadı; rapora yazarken güncel sayfaya bak, doğrulayamazsan "eşleşme doğrulanmadı" de.
Yalnızca **Koşul** sağlanırsa çalıştır; sağlanmıyorsa NOT_APPLICABLE. Rapor bölüm G'ye yalnızca gerçekten tespit edilen önemli bulguları yaz (SEC ile aynı olanı SEC altında birleştir). Secret/PII değerini yazma.

## EXT kontrolleri (spec §10 — 21 madde)

| ID | Konu | Koşul | Ara | FAIL ölçütü |
|---|---|---|---|---|
| EXT-01 | SQL / NoSQL injection | SQL, Mongo, Firestore veya Supabase sorgusu kullanıcı girdisiyle kuruluyor | String birleştirme, şablon literal ile sorgu, `$where`, `raw()`, `execute(f"…")` | Girdi parametresiz/şemasız sorguya giriyor |
| EXT-02 | XSS | WebView veya web içerik var | `loadHTMLString`, `evaluateJavascript`, `innerHTML`, `dangerouslySetInnerHTML` | Doğrulanmamış girdi HTML/JS bağlamına |
| EXT-03 | CSRF | Çerez tabanlı web oturumu/admin paneli | CSRF token, `SameSite`, Origin kontrolü | State değiştiren istek korumasız |
| EXT-04 | Authorization bypass | Yetkili uç/rol var | Auth middleware'siz rota, yalnızca istemcide rol kontrolü, doğrudan nesne erişimi (SEC-01 ile birleştir) | Yetki kontrolü sunucuda yok |
| EXT-05 | Güvensiz deserialization | Nesne/binary veri deserialize ediliyor | `pickle.loads`, `yaml.load`, `ObjectInputStream`, `NSKeyedUnarchiver` (secure coding yok), `unserialize()` | Güvenilmeyen veri deserialize |
| EXT-06 | Insecure WebView | WebView var | `javaScriptEnabled` + `addJavascriptInterface`, `allowFileAccess`, `WKWebView` mesaj köprüsü, URL allowlist yokluğu | Keyfi URL + köprü açık |
| EXT-07 | TLS doğrulama hataları | Ağ iletişimi var | Trust-all `TrustManager`, `URLSessionDelegate` kör kabul, `badCertificateCallback => true`, `NSAllowsArbitraryLoads` (SEC-19 ile birleştir) | Production'da doğrulama kapalı |
| EXT-08 | Hardcoded credentials | Her proje | Gömülü parola/kullanıcı/token/anahtar (SEC-14 ile birleştir) | Gerçek credential kodda (değeri yazma) |
| EXT-09 | Güvensiz loglama | Log/crash/analytics var | `print`, `NSLog`, `Log.d`, `console.log`, Crashlytics custom key ile token/e-posta/PII | Hassas veri log'a gidiyor |
| EXT-10 | PII sızıntıları | Kullanıcı verisi işleniyor | Analytics event parametreleri, URL query'de PII, pano, ekran görüntüsü önizleme, bildirim içeriği | PII gereksiz yere dışarı/loglara |
| EXT-11 | Üçüncü taraf SDK riskleri | Analytics/reklam/crash/social SDK | SDK listesi ↔ toplanan veri ↔ gizlilik beyanı (APP-06, GP-09); bilinen zafiyet, bakımsız SDK | Beyan dışı veri toplama |
| EXT-12 | Eksik veri silme ve saklama politikası | Kullanıcı verisi tutuluyor | Silme akışı (APP-13/GP-10), saklama süresi, yedek/log kopyaları, soft-delete | Silme yok veya yalnızca bayrak |
| EXT-13 | Transaction doğrulama | Ödeme/kredi/kota işlemi | Sunucu tarafı doğrulama, tutar/ürün/kullanıcı eşleşmesi, idempotency | İstemcinin bildirdiği sonuç kabul ediliyor |
| EXT-14 | Race conditions | Bakiye/kredi/kota/stok güncellemesi | Oku-değiştir-yaz, kilit/transaction/atomic işlem yokluğu | Eşzamanlı istekle çift harcama |
| EXT-15 | Replay attacks | İmzalı/tek seferlik istek, receipt, webhook | Nonce, zaman damgası, tek kullanımlık token, webhook imza + olay ID tekrar kontrolü | Aynı istek tekrar işleniyor |
| EXT-16 | Güvensiz dosya yükleme | Dosya yükleme var | Tür/boyut/içerik doğrulaması, dosya adı/yol, herkese açık bucket, imzalı URL ömrü | Doğrulamasız veya herkese açık yazma |
| EXT-17 | Broken authentication | Giriş akışı var | Zayıf parola politikası, kimlik doğrulamasız uç, sabit token, kaba kuvvet koruması yokluğu (SEC-03/04/06 ile birleştir) | Kimlik doğrulaması atlanabiliyor |
| EXT-18 | Authentication state tutarsızlıkları | Oturum durumu istemci + sunucu | Çıkış/silinmiş hesap/iptal edilmiş token sonrası eski durum, UI'nin yerel bayrağa güvenmesi, çoklu cihaz | Sunucu geçersiz, istemci yetkili |
| EXT-19 | Abuse prevention | Kayıt/OTP/pahalı/UGC uç | Hız sınırı, CAPTCHA/App Attest/Play Integrity, hesap başına limit (SEC-06/10 ile birleştir) | Otomasyon sınırsız |
| EXT-20 | Production debug özellikleri | Release build | Debug menüsü, test endpoint'i, `#if DEBUG` dışı bayrak, `debuggable=true`, gizli gesture | Release'te debug yüzeyi açık |
| EXT-21 | Release build konfigürasyon hataları | Release build | Staging/dev URL'si, test anahtarı, açık verbose log, `NSAllowsArbitraryLoads`, `usesCleartextTraffic`, source map/dSYM sızıntısı | Release dev/test ayarıyla çıkıyor |

## AI ve abonelikli uygulamalar profili (spec §12 — 19 madde)

Yalnızca AI veya ücretli abonelik varsa çalıştır; yoksa hepsi NOT_APPLICABLE (gereksiz ödeme kontrolü çalıştırma). Sunucu kodu yoksa sunucu-taraflı maddeler UNVERIFIED; istemcideki premium bayrağı tek başına FAIL kanıtı değildir, sunucu enforcement'ı doğrulanamayan güven sınırıdır.

| ID | Madde | Ara / ölçüt |
|---|---|---|
| AI-01 | LLM API key güvenliği | Anahtar istemcide/pakette → FAIL (SEC-14); yalnızca backend'de → PASS |
| AI-02 | İstemciden doğrudan AI API çağrısı | `api.openai.com`, `api.anthropic.com`, `generativelanguage` çağrısı istemci kodunda → FAIL |
| AI-03 | Token ve kullanım bütçeleri | `max_tokens`, günlük/aylık bütçe, sunucu tarafı kullanım sayacı |
| AI-04 | Kullanıcı bazlı request rate limit | Sunucuda kullanıcı/IP/anahtar başına limit (SEC-10) |
| AI-05 | Prompt injection savunmaları | Kullanıcı/dış içerik ayrımı, sunucu yetkisi (SEC-25); yalnızca prompt cümlesi yetmez |
| AI-06 | Tool-calling yetkilendirmesi | Tool allowlist, işlem bazlı authz, onay (SEC-26) |
| AI-07 | Model çıktı doğrulama | Çıktının kod/komut/SQL/HTML olarak doğrulamadan çalıştırılması → FAIL; şema doğrulama |
| AI-08 | Uygunsuz içerik riskleri | Moderasyon/filtre, yaş derecelendirmesiyle uyum (APP-20), raporlama yolu |
| AI-09 | Hassas verinin prompt'a taşınması | PII/sağlık/finans verisinin gereksiz prompt'a konması, sağlayıcı veri politikası |
| AI-10 | AI servis kesintisinde davranış | Zaman aşımı, hata ekranı, yeniden deneme sınırı, çökme yok |
| AI-11 | Ücretli servislerin kötüye kullanımı | Anonim/ücretsiz kullanıcıya açık pahalı uç, otomasyon |
| AI-12 | Maliyet patlamasına karşı koruma | Bütçe üst sınırı, alarm, eşzamanlılık sınırı, kill-switch |
| AI-13 | Plus/Pro yetkisinin sunucuda doğrulanması | Entitlement sunucuda; yalnızca `UserDefaults`/yerel bayrak → FAIL/UNVERIFIED |
| AI-14 | İptal/bitişte entitlement güncellemesi | Server notification/webhook ile durum güncelleme, süre bitimi kontrolü |
| AI-15 | Restore purchases | `AppStore.sync()`/`restorePurchases`/`queryPurchasesAsync` ve düğme |
| AI-16 | Duplicate transaction işleme | İşlem ID'sine göre idempotency, tekrar teslim edilen transaction |
| AI-17 | Webhook / server notification doğrulaması | İmza/JWS doğrulaması (App Store Server Notifications, Google RTDN/Pub-Sub, RevenueCat webhook auth), olay ID tekrar kontrolü |
| AI-18 | Ödeme başarısızlığı ve grace period | Billing retry/grace/hold durumlarının entitlement'a yansıması |
| AI-19 | Farklı cihazlarda abonelik durumu eşitleme | Hesap bazlı sunucu durumu, yeni cihazda geri yükleme |

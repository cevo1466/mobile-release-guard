# Güvenlik kontrolleri (SEC-01 … SEC-26)

Her kontrol: **Koşul** (ne zaman uygulanır, değilse NOT_APPLICABLE) · **Ara** (grep/okuma ipuçları) · **Ölçüt** (PASS/FAIL) · **Dikkat** (yanlış pozitif) · **Test**.
Sunucu tarafı kanıt (backend kodu, RLS, Security Rules) yoksa istemci bulgusu tek başına PASS vermez → UNVERIFIED veya PARTIAL.
**Düzeltme yönü (`fix`):** Güvenle yapılabilir: yerel depoyu Keychain/Keystore'a taşıma, `allowBackup`/R8/ATS ayarı, boş izin metni, `.gitignore`, kullanılmayan izin kaldırma, sunucu kodunda sahiplik/allowlist ekleme (testle). Açık onay ister: RLS/Security Rules'u production'a uygulama, token ömrü/oturum iptali davranışı, ödeme/entitlement mantığı, secret döndürme, CI/deploy değişikliği, mimari taşıma (örn. AI çağrısını backend'e alma).
Secret değerlerini asla raporlama; yalnızca dosya:satır ve tür.

## SEC-01 — Nesnenin sahibini sor
**Koşul:** Kullanıcıya ait nesne (profil, rezervasyon, ilerleme, dosya, abonelik) sunan backend/DB var.
**Ara:** ID ile okuma/yazma endpoint'leri; Firebase `firestore.rules`/`storage.rules` (`request.auth.uid == resource.data.ownerId`); Supabase `ENABLE ROW LEVEL SECURITY` + policy `auth.uid()`; middleware'de sahiplik kontrolü.
**Ölçüt:** Sahiplik kontrolü sunucu/DB katmanında → PASS. Yalnızca istemcide `userId ==` karşılaştırması veya `allow read: if true` / RLS kapalı → FAIL. Backend yok/erişilemiyor → UNVERIFIED.
**Test:** Kullanıcı A token'ı ile B'nin nesne ID'sine istek → 403/404 beklenir (yalnızca test ortamında, izinle).

## SEC-02 — Fazla alanı kırp
**Koşul:** İstemci JSON/form verisi DB'ye yazılıyor.
**Ara:** `Object.assign(model, req.body)`, `...req.body`, ORM `create(req.body)`, Firestore rules'ta alan kısıtı yokluğu; `role`, `isAdmin`, `credits`, `subscriptionStatus`, `price`, `ownerId` alanları.
**Ölçüt:** Allowlist/DTO/şema doğrulaması ve kritik alanların sunucuda belirlenmesi → PASS; kritik alan istemciden yazılabiliyor → FAIL.
**Test:** İstekte ek `role: "admin"` alanı → yok sayılmalı/reddedilmeli.

## SEC-03 — Token'ın ömrünü kıs
**Koşul:** Access/refresh token veya session kullanılıyor (yönetilen sağlayıcı varsayılanları da değerlendirilir).
**Ara:** JWT `exp`, refresh rotation, revocation, uzun ömürlü statik token.
**Ölçüt:** Risk ve mimariye uygun ömür + yenileme/iptal → PASS; süresiz token veya iptal yok → FAIL. Tek bir süreyi herkese dayatma.
**Test:** Süresi dolmuş/iptal edilmiş token reddedilmeli.

## SEC-04 — Çıkışta oturumu düşür
**Koşul:** Hesap/oturum sistemi var.
**Ara:** Logout fonksiyonu: Keychain/Keystore temizliği, sunucu `signOut`/revoke çağrısı, push token/cihaz kaydı silme, önbelleğe alınmış kullanıcı verisi; cihazlar arası oturum yönetimi (diğer cihazlardaki oturumları listeleme/sonlandırma, parola değişiminde toplu iptal).
**Ölçüt:** Yerel kimlik bilgisi silinir + sunucu tarafı iptal → PASS; yalnızca login ekranına yönlendirme → FAIL/PARTIAL.
**Test:** Logout sonrası eski refresh token ile yenileme başarısız olmalı.

## SEC-05 — Kendine 2FA aç
**Koşul:** Geliştirici/yönetici/bulut/yayın/CI hesapları (kod dışı).
**Ara:** Kodda doğrulanamaz; CI/CD ve admin akışlarında MFA zorunluluğu belgeleri, admin panel girişi.
**Ölçüt:** Harici hesap ayarları kodla doğrulanamaz → UNVERIFIED + kullanıcıya manuel kontrol listesi (Apple, Google Play, Firebase/Supabase, GitHub, bulut). Son kullanıcı MFA'sını her uygulamaya dayatma.

## SEC-06 — OTP'yi sınırla
**Koşul:** OTP/SMS/e-posta kodu veya şifre sıfırlama kodu var.
**Ara:** Deneme sayacı, rate limit, TTL, tek kullanımlık, yeniden gönderim bekleme süresi, sunucu tarafı uygulama.
**Ölçüt:** Sunucuda sınırlar var → PASS; yalnızca istemcide sayaç veya sınırsız deneme → FAIL.
**Test:** Canlı serviste brute-force yapma; yalnızca kod/konfig analizi veya izinli test ortamı.

## SEC-07 — Ülke filtresi koy
**Koşul:** Yalnızca yasal/ödeme/veri yerleşimi/kötüye kullanım gerekçesi varsa.
**Ara:** Geo/IP kısıtı, bölge bazlı ürün erişimi.
**Ölçüt:** Gereklilik yoksa NOT_APPLICABLE. Varsa uygulanıp VPN/dolaşım yanlış pozitifleri değerlendirilmiş olmalı. Otomatik IP engeli önerme.

## SEC-08 — E-posta ifşasını kes
**Koşul:** Login/kayıt/şifre sıfırlama var.
**Ara:** "Bu e-posta kayıtlı değil" gibi ayrık hata mesajları, ayrık HTTP kodları, zamanlama farkı.
**Ölçüt:** Genel yanıt → PASS; hesap varlığı ifşa → FAIL (iş gereksinimi kayıt sırasında bunu zorunlu kılıyorsa PARTIAL + not).

## SEC-09 — Sıfırlama linkini yak
**Koşul:** Password reset / magic link var (yönetilen sağlayıcı kullanıyorsa onun ayarları UNVERIFIED olabilir).
**Ara:** Token süresi, tek kullanımlık, kullanım sonrası geçersizlik, redirect allowlist, token'ın log/analytics/Referer'a sızması, sıfırlama sonrası oturum iptali.
**Ölçüt:** Hepsi sağlanıyor → PASS; yeniden kullanılabilir veya süresiz → FAIL.

## SEC-10 — Pahalı uca kota
**Koşul:** AI inference, TTS/STT, SMS, e-posta, dosya/görsel işleme gibi maliyetli endpoint var.
**Ara:** Kullanıcı bazlı kota, rate limit, eşzamanlılık sınırı, bütçe üst sınırı, sunucuda kullanım sayacı; istemciden doğrudan üçüncü taraf API çağrısı.
**Ölçüt:** Sunucu tarafı kota → PASS; kota yalnızca istemcide veya yok → FAIL.

## SEC-11 — SSRF'i kapat
**Koşul:** Backend kullanıcı kontrollü URL'den içerik çekiyor (webhook, link önizleme, görsel indirme, import).
**Ara:** `fetch(req.body.url)`, `requests.get(user_url)`; allowlist, iç IP/metadata (169.254.169.254) engeli, redirect takibi, DNS rebinding.
**Ölçüt:** Yüzey yoksa NOT_APPLICABLE; yüzey var ve doğrulama yok → FAIL.

## SEC-12 — Depolamayı kapat
**Koşul:** Yerel veri saklama var. Amaç tüm depolamayı kapatmak değil, hassas veriyi güvensiz yerde tutmamak.
**Ara:** UserDefaults/SharedPreferences/AsyncStorage/SQLite/dosya/cache/log içinde token, parola, PII, sağlık/finans verisi.
**Ölçüt:** Hassas veri Keychain/Keystore veya şifreli depoda → PASS; düz metin → FAIL.

## SEC-13 — App Check zorunlu
**Koşul:** Yalnızca Firebase (veya eşdeğer) kullanılıyorsa.
**Ara:** `FirebaseAppCheck`, App Attest/DeviceCheck, Play Integrity sağlayıcısı, backend'de enforcement (konsol ayarı kodda görünmez).
**Ölçüt:** Firebase yoksa NOT_APPLICABLE. İstemcide etkin ama enforcement doğrulanamıyorsa PARTIAL/UNVERIFIED. App Check authN/authZ yerine geçmez.

## SEC-14 — APK'daki anahtar
**Koşul:** Her mobil proje.
**Ara:** Kaynak, build config, `strings.xml`, plist, manifest, `.env` içinde gerçek secret (özel API anahtarı, service account, `sk-…`, JWT secret). Firebase `apiKey`, Google Maps istemci anahtarı, Supabase `anon` anahtarı gibi kamuya açık istemci tanımlayıcılar secret değildir (kısıtlama/RLS ile birlikte değerlendir).
**Ölçüt:** Gerçek secret pakete gömülü → FAIL (değeri yazma; backend'e taşı, döndür).

## SEC-15 — Kodu karart
**Koşul:** Android release build (iOS'a aynı yöntem dayatılmaz).
**Ara:** `minifyEnabled`/`isMinifyEnabled`, `shrinkResources`, R8 kuralları, ProGuard dosyası.
**Ölçüt:** Release'de R8 açık → PASS; kapalı → FAIL/PARTIAL. Obfuscation secret koruması veya authorization yerine geçmez.

## SEC-16 — Token'ı kasaya koy
**Koşul:** Token/session secret saklanıyor.
**Ara:** Keychain (`kSecAttrAccessible…`), Android Keystore/EncryptedSharedPreferences, `flutter_secure_storage`, `expo-secure-store`; log, crash raporu, analytics, debug çıktısı ve yedekte (SEC-17) token ifşası.
**Ölçüt:** Güvenli depo → PASS; düz depo veya log'a yazım → FAIL.

## SEC-17 — Yedeklemeyi kapat
**Koşul:** Hassas yerel veri var. Tüm yedeklemeyi kapatma amaçlanmaz.
**Ara:** Android `allowBackup`, `dataExtractionRules`/`fullBackupContent`; iOS `isExcludedFromBackup`, Data Protection sınıfı.
**Ölçüt:** Hassas dosyalar yedekten hariç/korumalı → PASS; hassas veri yedeğe dahil → FAIL/PARTIAL.

## SEC-18 — Deep Link'i doğrula
**Koşul:** Universal Links, App Links veya custom scheme var.
**Ara:** `application(_:open:)`, `onOpenURL`, intent-filter, `assetlinks.json`/`apple-app-site-association`, parametre doğrulama, open redirect, OAuth callback state/PKCE, link ile yetkisiz ekran/işlem.
**Ölçüt:** Parametreler doğrulanıyor, auth gerektiren ekranlar korunuyor → PASS; aksi FAIL.

## SEC-19 — Sertifikayı sabitle
**Koşul:** Ağ iletişimi var. Pinning yalnızca tehdit modeli gerektiriyorsa önerilir.
**Ara:** ATS istisnaları (`NSAllowsArbitraryLoads`), `usesCleartextTraffic`, network-security-config, trust-all `TrustManager`/`URLSessionDelegate`, `badCertificateCallback => true`.
**Ölçüt:** Production'da HTTPS + doğru TLS doğrulaması → PASS; trust-all/cleartext → FAIL. Pinning yoksa tek başına FAIL değil; rotasyon/operasyon riskini not et.

## SEC-20 — İzinleri azalt
**Koşul:** Her mobil proje.
**Ara:** Info.plist `NS*UsageDescription`, AndroidManifest `uses-permission`, runtime izin istekleri, gerçek kullanımla eşleşme.
**Ölçüt:** Kullanılmayan izin → FAIL/PARTIAL; açıklama gerçek davranışla uyuşmuyorsa PARTIAL.

## SEC-21 — .env'i kapat
**Koşul:** Env/secret dosyaları veya CI secret'ları var.
**Ara:** `.gitignore` kapsamı, repoya eklenmiş `.env*`, `git ls-files | grep -i env`, istemci paketine giren env değişkenleri (`EXPO_PUBLIC_*`, `--dart-define` değerleri), CI secret ayrımı, dev/staging/production ortam ayrımı (aynı anahtar her ortamda mı), secret rotation planı/izi. `scripts/scan_secrets.sh <dizin>` yalnızca dosya:satır ve tür verir.
**Ölçüt:** Her `.env` değeri secret değildir; gerçek secret repoda/pakette → FAIL. Production secret'ını rapora yazma.

## SEC-22 — Paketleri dondur
**Koşul:** Bağımlılık yöneticisi var.
**Ara:** Lockfile varlığı/commit'i (`Package.resolved`, `Podfile.lock`, `package-lock.json`/`pnpm-lock.yaml`/`yarn.lock`, `pubspec.lock`, Gradle lock/version catalog), `^`/`latest`/`*` aralıkları, git/URL bağımlılıkları, dependency confusion (özel paket adının genel kayıt defterinde de bulunması, scope'suz iç paketler), typosquatting, bilinen CVE (araç varsa `npm audit` vb.; kurma).
**Ölçüt:** Lockfile + sabit sürüm → PASS. Toplu sürüm yükseltmesi yapma.

## SEC-23 — Kurulum script'ini kes
**Koşul:** Build/install/CI lifecycle script'leri var.
**Ara:** npm `preinstall/postinstall`, Gradle plugin'leri, Xcode Run Script, Podfile `post_install`, `curl | sh`, CI adımları.
**Ölçüt:** Güvenilmeyen kaynaktan script → FAIL; kaynak ve gerekçe belli → PASS. Tüm script'leri kapatmayı önerme.

## SEC-24 — Fork'a secret verme
**Koşul:** GitHub Actions veya benzeri CI var.
**Ara:** `pull_request_target`, `${{ github.event.* }}` enjeksiyonu, fork PR'a `secrets.*`, geniş `permissions`, SHA'siz üçüncü taraf action, artifact/deploy yetkisi.
**Ölçüt:** Untrusted PR koduna secret/yayın yetkisi → FAIL. CI yoksa NOT_APPLICABLE.

## SEC-25 — Prompt enjeksiyonu
**Koşul:** Uygulama/backend LLM veya agent kullanıyor; yoksa NOT_APPLICABLE.
**Ara:** Kullanıcı/dış doküman/web/tool çıktısının prompt'a karışması, system prompt sızıntısı, model çıktısının doğrulanmadan işlenmesi, tool çağrısı yetki kontrolü, hassas verinin prompt'a konması.
**Ölçüt:** Kontroller prompt metnine değil sunucu tarafı authorization, tool allowlist ve veri sınırlarına dayanıyor → PASS; yalnızca "talimatlara uyma" cümlesi → FAIL/PARTIAL.

## SEC-26 — Ajana yetki verme
**Koşul:** AI agent / tool-calling var; normal uygulama mantığını agent sayma.
**Ara:** Agent'ın DB/dosya/API/ödeme/e-posta/admin erişimi, işlem bazlı yetki, insan onayı, audit log, en az yetki.
**Ölçüt:** Geniş yetki ve onaysız yıkıcı işlem → FAIL; en az yetki + onay + log → PASS.

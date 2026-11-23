# Google Play kontrolleri (GP-01 … GP-25)

Yalnızca Android hedefleniyorsa. Apple kontrollerini kopyalama. API seviyesi ve Billing sürümü gibi zamanla değişen gereksinimleri bu dosyaya gömme: güncel zorunluluğu Play Console Help / Policy Center'dan doğrula; erişim yoksa "güncel politika doğrulanamadı" yaz ve sayı uydurma. Play Console erişimi yoksa konsol beyanları UNVERIFIED.

## GP-01 — Target API ve minimum SDK
`targetSdk`/`minSdk`/`compileSdk` değerlerini `build.gradle(.kts)`'ten oku; güncel Play hedef gereksinimiyle karşılaştır (doğrulanamazsa UNVERIFIED, değeri raporla).
## GP-02 — App Bundle ve release artifact
Release çıktısı AAB mi (`bundleRelease`), CI'da üretiliyor mu.
## GP-03 — Release signing ve anahtar güvenliği
`signingConfigs`: keystore/parola repoda düz metin mi (FAIL, değeri yazma), env/CI secret mi; Play App Signing kullanımı (konsol → UNVERIFIED).
## GP-04 — Google Play Billing uygunluğu
Dijital ürün/abonelik için Play Billing kullanımı; harici ödeme yönlendirmesi güncel politikaya göre değerlendirilir.
## GP-05 — Billing Library sürümü
Gradle'daki `billing`/`billing-ktx` sürümünü güncel Play gereksinimiyle karşılaştır (sürüm numarası gömme).
## GP-06 — Abonelik ürün / base plan / offer yapılandırması
`ProductDetails` → `subscriptionOfferDetails`, base plan ve offer seçimi, ürün ID eşleşmesi; konsol tanımları UNVERIFIED.
## GP-07 — Satın alma doğrulama ve acknowledgment
Sunucuda `purchaseToken` doğrulaması (Play Developer API), `acknowledgePurchase`/`consumeAsync` 3 gün içinde yapılıyor mu; yalnızca istemci doğrulaması → FAIL/PARTIAL.
## GP-08 — Abonelik yaşam döngüsü ve entitlement
RTDN (Real-time developer notifications), iptal/askıya alma/grace period/hesap tutma, yenileme, entitlement'ın sunucuda tutulması.
## GP-09 — Data Safety beyanı
SDK/analytics/auth/reklam ve toplanan veri ↔ konsol beyanı; konsol erişimi yoksa UNVERIFIED + manuel liste.
## GP-10 — Hesap silme gereksinimi
Hesap oluşturma varsa uygulama içi silme yolu ve sunucu tarafı veri silme.
## GP-11 — Hesap silme için web bağlantısı
Play Console'da hesap/veri silme web URL'si gerekliliği (konsol → UNVERIFIED), sayfanın var olması.
## GP-12 — Privacy Policy
Uygulama içi bağlantı ve konsol URL'si; içerik gerçek veri işleme ile uyumlu mu.
## GP-13 — Android runtime izinleri
Manifest `uses-permission` ↔ gerçek kullanım; runtime isteme akışı ve gerekçe ekranı (SEC-20 ile birleştir).
## GP-14 — Hassas izinler
SMS, Call Log, Tüm dosya erişimi (`MANAGE_EXTERNAL_STORAGE`), `QUERY_ALL_PACKAGES`, erişilebilirlik API'si gibi kısıtlı izinler için bildirim formu gerekliliği.
## GP-15 — Arka plan konumu
`ACCESS_BACKGROUND_LOCATION` kullanımı ve gerekçesi; yoksa NOT_APPLICABLE.
## GP-16 — Foreground service
`foregroundServiceType` bildirimi ve izin; amaç beyanı; yoksa NOT_APPLICABLE.
## GP-17 — Bildirim izinleri
Güncel Android sürümlerinde runtime bildirim izni isteme akışı.
## GP-18 — Android backup güvenliği
`allowBackup`, `dataExtractionRules`, `fullBackupContent`; hassas veri yedeğe giriyor mu (SEC-17).
## GP-19 — Deep Link / App Links güvenliği
`autoVerify`, `assetlinks.json`, intent-filter `exported`, parametre doğrulama (SEC-18).
## GP-20 — Play Integrity gereken senaryolar
Ücretli/ kötüye kullanıma açık uçlarda Play Integrity doğrulamasının sunucuda yapılması; gerekmiyorsa NOT_APPLICABLE. Tek başına authN/authZ değildir.
## GP-21 — Açıklama ve özellik uyumu
Store listing vaatleri ↔ gerçek işlev (APP-04/22 karşılığı); listing erişimi yoksa UNVERIFIED.
## GP-22 — Çocuklara yönelik içerik / Families
Hedef kitle çocuk içeriyorsa Families politikası, reklam SDK'ları ve veri toplama; değilse NOT_APPLICABLE.
## GP-23 — SDK ve üçüncü taraf veri işleme
Bağımlılıkların toplayıp ilettiği veri, politika uyumu ve Data Safety ile eşleşme.
## GP-24 — Crash / ANR
Ana thread'de ağ/disk, `StrictMode`, bilinen çökme kalıpları; gerçek Android Vitals verisi yoksa UNVERIFIED.
## GP-25 — Release build güvenlik ayarları ve cihaz/mimari uyumu
`debuggable=false`, R8 (SEC-15), `usesCleartextTraffic`, ABI/`abiFilters` ve 64-bit gereksinimi, manifest `exported` bileşenleri.

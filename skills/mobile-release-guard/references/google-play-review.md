# Google Play kontrolleri (GP-01 … GP-25)

Yalnızca Android hedefleniyorsa. Apple kontrollerini kopyalama. API seviyesi ve Billing sürümü gibi zamanla değişen gereksinimleri bu dosyaya gömme: güncel zorunluluğu Play Console Help / Policy Center'dan doğrula; erişim yoksa "güncel politika doğrulanamadı" yaz ve sayı uydurma. Play Console erişimi yoksa konsol beyanları UNVERIFIED.

## GP-01 — Target API ve minimum SDK
`targetSdk`/`minSdk`/`compileSdk` değerlerini `build.gradle(.kts)`'ten oku; güncel Play hedef gereksinimiyle karşılaştır (doğrulanamazsa UNVERIFIED, değeri raporla).
**Son doğrulama 2026-11-23:** Hedef API gereksinimi form faktörüne ve tarihe göre değişen, düzenli yükselen bir tablodur; sayı bilerek yazılmadı. https://support.google.com/googleplay/android-developer/answer/11926878 · https://developer.android.com/google/play/requirements/target-sdk
## GP-02 — App Bundle ve release artifact
Release çıktısı AAB mi (`bundleRelease`), CI'da üretiliyor mu.
## GP-03 — Release signing ve anahtar güvenliği
`signingConfigs`: keystore/parola repoda düz metin mi (FAIL, değeri yazma), env/CI secret mi; Play App Signing kullanımı (konsol → UNVERIFIED).
## GP-04 — Google Play Billing uygunluğu
Dijital ürün/abonelik için Play Billing kullanımı; harici ödeme yönlendirmesi güncel politikaya göre değerlendirilir.
**Son doğrulama 2026-11-23 (arama özeti):** Play Billing birçok pazarda tek seçenek değil: alternatif faturalama / faturalama seçimi programları bölgeye göre değişiyor, katılım isteğe bağlı; kullanıcı seçimi, müşteri desteği ve ücret yükümlülükleri var. Oran ve tarihler yazılmadı; güncel sayfaya bak. https://support.google.com/googleplay/android-developer/answer/17161464
## GP-05 — Billing Library sürümü
Gradle'daki `billing`/`billing-ktx` sürümünü güncel Play gereksinimiyle karşılaştır (sürüm numarası gömme).
**Son doğrulama 2026-11-23:** Her Billing Library sürümünün bir deprecation döngüsü ve yeni uygulama/güncelleme için son tarihi var; geçerli sürüm bu dosyada tutulmaz. https://developer.android.com/google/play/billing/deprecation-faq
## GP-06 — Abonelik ürün / base plan / offer yapılandırması
`ProductDetails` → `subscriptionOfferDetails`, base plan ve offer seçimi, ürün ID eşleşmesi; konsol tanımları UNVERIFIED.
## GP-07 — Satın alma doğrulama ve acknowledgment
Sunucuda `purchaseToken` doğrulaması (Play Developer API), `acknowledgePurchase`/`consumeAsync` 3 gün içinde yapılıyor mu; yalnızca istemci doğrulaması → FAIL/PARTIAL.
**Son doğrulama 2026-11-23:** Satın alma 3 gün içinde acknowledge edilmezse otomatik iade edilir ve yetki kalkar (PENDING durumunda süre başlamaz); acknowledge'ın backend'den yapılması önerilir; doğrulamadan geçemeyen satın almada yetki verme, acknowledge/consume etme, API ile iade et/iptal et. https://developer.android.com/google/play/billing/integrate
## GP-08 — Abonelik yaşam döngüsü ve entitlement
RTDN (Real-time developer notifications), iptal/askıya alma/grace period/hesap tutma, yenileme, entitlement'ın sunucuda tutulması.
## GP-09 — Data Safety beyanı
SDK/analytics/auth/reklam ve toplanan veri ↔ konsol beyanı; konsol erişimi yoksa UNVERIFIED + manuel liste.
## GP-10 — Hesap silme gereksinimi
Hesap oluşturma varsa uygulama içi silme yolu ve sunucu tarafı veri silme.
**Son doğrulama 2026-11-23:** Hesap oluşturmaya izin veren uygulama hem uygulama içinden hem web bağlantısıyla silme sunmalı; bağlantı Data safety formunda verilir; dondurma/devre dışı bırakma silme sayılmaz; güvenlik, dolandırıcılık veya yasal nedenle tutulan veri açıkça belirtilmeli; kalıcı özel ve kurumsal cihaz yönetimi uygulamaları muaf. https://support.google.com/googleplay/android-developer/answer/13327111
## GP-11 — Hesap silme için web bağlantısı
Play Console'da hesap/veri silme web URL'si gerekliliği (konsol → UNVERIFIED), sayfanın var olması.
Kaynak ve kural: GP-10 notuna bak (web bağlantısı Data safety formunda verilir).
## GP-12 — Privacy Policy
Uygulama içi bağlantı ve konsol URL'si; içerik gerçek veri işleme ile uyumlu mu.
## GP-13 — Android runtime izinleri
Manifest `uses-permission` ↔ gerçek kullanım; runtime isteme akışı ve gerekçe ekranı (SEC-20 ile birleştir).
## GP-14 — Hassas izinler
SMS, Call Log, Tüm dosya erişimi (`MANAGE_EXTERNAL_STORAGE`), `QUERY_ALL_PACKAGES`, erişilebilirlik API'si gibi kısıtlı izinler için bildirim formu gerekliliği.
## GP-15 — Arka plan konumu (Background location)
`ACCESS_BACKGROUND_LOCATION` kullanımı ve gerekçesi; yoksa NOT_APPLICABLE.
**Son doğrulama 2026-11-23:** Arka plan ve ön plan konumu Play Console bildirimi gerektirir; ayrıntı ve önizleme (henüz yürürlükte olmayan) değişiklikler için GP-16 kaynaklarına bak.
## GP-16 — Foreground service
`foregroundServiceType` bildirimi ve izin; amaç beyanı; yoksa NOT_APPLICABLE.
**Son doğrulama 2026-11-23:** Android 14+ hedefleyen uygulamalar her foreground service türünü Console'da bildirir (açıklama, kullanıcı etkisi, demo video, kullanım senaryosu). https://support.google.com/googleplay/android-developer/answer/13392821 · https://support.google.com/googleplay/android-developer/answer/16558241
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
**Son doğrulama 2026-11-23:** Hedef kitle çocuksa reklamlar yalnızca Families self-certified reklam SDK'larından gelmeli (program yeni başvuru almıyor olabilir); ilgi alanına dayalı reklam/remarketing yok; çocuk odaklı uygulama reklam kimliği/IMEI/MAC iletmemeli; karma kitlede nötr yaş ekranı. https://support.google.com/googleplay/android-developer/answer/9893335 · https://support.google.com/googleplay/android-developer/answer/11043825
## GP-23 — SDK ve üçüncü taraf veri işleme
Bağımlılıkların toplayıp ilettiği veri, politika uyumu ve Data Safety ile eşleşme.
## GP-24 — Crash / ANR
Ana thread'de ağ/disk, `StrictMode`, bilinen çökme kalıpları; gerçek Android Vitals verisi yoksa UNVERIFIED.
## GP-25 — Release build güvenlik ayarları ve cihaz/mimari uyumu
`debuggable=false`, R8 (SEC-15), `usesCleartextTraffic`, ABI/`abiFilters` ve 64-bit gereksinimi, manifest `exported` bileşenleri.

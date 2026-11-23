# App Store inceleme kontrolleri (APP-01 … APP-24)

Yalnızca iOS/iPadOS hedefleniyorsa. Her maddede kural sınıfı: **K**=kesin kural, **C**=koşullu kural, **Q**=kalite önerisi. Guideline numaralarını bu dosyaya gömme; güncel metni `official-sources.md` bağlantılarından doğrula. App Store Connect, ekran görüntüsü, gerçek cihaz ve canlı URL erişimi yoksa ilgili kısım UNVERIFIED; manuel adımları rapora yaz.
Demo hesap bilgilerini veya secret'ları repoya/rapora yazma.

## APP-01 — Açılışta çöküyor
**Sınıf:** K · **Ara:** Cold/warm start akışı, `AppDelegate`/`@main`, force unwrap (`!`, `try!`), eksik internet, backend hatası, geçersiz session. **Not:** Cihaz/simülatör testi yapılmadıysa PASS verme (statik inceleme → PARTIAL/UNVERIFIED).

## APP-02 — Demo hesap vermedin
**Sınıf:** K (hesap gerektiriyorsa) · **Ara:** Login zorunluluğu. **Manuel:** App Store Connect "App Review Information" alanında demo hesap veya inceleme erişimi. Hesap gerektirmiyorsa NOT_APPLICABLE.

## APP-03 — Demo hesap geçersiz
**Sınıf:** K · **Not:** Hesabı kodla doğrulama; izinsiz harici hesapta test yapma. Süre/yetki (abonelik, 2FA) inceleme sırasında erişilebilir olmalı → UNVERIFIED + manuel kontrol.

## APP-04 — Özellik bulunamıyor
**Sınıf:** K · **Ara:** Mağaza açıklamasındaki özellikler ↔ kodda erişilebilir ekranlar; erişim adımları açık mı. Açıklamaya erişim yoksa UNVERIFIED.

## APP-05 — Gizlilik linki yok
**Sınıf:** K · **Ara:** Uygulama içi gizlilik politikası bağlantısı; URL'nin çalıştığını yalnızca doğrulayabiliyorsan belirt. **Manuel:** App Store Connect Privacy Policy URL.

## APP-06 — Etiket uyuşmuyor
**Sınıf:** K · **Ara:** SDK/analytics/auth/reklam/veri toplama ↔ App Privacy beyanı; `PrivacyInfo.xcprivacy`. Connect erişimi yoksa nihai eşleşme UNVERIFIED.
**Son doğrulama 2026-11-23:** Gönderimde her required-reason API kullanımı için onaylı neden (privacy manifest) gerekir; üçüncü taraf SDK manifest ve imzaları da denetlenir; güncel API/neden listesi değişebilir (arama özeti). https://developer.apple.com/news/?id=z6fu1dcu

## APP-07 — Destek linki ölü
**Sınıf:** K · **Ara:** Support URL ve uygulama içi destek erişimi; canlı doğrulama yapılamadıysa UNVERIFIED.

## APP-08 — Abonelik bilgisi yok
**Sınıf:** C (otomatik yenilenen abonelik) · **Ara:** Paywall'da fiyat, dönem, yenileme ve iptal bilgisi. Abonelik yoksa NOT_APPLICABLE.
**Son doğrulama 2026-11-23 (arama özeti; tam metni sayfadan oku):** 3.1.2(a) abonelik sürekli değer sunmalı, en az 7 gün sürmeli, kullanıcının tüm cihazlarında erişilebilir olmalı; 3.1.2(c) abone olmadan önce fiyat karşılığı ne alınacağı açık anlatılmalı. https://developer.apple.com/app-store/review/guidelines/

## APP-09 — Paywall'da EULA yok
**Sınıf:** C (abonelik paywall'u varsa; yoksa NOT_APPLICABLE) · **Ara:** Terms of Use/EULA ve Privacy bağlantıları; Apple standart EULA ile özel EULA'yı ayır.

## APP-10 — Fiyat görünmüyor
**Sınıf:** C (IAP/abonelik yoksa NOT_APPLICABLE) · **Ara:** StoreKit `Product.products(for:)`/`SKProductsRequest`, ürün ID eşleşmesi, yükleme hatası ve boş durum, fiyatın `displayPrice`/`localizedPrice` ile gösterilmesi (hardcoded fiyat yetmez). Gerçek ürün kullanılabilirliği Connect/StoreKit test olmadan UNVERIFIED.

## APP-11 — Geri yükleme yok
**Sınıf:** C (tüketilemez IAP/abonelik; yoksa NOT_APPLICABLE) · **Ara:** `AppStore.sync()`/`restoreCompletedTransactions`, `Transaction.currentEntitlements`, hesaplar arası entitlement eşitleme, "Restore Purchases" düğmesi.
**Son doğrulama 2026-11-23:** 3.1.1 restorable IAP için restore mekanizması şart (arama özeti). Tüketilebilir ürünlerin StoreKit ile geri yüklenemediği yalnızca forum bilgisi: **Doğrulanamadı**. https://developer.apple.com/app-store/review/guidelines/

## APP-12 — Dışarı ödeme linki
**Sınıf:** C · **Ara:** Dijital içerik/abonelik için harici ödeme bağlantısı veya yönlendirme. Kural bölgeye ve uygulama türüne göre değişir; güncel kuralı doğrula, tüm harici bağlantıları otomatik yasaklı sayma.
**Son doğrulama 2026-11-23 (arama özeti):** ABD dışı storefront'larda StoreKit External Purchase Link entitlement'ı olmadan IAP dışına yönlendiren düğme/bağlantı/CTA konamaz; ABD storefront'unda bu entitlement gerekmez. AB, Güney Kore, Hollanda (flört uygulamaları) için ayrı şartlar var ve sık değişir: güncel sayfaya bak. https://developer.apple.com/app-store/review/guidelines/ · https://developer.apple.com/support/communication-and-promotion-of-offers-on-the-app-store-in-the-eu/

## APP-13 — Hesap silme yok
**Sınıf:** K (hesap oluşturma varsa; hesap sistemi yoksa NOT_APPLICABLE) · **Ara:** Uygulama içi silme yolu, sunucu tarafı veri silme, abonelik etkisi, yeniden kimlik doğrulama. Logout silme değildir.
**Son doğrulama 2026-11-23:** Hesap oluşturan uygulama hesabı uygulama içinden silmeyi başlatma yolu sunmalı (5.1.1(v)); devre dışı bırakma/dondurma yetmez; kolay bulunmalı; Sign in with Apple kullanılıyorsa silmede Sign in with Apple REST API ile token iptal edilmeli. Uygulama içi web view'in kabulü için resmî açıklama bulunamadı: **Doğrulanamadı**. https://developer.apple.com/news/?id=12m75xbj

## APP-14 — Apple ile giriş yok
**Sınıf:** C (üçüncü taraf/sosyal giriş yoksa NOT_APPLICABLE) · **Ara:** Üçüncü taraf/sosyal giriş (Google, Facebook…) var mı; Sign in with Apple veya güncel kural kapsamındaki eşdeğer seçenek/istisna. Her uygulamada zorunlu varsayma.
**Son doğrulama 2026-11-23:** Resmî guidelines sayfası aramada gelmedi; 4.8 için yalnızca forum alıntıları görüldü (üçüncü taraf/sosyal birincil giriş → Sign in with Apple veya eşdeğer servis; istisna listesi). Eşdeğer servis ölçütleri ve istisnalar: **Doğrulanamadı**, güncel 4.8 metnini sayfadan oku. https://developer.apple.com/app-store/review/guidelines/

## APP-15 — İzin metni boş
**Sınıf:** K · **Ara:** Info.plist `NS…UsageDescription` boş/jenerik mi; kullanılan API ↔ tanımlı anahtar; gerçek kullanım açıklamayla uyumlu mu.

## APP-16 — Takip izni yok
**Sınıf:** C · **Ara:** Takip tanımına giren kullanım (kullanıcıyı uygulamalar/siteler arası izleme, IDFA, veri aracıları) varsa ATT (`ATTrackingManager`) ve `NSUserTrackingUsageDescription`. Her analytics SDK'sını tracking sayma.
**Son doğrulama 2026-11-23:** Takip = uygulamada toplanan kullanıcı/cihaz verisini başka şirketlerin uygulama/site/offline verileriyle hedefli reklam veya reklam ölçümü için ilişkilendirmek ya da veri komisyoncularıyla paylaşmak; izin ATT çerçevesiyle alınır, `NSUserTrackingUsageDescription` yoksa istem çökmeye yol açar. https://developer.apple.com/app-store/user-privacy-and-data-use/ · https://developer.apple.com/documentation/bundleresources/information-property-list/nsusertrackingusagedescription

## APP-17 — "Yakında" ekranı
**Sınıf:** K (tamamlanmamış/çalışmayan özellik) · **Ara:** Çalışmayan düğme, boş ekran, vaat edilip yapılmamış özellik. Placeholder metni tek başına red sebebi değildir.

## APP-18 — Görseller uymuyor
**Sınıf:** K/Q · **Ara:** Ekran görüntüleri ve önizleme ↔ gerçek UI, cihaz boyutu gereksinimleri. Görsellere erişim yoksa UNVERIFIED.

## APP-19 — Metinde başka marka
**Sınıf:** K/Q · **Ara:** Eski proje adı, kopyalanmış metadata, placeholder, yanlış marka (`grep` ile). Meşru üçüncü taraf marka kullanımı hata değildir.

## APP-20 — Yaş sınırı yanlış
**Sınıf:** K · **Ara:** Kullanıcı içeriği, sohbet, AI üretimi, sağlık/finans/hassas kategori. Nihai derecelendirmeyi güncel Connect anketiyle karşılaştır → genelde UNVERIFIED.

## APP-21 — Şablon uygulama
**Sınıf:** K (spam/düşük işlev) · **Ara:** Aşırı benzer/işlevsiz yapı. UI kütüphanesi kullanımı tek başına sorun değildir.

## APP-22 — Olmayan özellik vaadi
**Sınıf:** K · **Ara:** Store listing, onboarding, paywall ve uygulama içi vaatler arasındaki tutarsızlık; yanıltıcı açıklama.

## APP-23 — Sadece web sayfası
**Sınıf:** K · **Ara:** Uygulama yalnızca web sitesini sarıyor mu; yeterli yerel işlev/değer var mı. WebView tek başına red sebebi değildir.

## APP-24 — İtiraz etmedin
**Sınıf:** süreç (teknik gereksinim değil) · Reddedilme yoksa NOT_APPLICABLE. Red varsa: Resolution Center yanıtı, düzeltme kanıtı, itiraz seçenekleri için taslak hazırla (kullanıcı gönderir).

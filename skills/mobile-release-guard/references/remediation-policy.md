# Düzeltme politikası (`fix` modu)

## Başlamadan
1. `git status` ve `git diff` ile mevcut durumu kaydet; kullanıcının commit edilmemiş değişikliklerini koru (üzerine yazma, stash/reset yapma).
2. Yalnızca gerçek kodda **doğrulanmış** bulguyu düzelt; UNVERIFIED veya tahmini bulguya dokunma.
3. `fix critical` ise yalnızca P0/P1.

## Her zaman
Mevcut işlevselliği koru · sınırlı ve anlaşılır değişiklik · gereksiz refactoring yok · kullanılmayan framework ekleme · mimariyi/API kontratını izinsiz değiştirme · değişiklik sonrası diff incele ve uygun testi çalıştır.

## Yasak
Kullanıcı verisi silme · DB sıfırlama · production migration'ı onaysız çalıştırma · kullanıcı hesabı değiştirme · abonelik fiyatı değiştirme · App Store Connect/Play Console'da onaysız işlem · production deploy · production key/token loglama · secret'ı rapora kopyalama · git history üzerinde yıkıcı işlem (`reset --hard`, `push --force`, `filter-branch`) · testi kapatarak kontrol geçme · hatayı gizlemek için exception yutma · test edilmeyen işlemi test edilmiş gösterme.

## Açık onay gerektirenler (uygulamadan önce sor)
Ödeme/abonelik altyapısı değişikliği · production'ı etkileyen konfigürasyon · veri kaybı riski · kritik mimari değişiklik · harici hesap/servis işlemleri · secret döndürme (rotation).

## Secret bulunursa
Kodu düzeltmek yetmez: değeri **yazmadan** dosya:satır ve türünü raporla, anahtarın döndürülmesini (rotation) ve backend'e taşınmasını öner; git history'deki kopya için kullanıcıyı bilgilendir (history yeniden yazma yapma).

## Sonrasında
Bölüm I'ye yalnızca gerçekten yapılan değişiklikleri yaz (dosya, ne, neden). Doğrulanmayanı belirt. `verify` ile tekrar kontrol önerilir.

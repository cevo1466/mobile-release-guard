# Test ve doğrulama stratejisi

Önce ortamı kontrol et (`uname`, `command -v xcodebuild swift gradle flutter node`). Araç yoksa kurma; çalıştırılamayan testi "çalıştırılamadı" olarak raporla (bölüm J) ve uygun CI/macOS adımlarını hazırla. Canlı servise saldırı, stres, brute-force veya maliyet doğuran test yapma.

| Teknoloji | Çalıştırılabilir doğrulama |
|---|---|
| Swift/iOS | `xcodebuild build/test` (yalnızca macOS+Xcode); `swift build/test` (SPM paketleri); StoreKit test config incelemesi; Info.plist/entitlements/PrivacyInfo statik inceleme; async/await ve `@MainActor` kullanımı kod incelemesi |
| Kotlin/Android | `./gradlew lint testReleaseUnitTest assembleRelease`; manifest ve release config incelemesi; Billing/auth birim testleri |
| Flutter | `dart analyze`, `flutter test`; `ios/Runner/Info.plist`, `android/app/src/main/AndroidManifest.xml` incelemesi |
| React Native / Expo | `npx tsc --noEmit`, `npx eslint .`, `npx jest`; `app.json`/native config incelemesi |
| Backend | Birim testi, API integration, authorization (A kullanıcısı ↔ B nesnesi) ve şema doğrulama testleri; bağımlılık denetimi (`npm audit` vb., yalnızca kuruluysa) |

## Linux'ta iOS projesi

macOS/Xcode gerektiren her komut: **çalıştırılamadı**. Yerine: statik analiz (plist/entitlements/`.xcprivacy`, kaynak grep), SPM paketi saf Swift ise `swift build` (kuruluysa). Rapora macOS/CI adımını yaz: `xcodebuild -scheme <S> -destination 'platform=iOS Simulator,name=<cihaz>' test`.

## Regresyon

`fix` sonrası: `git diff` incele, ilgili testleri çalıştır, başarısız testi kapatma/silme. Önce-sonra sonucunu karşılaştır. Test yoksa yeni, hedefli test ekle ya da bunun yapılamadığını belirt.

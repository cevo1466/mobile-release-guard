# Teknoloji ve mimari tanıma

Önce `scripts/detect_stack.sh <dizin>` çıktısını al (yalnızca dosya adı/sabit dize eşleşmesi; kod çalıştırmaz). Etiketler kanıt değil ipucudur; ilgili dosyayı okuyarak doğrula. Bilinmeyen teknolojide kod tabanı ve resmî dokümana bak.

## İşaretler

| Teknoloji | İşaret |
|---|---|
| Swift/SwiftUI/UIKit | `*.swift`, `import SwiftUI/UIKit`, `*.xcodeproj/*.xcworkspace`, `Package.swift` |
| Objective-C | `*.m`, `*.h` + Xcode projesi |
| CocoaPods / SPM | `Podfile(.lock)` / `Package.resolved` |
| StoreKit 1/2 | `SKPaymentQueue` / `Product`, `Transaction.updates` |
| Kotlin/Java/Compose | `*.kt`, `*.java`, `androidx.compose`, `AndroidManifest.xml`, `build.gradle(.kts)` |
| Play Billing | `com.android.billingclient` |
| Flutter | `pubspec.yaml`, `lib/main.dart` |
| React Native / Expo | `package.json` içinde `react-native` / `expo`, `app.json`/`app.config.*` |
| Capacitor/Ionic | `capacitor.config.*`, `@capacitor/core`, `@ionic/*` |
| KMP | `kotlin("multiplatform")`, `shared/` modülü |
| Firebase | `GoogleService-Info.plist`, `google-services.json`, `firebase.json`, `firestore.rules` |
| Supabase | `supabase/` dizini, `supabase-js`/`supabase-swift`, `*.sql` içinde RLS |
| Backend | `express`, `@nestjs`, `laravel` (`composer.json`), `fastapi`, `wrangler.toml`, Edge Functions |
| Ödeme | StoreKit, Play Billing, RevenueCat SDK, backend `verifyReceipt`/Server API |
| AI | `openai`, `anthropic`, `generativelanguage`/Gemini, TTS/STT SDK'ları |

## Monorepo ve modül sınıflandırma

Kök dizinden başla; `apps/`, `packages/`, `ios/`, `android/`, `server/`, `functions/`, `admin/` gibi klasörleri ayır. Her modüle rol ver: **mobil istemci** (mağaza kontrolleri uygulanır), **backend** (SEC-01/02/06/10/11 sunucu kanıtı buradadır), **admin paneli** (yetki ve auth odaklı), **paylaşılan** (kütüphane). Backend'i mobil sayma; mağaza kontrollerini backend'e uygulama. React Native/Flutter/Capacitor projelerinde `ios/` ve `android/` alt klasörleri ilgili platform kontrol setini tetikler.

## Tanıma çıktısı (rapor A bölümü)

Proje adı, platformlar, framework, backend, auth, ödeme, AI, denetim kapsamı, erişilemeyen alanlar (backend kodu yok, Connect/Console yok, cihaz testi yok).

# Rapor şablonu (Türkçe)

Kanıt odaklı, tekrarsız yaz. Secret değeri yazma. Garanti verme.

## Kontrol satırı (her kontrol için)

```
<ID> — <ad> | <PASS|FAIL|PARTIAL|NOT_APPLICABLE|UNVERIFIED> | Risk: <P0–P3 veya —>
Uygulanabilirlik: <neden uygulanır / neden değil>
Bulgu: <ne görüldü>
Kanıt: <dosya:satır, fonksiyon, veri akışı>
Etki: <ne olabilir>
Düzeltme: <güvenli çözüm>
Test: <nasıl doğrulanır>
```

PASS/NOT_APPLICABLE satırlarını tek satıra sıkıştır (kanıt veya neden yeterli). Erişilemeyen kanıt → UNVERIFIED + neyin eksik olduğu.

## Bölümler

- **A. Proje profili** — ad, platform, framework, backend, auth, ödeme, AI, denetim kapsamı, incelenemeyen alanlar.
- **B. Genel sonuç** — incelenen / PASS / FAIL / PARTIAL / NOT_APPLICABLE / UNVERIFIED sayıları.
- **C. Kritik güvenlik bulguları** — en önemlileri önce.
- **D. 26 güvenlik kontrolü** — SEC-01…SEC-26 (orijinal ID ve adlarla).
- **E. 24 App Store kontrolü** — APP-01…APP-24; Android-only projede "kapsam dışı".
- **F. Google Play kontrolleri** — GP-01…GP-25; yalnızca Android'de.
- **G. Ek OWASP bulguları** — orijinal listede olmayan, gerçekten tespit edilenler (EXT-xx).
- **H. Düzeltme planı** — P0 Kritik, P1 Yüksek, P2 Orta, P3 Düşük.
- **I. Uygulanan düzeltmeler** — yalnızca `fix` modunda gerçekten yapılanlar.
- **J. Test sonuçları** — geçen / başarısız / çalıştırılamayan (neden: ortam, araç, erişim).
- **K. Yayın hazırlık değerlendirmesi** — BLOCKED | NEEDS_WORK | READY_WITH_CAVEATS | READY_BASED_ON_VERIFIED_SCOPE. Yalnızca doğrulanan kapsama dayan; erişilmeyen metadata/hesap/cihaz sınırlamalarını yaz.
- **L. Sonraki adımlar** — en önemli uygulanabilir aksiyonlar, manuel App Store Connect / Play Console adımları dahil.

Politika doğrulaması yapılamadıysa K'da "güncel politika doğrulanamadı" yaz.

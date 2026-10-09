# seslen-tts

> **English:** An open Turkish text-to-speech model that runs on CPU, without PyTorch and without internet: 6 voices × 9
> emotions, correct Turkish lexical stress and question intonation, automatic emotion per sentence and reading style per
> text. ONNX Runtime only (~330 MB model, downloaded from Hugging Face on first use). Real-time factor ≈ 0.2–0.4 on a
> laptop CPU.

**İşlemcide çalışan, duygulu, vurguyu bilen açık Türkçe ses modeli.** GPU, internet ve PyTorch gerekmez.

```python
from seslen_tts import Seslen, wav_yaz

s = Seslen()                                    # model ilk kullanımda Hugging Face'ten iner (~330 MB)
wav_yaz("merhaba.wav", s.tum("Merhaba! Yarın bize gelecek misiniz? Dikkat edin, yol kaygan.", ses="zeynep"))
```

```
seslen-tts "Bir varmış bir yokmuş, ormanda meraklı bir sincap yaşarmış." -s ayse -o masal.wav
seslen-tts --sesler
```

## Neler yapar

- **6 ses, 9 duygu:** nötr, neşeli, heyecan, uyarı, merak, özür, üzgün, kızgın, fısıltı.
- **Türkçe vurgu doğru okunur:** "ANkara", "geLİyor", "GELmedi". Okunuş [turkce-vurgu](https://github.com/seslen-tr/turkce-vurgu)
  ile çıkarılır; sayılar, tarihler, saatler, para ve kısaltmalar [turkce-normalize](https://github.com/seslen-tr/turkce-normalize)
  ile okunur hâle gelir ("14:30'da" → "on dört otuzda").
- **Soru ezgisi:** evet/hayır sorusunda ezgi soru ekinden önceki sözcüğün vurgulu hecesinde yükselir
  ("yardımcı olaBİLİR misin?").
- **Otomatik duygu:** her cümlenin tonu metinden seçilir: soru merakla, uyarı uyarıyla, sevinç neşeyle okunur.
  [turkce-duygu](https://github.com/seslen-tr/turkce-duygu) gerekir (`pip install "seslen-tts[duygu]"`).
- **Otomatik üslup:** haber tempolu ve düz, masal yavaş ve hareketli, tarif adım adım okunur.
  [turkce-uslup](https://github.com/seslen-tr/turkce-uslup) gerekir (`pip install "seslen-tts[uslup]"`).

## Kurulum

```
pip install seslen-tts               # temel: sesler, vurgu, soru ezgisi
pip install "seslen-tts[hepsi]"      # + otomatik duygu ve üslup
```

Python 3.9+, Windows / Linux / macOS. Model `SESLEN_TTS_MODEL` ortam değişkeniyle yerel bir klasörden de okunur.

## Sesler

| Ses | Kim | Doğallık (UTMOS) |
|---|---|---|
| `ayse` | olgun kadın (~45), orta-kalın, güven veren | 4,04 |
| `zeynep` | genç kız (~17), ince, canlı | 3,95 |
| `koca` | iri kalın dev, gürleyen ama sevimli (çizgi karakter) | 3,90 |
| `fatma` | yaşlı kadın (~70), ince, şefkatli nine | 3,53 |
| `emre` | genç erkek (~18), orta, enerjik | 2,93 |
| `hasan` | yaşlı erkek (~72), kalın, bilge dede | 2,78 |

Örnek sesler: [Hugging Face model sayfası](https://huggingface.co/seslen-tr/seslen-tts/tree/main/ornekler).

## Kullanım

```python
s = Seslen()
for p in s.seslendir(metin, ses="emre", ton="otomatik", uslup="otomatik"):   # cümle cümle, akış hâlinde
    print(p.ton, p.cumle)            # p.ses: 24 kHz float32 dizi; p.sessizlik_ms: sonraki duraklama

s.tum(metin, ses="fatma", ton="uzgun")        # bütün metin tek tonda
s.tum(metin, ses="hasan", hiz=0.9, perde=1.05) # hız ve ses perdesi
s.tum(metin, ses="zeynep", ton="neseli", yogunluk=0.6)   # duygu şiddeti (0-1, 1 = tam ton)
```

Alt düzey: `s.model.konus(cumle, s.model.stil("ayse", "merak"))` tek cümleyi seslendirir.

## Ölçümler

- **Anlaşılırlık** (Whisper medium, 6 ses × 4 yeni cümle): %100. Whisper sayıları rakamla yazdığı için ("onda" →
  "10'da") ham ölçüm %93,2 görünür.
- **Doğallık:** UTMOS 2,8–4,0 (tablo). UTMOS İngilizce dinleyicilerle eğitildi; Türkçe vurguyu yargılayamaz,
  yapaylığı yakalar.
- **Hız** (i7-12700H, 6 iş parçacığı): gerçek zaman oranı ≈ 0,2–0,4. Yani 5 saniyelik cümle 1–2 saniyede üretilir.
  Windows'un arka plan süreçlerine uyguladığı enerji kısıtı paket tarafından kapatılır (yoksa 4–5 kat yavaşlıyordu).

## Nasıl yapıldı

[StyleTTS2](https://github.com/yl4579/StyleTTS2) (iSTFTNet çözücü) öğrenci modeli. Ses ve duygu verisini öğretmen model
[VoxCPM2](https://huggingface.co/openbmb/VoxCPM2) üretti: sesler tariften tasarlandı, gerçek bir kişinin sesi değildir.
Eğitim üç aşamalıdır: temel, difüzyon ve çekişmeli ince ayar, son olarak vurgu işaretli okunuş ile
[Türkçe PL-BERT](https://huggingface.co/seslen-tr/turkce-plbert). Eğitim tek RTX 4090'da yapıldı. Ağlar ONNX'e
aktarıldı; aktarımın sesi değiştirmediği sınandı (log-mel farkı, modelin kendi iki çalıştırması arasındaki farkın altında).

## Sınırlılıklar

- **Ses klonlama yok.** Bu bilerek böyle: açık modelle başkasının sesini taklit etmek mümkün olmasın diye yalnız hazır
  sesler var.
- Yalnız Türkçe. Yabancı sözcükler Türkçe okunuşla okunur.
- Uzun yabancı adlarda, kısaltma yığınlarında ve çok uzun cümlelerde okunuş hataları olabilir.
- Duygular seslere göre farklı belirginliktedir (ölçülenler arasında en belirgin: Ayşe ve Zeynep).

## Lisans ve kullanım koşulları

- **Kod:** MIT ([LICENSE](LICENSE)).
- **Model ağırlıkları ve sesler:** CC BY-SA 4.0. Türkçe PL-BERT Vikipedi metniyle eğitildi; öğretmen VoxCPM2
  Apache-2.0, StyleTTS2 MIT.
- **Kullanım koşulu (öğretmen modelin ve StyleTTS2'nin koşullarından):**
  - Üretilen sesin yapay zekâ sesi olduğu dinleyiciye belirtilmelidir.
  - Gerçek bir kişiyi taklit etmek, dolandırıcılık ve dezenformasyon için kullanmak yasaktır.

Ticari ürün sesleri, özel ses tasarımı, stüdyo arayüzü ve kurum içi kurulum: Seslen ([iletişim](https://github.com/seslen-tr)).

## Kardeş projeler

[turkce-normalize](https://github.com/seslen-tr/turkce-normalize) · [turkce-vurgu](https://github.com/seslen-tr/turkce-vurgu) ·
[turkce-duygu](https://github.com/seslen-tr/turkce-duygu) · [turkce-uslup](https://github.com/seslen-tr/turkce-uslup) ·
[turkce-plbert](https://github.com/seslen-tr/turkce-plbert) · [turkce-tts-sinav](https://github.com/seslen-tr/turkce-tts-sinav)

# Değişiklikler

## 0.3.11 — turkce-duygu tabanı 0.1.3

- `[duygu]` ve `[hepsi]` ekleri turkce-duygu ≥ 0.1.3 ister: "Bırakın beni!" kızgın (önceden neşeli), "Sessiz ol,
  bebek uyuyor." fısıltı (önceden kızgın), "Lütfen gitme." üzgün, "Lütfen kapıyı kapatmayı unutma." nötr (ikisi de
  önceden uyarı), "Yaşasın, kazandık!" neşeli (önceden uyarı), iki noktayla biten liste girişi nötr.

## 0.3.10 — turkce-uslup tabanı 0.1.1

- `[uslup]` ve `[hepsi]` ekleri turkce-uslup ≥ 0.1.1 ister: tekerlemesiz masal ("… yaşarmış. Bir gün … gitmiş")
  masal (önceden talimat), "-ıyoruz"lu tarif talimat (önceden deneme), "Sevgili dinleyiciler" hitabı sohbet, boş
  metin bilgi okunur.

## 0.3.9 — turkce-vurgu tabanı 0.1.6

- turkce-vurgu ≥ 0.1.6 ister; şapkasız yazılan alıntı şapkalı gibi okunur: "hikaye" → "hicaːje" (önceden "hikaje"),
  "dükkan", "rüzgar", "mekan", "imkan", "dahil" → "daːhil"; ek ünlüsü ince alıntıda l incedir: "gol" → "ɡol",
  "petrol", "kalp", "plan".

## 0.3.8 — turkce-normalize tabanı 0.1.9

- turkce-normalize ≥ 0.1.9 ister; döviz okunur: "100 $" → "yüz dolar" (önceden simge okunmuyordu), "$100'den" →
  "yüz dolardan", "25 €" → "yirmi beş avro", "€25'e" → "yirmi beş avroya", "10,5 GBP" → "on sterlin elli peni".

## 0.3.7 — turkce-normalize tabanı 0.1.8

- turkce-normalize ≥ 0.1.8 ister; noktalı kuruş doğru okunur: "2450.75 TL" → "iki bin dört yüz elli lira yetmiş beş
  kuruş" (önceden "iki yüz kırk beş bin yetmiş beş lira"), "1,5 TL" → "bir lira elli kuruş", "0.99 TL" → "doksan
  dokuz kuruş".

## 0.3.6 — turkce-vurgu tabanı 0.1.5

- turkce-vurgu ≥ 0.1.5 ister; `pip install -U seslen-tts` ile şunlar da gelir: kökten sonrası baştan sona ek olmalı
  ("Hatay'da" → "ˈhatajda", önceden "hataːjda"; "kilisede" → "ciˈlisede"), büyük harfli sıradan sözcük özel ad
  vurgusu almaz ("Bugün Pazar" → "paˈzar", başlıktaki "Madde", "Komut"), cümle başındaki yabancı yer adı özel ad
  ("Rusya ile" → "ˈrusja").

## 0.3.5 — boş metin ve hatalı ayar

- Harf ya da rakam içermeyen metin ("...", "😀", "") çökmüyor: `tum` boş dalga döner, `wav_yaz` boş dalgayı yazar
  (önceden "zero-size array" hatası), komut satırı "okunacak metin yok" der ve dosya yazmaz.
- Komut satırında `""` verilince standart girdi beklenmez (önceden takılıyordu); metin yoksa ve standart girdi bir
  uçbirimse açık hata.
- Bilinmeyen üslup, ses, ton ve okunamayan dosya Python izi yerine kısa hata verir; `hiz` / `perde` sıfır ya da eksi
  ise ValueError (önceden `hiz=0` sessizce yok sayılıyordu).

## 0.3.4 — bağımlılık tabanı

- turkce-normalize ≥ 0.1.7, turkce-vurgu ≥ 0.1.3 ister. Önceki taban (0.1.4 / 0.1.2) `pip install -U seslen-tts`
  ile eski metin hazırlamayı bırakıyordu; şimdi yükseltmede şunlar da gelir: bitişik kısaltma ("TBMM'de" →
  "tebememede"), alan adı ("github.com" → "githab nokta kom"), "saat"siz noktalı saat ("06.45'te" → "altı kırk
  beşte"), baştaki sıfır ("TR-042"), "dört" yumuşaması ("4'e" → "dörde"), ekli Roma rakamı ("Bölüm III'te" → "Bölüm
  üçte", "Louis XIV'ün" → "Lui on dördüncünün"), g / mg / ml.
- CITATION.cff sürümü güncellendi (0.2.1'de kalmıştı).

## 0.3.3 — cümle başında "s" → "z"

- Cümle sürtünmeli ötümsüz ünsüzle (s, ş, f, h) başlayınca model baştaki dolguda ve ünsüzün altında ötümlü mırıltı
  (80-500 Hz) üretiyordu: "Su" → "zu", "Sınıf" → "zenef", "Süt" → "züt". Dalganın başından ilk ünlüye dek 1 kHz altı
  süzülür (`model.bas_mirilti`). 6 ses × 24 cümlede (önünde 150 ms sessizlikle) tanıyıcının "z" duyduğu 20 → 3, ilk
  sözcüğü doğru duyduğu 94 → 110 / 144; altı makalede okunuş denetiminde takılan 15 → 9. Dolguyu kısaltmak yetmedi
  (2 birimde 14 "z", 1 birimde sözcük başı kırpılıyor); patlamalılarda (k, t, p) süzgeç kazanç getirmedi.

## 0.3.2 — paragraf ezgisi

- **Paragraf ezgisi:** perde düzeyi paragrafın ilk cümlesinde +1,5 yarım ton başlar, son cümlesinde bugünkü düzeye (0) iner, yeni
  paragrafta yeniden yükselir (iki cümlelik paragrafta yarısı; başlık ve madde gibi tek cümlelik paragrafa
  dokunulmaz). Model her cümleyi aynı düzeyde okuyordu, uzun metin tekdüze geliyordu. Perde hiçbir cümlede
  aşağı inmez: −1'e inen biçimde okunuş denetiminde takılan cümle arttı (iki makalede 4 → 7), bu biçimde artmadı. `seslendir(paragraf_ezgisi=False)`
  ya da `--paragraf-ezgisiz` ile kapanır; `Parca.bilgi["paragraf_perde"]` cümlenin kaymasını verir.
- Harf ya da rakam içermeyen parça okunmaz: '(… misin?").' bölününce kalan "." için model 0,4 sn uydurma ses
  üretiyordu.

## 0.3.1 — duraklamada çift başlangıç

- Cümle içi duraklamanın sessizliği noktalamanın başına (önceki sözcüğün bitişine) eklenir. Noktalamanın içine
  eklenince model sonraki sözcüğe orada hazırlandığı için sözcüğün başı iki kez duyuluyordu ("İkincisi: yetmiş" →
  "yetyetmiş", "rrögar"). 4 ses × 7 cümle × 2 okumada tanıyıcının birebir duyduğu 4/56 → 11/56.

## 0.3.0 — 16 ses, makale okuma

Makale okuma (03.11.2026: gerçek makaleler seslendirildi; Markdown işaretleri okunuyor, duygu cümle cümle sıçrıyor,
hız 4,6–7,3 hece/sn oynuyor, kısaltma ve model adları okunmuyor, tablo modeli çökertiyordu):
- **Belge okuyucu:** Markdown / HTML metin cümle yapısına çevrilir (turkce-normalize 0.1.4 `paragraflar`): yorum, kod,
  etiket satırı atılır; başlık, liste maddesi, tablo satırı kendi cümlesi; numaralı madde "Birincisi: …"; paragraf
  sonunda iki kat duraklama. 220 karakterden uzun cümle bölünür (önceden çöküyordu).
- **Belgede duygu sabit:** haber, bilgi, deneme, talimat üslubunda heyecan / kızgın / üzgün / fısıltı seçilmez,
  belirsiz duygu nötr, kısa cümle (başlık) nötr, ton en çok %60. Otomatik yoğunluk 1'i aşmaz (önceden 1,5'e çıkıp
  tonu abartıyordu).
- **Hız dengesi:** model uzun cümleyi hızlı okuyordu; her cümle sesin doğal hızının (`Seslen.dogal_hiz`) ±%7
  bandına çekilir (`SesModeli.konus(hedef_hece=…)`). Bir makalede 4,6–7,7 → 5,4–6,5 hece/sn.
- **Özdenetim** (`Seslen(denetim=…)`, komut satırında `--denetim`): her cümle Türkçe CTC tanıyıcıyla dinlenir,
  bozuk okunan sözcük onarılır (sözcüğü yavaşlatma, ünlüyü uzatma, vurguyu kaldırma, öncesine duraklama, nötr ton).
  PyTorch gerekmez: tanıyıcı (wav2vec2 XLS-R 300M, Common Voice 8 Türkçe, Apache-2.0) ONNX'e aktarılıp 8 bite
  indirildi (`denetim.onnx`, ~360 MB, isteğe bağlı iner; model klasöründe varsa kendiliğinden açık).
- **Uzun cümle** (12 sözcükten uzun) virgül / noktalı virgül / iki noktadan parçalara bölünüp ayrı okunur: model
  uzun cümlede sesleri kaydırıyordu.
- **Duraklama:** virgülde en az 125 ms, iki noktada 200 ms, cümle sonunda 450 ms (model virgülü bazen geçiyordu).
  Duraklama dalgaya **sessizlik** olarak eklenir; noktalamanın süresi modelde 50 ms'yi aşmaz. Süre uzatılınca model o
  boşluğu sesle dolduruyordu: Whisper'la dinlenen 321 makale cümlesinde "İkincisi:" → "ikincisihe", "örnek;" →
  "örneka", "79 il," → "ile". Bedeli: 40 uzun genel cümlede UTMOS 3,07 → 2,99 (ölçü eklenmiş sessizliği sevmiyor);
  okunuş denetimi aynı.
- **Cümle sonu:** dalga son harften 50 ms sonra kesilip söner (sondaki uydurma ses: "Ne yapıyor?" → "yapıyors").
  Kısa cümlenin taşıyıcısı "Hem bunu…" ile başlar; "Bunu…" ile dudak sesi sızıyordu ("Katkı." → "katkım"; 4 ses ×
  20 kısa cümlede doğru duyulan 49 → 71).
- **Özdenetimde stil sapması:** süre ve vurgu onarımlarının düzeltemediği ünlü kaymasında ("giriş" → "geriş") stile
  küçük, tohumu sabit sapma verilip yeniden okunur (iki deneme).
- **Yerel hız:** cümlenin bir bölümü cümle ortalamasının 1,3 katından hızlıysa yavaşlatılır.
- `-d / --dosya`: Markdown, HTML ya da düz metin dosyası okunur.
- turkce-normalize 0.1.4 ve turkce-vurgu 0.1.2: teknik kısaltma ("LLM" → elelem), "EVREN" sözcük gibi, sözcük içi tire, sürüm, model adı,
  birim, İngilizce teknik terimler.

16 ses:

- Açık model 6 sesten 16 sese çıktı: yeni sesler Nehir, Ege, Serdar, Selin (yetişkin ve genç), Elif, Can, Ece
  (çocuk), Pıtırcık, Fırfır, Kara (çizgi karakter). Ağırlıklar 0.2'dekiyle aynı (Seslen t10); yalnız `stiller.npz`
  ve `sesler.json` büyüdü. Eski paket sürümleri de yeni sesleri kullanabilir.
- Ölçüm (paketin kendi yoluyla, 16 ses × 14 cümle): okunuş denetiminde 224 cümlede 6 sözcük hatası.

## 0.2.1 — kısa cümle

- Tek başına 1-2 sözcüklük cümle ("Evet.", "Eyvah!", "dedi.") arkasına taşıyıcı cümle eklenerek üretilir, ses son
  harfte kesilir: model sona uydurma hece ekliyordu ("evetnı", "dikkatsınız"). 6 ses × 15 kısa cümlede takılan 0.
- Yabancı adlar turkce-normalize 0.1.3 ile Türkçe okunuşla okunur ("Michael Jackson" → Maykıl Ceksın).

## 0.2.0 — yeni model

- Model yenilendi (Seslen t10): sesler yeni öğretmen verisiyle ince ayarlandı; her eğitim kaydı otomatik okunuş
  denetiminden (Türkçe wav2vec2 CTC + sözcük başına GOP) geçti. Ses renkleri değişti. Model dosyalarının adı ve
  biçimi aynı; 0.1.0 paketi de yeni modelle çalışır.
- Kısa ünlem ya da cümle sonrakine virgülle bağlanır (`akici`): tek başına "Dikkat!" ya da "Merhaba!" okunurken
  sona uydurma hece ekleniyordu.
- Noktalı virgülde en az 200 ms duraklama (önceden virgülden ayırt edilmiyordu).

## 0.1.0 — ilk açık sürüm

- 6 ses × 9 duygu, PyTorch'suz (ONNX Runtime) çıkarım, soru ezgisi, otomatik duygu ve üslup (isteğe bağlı).
- `Seslen.seslendir` (cümle cümle akış), `Seslen.tum`, `wav_yaz`; hız, perde ve duygu yoğunluğu ayarı.
- Komut satırı: `seslen-tts` / `python -m seslen_tts` (`--sesler`, `-s`, `-t`, `-u`, `--hiz`, `--perde`, `-o`).
- Model Hugging Face'ten (`seslen-tr/seslen-tts`) ilk kullanımda iner; `SESLEN_TTS_MODEL` ile yerel klasör.
- Windows'ta arka plan enerji kısıtı (EcoQoS) süreç için kapatılır.
- Hugging Face model kartı (`hf/README.md`): 6 sesin dinleme örnekleri.

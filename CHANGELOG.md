# Değişiklikler

## 0.1.0 — ilk açık sürüm

- 6 ses × 9 duygu, PyTorch'suz (ONNX Runtime) çıkarım, soru ezgisi, otomatik duygu ve üslup (isteğe bağlı).
- `Seslen.seslendir` (cümle cümle akış), `Seslen.tum`, `wav_yaz`; hız, perde ve duygu yoğunluğu ayarı.
- Komut satırı: `seslen-tts` / `python -m seslen_tts` (`--sesler`, `-s`, `-t`, `-u`, `--hiz`, `--perde`, `-o`).
- Model Hugging Face'ten (`seslen-tr/seslen-tts`) ilk kullanımda iner; `SESLEN_TTS_MODEL` ile yerel klasör.
- Windows'ta arka plan enerji kısıtı (EcoQoS) süreç için kapatılır.
- Hugging Face model kartı (`hf/README.md`): 6 sesin dinleme örnekleri.

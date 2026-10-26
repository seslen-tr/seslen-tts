# -*- coding: utf-8 -*-
"""
SES MODELİ — Türkçe okunuştan sese, yalnız ONNX Runtime ile (PyTorch gerekmez), işlemcide.

İki ağ (Seslen'in StyleTTS2 öğrencisinden aktarıldı):
  metin.onnx  işaretler + stil → süre kodlayıcı çıkışı (d), metin kodlayıcı çıkışı (t_en), işaret başına süre
  ses.onnx    hizalanmış özellikler + stil + perde/tonlama + soru ezgisi → 24 kHz dalga
Aradaki hizalama (süreleri yuvarlama, çerçevelere yayma) burada numpy ile yapılır.

Model klasörü (öncelik sırasıyla): SesModeli(klasor), SESLEN_TTS_MODEL ortam değişkeni, Hugging Face
(SESLEN_TTS_HF deposu, ilk kullanımda iner ve önbellekte kalır; SESLEN_TTS_INDIRME=0 ile kapalı).
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

import numpy as np

ORAN = 24000
HF_DEPO = os.environ.get("SESLEN_TTS_HF", "seslen-tr/seslen-tts")
DOSYALAR = ["metin.onnx", "ses.onnx", "stiller.npz", "sesler.json", "semboller.json"]
BAS_DOLGU = 4          # baştaki dolgu işaretinin en uzun süresi (25 ms birim); uzarsa model boşluğu sesle dolduruyor
BIRIM_MS = 25          # bir süre birimi = 2 mel çerçevesi = 600 örnek
NOKTALI_MS = 200       # noktalı virgülde en az duraklama (yoksa virgülden ayırt edilmiyor)
# SORU EZGİSİ: evet/hayır sorusunda ezginin tepesi soru ekinden (mı/mi/mu/mü + kişi ekleri) önceki sözcüğün vurgulu
# hecesindedir ("yardımcı olaBİLİR misin?", "ANkara mı?"; Göksel & Kerslake §21.2). Model bunu düz geçtiği için o
# heceye bu kadar yarım ton eklenir (ses.onnx içinde ~175 ms ile yumuşatılır). Soru sözcüklü sorulara dokunmaz.
SORU_TEPE = 6.0
_SORU_EKI = re.compile(
    r"^m[ɯiuy](s[ɯiuy]n([ɯiuy]z)?|j[ɯiuy][mz]|d[ɯiuy]ɾ?|jd[ɯiuy](m|n|[ɯiuy]z)?|jmɯʃ|jmiʃ|jmuʃ|jmyʃ)?[?.,!]*$")
_UNLU = set("aeɯiouøyœæɛɪʊ")


def model_klasoru(klasor: str | Path | None = None) -> Path:
    adaylar = [Path(klasor)] if klasor else []
    if os.environ.get("SESLEN_TTS_MODEL"):
        adaylar.append(Path(os.environ["SESLEN_TTS_MODEL"]))
    for a in adaylar:
        if all((a / f).exists() for f in DOSYALAR):
            return a
    if os.environ.get("SESLEN_TTS_INDIRME") != "0":
        try:
            from huggingface_hub import snapshot_download
            a = Path(snapshot_download(HF_DEPO, allow_patterns=DOSYALAR))
            if all((a / f).exists() for f in DOSYALAR):
                return a
        except Exception:
            pass
    raise FileNotFoundError(f"ses modeli bulunamadı: Hugging Face'ten ({HF_DEPO}) indirilemedi ve SESLEN_TTS_MODEL "
                            f"ile klasör gösterilmedi. Gereken dosyalar: {', '.join(DOSYALAR)}")


def soru_egrisi(okunus: str, sozluk: dict) -> np.ndarray:
    """Okunuşun modele giren her işaretine yarım ton eki: soru ekinden önceki sözcüğün vurgulu hecesine SORU_TEPE,
    gerisine 0. Uzunluk, sözlükte olan karakter sayısıdır (olmayanlar işarete çevrilmez)."""
    ek = np.zeros(len(okunus), np.float32)
    if "?" in okunus:
        sozcukler, i = [], 0
        for s in okunus.split(" "):
            sozcukler.append((i, s))
            i += len(s) + 1
        for j in range(1, len(sozcukler)):
            bas, s = sozcukler[j]
            if not _SORU_EKI.match(s.replace("ˈ", "")) or "?" not in okunus[bas:]:
                continue
            b0, onceki = sozcukler[j - 1]
            if not onceki or onceki[-1] in "?.,!;:":
                continue
            v = onceki.rfind("ˈ")
            if v < 0:               # vurgu işareti yoksa son hece: son ünlü + önündeki ünsüz
                v = max((k for k, c in enumerate(onceki) if c in _UNLU), default=0)
                v -= v > 0 and onceki[v - 1] not in _UNLU
            # hecenin sonu: vurgulu ünlüden sonraki ilk ayrı ünlünün (bitişik ünlü aynı çekirdek) önündeki ünsüz
            k = next((k for k in range(v, len(onceki)) if onceki[k] in _UNLU), len(onceki))
            while k < len(onceki) and (onceki[k] in _UNLU or onceki[k] == "ː"):
                k += 1
            sonraki = next((m for m in range(k, len(onceki)) if onceki[m] in _UNLU), None)
            son = len(onceki) if sonraki is None else max(sonraki - 1, k)
            ek[b0 + v: b0 + son] = SORU_TEPE
    return np.array([e for c, e in zip(okunus, ek) if c in sozluk], np.float32)


def windows_kisitini_kaldir() -> None:
    """Windows arka plandaki süreçleri enerji tasarrufu için yavaşlatıyor (EcoQoS): ölçümde ses üretimi 4-5 kat
    yavaşladı. Bu süreç için kısıt kapatılır; önceliğe dokunulmaz. SESLEN_TTS_SUREC=0 ile kapalı."""
    if os.name != "nt" or os.environ.get("SESLEN_TTS_SUREC") == "0":
        return
    import ctypes
    import ctypes.wintypes as w

    class _Kisit(ctypes.Structure):
        _fields_ = [("Version", w.ULONG), ("ControlMask", w.ULONG), ("StateMask", w.ULONG)]
    k = ctypes.windll.kernel32
    k.OpenProcess.restype = w.HANDLE
    h = k.OpenProcess(0x0200 | 0x0400, False, os.getpid())       # PROCESS_SET_INFORMATION | QUERY_INFORMATION
    if h:
        s = _Kisit(1, 0x1, 0)                                         # PROCESS_POWER_THROTTLING_EXECUTION_SPEED: kapalı
        k.SetProcessInformation(w.HANDLE(h), 4, ctypes.byref(s), ctypes.sizeof(s))
        k.CloseHandle(w.HANDLE(h))


def hizala(sure: np.ndarray) -> np.ndarray:
    """İşaret başına süre (birim) → hizalama matrisi (1, L, F): her işaret kendi süresi kadar çerçeveye yayılır."""
    return np.repeat(np.eye(len(sure), dtype=np.float32), sure, axis=1)[None]


class SesModeli:
    def __init__(self, klasor: str | Path | None = None, is_parcacigi: int = 0):
        import onnxruntime as ort
        windows_kisitini_kaldir()
        k = model_klasoru(klasor)
        se = ort.SessionOptions()
        se.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        se.intra_op_num_threads = is_parcacigi or min(6, os.cpu_count() or 1)
        self.metin = ort.InferenceSession(str(k / "metin.onnx"), se, providers=["CPUExecutionProvider"])
        self.ses = ort.InferenceSession(str(k / "ses.onnx"), se, providers=["CPUExecutionProvider"])
        v = np.load(k / "stiller.npz")
        self.stiller = {a: v[a].astype(np.float32) for a in v.files}
        self.sesler: dict = json.loads((k / "sesler.json").read_text(encoding="utf-8"))
        self.semboller: dict = json.loads((k / "semboller.json").read_text(encoding="utf-8"))
        self._virgul = {self.semboller[c] for c in "," if c in self.semboller}
        self._noktali = {self.semboller[c] for c in ";" if c in self.semboller}

    def okunus(self, metin: str) -> str:
        from turkce_vurgu import g2p
        return g2p(metin, vurgu=True)

    def stil(self, ses: str, ton: str = "notr") -> np.ndarray:
        try:
            return self.stiller[f"{ses}/{ton}"]
        except KeyError:
            raise KeyError(f"bilinmeyen ses/ton: {ses}/{ton}; sesler: {', '.join(self.sesler)}") from None

    def konus(self, metin: str, stil: np.ndarray, hiz: float = 1.0, perde: float = 1.0, tonlama: float = 1.0,
              virgul_ms: int = 0) -> np.ndarray:
        """Tek cümle → 24 kHz dalga (float32). hiz > 1 hızlı; perde: F0 çarpanı; tonlama: perde dalgalanması
        çarpanı (1 doğal); virgul_ms: virgül ve noktalı virgülde ek duraklama."""
        okunus = self.okunus(metin)
        kod = [self.semboller[c] for c in okunus if c in self.semboller]
        tokens = np.array([[0, *kod, 0]], np.int64)
        egri = np.concatenate([[0], soru_egrisi(okunus, self.semboller), [0]]).astype(np.float32)[None]
        stil = np.asarray(stil, np.float32).reshape(1, -1)
        d, t_en, sure = self.metin.run(None, {"tokens": tokens, "stil": stil})
        sure = np.maximum(np.round(sure / hiz), 1).astype(np.int64)
        sure[0] = min(sure[0], BAS_DOLGU)
        for i, k in enumerate(kod, 1):
            if k in self._noktali:
                sure[i] += round(max(virgul_ms, NOKTALI_MS) / BIRIM_MS)
            elif virgul_ms and k in self._virgul:
                sure[i] += round(virgul_ms / BIRIM_MS)
        g = {"d": d, "t_en": t_en, "hiza": hizala(sure), "s": stil[:, 128:], "ref": stil[:, :128],
             "perde": np.array([perde], np.float32), "tonlama": np.array([tonlama], np.float32), "egri": egri}
        return self.ses.run(None, g)[0][..., :-50].reshape(-1)       # sondaki tık

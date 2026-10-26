import os

import numpy as np
import pytest

from seslen_tts.model import SORU_TEPE, hizala, soru_egrisi
from seslen_tts.seslen import _cumleler, akici


class _Hepsi(dict):
    def __contains__(self, k):
        return True


def _tepe(okunus):
    e = soru_egrisi(okunus, _Hepsi())
    return "".join(c for c, x in zip(okunus, e) if x > 0)


def test_soru_tepesi_vurgulu_hecede():
    assert _tepe("baˈna jaɾdɯmˈdʒɯ oɫabiˈliɾ misin?") == "ˈliɾ"      # olaBİLİR misin
    assert _tepe("ˈankaɾa ɟyˈzel mi?") == "ˈzel"                     # güZEL mi
    assert _tepe("buˈnu ˈsen mi japˈtɯn?") == "ˈsen"                 # SEN mi yaptın
    assert _tepe("ɟeˈlijoɾ musunuz?") == "ˈli"                       # geLİyor musunuz


def test_soru_sozcuklu_ve_duz_cumleye_dokunmaz():
    assert _tepe("neˈden ˈɟelmedin?") == ""
    assert _tepe("mɯˈsɯɾ ˈtʃok ɟyzelˈdi.") == ""                     # "Mısır" soru eki değil


def test_egri_sozlukte_olmayani_atlar():
    e = soru_egrisi("ab mi?", {"a": 1, "b": 2, " ": 3, "m": 4, "i": 5})   # "?" sözlükte yok
    assert len(e) == 5 and e.max() == SORU_TEPE


def test_hizala():
    h = hizala(np.array([2, 1, 3]))
    assert h.shape == (1, 3, 6)
    assert h[0].sum(axis=0).tolist() == [1] * 6 and h[0].sum(axis=1).tolist() == [2, 1, 3]


def test_cumleler():
    assert _cumleler("Merhaba! Nasılsın? İyiyim.") == ["Merhaba, nasılsın?", "İyiyim."]
    assert _cumleler("Bugün hava güzel. Yarın yağmur var.") == ["Bugün hava güzel.", "Yarın yağmur var."]


def test_akici():
    assert akici("Dikkat! Bu işlem geri alınamaz.") == "Dikkat, bu işlem geri alınamaz."
    assert akici("Evet! Tamam! Gidelim.") == "Evet, tamam, gidelim."
    assert akici("Dr. Ahmet geldi.") == "Dr. Ahmet geldi."               # kısaltma
    assert akici("Madde 3. Sonra bakarız.") == "Madde 3. Sonra bakarız."  # sayı
    assert akici("Tamam! ABD'ye gidiyoruz.") == "Tamam, ABD'ye gidiyoruz."


@pytest.mark.skipif(not os.environ.get("SESLEN_TTS_MODEL"), reason="model yok (SESLEN_TTS_MODEL)")
def test_seslendirme():
    from seslen_tts import ORAN, Seslen
    s = Seslen()
    assert "notr" in s.tonlar("zeynep")
    parcalar = list(s.seslendir("Bugün hava güzel. Yarın gelecek misiniz?", ses="zeynep", ton="notr"))
    assert len(parcalar) == 2
    assert all(0.4 < len(p.ses) / ORAN < 5 and np.isfinite(p.ses).all() for p in parcalar)

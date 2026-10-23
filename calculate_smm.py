#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mali Müşavir ve Muhasebe Hesaplama CLI Motoru v2.0
--------------------------------------------------
- e-SMM Net/Brüt/Stopaj/KDV Hesabı
- GİB Tevkifat Kodları (601-626) ve KDV Tevkifatı Doğrulama Motoru
- 2026/2027 Gelir Vergisi Dilimleri ve Asgari Ücret Vergi İstisnası Bordro Motoru
- VUK Geçici 33 Enflasyon Düzeltmesi & 698 Hesap Bakiye Kontrolü
- Kıdem ve İhbar Tazminatı Hesaplayıcı
- Yeniden Değerleme Oranı (YDO) Hesaplayıcı
"""

import sys
import json

# Force UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ==============================================================================
# 1. GİB RESMİ KDV TEVKİFAT KODLARI REHBERİ
# ==============================================================================
GIB_TEVKIFAT_KODLARI = {
    "601": {
        "ad": "Yapım İşleri ile Bu İşlerle Birlikte İfa Edilen Mühendislik-Mimarlık ve Etüt-Proje Hizmetleri",
        "pay": 4, "payda": 10, "oran_str": "4/10",
        "aciklama": "Belirlenmiş alıcılara veya KDV mükelleflerine karşı ifa edilen yapım taahhüt işleri."
    },
    "602": {
        "ad": "Etüt, Plan-Proje, Danışmanlık, Denetim ve Benzeri Hizmetler",
        "pay": 9, "payda": 10, "oran_str": "9/10",
        "aciklama": "Piyasa araştırması, teknik müşavirlik, mali danışmanlık ve denetim hizmetleri."
    },
    "603": {
        "ad": "Makine, Teçhizat, Demirbaş ve Taşıtlara Ait Tadil, Bakım ve Onarım Hizmetleri",
        "pay": 7, "payda": 10, "oran_str": "7/10",
        "aciklama": "İşletmeye dahil aktif kıymetlerin bakım ve onarım işleri."
    },
    "604": {
        "ad": "Yemek Servis ve Organizasyon Hizmetleri",
        "pay": 5, "payda": 10, "oran_str": "5/10",
        "aciklama": "Toplu yemek, tabldot servisi ve catering organizasyonları."
    },
    "605": {
        "ad": "İşgücü Temin Hizmetleri (Özel Güvenlik Dahil)",
        "pay": 9, "payda": 10, "oran_str": "9/10",
        "aciklama": "Hizmet akdiyle bağlı personelin başka bir firmanın sevk ve idaresine verilmesi."
    },
    "606": {
        "ad": "Özel Güvenlik Hizmeti",
        "pay": 9, "payda": 10, "oran_str": "9/10",
        "aciklama": "5188 sayılı Kanun kapsamında güvenlik şirketlerince sağlanan koruma hizmetleri."
    },
    "607": {
        "ad": "Yapı Denetim Hizmetleri",
        "pay": 9, "payda": 10, "oran_str": "9/10",
        "aciklama": "Yapı denetim kuruluşları tarafından arsa sahibi veya müteahhide verilen denetim hizmeti."
    },
    "608": {
        "ad": "Fason Olarak Yaptırılan Tekstil ve Konfeksiyon İşleri",
        "pay": 7, "payda": 10, "oran_str": "7/10",
        "aciklama": "Kumaş, deri ve konfeksiyon fason dikim, kesim, boyama ve ütüleme işleri."
    },
    "609": {
        "ad": "Turistik Mağazalara Verilen Müşteri Bulma / Götürme Hizmetleri",
        "pay": 9, "payda": 10, "oran_str": "9/10",
        "aciklama": "Rehber ve acenteler tarafından mağazalara müşteri yönlendirilmesi."
    },
    "610": {
        "ad": "Spor Kulüplerinin Yayın, Reklâm ve İsim Hakkı Gelirleri",
        "pay": 9, "payda": 10, "oran_str": "9/10",
        "aciklama": "Profesyonel kulüplerin sponsorluk, forma reklamı ve isim hakkı devirleri."
    },
    "611": {
        "ad": "Temizlik, Çevre ve Bahçe Bakım Hizmetleri",
        "pay": 9, "payda": 10, "oran_str": "9/10",
        "aciklama": "Bina içi/dışı genel temizlik, dezenfeksiyon ve çevre düzenleme işleri."
    },
    "612": {
        "ad": "Servis Taşımacılığı Hizmeti",
        "pay": 5, "payda": 10, "oran_str": "5/10",
        "aciklama": "Personel ve öğrenci servis taşımacılığı işleri."
    },
    "613": {
        "ad": "Her Türlü Yük Taşımacılığı Hizmeti",
        "pay": 2, "payda": 10, "oran_str": "2/10",
        "aciklama": "Karayolu, denizyolu ve havayolu ile yük ve kargo taşıma hizmetleri."
    },
    "614": {
        "ad": "Her Türlü Baskı ve Basım Hizmetleri",
        "pay": 7, "payda": 10, "oran_str": "7/10",
        "aciklama": "Matbaacılık, broşür, katalog, ambalaj baskı ve ciltleme işleri."
    },
    "615": {
        "ad": "Ticari Reklam Hizmetleri",
        "pay": 3, "payda": 10, "oran_str": "3/10",
        "aciklama": "Dijital, televizyon, gazete veya billboard reklam yayınlama ve tasarım hizmetleri."
    },
    "616": {
        "ad": "Diğer Hizmetler (Kapsam İçi Kurumlarca Alınan)",
        "pay": 5, "payda": 10, "oran_str": "5/10",
        "aciklama": "Belirlenmiş alıcı kurum ve kuruluşlara ifa edilen diğer genel hizmetler."
    },
    "617": {
        "ad": "Hurda ve Atık Teslimleri (Metal, Plastik, Kağıt, Cam)",
        "pay": 7, "payda": 10, "oran_str": "7/10",
        "aciklama": "KDV Kanunu 17/4-g istisnasından vazgeçenlerin hurda teslimleri."
    },
    "620": {
        "ad": "Pamuk, Tiftik, Yün ve Yapağı ile Ham Post ve Deri Teslimleri",
        "pay": 2, "payda": 10, "oran_str": "2/10",
        "aciklama": "Tekstil ve deri sanayii ham madde teslimleri."
    },
    "621": {
        "ad": "Ağaç ve Orman Ürünleri Teslimi (Tomruk, Kereste, Talaş)",
        "pay": 5, "payda": 10, "oran_str": "5/10",
        "aciklama": "Orman ürünleri, tomruk, odun ve kereste teslimleri."
    },
    "622": {
        "ad": "Demir-Çelik Ürünlerinin Teslimi",
        "pay": 4, "payda": 10, "oran_str": "4/10",
        "aciklama": "İnşaat demiri, çubuk, profil ve çelik levha teslimleri."
    },
    "623": {
        "ad": "Bakır, Çinko, Alüminyum ve Kurşun Ürünlerinin Teslimi",
        "pay": 7, "payda": 10, "oran_str": "7/10",
        "aciklama": "İlk üreticilerden veya tüccarlardan alınan demir dışı metal mamulleri."
    }
}

# ==============================================================================
# 2. GELİR VERGİSİ DİLİMLERİ VE ASGARİ ÜCRET İSTİSNASI (2026/2027)
# ==============================================================================
# GVK Madde 103 Ücret Gelirleri Tarifesi (2026 Yılı Esas)
GELIR_VERGISI_DILIMLERI_2026_UCRET = [
    {"limit": 158000.0, "oran": 0.15, "sabit": 0.0},
    {"limit": 330000.0, "oran": 0.20, "sabit": 23700.0},
    {"limit": 1200000.0, "oran": 0.27, "sabit": 58100.0},
    {"limit": 3000000.0, "oran": 0.35, "sabit": 293000.0},
    {"limit": float("inf"), "oran": 0.40, "sabit": 923000.0}
]

# 2026 Yılı Tahmini/Resmi Aylık Brüt Asgari Ücret Parametreleri
ASGARI_UCRET_2026_BRUT = 26005.50
ASGARI_UCRET_2026_SGK_ISCI = round(ASGARI_UCRET_2026_BRUT * 0.14, 2)       # %14
ASGARI_UCRET_2026_ISSIZLIK_ISCI = round(ASGARI_UCRET_2026_BRUT * 0.01, 2)  # %1
ASGARI_UCRET_2026_MATRAH = round(ASGARI_UCRET_2026_BRUT - ASGARI_UCRET_2026_SGK_ISCI - ASGARI_UCRET_2026_ISSIZLIK_ISCI, 2)
ASGARI_UCRET_2026_GV_ISTISNA = round(ASGARI_UCRET_2026_MATRAH * 0.15, 2)   # %15 ilk dilim
ASGARI_UCRET_2026_DV_ISTISNA = round(ASGARI_UCRET_2026_BRUT * 0.00759, 2)  # Damga Vergisi İstisnası

# ==============================================================================
# 3. HESAPLAMA FONKSİYONLARI
# ==============================================================================

def calculate_esmm_from_brut(brut_tutar: float, stopaj_orani: float = 0.20, kdv_orani: float = 0.20) -> dict:
    """Brütten Nete e-SMM (Serbest Meslek Makbuzu) Hesabı."""
    brut = float(brut_tutar)
    stopaj = brut * stopaj_orani
    kdv = brut * kdv_orani
    net = brut - stopaj
    tahsilat = net + kdv

    return {
        "brut_ucret": round(brut, 2),
        "stopaj_orani": stopaj_orani,
        "stopaj_tutari": round(stopaj, 2),
        "kdv_orani": kdv_orani,
        "kdv_tutari": round(kdv, 2),
        "net_ucret": round(net, 2),
        "tahsil_edilen_toplam": round(tahsilat, 2)
    }

def calculate_esmm_from_net(net_tutar: float, stopaj_orani: float = 0.20, kdv_orani: float = 0.20) -> dict:
    """Netten Brüte e-SMM Hesabı."""
    net = float(net_tutar)
    brut = net / (1.0 - stopaj_orani)
    return calculate_esmm_from_brut(brut, stopaj_orani, kdv_orani)

def calculate_kdv_tevkifat(matrah: float, kdv_orani: float = 0.20, tevkifat_pay: int = 5, tevkifat_payda: int = 10, tevkifat_kodu: str = "") -> dict:
    """
    KDV Tevkifatı Hesaplama:
    - Tevkifat Kodu girilmişse otomatik pay/payda ve açıklama çeker.
    """
    matrah = float(matrah)
    oran = float(kdv_orani)
    hesaplanan_kdv = matrah * oran

    kod_bilgisi = None
    if tevkifat_kodu and tevkifat_kodu in GIB_TEVKIFAT_KODLARI:
        kod_bilgisi = GIB_TEVKIFAT_KODLARI[tevkifat_kodu]
        tevkifat_pay = kod_bilgisi["pay"]
        tevkifat_payda = kod_bilgisi["payda"]

    oran_tevkifat = float(tevkifat_pay) / float(tevkifat_payda)
    tevkif_edilen = hesaplanan_kdv * oran_tevkifat
    tahsil_edilen_kdv = hesaplanan_kdv - tevkif_edilen
    fatura_toplam = matrah + tahsil_edilen_kdv

    res = {
        "matrah": round(matrah, 2),
        "kdv_orani": oran,
        "hesaplanan_kdv": round(hesaplanan_kdv, 2),
        "tevkifat_orani_str": f"{tevkifat_pay}/{tevkifat_payda}",
        "tevkif_edilen_kdv": round(tevkif_edilen, 2),
        "tahsil_edilen_kdv": round(tahsil_edilen_kdv, 2),
        "fatura_toplam": round(fatura_toplam, 2),
        "kdv2_beyan_tutari": round(tevkif_edilen, 2)
    }
    if kod_bilgisi:
        res["tevkifat_kodu"] = tevkifat_kodu
        res["tevkifat_adi"] = kod_bilgisi["ad"]
        res["aciklama"] = kod_bilgisi["aciklama"]
    return res

def calculate_gelir_vergisi_dilimleri(kumulatif_onceki: float, aylik_matrah: float, tarifeler=None) -> dict:
    """
    Kümülatif matraha göre Gelir Vergisi Dilimlerini (%15, %20, %27, %35, %40) hassas hesaplar.
    Dilim geçişlerinde orantılı bölüştürme yapar.
    """
    if tarifeler is None:
        tarifeler = GELIR_VERGISI_DILIMLERI_2026_UCRET

    k_onceki = float(kumulatif_onceki)
    matrah = float(aylik_matrah)
    k_sonraki = k_onceki + matrah

    vergi_toplam = 0.0
    dilim_kirilimlari = []

    # Her dilim aralığındaki payı hesapla
    alt_sinir = 0.0
    for idx, d in enumerate(tarifeler):
        ust_sinir = d["limit"]
        oran = d["oran"]

        # Bu dilime düşen matrah parçası
        if k_sonraki > alt_sinir and k_onceki < ust_sinir:
            baslangic = max(k_onceki, alt_sinir)
            bitis = min(k_sonraki, ust_sinir)
            dilim_matrahi = max(0.0, bitis - baslangic)
            dilim_vergisi = dilim_matrahi * oran

            if dilim_matrahi > 0:
                vergi_toplam += dilim_vergisi
                dilim_kirilimlari.append({
                    "dilim": f"%{int(oran*100)}",
                    "matrah": round(dilim_matrahi, 2),
                    "vergi": round(dilim_vergisi, 2)
                })

        alt_sinir = ust_sinir

    return {
        "kumulatif_onceki": round(k_onceki, 2),
        "aylik_matrah": round(matrah, 2),
        "kumulatif_sonraki": round(k_sonraki, 2),
        "hesaplanan_gelir_vergisi": round(vergi_toplam, 2),
        "dilim_detaylari": dilim_kirilimlari
    }

def calculate_bordro(brut_ucret: float, kumulatif_onceki: float = 0.0, engellilik_indirimi: float = 0.0) -> dict:
    """
    7349 Sayılı Kanun Uyumlu Personel Bordro ve Asgari Ücret Vergi İstisnası Hesaplayıcı.
    """
    brut = float(brut_ucret)
    sgk_isci = round(brut * 0.14, 2)       # %14 SGK İşçi Payı
    issizlik_isci = round(brut * 0.01, 2)  # %1 İşsizlik Sigortası İşçi Payı
    toplam_sgk_kesintisi = round(sgk_isci + issizlik_isci, 2)

    gv_matrahi = max(0.0, round(brut - toplam_sgk_kesintisi - engellilik_indirimi, 2))

    gv_hesap = calculate_gelir_vergisi_dilimleri(kumulatif_onceki, gv_matrahi)
    hesaplanan_gv = gv_hesap["hesaplanan_gelir_vergisi"]

    # Asgari Ücret Gelir Vergisi İstisnası (Kümülatif aşım kontrolü)
    gv_istisnasi = min(hesaplanan_gv, ASGARI_UCRET_2026_GV_ISTISNA)
    odenecek_gv = max(0.0, round(hesaplanan_gv - gv_istisnasi, 2))

    # Damga Vergisi ve İstisnası (Binde 7.59)
    hesaplanan_dv = round(brut * 0.00759, 2)
    dv_istisnasi = min(hesaplanan_dv, ASGARI_UCRET_2026_DV_ISTISNA)
    odenecek_dv = max(0.0, round(hesaplanan_dv - dv_istisnasi, 2))

    toplam_kesinti = round(toplam_sgk_kesintisi + odenecek_gv + odenecek_dv, 2)
    net_ucret = round(brut - toplam_kesinti, 2)

    # İşveren Maliyeti
    sgk_isveren = round(brut * 0.205, 2)      # %20.5 (5 puan teşviksiz) veya %15.5
    issizlik_isveren = round(brut * 0.02, 2)  # %2 İşveren İşsizlik
    toplam_isveren_maliyeti = round(brut + sgk_isveren + issizlik_isveren, 2)

    return {
        "brut_ucret": round(brut, 2),
        "sgk_isci_payi": sgk_isci,
        "issizlik_isci_payi": issizlik_isci,
        "toplam_sgk_kesintisi": toplam_sgk_kesintisi,
        "gelir_vergisi_matrahi": gv_matrahi,
        "kumulatif_gelir_vergisi_matrahi": round(kumulatif_onceki + gv_matrahi, 2),
        "hesaplanan_gelir_vergisi": hesaplanan_gv,
        "asgari_ucret_gv_istisnasi": gv_istisnasi,
        "odenecek_gelir_vergisi": odenecek_gv,
        "hesaplanan_damga_vergisi": hesaplanan_dv,
        "asgari_ucret_dv_istisnasi": dv_istisnasi,
        "odenecek_damga_vergisi": odenecek_dv,
        "toplam_yasal_kesintiler": toplam_kesinti,
        "net_ele_gecen_ucret": net_ucret,
        "isveren_sgk_payi": sgk_isveren,
        "isveren_issizlik_payi": issizlik_isveren,
        "toplam_isveren_maliyeti": toplam_isveren_maliyeti,
        "dilim_detaylari": gv_hesap["dilim_detaylari"]
    }

def calculate_enflasyon_katsayisi(endeks_donem_sonu: float, endeks_esas_tarih: float) -> float:
    """VUK Geçici 33 uyarınca Enflasyon Düzeltme Katsayısı = Son Endeks / Esas Endeks."""
    if endeks_esas_tarih <= 0:
        return 1.0
    return round(float(endeks_donem_sonu) / float(endeks_esas_tarih), 5)

def calculate_kiymet_duzeltme(deger: float, endeks_donem_sonu: float, endeks_esas_tarih: float, birikmis_amortisman: float = 0.0) -> dict:
    """
    Maddi Duran Varlık ve Birikmiş Amortisman Enflasyon Düzeltmesi:
    - Varlık Düzeltilmiş Değeri = Varlık Değeri * Düzeltme Katsayısı
    - Amortisman Düzeltilmiş Değeri = Birikmiş Amortisman * Düzeltme Katsayısı
    - Net Düzeltme Farkı = Varlık Düzeltme Farkı - Amortisman Düzeltme Farkı
    """
    deger = float(deger)
    amort = float(birikmis_amortisman)
    katsayi = calculate_enflasyon_katsayisi(endeks_donem_sonu, endeks_esas_tarih)

    duzeltilmis_deger = round(deger * katsayi, 2)
    varlik_farki = round(duzeltilmis_deger - deger, 2)

    duzeltilmis_amortisman = round(amort * katsayi, 2)
    amortisman_farki = round(duzeltilmis_amortisman - amort, 2)

    net_fark = round(varlik_farki - amortisman_farki, 2)

    return {
        "tarihi_deger": round(deger, 2),
        "birikmis_amortisman": round(amort, 2),
        "duzeltme_katsayisi": katsayi,
        "duzeltilmis_deger": duzeltilmis_deger,
        "varlik_duzeltme_farki": varlik_farki,
        "duzeltilmis_amortisman": duzeltilmis_amortisman,
        "amortisman_duzeltme_farki": amortisman_farki,
        "net_698_farki": net_fark
    }

def calculate_stok_basit_ortalama(stok_tutari: float, endeks_donem_sonu: float, endeks_onceki_donem: float) -> dict:
    """
    Stoklar için VUK Basit Ortalama Yöntemi:
    - Ortalama Endeks = (Dönem Sonu Yİ-ÜFE + Bir Önceki Dönem Sonu Yİ-ÜFE) / 2
    - Düzeltme Katsayısı = Dönem Sonu Yİ-ÜFE / Ortalama Endeks
    """
    stok = float(stok_tutari)
    son = float(endeks_donem_sonu)
    onceki = float(endeks_onceki_donem)

    ortalama_endeks = (son + onceki) / 2.0
    katsayi = round(son / ortalama_endeks, 5) if ortalama_endeks > 0 else 1.0

    duzeltilmis_stok = round(stok * katsayi, 2)
    enflasyon_farki = round(duzeltilmis_stok - stok, 2)

    return {
        "stok_tutari": round(stok, 2),
        "donem_sonu_endeks": son,
        "onceki_donem_endeks": onceki,
        "ortalama_endeks": round(ortalama_endeks, 2),
        "basit_ortalama_katsayisi": katsayi,
        "duzeltilmis_stok": duzeltilmis_stok,
        "stok_enflasyon_farki": enflasyon_farki
    }

def calculate_698_enflasyon_hesabi(aktif_farklar_toplami: float, pasif_farklar_toplami: float) -> dict:
    """
    698 Enflasyon Düzeltme Hesabı Bakiye Analizi:
    - Aktif Parasal Olmayan Farklar -> 698 Hesabın ALACAĞINA
    - Pasif Parasal Olmayan Farklar -> 698 Hesabın BORCUNA
    - Eğer Alacak > Borç: Bakiye 648 Enflasyon Düzeltme Karı (Gelir)
    - Eğer Borç > Alacak: Bakiye 658 Enflasyon Düzeltme Zararı (Gider)
    """
    aktif_alacak = float(aktif_farklar_toplami)
    pasif_borc = float(pasif_farklar_toplami)
    fark = round(aktif_alacak - pasif_borc, 2)

    if fark > 0:
        durum = "KÂR"
        sonuc_hesap = "648 Enflasyon Düzeltmesi Kârları"
        kar_tutari = fark
        zarar_tutari = 0.0
    elif fark < 0:
        durum = "ZARAR"
        sonuc_hesap = "658 Enflasyon Düzeltmesi Zararları"
        kar_tutari = 0.0
        zarar_tutari = abs(fark)
    else:
        durum = "DENK"
        sonuc_hesap = "Bakiye Yok (Denk)"
        kar_tutari = 0.0
        zarar_tutari = 0.0

    return {
        "aktif_farklar_alacak": round(aktif_alacak, 2),
        "pasif_farklar_borc": round(pasif_borc, 2),
        "net_bakiye": abs(fark),
        "sonuc_durum": durum,
        "kapanis_hesabi": sonuc_hesap,
        "enflasyon_kari": kar_tutari,
        "enflasyon_zarari": zarar_tutari
    }

def calculate_kidem_tazminati(brut_ucret: float, yil: float, kidem_tavani: float = 46500.0) -> dict:
    """Kıdem Tazminatı Hesabı."""
    uygulanan_ucret = min(float(brut_ucret), float(kidem_tavani))
    brut_kidem = uygulanan_ucret * float(yil)
    damga_vergisi = brut_kidem * 0.00759
    net_kidem = brut_kidem - damga_vergisi

    return {
        "giydirilmis_brut": round(brut_ucret, 2),
        "kidem_tavani": round(kidem_tavani, 2),
        "uygulanan_brut": round(uygulanan_ucret, 2),
        "calisma_yili": round(yil, 2),
        "brut_kidem": round(brut_kidem, 2),
        "damga_vergisi": round(damga_vergisi, 2),
        "net_kidem_tazminati": round(net_kidem, 2)
    }

def calculate_ydo(tutar: float, ydo_orani: float = 0.4393) -> dict:
    """Yeniden Değerleme Oranı (YDO) Artış Hesabı."""
    tutar = float(tutar)
    oran = float(ydo_orani)
    artis = tutar * oran
    yeni = tutar + artis
    return {
        "eski_tutar": round(tutar, 2),
        "ydo_orani": oran,
        "artis_tutari": round(artis, 2),
        "yeni_tutar": round(yeni, 2)
    }

# ==============================================================================
# CLI KOMUT SATIRI ARAYÜZÜ
# ==============================================================================
def main():
    import argparse
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--json", action="store_true", help="Çıktıyı JSON formatında ver")
    parent_parser.add_argument("--markdown", action="store_true", help="Çıktıyı Markdown tablosu formatında ver")

    parser = argparse.ArgumentParser(description="Mali Müşavir ve Muhasebe Hesaplama Motoru (CLI)", parents=[parent_parser])
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. e-SMM
    p_smm = subparsers.add_parser("esmm", help="e-SMM Makbuz Hesaplayıcı", parents=[parent_parser])
    p_smm.add_argument("tutar", type=float, help="Tutar (TL)")
    p_smm.add_argument("--net", action="store_true", help="Girilen tutarı net kabul et (Varsayılan: brüt)")
    p_smm.add_argument("--stopaj", type=float, default=0.20, help="Stopaj oranı (Varsayılan: 0.20)")
    p_smm.add_argument("--kdv", type=float, default=0.20, help="KDV oranı (Varsayılan: 0.20)")

    # 2. Tevkifat
    p_tev = subparsers.add_parser("tevkifat", help="KDV Tevkifat Hesaplayıcı ve GİB Kod Doğrulayıcı", parents=[parent_parser])
    p_tev.add_argument("matrah", type=float, help="KDV Hariç Matrah (TL)")
    p_tev.add_argument("--kod", type=str, default="", help="GİB Tevkifat Kodu (örn: 601, 608, 622)")
    p_tev.add_argument("--oran", type=str, default="5/10", help="Tevkifat oranı (varsayılan: 5/10)")
    p_tev.add_argument("--kdv", type=float, default=0.20, help="KDV oranı (Varsayılan: 0.20)")

    # 3. Bordro
    p_bor = subparsers.add_parser("bordro", help="2026 Bordro ve Asgari Ücret Vergi İstisnası Hesaplayıcı", parents=[parent_parser])
    p_bor.add_argument("brut", type=float, help="Aylık brüt ücret (TL)")
    p_bor.add_argument("--kumulatif", type=float, default=0.0, help="Önceki aylardan devreden kümülatif GV matrahı (TL)")
    p_bor.add_argument("--engelli", type=float, default=0.0, help="Engellilik indirim tutarı (TL)")

    # 4. Enflasyon Düzeltmesi (VUK Geçici 33)
    p_enf = subparsers.add_parser("enflasyon", help="VUK Geçici 33 Enflasyon Düzeltmesi & 698 Hesap Kontrolü", parents=[parent_parser])
    p_enf.add_argument("deger", type=float, help="Kıymet veya Stok Değeri (TL)")
    p_enf.add_argument("--son-endeks", type=float, required=True, help="Dönem sonu Yİ-ÜFE endeksi")
    p_enf.add_argument("--esas-endeks", type=float, default=0.0, help="Düzeltmeye esas tarih Yİ-ÜFE endeksi (Duran Varlık için)")
    p_enf.add_argument("--onceki-endeks", type=float, default=0.0, help="Bir önceki dönem sonu Yİ-ÜFE (Stok Basit Ortalama için)")
    p_enf.add_argument("--amortisman", type=float, default=0.0, help="Varsa birikmiş amortisman tutarı (TL)")

    # 5. Kıdem
    p_kidem = subparsers.add_parser("kidem", help="Kıdem Tazminatı Hesaplayıcı", parents=[parent_parser])
    p_kidem.add_argument("brut", type=float, help="Aylık giydirilmiş brüt ücret (TL)")
    p_kidem.add_argument("yil", type=float, help="Hizmet süresi (Yıl)")
    p_kidem.add_argument("--tavan", type=float, default=46500.0, help="Güncel kıdem tazminatı tavanı")

    # 6. YDO
    p_ydo = subparsers.add_parser("ydo", help="Yeniden Değerleme Oranı (YDO) Hesaplayıcı", parents=[parent_parser])
    p_ydo.add_argument("tutar", type=float, help="Eski Tutar (TL)")
    p_ydo.add_argument("--oran", type=float, default=0.4393, help="YDO oranı (Varsayılan: 0.4393 / %43.93)")

    args = parser.parse_args()

    if args.command == "esmm":
        res = calculate_esmm_from_net(args.tutar, args.stopaj, args.kdv) if args.net else calculate_esmm_from_brut(args.tutar, args.stopaj, args.kdv)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print("          e-SMM MAKBUZ HESAPLAMA TABLOSU")
            print("=" * 60)
            print(f"Brüt Ücret              : {res['brut_ucret']:,.2f} TL")
            print(f"GV Stopajı (%{int(res['stopaj_orani']*100)})         : -{res['stopaj_tutari']:,.2f} TL")
            print(f"Net Ücret               : {res['net_ucret']:,.2f} TL")
            print(f"KDV (%{int(res['kdv_orani']*100)})                : +{res['kdv_tutari']:,.2f} TL")
            print("-" * 60)
            print(f"TAHSİL EDİLECEK TOPLAM  : {res['tahsil_edilen_toplam']:,.2f} TL")
            print("=" * 60)

    elif args.command == "tevkifat":
        pay, payda = 5, 10
        if args.oran and "/" in args.oran:
            parts = args.oran.split("/")
            pay, payda = int(parts[0]), int(parts[1])
        res = calculate_kdv_tevkifat(args.matrah, args.kdv, pay, payda, tevkifat_kodu=args.kod)

        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print("          KDV TEVKİFAT HESAPLAMA VE DOĞRULAMA")
            print("=" * 60)
            if "tevkifat_kodu" in res:
                print(f"GİB Tevkifat Kodu       : {res['tevkifat_kodu']} - {res['tevkifat_adi']}")
            print(f"Matrah (KDV Hariç)      : {res['matrah']:,.2f} TL")
            print(f"Hesaplanan KDV (%{int(res['kdv_orani']*100)})     : {res['hesaplanan_kdv']:,.2f} TL")
            print(f"Tevkifat Oranı          : {res['tevkifat_orani_str']}")
            print(f"Tevkif Edilen KDV       : {res['tevkif_edilen_kdv']:,.2f} TL")
            print(f"Tahsil Edilen KDV       : {res['tahsil_edilen_kdv']:,.2f} TL")
            print("-" * 60)
            print(f"FATURA TOPLAM TUTARI    : {res['fatura_toplam']:,.2f} TL")
            print(f"ALICININ KDV-2 BEYANI   : {res['kdv2_beyan_tutari']:,.2f} TL")
            print("=" * 60)

    elif args.command == "bordro":
        res = calculate_bordro(args.brut, args.kumulatif, args.engelli)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print("       2026 PERSONEL BORDRO VE VERGİ İSTİSNASI HESABI")
            print("=" * 60)
            print(f"Brüt Ücret                  : {res['brut_ucret']:,.2f} TL")
            print(f"SGK İşçi Kesintisi (%15)    : -{res['toplam_sgk_kesintisi']:,.2f} TL")
            print(f"Gelir Vergisi Matrahı       : {res['gelir_vergisi_matrahi']:,.2f} TL (Küm: {res['kumulatif_gelir_vergisi_matrahi']:,.2f} TL)")
            print(f"Hesaplanan Gelir Vergisi    : {res['hesaplanan_gelir_vergisi']:,.2f} TL")
            print(f"Asgari Ücret GV İstisnası   : -{res['asgari_ucret_gv_istisnasi']:,.2f} TL")
            print(f"Ödenecek Gelir Vergisi      : {res['odenecek_gelir_vergisi']:,.2f} TL")
            print(f"Ödenecek Damga Vergisi      : {res['odenecek_damga_vergisi']:,.2f} TL")
            print("-" * 60)
            print(f"NET ELE GEÇEN ÜCRET         : {res['net_ele_gecen_ucret']:,.2f} TL")
            print(f"TOPLAM İŞVEREN MALİYETİ     : {res['toplam_isveren_maliyeti']:,.2f} TL")
            print("=" * 60)

    elif args.command == "enflasyon":
        if args.onceki_endeks > 0:
            res = calculate_stok_basit_ortalama(args.deger, args.son_endeks, args.onceki_endeks)
        else:
            res = calculate_kiymet_duzeltme(args.deger, args.son_endeks, args.esas_endeks, args.amortisman)

        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print("     VUK GEÇİCİ 33 ENFLASYON DÜZELTMESİ HESAP TABLOSU")
            print("=" * 60)
            for k, v in res.items():
                print(f"{k:<26}: {v}")
            print("=" * 60)

    elif args.command == "kidem":
        res = calculate_kidem_tazminati(args.brut, args.yil, args.tavan)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print("           KIDEM TAZMİNATI HESAP TABLOSU")
            print("=" * 60)
            print(f"Giydirilmiş Brüt Ücret  : {res['giydirilmis_brut']:,.2f} TL")
            print(f"Uygulanan Kıdem Tavanı  : {res['kidem_tavani']:,.2f} TL")
            print(f"Esas Alınan Brüt        : {res['uygulanan_brut']:,.2f} TL")
            print(f"Hizmet Yılı             : {res['calisma_yili']} Yıl")
            print(f"Brüt Kıdem Tazminatı    : {res['brut_kidem']:,.2f} TL")
            print(f"Damga Vergisi (‰7.59)   : -{res['damga_vergisi']:,.2f} TL")
            print("-" * 60)
            print(f"NET ÖDENECEK KIDEM TAZ. : {res['net_kidem_tazminati']:,.2f} TL")
            print("=" * 60)

    elif args.command == "ydo":
        res = calculate_ydo(args.tutar, args.oran)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print("       YENİDEN DEĞERLEME ORANI (YDO) HESAP TABLOSU")
            print("=" * 60)
            print(f"Eski Tutar              : {res['eski_tutar']:,.2f} TL")
            print(f"YDO Oranı               : %{res['ydo_orani']*100:.2f}")
            print(f"Artış Tutarı            : +{res['artis_tutari']:,.2f} TL")
            print("-" * 60)
            print(f"YENİ GÜNCELLENMİŞ TUTAR : {res['yeni_tutar']:,.2f} TL")
            print("=" * 60)

if __name__ == "__main__":
    main()

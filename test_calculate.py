# -*- coding: utf-8 -*-
"""
test_calculate.py
-----------------
Mali Müşavir ve Muhasebe Hesaplama CLI Motoru Test Süiti.
- e-SMM Hesabı
- GİB Tevkifat Kodları ve KDV Tevkifatı Doğrulama
- 2026/2027 Gelir Vergisi Dilimleri ve Asgari Ücret Vergi İstisnası
- VUK Geçici 33 Enflasyon Düzeltmesi & 698 Hesap Kontrolü
- Kıdem Tazminatı ve YDO
"""

import unittest
from calculate_smm import (
    calculate_esmm_from_brut,
    calculate_esmm_from_net,
    calculate_kidem_tazminati,
    calculate_kdv_tevkifat,
    calculate_ydo,
    calculate_gelir_vergisi_dilimleri,
    calculate_bordro,
    calculate_enflasyon_katsayisi,
    calculate_kiymet_duzeltme,
    calculate_stok_basit_ortalama,
    calculate_698_enflasyon_hesabi,
    GIB_TEVKIFAT_KODLARI
)

class TestCalculateSmm(unittest.TestCase):
    def test_esmm_from_brut(self):
        # 10.000 TL brüt -> Stopaj: 2.000 TL, Net: 8.000 TL, KDV: 2.000 TL, Tahsilat: 10.000 TL
        res = calculate_esmm_from_brut(10000)
        self.assertEqual(res["brut_ucret"], 10000.0)
        self.assertEqual(res["stopaj_tutari"], 2000.0)
        self.assertEqual(res["net_ucret"], 8000.0)
        self.assertEqual(res["kdv_tutari"], 2000.0)
        self.assertEqual(res["tahsil_edilen_toplam"], 10000.0)

    def test_esmm_from_net(self):
        # 8.000 TL net -> Brüt 10.000 TL
        res = calculate_esmm_from_net(8000)
        self.assertEqual(res["brut_ucret"], 10000.0)

    def test_kidem_tazminati(self):
        res = calculate_kidem_tazminati(30000, 5, kidem_tavani=45000)
        self.assertEqual(res["brut_kidem"], 150000.0)
        self.assertAlmostEqual(res["damga_vergisi"], 150000 * 0.00759, places=2)
        self.assertEqual(res["net_kidem_tazminati"], round(150000 - (150000 * 0.00759), 2))

    def test_kdv_tevkifat(self):
        # Matrah: 100.000 TL, %20 KDV: 20.000 TL, 5/10 Tevkifat -> 10.000 TL Tevkif, 10.000 TL Tahsil
        res = calculate_kdv_tevkifat(100000, 0.20, 5, 10)
        self.assertEqual(res["matrah"], 100000.0)
        self.assertEqual(res["hesaplanan_kdv"], 20000.0)
        self.assertEqual(res["tevkif_edilen_kdv"], 10000.0)
        self.assertEqual(res["tahsil_edilen_kdv"], 10000.0)
        self.assertEqual(res["fatura_toplam"], 110000.0)
        self.assertEqual(res["kdv2_beyan_tutari"], 10000.0)

    def test_tevkifat_gib_kodlari(self):
        # GİB Kodu 601 (Yapım İşleri): 4/10
        res601 = calculate_kdv_tevkifat(100000, 0.20, tevkifat_kodu="601")
        self.assertEqual(res601["tevkifat_orani_str"], "4/10")
        self.assertEqual(res601["tevkif_edilen_kdv"], 8000.0)
        self.assertEqual(res601["tahsil_edilen_kdv"], 12000.0)
        self.assertEqual(res601["kdv2_beyan_tutari"], 8000.0)

        # GİB Kodu 608 (Tekstil): 7/10
        res608 = calculate_kdv_tevkifat(100000, 0.20, tevkifat_kodu="608")
        self.assertEqual(res608["tevkifat_orani_str"], "7/10")
        self.assertEqual(res608["tevkif_edilen_kdv"], 14000.0)

        # GİB Kodu 622 (Demir-Çelik): 4/10
        res622 = calculate_kdv_tevkifat(200000, 0.20, tevkifat_kodu="622")
        self.assertEqual(res622["tevkifat_orani_str"], "4/10")
        self.assertEqual(res622["tevkif_edilen_kdv"], 16000.0)

        self.assertIn("602", GIB_TEVKIFAT_KODLARI)
        self.assertEqual(GIB_TEVKIFAT_KODLARI["602"]["oran_str"], "9/10")

    def test_gelir_vergisi_dilimleri_ve_gecisler(self):
        # 1. Dilim içi (0 - 158.000 TL arası): %15
        res1 = calculate_gelir_vergisi_dilimleri(0, 100000)
        self.assertEqual(res1["hesaplanan_gelir_vergisi"], 15000.0)
        self.assertEqual(len(res1["dilim_detaylari"]), 1)

        # Dilim geçişi: Önceki 150.000 TL, aylık 20.000 TL -> 8.000 TL'si %15, 12.000 TL'si %20
        res2 = calculate_gelir_vergisi_dilimleri(150000, 20000)
        beklenen_vergi = round((8000 * 0.15) + (12000 * 0.20), 2)
        self.assertEqual(res2["hesaplanan_gelir_vergisi"], beklenen_vergi)
        self.assertEqual(len(res2["dilim_detaylari"]), 2)

    def test_bordro_ve_asgari_ucret_istisnasi(self):
        brut = 45000.0
        res = calculate_bordro(brut, kumulatif_onceki=0.0)

        self.assertEqual(res["sgk_isci_payi"], 6300.0) # %14
        self.assertEqual(res["issizlik_isci_payi"], 450.0) # %1
        self.assertEqual(res["toplam_sgk_kesintisi"], 6750.0)
        self.assertEqual(res["gelir_vergisi_matrahi"], 38250.0)

        # Asgari ücret vergi istisnası uygulanmalı
        self.assertGreater(res["asgari_ucret_gv_istisnasi"], 0.0)
        self.assertGreater(res["asgari_ucret_dv_istisnasi"], 0.0)
        self.assertLess(res["odenecek_gelir_vergisi"], res["hesaplanan_gelir_vergisi"])
        self.assertLess(res["odenecek_damga_vergisi"], res["hesaplanan_damga_vergisi"])
        self.assertGreater(res["net_ele_gecen_ucret"], 30000.0)

    def test_enflasyon_katsayisi_ve_kiymet_duzeltme(self):
        # Katsayı = 3750 / 2500 = 1.50000
        katsayi = calculate_enflasyon_katsayisi(3750.0, 2500.0)
        self.assertEqual(katsayi, 1.5)

        # Varlık: 1.000.000 TL, Amortisman: 200.000 TL
        res = calculate_kiymet_duzeltme(1000000.0, 3750.0, 2500.0, birikmis_amortisman=200000.0)
        self.assertEqual(res["duzeltilmis_deger"], 1500000.0)
        self.assertEqual(res["varlik_duzeltme_farki"], 500000.0)
        self.assertEqual(res["duzeltilmis_amortisman"], 300000.0)
        self.assertEqual(res["amortisman_duzeltme_farki"], 100000.0)
        self.assertEqual(res["net_698_farki"], 400000.0)

    def test_stok_basit_ortalama(self):
        # Stok: 500.000 TL, Son: 3600, Önceki: 3200 -> Ortalama: 3400 -> Katsayı: 3600/3400 = 1.05882
        res = calculate_stok_basit_ortalama(500000.0, 3600.0, 3200.0)
        self.assertEqual(res["ortalama_endeks"], 3400.0)
        self.assertEqual(res["basit_ortalama_katsayisi"], round(3600.0 / 3400.0, 5))
        self.assertGreater(res["duzeltilmis_stok"], 500000.0)
        self.assertGreater(res["stok_enflasyon_farki"], 0.0)

    def test_698_enflasyon_hesabi_bakiye(self):
        # Aktif fark (Alacak): 1.500.000 TL, Pasif fark (Borç): 1.200.000 TL -> Net KÂR 300.000 TL (648 virman)
        res_kar = calculate_698_enflasyon_hesabi(1500000.0, 1200000.0)
        self.assertEqual(res_kar["sonuc_durum"], "KÂR")
        self.assertEqual(res_kar["enflasyon_kari"], 300000.0)
        self.assertIn("648", res_kar["kapanis_hesabi"])

        # Aktif fark: 800.000 TL, Pasif fark: 1.100.000 TL -> Net ZARAR 300.000 TL (658 virman)
        res_zarar = calculate_698_enflasyon_hesabi(800000.0, 1100000.0)
        self.assertEqual(res_zarar["sonuc_durum"], "ZARAR")
        self.assertEqual(res_zarar["enflasyon_zarari"], 300000.0)
        self.assertIn("658", res_zarar["kapanis_hesabi"])

    def test_ydo(self):
        # 10.000 TL * 0.4393 -> artış 4.393 TL, yeni tutar 14.393 TL
        res = calculate_ydo(10000, 0.4393)
        self.assertEqual(res["eski_tutar"], 10000.0)
        self.assertEqual(res["artis_tutari"], 4393.0)
        self.assertEqual(res["yeni_tutar"], 14393.0)

if __name__ == "__main__":
    print("=" * 60)
    print("  MALİ MÜŞAVİR VE MUHASEBE HESAPLAMA MOTORU TEST SÜİTİ")
    print("=" * 60)
    unittest.main(verbosity=2)

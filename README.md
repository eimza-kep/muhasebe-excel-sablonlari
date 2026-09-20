# Muhasebe ve Mali Müşavirlik Excel Araçları 📊🧾

[![CI - Excel Doğrulama](https://github.com/eimza-kep/muhasebe-excel-sablonlari/actions/workflows/ci.yml/badge.svg)](https://github.com/eimza-kep/muhasebe-excel-sablonlari/actions/workflows/ci.yml)
[![Şablon Sayısı](https://img.shields.io/badge/%C5%9Eablon_Say%C4%B1s%C4%B1-7_Excel_Arac%C4%B1-success.svg)](#-içerik-ve-şablon-listesi)
[![Mevzuat](https://img.shields.io/badge/Mevzuat-2026_Uyumlu-blue.svg)](#)
[![Lisans](https://img.shields.io/badge/Lisans-MIT-orange.svg)](LICENSE)
[![Organizasyon](https://img.shields.io/badge/GitHub-eimza--kep-blue.svg)](https://github.com/eimza-kep)

Mali Müşavirler (SMMM/YMM), muhasebe departmanları ve finans profesyonelleri için Türk Vergi Mevzuatı (VUK, GVK, KDV Kanunu, SGK Kanunu) esas alınarak hazırlanmış **7 adet profesyonel ve formüllü Excel (.xlsx) hesaplama aracı**.

Tüm dosyalar gerçek Excel formülleriyle (`SUM`, `ROUND`, `IF`, `MIN`, `MAX`) çalışır, hücre kilitleri olmadan ihtiyaca göre serbestçe düzenlenebilir.

---

## 📑 İçerik ve Şablon Listesi

| No | Dosya Adı | Açıklama ve Kapsam | İlgili Mevzuat |
| :---: | :--- | :--- | :--- |
| **01** | [`01_e_smm_net_brut_stopaj_kdv_hesaplayici.xlsx`](01_e_smm_net_brut_stopaj_kdv_hesaplayici.xlsx) | Serbest Meslek Makbuzu (e-SMM) için **Brütten Nete** ve **Netten Brüte** simülasyonu. %20 Stopaj ve %20 KDV hesabı. | 509 VUK Tebliği & GVK M.94 |
| **02** | [`02_kdv_tevkifat_hesaplama_ve_beyan_tablosu.xlsx`](02_kdv_tevkifat_hesaplama_ve_beyan_tablosu.xlsx) | Yapım (4/10), Servis (5/10), Danışmanlık (5/10), Temizlik/Güvenlik (9/10) tevkifatlı faturalar ve KDV-2 beyan tutarları. | KDV Genel Uygulama Tebliği |
| **03** | [`03_amortisman_hesaplama_tablosu.xlsx`](03_amortisman_hesaplama_tablosu.xlsx) | Sabit kıymetler ve demirbaşlar için Normal Amortisman itfa planı ve yıllık gider yazılacak amortisman payı. | VUK M.315 & M.320 |
| **04** | [`04_kidem_ve_ihbar_tazminati_hesaplayici.xlsx`](04_kidem_ve_ihbar_tazminati_hesaplayici.xlsx) | Giydirilmiş brüt ücret, yasal tavan sınırlaması, Damga Vergisi (0.00759) ve Gelir Vergisi kesintileriyle net tazminat. | 1475 M.14 & 4857 Sayılı Kanun |
| **05** | [`05_gecici_vergi_ve_gelir_tablosu_kontrol.xlsx`](05_gecici_vergi_ve_gelir_tablosu_kontrol.xlsx) | 1, 2, 3 ve 4. Çeyrek karşılaştırmalı gelir tablosu, KKEG ilavesi ve %25 Kurumlar Geçici Vergi matrah simülasyonu. | KVK M.32 & GVK M.120 |
| **06** | [`06_ba_bs_mutabakat_ve_fatura_eslestirme.xlsx`](06_ba_bs_mutabakat_ve_fatura_eslestirme.xlsx) | Form Ba alış faturaları listesi, 5.000 TL KDV hariç had kontrolü (`=IF(Tutar>=5000,...)`) ve cari mutabakat takibi. | 396 Sıra No.lu VUK Tebliği |
| **07** | [`07_personel_bordro_ve_sgk_maliyet_hesaplayici.xlsx`](07_personel_bordro_ve_sgk_maliyet_hesaplayici.xlsx) | Asgari ücret vergi istisnası, SGK işçi payı (%14), işsizlik (%1), SGK işveren primi (%15.5) ve işverene toplam maliyet. | 5510 Sayılı Kanun & 7349 Sayılı Kanun |

---

## 💡 Öne Çıkan Özellikler

* **Dinamik Formüller:** Hiçbir değer statik metin değildir; parametreleri (brüt ücret, matrah, oran vb.) değiştirdiğinizde tüm tablo otomatik güncellenir.
* **Türkçe Para Formatı:** Tutarlar otomatik olarak `#,##0.00 "TL"` ve oranlar `0.0%` biçimindedir.
* **Koşullu Renklendirme:** 5.000 TL limitini aşan faturalar, tavanı aşan kıdem hesapları ve ödenecek net tutarlar zümrüt yeşili ve lacivert tonlarıyla öne çıkarılmıştır.
* **Sıfır Makro / Tam Güvenlik:** Dosyalarda hiçbir VBA makrosu yoktur; saf `.xlsx` yapısındadır, şirket güvenlik duvarlarına veya virüs tarayıcılarına takılmaz.

---

## 🧪 Test ve Doğrulama

Repodaki tüm tablolar `scripts/test_spreadsheets.py` betiği ile otomatik olarak test edilir:

```bash
pip install openpyxl
python scripts/test_spreadsheets.py
```

---

## 🌐 E-Dönüşüm Ekosistemi

Bu depo, [@eimza-kep](https://github.com/eimza-kep) açık kaynak ekosisteminin bir parçasıdır:
* 📖 [e-donusum-rehberleri](https://github.com/eimza-kep/e-donusum-rehberleri) - Türkiye'nin en kapsamlı 24 e-Dönüşüm rehberi ve tıkla-çalıştır araçları.
* ⚖️ [avukat-hukuk-excel-hesaplamalari](https://github.com/eimza-kep/avukat-hukuk-excel-hesaplamalari) - Avukatlar için AAÜT, icra kapak, faiz ve dava harcı Excel şablonları.
* 🏢 [kobi-finans-yonetim-excel-sablonlari](https://github.com/eimza-kep/kobi-finans-yonetim-excel-sablonlari) - KOBİ'ler için nakit akış, başabaş ve stok takip tabloları.

---

## 📜 Lisans

Bu proje **MIT Lisansı** ile lisanslanmıştır. Ticari veya bireysel olarak serbestçe indirilebilir, kopyalanabilir ve mesleki çalışmalarda kullanılabilir.

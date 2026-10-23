# Muhasebe ve Mali Müşavirlik Excel Araçları 📊🧾

[![CI - Excel Doğrulama](https://github.com/eimza-kep/muhasebe-excel-sablonlari/actions/workflows/ci.yml/badge.svg)](https://github.com/eimza-kep/muhasebe-excel-sablonlari/actions/workflows/ci.yml)
[![Şablon Sayısı](https://img.shields.io/badge/%C5%9Eablon_Say%C4%B1s%C4%B1-8_Excel_Arac%C4%B1-success.svg)](#-içerik-ve-şablon-listesi)
[![Mevzuat](https://img.shields.io/badge/Mevzuat-2026%2F2027_Uyumlu-blue.svg)](#)
[![VUK Geçici 33](https://img.shields.io/badge/Enflasyon_D%C3%BCzeltmesi-VUK_Ge%C3%A7ici_33-blueviolet.svg)](#)
[![GİB Tevkifat](https://img.shields.io/badge/G%C4%B0B_Tevkifat_Kodlar%C4%B1-601--626_Uyumlu-darkgreen.svg)](#)
[![Lisans](https://img.shields.io/badge/Lisans-MIT-orange.svg)](LICENSE)
[![Organizasyon](https://img.shields.io/badge/GitHub-eimza--kep-blue.svg)](https://github.com/eimza-kep)

Mali Müşavirler (SMMM/YMM), muhasebe departmanları ve finans profesyonelleri için Türk Vergi Mevzuatı (VUK, GVK, KDV Kanunu, SGK Kanunu, VUK Geçici 33 Enflasyon Düzeltmesi) esas alınarak hazırlanmış **8 adet profesyonel, formüllü ve parametrik Excel (.xlsx) hesaplama aracı**.

Tüm dosyalar gerçek Excel formülleriyle (`SUM`, `ROUND`, `IF`, `MIN`, `MAX`, `VLOOKUP`) çalışır, hücre kilitleri olmadan ihtiyaca göre serbestçe düzenlenebilir ve VBA makro bağımlılığı içermez.

---

## 📑 İçerik ve Şablon Listesi

| No | Dosya Adı | Açıklama ve Kapsam | İlgili Mevzuat |
| :---: | :--- | :--- | :--- |
| **01** | [`01_e_smm_net_brut_stopaj_kdv_hesaplayici.xlsx`](01_e_smm_net_brut_stopaj_kdv_hesaplayici.xlsx) | Serbest Meslek Makbuzu (e-SMM) için **Brütten Nete** ve **Netten Brüte** simülasyonu. %20 Stopaj ve %20 KDV hesabı. | 509 VUK Tebliği & GVK M.94 |
| **02** | [`02_kdv_tevkifat_hesaplama_ve_beyan_tablosu.xlsx`](02_kdv_tevkifat_hesaplama_ve_beyan_tablosu.xlsx) | **GİB 601-626 Tevkifat Kodları** entegreli; Yapım (4/10), Servis (5/10), Danışmanlık (9/10), Demir-Çelik (4/10) tevkifatlı faturalar ve KDV-2 beyan tutarları. | KDV Genel Uygulama Tebliği |
| **03** | [`03_amortisman_hesaplama_tablosu.xlsx`](03_amortisman_hesaplama_tablosu.xlsx) | Sabit kıymetler ve demirbaşlar için Normal Amortisman itfa planı ve yıllık gider yazılacak amortisman payı. | VUK M.315 & M.320 |
| **04** | [`04_kidem_ve_ihbar_tazminati_hesaplayici.xlsx`](04_kidem_ve_ihbar_tazminati_hesaplayici.xlsx) | Giydirilmiş brüt ücret, yasal tavan sınırlaması, Damga Vergisi (0.00759) ve Gelir Vergisi kesintileriyle net tazminat. | 1475 M.14 & 4857 Sayılı Kanun |
| **05** | [`05_gecici_vergi_ve_gelir_tablosu_kontrol.xlsx`](05_gecici_vergi_ve_gelir_tablosu_kontrol.xlsx) | 1, 2, 3 ve 4. Çeyrek karşılaştırmalı gelir tablosu, KKEG ilavesi ve %25 Kurumlar Geçici Vergi matrah simülasyonu. | KVK M.32 & GVK M.120 |
| **06** | [`06_ba_bs_mutabakat_ve_fatura_eslestirme.xlsx`](06_ba_bs_mutabakat_ve_fatura_eslestirme.xlsx) | Form Ba alış faturaları listesi, 5.000 TL KDV hariç had kontrolü (`=IF(Tutar>=5000,...)`) ve cari mutabakat takibi. | 396 Sıra No.lu VUK Tebliği |
| **07** | [`07_personel_bordro_ve_sgk_maliyet_hesaplayici.xlsx`](07_personel_bordro_ve_sgk_maliyet_hesaplayici.xlsx) | **2026/2027 Gelir Vergisi Dilimleri (%15, %20, %27, %35, %40)** ve **7349 Asgari Ücret Vergi İstisnası**, kümülatif dilim geçiş formülleri ve işveren maliyeti. | 5510 Sayılı Kanun & 7349 Sayılı Kanun |
| **08** | [`08_vuk_gecici_33_enflasyon_duzeltmesi_kontrol_cizelgesi.xlsx`](08_vuk_gecici_33_enflasyon_duzeltmesi_kontrol_cizelgesi.xlsx) | **VUK Geçici 33 Enflasyon Düzeltmesi:** Yİ-ÜFE katsayıları, Duran Varlık & Amortisman Düzeltmesi, Stoklar Basit Ortalama Yöntemi ve **698 Hesap Bakiye (648 Kar / 658 Zarar)** Kontrolü. | VUK Geçici 33 & 555 Sıra No.lu VUK Tebliği |

---

## 🌟 Önemli Mevzuat ve Özellik Açıklamaları

### 1. 2026/2027 Gelir Vergisi Dilimleri & Asgari Ücret İstisnası (Issue #1 Çözümü)
- **GVK 103 Ücret Gelirleri Tarifesi:**
  - 158.000 TL'ye kadar: **%15**
  - 330.000 TL'nin 158.000 TL'si için 23.700 TL, fazlası: **%20**
  - 1.200.000 TL'nin 330.000 TL'si için 58.100 TL, fazlası: **%27**
  - 3.000.000 TL'nin 1.200.000 TL'si için 293.000 TL, fazlası: **%35**
  - 3.000.000 TL'den fazlası: **%40**
- **7349 Sayılı Kanun İstisnası:** Tüm ücretlilerin asgari ücrete isabet eden aylık kümülatif Gelir Vergisi ve Damga Vergisi tutarı net vergiden mahsup edilerek istisna tutulur.

### 2. GİB e-Fatura / e-Arşiv Tevkifat Kodları Tablosu (Issue #2 Çözümü)
- Tabloda GİB tarafından tanımlanan tüm resmi tevkifat kodları (601 Yapım: 4/10, 602 Danışmanlık: 9/10, 608 Tekstil: 7/10, 613 Yük Taşımacılığı: 2/10, 622 Demir-Çelik: 4/10 vb.) yer almaktadır.
- Kodu girdiğinizde tevkifat oranı, işin mahiyeti ve alıcının KDV-2 ile beyan edeceği vergi tutarı otomatik hesaplanır.

### 3. VUK Geçici 33 Enflasyon Düzeltmesi ve 698 Hesap Kontrolü (Issue #4 Çözümü)
- **Düzeltme Katsayısı:** Dönem Sonu Yİ-ÜFE / Düzeltmeye Esas Tarih Yİ-ÜFE.
- **Stoklar Basit Ortalama Yöntemi:** Dönem Sonu Yİ-ÜFE / ((Dönem Sonu Yİ-ÜFE + Bir Önceki Dönem Sonu Yİ-ÜFE) / 2).
- **698 Enflasyon Düzeltme Hesabı Bakiyesi:**
  - Aktif Parasal Olmayan Farklar ➔ 698 Hesabın **ALACAĞINA**
  - Pasif Parasal Olmayan Farklar ➔ 698 Hesabın **BORCUNA**
  - Alacak > Borç ise fark **648 Enflasyon Düzeltmesi Kârları** hesabına, Borç > Alacak ise fark **658 Enflasyon Düzeltmesi Zararları** hesabına virmanlanır.

---

## 💻 Komut Satırı (CLI) Hesaplama Motoru (`calculate_smm.py`)

Terminal veya komut istemcisinden saniyeler içinde parametrik hesaplamalar yapabilirsiniz:

```bash
# 1. e-SMM Brütten Nete Hesaplama
python calculate_smm.py esmm 25000

# 2. e-SMM Netten Brüte Hesaplama
python calculate_smm.py esmm 20000 --net

# 3. GİB Kodu ile KDV Tevkifatı (örn: 601 Yapım İşleri - 4/10)
python calculate_smm.py tevkifat 100000 --kod 601

# 4. GİB Kodu ile KDV Tevkifatı (örn: 608 Tekstil - 7/10, JSON formatında)
python calculate_smm.py tevkifat 80000 --kod 608 --json

# 5. 2026 Personel Bordro Hesabı (Kümülatif GV Dilimi ve İstisna Uygulamalı)
python calculate_smm.py bordro 45000 --kumulatif 120000

# 6. VUK Geçici 33 Maddi Duran Varlık & Amortisman Enflasyon Düzeltmesi
python calculate_smm.py enflasyon 1500000 --son-endeks 3750 --esas-endeks 2500 --amortisman 300000

# 7. VUK Geçici 33 Stoklar Basit Ortalama Enflasyon Düzeltmesi
python calculate_smm.py enflasyon 600000 --son-endeks 3750 --onceki-endeks 3400

# 8. Kıdem Tazminatı ve Damga Vergisi Hesabı
python calculate_smm.py kidem 40000 4.5 --json

# 9. Yeniden Değerleme Oranı (YDO) Artışı
python calculate_smm.py ydo 10000 --oran 0.4393
```

---

## 🚀 Kurulum ve Test Kılavuzu

### Gereksinimler
- Python 3.10 veya üzeri
- `openpyxl` kütüphanesi (Excel okuma/yazma ve doğrulama için)

```bash
# 1. Depoyu klonlayın
git clone https://github.com/eimza-kep/muhasebe-excel-sablonlari.git
cd muhasebe-excel-sablonlari

# 2. Gerekli kütüphaneyi kurun
pip install openpyxl

# 3. Muhasebe hesaplama motoru birim testlerini çalıştırın
python test_calculate.py

# 4. Tüm 8 Excel tablosunun formül ve yapı doğrulamalarını yapın
python scripts/test_spreadsheets.py
```

---

## 🌐 E-Dönüşüm Açık Kaynak Ekosistemi

Bu depo, [@eimza-kep](https://github.com/eimza-kep) açık kaynak ekosisteminin muhasebe ve finans bileşenidir. İlgili diğer araçlar:

* 📄 [e-fatura-xml-goruntuleyici](https://github.com/eimza-kep/e-fatura-xml-goruntuleyici) - UBL-TR e-Fatura ve e-İrsaliye XML dosyalarını ayrıştırma ve KDV dökümü aracı.
* 📊 [muhasebe-mukellef-evrak-scripti](https://github.com/eimza-kep/muhasebe-mukellef-evrak-scripti) - Mükellef aylık evrak toplama, e-fatura ayrıştırma ve WhatsApp bildirim portalı.
* 📑 [gib-edefter-berat-xml-dogrulayici](https://github.com/eimza-kep/gib-edefter-berat-xml-dogrulayici) - GİB e-Defter ve berat XML dosyaları hash ve şema doğrulayıcı.
* 📋 [smmm-stok-sayim-tutanak-scripti](https://github.com/eimza-kep/smmm-stok-sayim-tutanak-scripti) - Yıl sonu ve dönemlik fiili stok sayım tutanağı hazırlayıcı.
* 🏢 [kobi-finans-yonetim-excel-sablonlari](https://github.com/eimza-kep/kobi-finans-yonetim-excel-sablonlari) - KOBİ'ler için nakit akış, başabaş ve stok takip tabloları.
* ⚖️ [avukat-hukuk-excel-hesaplamalari](https://github.com/eimza-kep/avukat-hukuk-excel-hesaplamalari) - Avukatlar ve hukuk büroları için arabuluculuk, serbest meslek ve icra faiz araçları.
* 🌟 [awesome-turkiye-e-donusum](https://github.com/eimza-kep/awesome-turkiye-e-donusum) - Türkiye e-Dönüşüm açık kaynak araçları ve kütüphaneleri kürasyonu.

---

## 📜 Lisans

Bu proje **MIT Lisansı** ile lisanslanmıştır. Ticari veya bireysel olarak serbestçe indirilebilir, kopyalanabilir ve mesleki çalışmalarda kullanılabilir.

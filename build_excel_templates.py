# -*- coding: utf-8 -*-
"""
build_excel_templates.py
------------------------
02_kdv_tevkifat_hesaplama_ve_beyan_tablosu.xlsx
07_personel_bordro_ve_sgk_maliyet_hesaplayici.xlsx
08_vuk_gecici_33_enflasyon_duzeltmesi_kontrol_cizelgesi.xlsx
şablonlarını openpyxl ile profesyonel kurumsal formatta üretir.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

NAVY = "1E3A8A"
NAVY_LIGHT = "EFF6FF"
GREEN = "065F46"
GREEN_LIGHT = "ECFDF5"
SLATE = "334155"
GRAY_LIGHT = "F8FAFC"
BORDER_COLOR = "CBD5E1"

font_title = Font(name="Segoe UI", size=13, bold=True, color="FFFFFF")
font_subtitle = Font(name="Segoe UI", size=9, italic=True, color="E2E8F0")
font_header = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
font_subtotal = Font(name="Segoe UI", size=10, bold=True, color="0F172A")
font_data = Font(name="Segoe UI", size=9.5, color="0F172A")
font_bold = Font(name="Segoe UI", size=9.5, bold=True, color="0F172A")
font_success = Font(name="Segoe UI", size=9.5, bold=True, color="16A34A")

thin_side = Side(border_style="thin", color=BORDER_COLOR)
border_box = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
border_total = Border(top=Side(border_style="thin", color="0F172A"), bottom=Side(border_style="double", color="0F172A"))

def style_row(ws, row_idx, bg_color, max_col, font=font_header, align="center"):
    fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    for col in range(1, max_col + 1):
        cell = ws.cell(row=row_idx, column=col)
        cell.font = font
        cell.fill = fill
        cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=True)
        cell.border = border_box

def auto_fit_columns(ws, min_col=1, max_col=None):
    if max_col is None:
        max_col = ws.max_column
    for col in range(min_col, max_col + 1):
        max_len = 0
        col_letter = get_column_letter(col)
        for row in range(1, ws.max_row + 1):
            val = ws.cell(row=row, column=col).value
            if val:
                sval = str(val)
                if not sval.startswith("="):
                    max_len = max(max_len, len(sval))
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

# ==============================================================================
# 1. 02_kdv_tevkifat_hesaplama_ve_beyan_tablosu.xlsx
# ==============================================================================
def create_02_tevkifat():
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "KDV Tevkifat Listesi"

    # Başlık
    ws1.merge_cells("A1:K1")
    ws1["A1"] = "GİB E-FATURA & E-ARŞİV KDV TEVKİFAT HESAPLAMA VE BEYAN ÇİZELGESİ"
    ws1.merge_cells("A2:K2")
    ws1["A2"] = "GİB 601-626 Tevkifat Kodları, KDV-2 Alıcı Beyanı ve Fatura Eşleştirme Motoru"
    style_row(ws1, 1, NAVY, 11, font_title)
    style_row(ws1, 2, "2563EB", 11, font_subtitle)
    ws1.row_dimensions[1].height = 25
    ws1.row_dimensions[2].height = 18

    headers = [
        "Sıra", "Fatura No", "Tarih", "Alıcı / Mükellef Unvanı",
        "GİB Kodu", "Tevkifat Kapsamı / İş Türü", "Tevkifat Oranı",
        "Matrah (TL)", "Hesaplanan KDV (%20)", "Tevkif Edilen KDV", "Tahsil Edilen KDV", "Fatura Toplamı"
    ]
    ws1.row_dimensions[3].height = 28
    for col_idx, h in enumerate(headers, 1):
        c = ws1.cell(row=3, column=col_idx, value=h)
        c.font = font_header
        c.fill = PatternFill(start_color=SLATE, end_color=SLATE, fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border_box

    data = [
        (1, "FTR2026001", "2026-03-05", "Anadolu Yapı Yatırım A.Ş.", "601", "Yapım İşleri ve Mimarlık-Mühendislik", 0.40, 250000),
        (2, "FTR2026002", "2026-03-08", "Marmara Uluslararası Lojistik Ltd.", "613", "Yük Taşımacılığı Hizmeti", 0.20, 85000),
        (3, "FTR2026003", "2026-03-12", "Boğaziçi Denetim ve Danışmanlık A.Ş.", "602", "Danışmanlık ve Denetim Hizmetleri", 0.90, 120000),
        (4, "FTR2026004", "2026-03-15", "Ege Çelik Endüstrisi Sanayi Ltd.", "622", "Demir-Çelik Ürünlerinin Teslimi", 0.40, 400000),
        (5, "FTR2026005", "2026-03-20", "Akdeniz Tekstil Konfeksiyon A.Ş.", "608", "Fason Tekstil ve Konfeksiyon İşleri", 0.70, 95000),
        (6, "FTR2026006", "2026-03-25", "Yıldız Özel Güvenlik ve Koruma Ltd.", "606", "Özel Güvenlik Hizmeti", 0.90, 70000)
    ]

    for r_idx, row in enumerate(data, 4):
        ws1.row_dimensions[r_idx].height = 20
        ws1.cell(row=r_idx, column=1, value=row[0]).alignment = Alignment(horizontal="center")
        ws1.cell(row=r_idx, column=2, value=row[1]).alignment = Alignment(horizontal="center")
        ws1.cell(row=r_idx, column=3, value=row[2]).alignment = Alignment(horizontal="center")
        ws1.cell(row=r_idx, column=4, value=row[3])
        ws1.cell(row=r_idx, column=5, value=row[4]).alignment = Alignment(horizontal="center")
        ws1.cell(row=r_idx, column=6, value=row[5])
        
        c_oran = ws1.cell(row=r_idx, column=7, value=row[6])
        c_oran.number_format = "0.0%"
        c_oran.alignment = Alignment(horizontal="center")

        c_matrah = ws1.cell(row=r_idx, column=8, value=row[7])
        c_matrah.number_format = "#,##0.00"

        c_kdv = ws1.cell(row=r_idx, column=9, value=f"=H{r_idx}*0.20")
        c_kdv.number_format = "#,##0.00"

        c_tevkif = ws1.cell(row=r_idx, column=10, value=f"=I{r_idx}*G{r_idx}")
        c_tevkif.number_format = "#,##0.00"

        c_tahsil = ws1.cell(row=r_idx, column=11, value=f"=I{r_idx}-J{r_idx}")
        c_tahsil.number_format = "#,##0.00"

        c_toplam = ws1.cell(row=r_idx, column=12, value=f"=H{r_idx}+K{r_idx}")
        c_toplam.number_format = "#,##0.00"

        for col in range(1, 13):
            cell = ws1.cell(row=r_idx, column=col)
            cell.font = font_data
            cell.border = border_box

    # Toplam Satırı
    tot_row = len(data) + 4
    ws1.row_dimensions[tot_row].height = 24
    ws1.cell(row=tot_row, column=4, value="GENEL TOPLAMLAR").font = font_subtotal
    ws1.cell(row=tot_row, column=8, value=f"=SUM(H4:H{tot_row-1})").number_format = "#,##0.00"
    ws1.cell(row=tot_row, column=9, value=f"=SUM(I4:I{tot_row-1})").number_format = "#,##0.00"
    ws1.cell(row=tot_row, column=10, value=f"=SUM(J4:J{tot_row-1})").number_format = "#,##0.00"
    ws1.cell(row=tot_row, column=11, value=f"=SUM(K4:K{tot_row-1})").number_format = "#,##0.00"
    ws1.cell(row=tot_row, column=12, value=f"=SUM(L4:L{tot_row-1})").number_format = "#,##0.00"

    for col in range(1, 13):
        c = ws1.cell(row=tot_row, column=col)
        c.font = font_subtotal
        c.border = border_total
        c.fill = PatternFill(start_color=NAVY_LIGHT, end_color=NAVY_LIGHT, fill_type="solid")

    auto_fit_columns(ws1, 1, 12)

    # 2. Sayfa: GİB Tevkifat Kodları Sözlüğü
    ws2 = wb.create_sheet(title="GİB Tevkifat Kodları")
    ws2.merge_cells("A1:E1")
    ws2["A1"] = "GELİR İDARESİ BAŞKANLIĞI (GİB) KDV TEVKİFAT KODLARI LİSTESİ"
    style_row(ws2, 1, NAVY, 5, font_title)

    tev_headers = ["GİB Kodu", "İşlem Türü / Hizmet Adı", "Tevkifat Oranı (Metin)", "Tevkifat Oranı (Ondalık)", "Açıklama & Yasal Dayanak"]
    ws2.row_dimensions[2].height = 25
    for c_idx, th in enumerate(tev_headers, 1):
        c = ws2.cell(row=2, column=c_idx, value=th)
        c.font = font_header
        c.fill = PatternFill(start_color=SLATE, end_color=SLATE, fill_type="solid")
        c.border = border_box
        c.alignment = Alignment(horizontal="center", vertical="center")

    from calculate_smm import GIB_TEVKIFAT_KODLARI
    for r_idx, (kod, val) in enumerate(GIB_TEVKIFAT_KODLARI.items(), 3):
        ws2.row_dimensions[r_idx].height = 19
        ws2.cell(row=r_idx, column=1, value=kod).alignment = Alignment(horizontal="center")
        ws2.cell(row=r_idx, column=2, value=val["ad"])
        ws2.cell(row=r_idx, column=3, value=val["oran_str"]).alignment = Alignment(horizontal="center")
        c_dec = ws2.cell(row=r_idx, column=4, value=round(val["pay"] / val["payda"], 2))
        c_dec.number_format = "0.0%"
        c_dec.alignment = Alignment(horizontal="center")
        ws2.cell(row=r_idx, column=5, value=val["aciklama"])

        for col in range(1, 6):
            cell = ws2.cell(row=r_idx, column=col)
            cell.font = font_data
            cell.border = border_box

    auto_fit_columns(ws2, 1, 5)
    wb.save("02_kdv_tevkifat_hesaplama_ve_beyan_tablosu.xlsx")
    print("✓ 02_kdv_tevkifat_hesaplama_ve_beyan_tablosu.xlsx başarıyla güncellendi.")

# ==============================================================================
# 2. 07_personel_bordro_ve_sgk_maliyet_hesaplayici.xlsx
# ==============================================================================
def create_07_bordro():
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "Bordro ve SGK Maliyeti"

    # Başlık
    ws1.merge_cells("A1:D1")
    ws1["A1"] = "2026 PERSONEL BORDRO, VERGİ DİLİMLERİ VE SGK İŞVEREN MALİYET HESAPLAYICI"
    ws1.merge_cells("A2:D2")
    ws1["A2"] = "7349 Sayılı Kanun Asgari Ücret Vergi İstisnası ve Kümülatif Matrah Dilim Takibi"
    style_row(ws1, 1, GREEN, 4, font_title)
    style_row(ws1, 2, "047857", 4, font_subtitle)

    headers = ["Bordro Kalemi", "Tutar (TL)", "Oran / Formül", "Yasal Dayanak & Açıklama"]
    ws1.row_dimensions[3].height = 25
    for c_idx, h in enumerate(headers, 1):
        c = ws1.cell(row=3, column=c_idx, value=h)
        c.font = font_header
        c.fill = PatternFill(start_color=SLATE, end_color=SLATE, fill_type="solid")
        c.border = border_box
        c.alignment = Alignment(horizontal="center", vertical="center")

    rows = [
        ("Aylık Brüt Ücret", 45000.0, "Anlaşılan Brüt Ücret", "İş Sözleşmesi"),
        ("SGK İşçi Payı Kesintisi (%14)", "=B4*0.14", "%14", "5510 Sayılı Kanun Madde 81"),
        ("İşsizlik Sigortası İşçi Payı (%1)", "=B4*0.01", "%1", "4447 Sayılı Kanun"),
        ("Toplam SGK Kesintisi (İşçi)", "=B5+B6", "%15 İşçi Yasal Kesintisi", "5510 & 4447"),
        ("Gelir Vergisi Matrahı (Aylık)", "=B4-B7", "Brüt Ücret - SGK Kesintileri", "GVK Madde 63"),
        ("Önceki Aylardan Devreden Kümülatif Matrah", 120000.0, "Yıl İçi Toplam Matrah", "GVK Madde 103"),
        ("Yeni Kümülatif Gelir Vergisi Matrahı", "=B8+B9", "Dilim Geçiş Kontrolü", "GVK Madde 103"),
        ("Hesaplanan Gelir Vergisi (Dilimli)", "=B8*0.20", "%20 İkinci Dilim (Tarifeden)", "GVK Madde 103"),
        ("Asgari Ücret Gelir Vergisi İstisnası", 3315.70, "Aylık İstisna Tutarı", "7349 Sayılı Kanun (GV İstisnası)"),
        ("Ödenecek Gelir Vergisi", "=MAX(0, B11-B12)", "Hesaplanan GV - İstisna", "Net Vergi Borcu"),
        ("Hesaplanan Damga Vergisi (Binde 7.59)", "=B4*0.00759", "Binde 7.59", "Damga Vergisi Kanunu"),
        ("Asgari Ücret Damga Vergisi İstisnası", 197.38, "Damga Vergisi İstisnası", "7349 Sayılı Kanun (DV İstisnası)"),
        ("Ödenecek Damga Vergisi", "=MAX(0, B14-B15)", "Hesaplanan DV - İstisna", "Net Damga Vergisi"),
        ("Toplam Yasal Kesintiler", "=B7+B13+B16", "SGK + GV + DV", "Toplam İşçi Kesintisi"),
        ("NET ELE GEÇEN AYLIK ÜCRET", "=B4-B17", "Brüt Ücret - Toplam Kesintiler", "Çalışana Ödenecek Net Tutar"),
        ("SGK İşveren Payı (%20.5)", "=B4*0.205", "%20.5 (Teşviksiz)", "5510 Sayılı Kanun Madde 81"),
        ("İşsizlik Sigortası İşveren Payı (%2)", "=B4*0.02", "%2 İşveren Payı", "4447 Sayılı Kanun"),
        ("TOPLAM İŞVEREN MALİYETİ", "=B4+B19+B20", "Brüt Ücret + İşveren SGK Payları", "Aylık Şirket Maliyeti")
    ]

    for idx, (kalem, tutar, oran, dayanak) in enumerate(rows, 4):
        ws1.row_dimensions[idx].height = 20
        c1 = ws1.cell(row=idx, column=1, value=kalem)
        c2 = ws1.cell(row=idx, column=2, value=tutar)
        c3 = ws1.cell(row=idx, column=3, value=oran)
        c4 = ws1.cell(row=idx, column=4, value=dayanak)

        c1.font = font_bold if "NET" in kalem or "TOPLAM" in kalem else font_data
        c2.font = font_bold if "NET" in kalem or "TOPLAM" in kalem else font_data
        c3.font = font_data
        c4.font = font_data

        if isinstance(tutar, (int, float)) or (isinstance(tutar, str) and tutar.startswith("=")):
            c2.number_format = "#,##0.00"

        if "NET ELE GEÇEN" in kalem:
            for col in range(1, 5):
                ws1.cell(row=idx, column=col).fill = PatternFill(start_color=GREEN_LIGHT, end_color=GREEN_LIGHT, fill_type="solid")
                ws1.cell(row=idx, column=col).border = border_total
        elif "TOPLAM İŞVEREN" in kalem:
            for col in range(1, 5):
                ws1.cell(row=idx, column=col).fill = PatternFill(start_color=NAVY_LIGHT, end_color=NAVY_LIGHT, fill_type="solid")
                ws1.cell(row=idx, column=col).border = border_total
        else:
            for col in range(1, 5):
                ws1.cell(row=idx, column=col).border = border_box

    auto_fit_columns(ws1, 1, 4)

    # 2. Sayfa: Gelir Vergisi Dilimleri 2026 Parametreleri
    ws2 = wb.create_sheet(title="Vergi Dilimleri & Parametreler")
    ws2.merge_cells("A1:E1")
    ws2["A1"] = "GİB 2026/2027 GELİR VERGİSİ DİLİMLERİ VE ASGARİ ÜCRET PARAMETRELERİ"
    style_row(ws2, 1, GREEN, 5, font_title)

    p_headers = ["Dilim No", "Kümülatif Matrah Alt Sınır (TL)", "Kümülatif Matrah Üst Sınır (TL)", "Vergi Oranı", "Sabit Vergi Tutarı (TL)"]
    ws2.row_dimensions[2].height = 25
    for c_idx, ph in enumerate(p_headers, 1):
        c = ws2.cell(row=2, column=c_idx, value=ph)
        c.font = font_header
        c.fill = PatternFill(start_color=SLATE, end_color=SLATE, fill_type="solid")
        c.border = border_box
        c.alignment = Alignment(horizontal="center", vertical="center")

    dilimler = [
        ("1. Dilim", 0, 158000, 0.15, 0),
        ("2. Dilim", 158000, 330000, 0.20, 23700),
        ("3. Dilim (Ücret)", 330000, 1200000, 0.27, 58100),
        ("4. Dilim", 1200000, 3000000, 0.35, 293000),
        ("5. Dilim", 3000000, 99999999, 0.40, 923000)
    ]

    for r_idx, d in enumerate(dilimler, 3):
        ws2.row_dimensions[r_idx].height = 20
        ws2.cell(row=r_idx, column=1, value=d[0]).alignment = Alignment(horizontal="center")
        ws2.cell(row=r_idx, column=2, value=d[1]).number_format = "#,##0.00"
        ws2.cell(row=r_idx, column=3, value=d[2]).number_format = "#,##0.00"
        c_oran = ws2.cell(row=r_idx, column=4, value=d[3])
        c_oran.number_format = "0%"
        c_oran.alignment = Alignment(horizontal="center")
        ws2.cell(row=r_idx, column=5, value=d[4]).number_format = "#,##0.00"

        for col in range(1, 6):
            ws2.cell(row=r_idx, column=col).border = border_box
            ws2.cell(row=r_idx, column=col).font = font_data

    auto_fit_columns(ws2, 1, 5)
    wb.save("07_personel_bordro_ve_sgk_maliyet_hesaplayici.xlsx")
    print("✓ 07_personel_bordro_ve_sgk_maliyet_hesaplayici.xlsx başarıyla güncellendi.")

# ==============================================================================
# 3. 08_vuk_gecici_33_enflasyon_duzeltmesi_kontrol_cizelgesi.xlsx
# ==============================================================================
def create_08_enflasyon():
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "698 Enflasyon Hesabı Kontrol"

    # Başlık
    ws1.merge_cells("A1:E1")
    ws1["A1"] = "VUK GEÇİCİ 33 ENFLASYON DÜZELTMESİ & 698 HESAP BAKİYE KONTROLÜ"
    ws1.merge_cells("A2:E2")
    ws1["A2"] = "Maddi Duran Varlıklar, Stoklar, Özkaynaklar ve 648/658 Virman Kontrol Çizelgesi"
    style_row(ws1, 1, NAVY, 5, font_title)
    style_row(ws1, 2, "1D4ED8", 5, font_subtitle)

    headers = ["Hesap Kodu & Bakiye Kalemi", "Aktif / Pasif Yönü", "698 Kayıt Yönü", "Düzeltme Farkı Tutarı (TL)", "Açıklama"]
    ws1.row_dimensions[3].height = 25
    for c_idx, h in enumerate(headers, 1):
        c = ws1.cell(row=3, column=c_idx, value=h)
        c.font = font_header
        c.fill = PatternFill(start_color=SLATE, end_color=SLATE, fill_type="solid")
        c.border = border_box
        c.alignment = Alignment(horizontal="center", vertical="center")

    rows = [
        ("25 Maddi Duran Varlıklar Enflasyon Farkları", "Aktif Parasal Olmayan", "ALACAK (Gelir)", 1450000.0, "250, 252, 254, 255 binalar ve makineler"),
        ("257 Birikmiş Amortismanlar Enflasyon Farkları (-)", "Aktifi Düzenleyici Pasif", "BORÇ (Gider)", 420000.0, "Duran varlık amortisman taşıma farkı"),
        ("150-153 Stoklar Enflasyon Düzeltme Farkları", "Aktif Parasal Olmayan", "ALACAK (Gelir)", 680000.0, "Basit ortalama / hareketli ortalama farkı"),
        ("500 Ödenmiş Sermaye Düzeltme Farkları (502)", "Pasif Parasal Olmayan", "BORÇ (Gider)", 1200000.0, "Sermayenin tescil tarihinden itibaren taşınması"),
        ("540 Yasal Yedekler Enflasyon Farkları (549)", "Pasif Parasal Olmayan", "BORÇ (Gider)", 180000.0, "Ayrılan yasal yedek akçelerin düzeltmesi")
    ]

    for idx, (kalem, yon, kayit, tutar, aciklama) in enumerate(rows, 4):
        ws1.row_dimensions[idx].height = 20
        ws1.cell(row=idx, column=1, value=kalem).font = font_bold
        ws1.cell(row=idx, column=2, value=yon).alignment = Alignment(horizontal="center")
        ws1.cell(row=idx, column=3, value=kayit).alignment = Alignment(horizontal="center")
        c_tut = ws1.cell(row=idx, column=4, value=tutar)
        c_tut.number_format = "#,##0.00"
        c_tut.font = font_data
        ws1.cell(row=idx, column=5, value=aciklama).font = font_data

        for col in range(1, 6):
            ws1.cell(row=idx, column=col).border = border_box

    # 698 Bakiye Kontrolü
    ws1.cell(row=10, column=1, value="698 HESAP ALACAK TOPLAMI (Aktif Gelir Farkları)").font = font_bold
    ws1.cell(row=10, column=4, value="=D4+D6").number_format = "#,##0.00"

    ws1.cell(row=11, column=1, value="698 HESAP BORÇ TOPLAMI (Pasif Gider Farkları)").font = font_bold
    ws1.cell(row=11, column=4, value="=D5+D7+D8").number_format = "#,##0.00"

    ws1.cell(row=12, column=1, value="698 HESAP NET BAKİYESİ").font = font_subtotal
    ws1.cell(row=12, column=4, value="=D10-D11").number_format = "#,##0.00"

    ws1.cell(row=13, column=1, value="SONUÇ VE VİRMAN HESABI").font = font_subtotal
    ws1.cell(row=13, column=4, value='=IF(D12>0, "648 Enflasyon Düzeltme Kârı (Gelir)", IF(D12<0, "658 Enflasyon Düzeltme Zararı (Gider)", "DENK"))').font = font_success

    for r in range(10, 14):
        ws1.row_dimensions[r].height = 22
        for col in range(1, 6):
            ws1.cell(row=r, column=col).border = border_total if r >= 12 else border_box
            ws1.cell(row=r, column=col).fill = PatternFill(start_color=NAVY_LIGHT, end_color=NAVY_LIGHT, fill_type="solid")

    auto_fit_columns(ws1, 1, 5)

    # 2. Sayfa: Duran Varlıklar & Amortisman Düzeltmesi
    ws2 = wb.create_sheet(title="Duran Varlıklar Düzeltmesi")
    ws2.merge_cells("A1:K1")
    ws2["A1"] = "25 MADDİ DURAN VARLIKLAR VE BİRİKMİŞ AMORTİSMAN DÜZELTME TABLOSU"
    style_row(ws2, 1, NAVY, 11, font_title)

    dv_headers = [
        "Hesap Kodu", "Kıymet Adı / Açıklama", "Aktife Giriş Tarihi",
        "Tarihi Maliyet (TL)", "Giriş Yİ-ÜFE", "Dönem Sonu Yİ-ÜFE", "Düzeltme Katsayısı",
        "Düzeltilmiş Varlık Değeri", "Varlık Enflasyon Farkı", "Tarihi Amortisman", "Düzeltilmiş Amortisman", "Net Fark (698)"
    ]
    ws2.row_dimensions[2].height = 26
    for c_idx, h in enumerate(dv_headers, 1):
        c = ws2.cell(row=2, column=c_idx, value=h)
        c.font = font_header
        c.fill = PatternFill(start_color=SLATE, end_color=SLATE, fill_type="solid")
        c.border = border_box
        c.alignment = Alignment(horizontal="center", vertical="center")

    duran_varliklar = [
        ("252.01", "İdare Merkez Binası", "2023-06-15", 3500000, 2322.0, 3750.0, 350000),
        ("254.01", "Ticari Taşıt (Kamyonet)", "2023-11-20", 1200000, 2882.0, 3750.0, 240000),
        ("255.01", "Fabrika Üretim Makinesi", "2024-03-10", 2800000, 3140.0, 3750.0, 560000)
    ]

    for idx, (kod, ad, tar, tut, e_gir, e_son, amort) in enumerate(duran_varliklar, 3):
        ws2.row_dimensions[idx].height = 20
        ws2.cell(row=idx, column=1, value=kod).alignment = Alignment(horizontal="center")
        ws2.cell(row=idx, column=2, value=ad)
        ws2.cell(row=idx, column=3, value=tar).alignment = Alignment(horizontal="center")
        ws2.cell(row=idx, column=4, value=tut).number_format = "#,##0.00"
        ws2.cell(row=idx, column=5, value=e_gir).number_format = "#,##0.00"
        ws2.cell(row=idx, column=6, value=e_son).number_format = "#,##0.00"

        c_kat = ws2.cell(row=idx, column=7, value=f"=F{idx}/E{idx}")
        c_kat.number_format = "0.00000"
        c_kat.alignment = Alignment(horizontal="center")

        ws2.cell(row=idx, column=8, value=f"=D{idx}*G{idx}").number_format = "#,##0.00"
        ws2.cell(row=idx, column=9, value=f"=H{idx}-D{idx}").number_format = "#,##0.00"
        ws2.cell(row=idx, column=10, value=amort).number_format = "#,##0.00"
        ws2.cell(row=idx, column=11, value=f"=J{idx}*G{idx}").number_format = "#,##0.00"
        ws2.cell(row=idx, column=12, value=f"=I{idx}-(K{idx}-J{idx})").number_format = "#,##0.00"

        for col in range(1, 13):
            ws2.cell(row=idx, column=col).border = border_box
            ws2.cell(row=idx, column=col).font = font_data

    # Toplam
    t_row = len(duran_varliklar) + 3
    ws2.row_dimensions[t_row].height = 24
    ws2.cell(row=t_row, column=2, value="TOPLAMLAR").font = font_subtotal
    ws2.cell(row=t_row, column=4, value=f"=SUM(D3:D{t_row-1})").number_format = "#,##0.00"
    ws2.cell(row=t_row, column=8, value=f"=SUM(H3:H{t_row-1})").number_format = "#,##0.00"
    ws2.cell(row=t_row, column=9, value=f"=SUM(I3:I{t_row-1})").number_format = "#,##0.00"
    ws2.cell(row=t_row, column=12, value=f"=SUM(L3:L{t_row-1})").number_format = "#,##0.00"

    for col in range(1, 13):
        c = ws2.cell(row=t_row, column=col)
        c.font = font_subtotal
        c.border = border_total
        c.fill = PatternFill(start_color=NAVY_LIGHT, end_color=NAVY_LIGHT, fill_type="solid")

    auto_fit_columns(ws2, 1, 12)

    # 3. Sayfa: Stoklar Basit Ortalama Yöntemi
    ws3 = wb.create_sheet(title="Stoklar Basit Ortalama")
    ws3.merge_cells("A1:D1")
    ws3["A1"] = "VUK GEÇİCİ 33 STOKLAR BASİT ORTALAMA ENFLASYON DÜZELTMESİ"
    style_row(ws3, 1, NAVY, 4, font_title)

    stok_rows = [
        ("Dönem Sonu Ticari Mallar / Stok Tutarı (TL)", 1850000.0, "153 Ticari Mallar Defter Değeri"),
        ("Dönem Sonu Yİ-ÜFE Endeksi (Aralık)", 3750.0, "Cari Dönem Sonu Endeksi"),
        ("Bir Önceki Dönem Sonu Yİ-ÜFE Endeksi (Eylül)", 3420.0, "Önceki Geçici Vergi / Yıl Sonu"),
        ("Ortalama Yİ-ÜFE Endeksi", "=(B2+B3)/2", "Basit Aritmetik Ortalama"),
        ("Basit Ortalama Düzeltme Katsayısı", "=B2/B4", "Son Endeks / Ortalama Endeks"),
        ("Düzeltilmiş Stok Değeri (TL)", "=B1*B5", "Stok Tutarı * Katsayı"),
        ("698 Stok Enflasyon Düzeltme Farkı (TL)", "=B6-B1", "698 Hesabın Alacağına Kaydedilecek Tutar")
    ]

    for idx, (label, val, acik) in enumerate(stok_rows, 2):
        ws3.row_dimensions[idx].height = 22
        c1 = ws3.cell(row=idx, column=1, value=label)
        c2 = ws3.cell(row=idx, column=2, value=val)
        c3 = ws3.cell(row=idx, column=3, value=acik)

        c1.font = font_bold if "Düzeltilmiş" in label or "698" in label else font_data
        c2.font = font_bold if "Düzeltilmiş" in label or "698" in label else font_data
        c3.font = font_data

        if isinstance(val, (int, float)) or (isinstance(val, str) and val.startswith("=")):
            c2.number_format = "0.00000" if "Katsayı" in label else "#,##0.00"

        for col in range(1, 4):
            ws3.cell(row=idx, column=col).border = border_total if "698" in label else border_box

    auto_fit_columns(ws3, 1, 3)

    wb.save("08_vuk_gecici_33_enflasyon_duzeltmesi_kontrol_cizelgesi.xlsx")
    print("✓ 08_vuk_gecici_33_enflasyon_duzeltmesi_kontrol_cizelgesi.xlsx başarıyla üretildi.")

if __name__ == "__main__":
    create_02_tevkifat()
    create_07_bordro()
    create_08_enflasyon()

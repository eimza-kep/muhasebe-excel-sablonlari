#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mali Müşavir ve Muhasebe Hesaplama CLI Motoru
e-SMM Net/Brüt/Stopaj/KDV, KDV Tevkifatı ve Kıdem Tazminatı Hesaplayıcı.
"""

import sys
import json

# Force UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def calculate_esmm_from_brut(brut_tutar: float, stopaj_orani: float = 0.20, kdv_orani: float = 0.20) -> dict:
    """
    Brütten Nete e-SMM (Serbest Meslek Makbuzu) Hesabı:
    - Brüt Ücret
    - GV Stopajı = Brüt * Stopaj Oranı (Varsayılan %20)
    - KDV = Brüt * KDV Oranı (Varsayılan %20)
    - Net Alınan = Brüt - Stopaj
    - Tahsil Edilen Toplam = Net Alınan + KDV
    """
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
    """
    Netten Brüte e-SMM Hesabı:
    - Brüt = Net / (1 - Stopaj Oranı)
    """
    net = float(net_tutar)
    brut = net / (1.0 - stopaj_orani)
    return calculate_esmm_from_brut(brut, stopaj_orani, kdv_orani)

def calculate_kdv_tevkifat(matrah: float, kdv_orani: float = 0.20, tevkifat_pay: int = 5, tevkifat_payda: int = 10) -> dict:
    """
    KDV Tevkifatı Hesaplama:
    - Matrah
    - Hesaplanan KDV = Matrah * KDV Oranı
    - Tevkif Edilen KDV = Hesaplanan KDV * (Pay / Payda)
    - Tahsil Edilen KDV = Hesaplanan KDV - Tevkif Edilen KDV
    - Fatura Toplam Tutarı = Matrah + Tahsil Edilen KDV
    - Alıcının KDV-2 ile Beyan Edeceği Tutar = Tevkif Edilen KDV
    """
    matrah = float(matrah)
    oran = float(kdv_orani)
    hesaplanan_kdv = matrah * oran
    oran_tevkifat = float(tevkifat_pay) / float(tevkifat_payda)
    tevkif_edilen = hesaplanan_kdv * oran_tevkifat
    tahsil_edilen_kdv = hesaplanan_kdv - tevkif_edilen
    fatura_toplam = matrah + tahsil_edilen_kdv

    return {
        "matrah": round(matrah, 2),
        "kdv_orani": oran,
        "hesaplanan_kdv": round(hesaplanan_kdv, 2),
        "tevkifat_orani_str": f"{tevkifat_pay}/{tevkifat_payda}",
        "tevkif_edilen_kdv": round(tevkif_edilen, 2),
        "tahsil_edilen_kdv": round(tahsil_edilen_kdv, 2),
        "fatura_toplam": round(fatura_toplam, 2),
        "kdv2_beyan_tutari": round(tevkif_edilen, 2)
    }

def calculate_kidem_tazminati(brut_ucret: float, yil: float, kidem_tavani: float = 46500.0) -> dict:
    """
    Kıdem Tazminatı Hesabı:
    - Giydirilmiş Brüt Ücret (Kıdem Tavanı ile sınırlandırılır)
    - Brüt Kıdem = Uygulanan Brüt * Yıl
    - Damga Vergisi = Brüt Kıdem * 0.00759 (Binde 7.59)
    - Net Kıdem = Brüt Kıdem - Damga Vergisi
    """
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

def main():
    import argparse
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--json", action="store_true", help="Çıktıyı JSON formatında ver")
    parent_parser.add_argument("--markdown", action="store_true", help="Çıktıyı Markdown tablosu formatında ver")

    parser = argparse.ArgumentParser(description="Mali Müşavir ve Muhasebe Hesaplama Motoru (CLI)", parents=[parent_parser])
    subparsers = parser.add_subparsers(dest="command", required=True)

    # e-SMM
    p_smm = subparsers.add_parser("esmm", help="e-SMM Makbuz Hesaplayıcı", parents=[parent_parser])
    p_smm.add_argument("tutar", type=float, help="Tutar (TL)")
    p_smm.add_argument("--net", action="store_true", help="Girilen tutarı net kabul et (Varsayılan: brüt)")
    p_smm.add_argument("--stopaj", type=float, default=0.20, help="Stopaj oranı (Varsayılan: 0.20)")
    p_smm.add_argument("--kdv", type=float, default=0.20, help="KDV oranı (Varsayılan: 0.20)")

    # Tevkifat
    p_tev = subparsers.add_parser("tevkifat", help="KDV Tevkifat Hesaplayıcı", parents=[parent_parser])
    p_tev.add_argument("matrah", type=float, help="KDV Hariç Matrah (TL)")
    p_tev.add_argument("--kdv", type=float, default=0.20, help="KDV oranı (Varsayılan: 0.20)")
    p_tev.add_argument("--oran", type=str, default="5/10", help="Tevkifat oranı (örn: 2/10, 5/10, 9/10, varsayılan: 5/10)")

    # Kıdem
    p_kidem = subparsers.add_parser("kidem", help="Kıdem Tazminatı Hesaplayıcı", parents=[parent_parser])
    p_kidem.add_argument("brut", type=float, help="Aylık giydirilmiş brüt ücret (TL)")
    p_kidem.add_argument("yil", type=float, help="Hizmet süresi (Yıl)")
    p_kidem.add_argument("--tavan", type=float, default=46500.0, help="Güncel kıdem tazminatı tavanı")

    args = parser.parse_args()

    if args.command == "esmm":
        if args.net:
            res = calculate_esmm_from_net(args.tutar, args.stopaj, args.kdv)
        else:
            res = calculate_esmm_from_brut(args.tutar, args.stopaj, args.kdv)

        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif args.markdown:
            print("| Kalem | Tutar |")
            print("| :--- | :--- |")
            print(f"| **Brüt Ücret** | {res['brut_ucret']:,.2f} TL |")
            print(f"| **GV Stopajı (%{int(res['stopaj_orani']*100)})** | -{res['stopaj_tutari']:,.2f} TL |")
            print(f"| **Net Ücret** | {res['net_ucret']:,.2f} TL |")
            print(f"| **KDV (%{int(res['kdv_orani']*100)})** | +{res['kdv_tutari']:,.2f} TL |")
            print(f"| **Tahsil Edilecek Toplam** | **{res['tahsil_edilen_toplam']:,.2f} TL** |")
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
        parts = args.oran.split("/")
        pay = int(parts[0])
        payda = int(parts[1]) if len(parts) > 1 else 10
        res = calculate_kdv_tevkifat(args.matrah, args.kdv, pay, payda)

        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif args.markdown:
            print("| Kalem | Tutar / Değer |")
            print("| :--- | :--- |")
            print(f"| **Matrah (KDV Hariç)** | {res['matrah']:,.2f} TL |")
            print(f"| **Hesaplanan KDV (%{int(res['kdv_orani']*100)})** | {res['hesaplanan_kdv']:,.2f} TL |")
            print(f"| **Tevkifat Oranı** | {res['tevkifat_orani_str']} |")
            print(f"| **Tevkif Edilen KDV** | {res['tevkif_edilen_kdv']:,.2f} TL |")
            print(f"| **Tahsil Edilen KDV** | {res['tahsil_edilen_kdv']:,.2f} TL |")
            print(f"| **Fatura Toplam Tutarı** | **{res['fatura_toplam']:,.2f} TL** |")
            print(f"| **KDV-2 Beyan Tutarı (Alıcı)** | {res['kdv2_beyan_tutari']:,.2f} TL |")
        else:
            print("=" * 60)
            print("          KDV TEVKİFAT HESAPLAMA TABLOSU")
            print("=" * 60)
            print(f"Matrah (KDV Hariç)      : {res['matrah']:,.2f} TL")
            print(f"Hesaplanan KDV (%{int(res['kdv_orani']*100)})     : {res['hesaplanan_kdv']:,.2f} TL")
            print(f"Tevkifat Oranı          : {res['tevkifat_orani_str']}")
            print(f"Tevkif Edilen KDV       : {res['tevkif_edilen_kdv']:,.2f} TL")
            print(f"Tahsil Edilen KDV       : {res['tahsil_edilen_kdv']:,.2f} TL")
            print("-" * 60)
            print(f"FATURA TOPLAM TUTARI    : {res['fatura_toplam']:,.2f} TL")
            print(f"ALICININ KDV-2 BEYANI   : {res['kdv2_beyan_tutari']:,.2f} TL")
            print("=" * 60)

    elif args.command == "kidem":
        res = calculate_kidem_tazminati(args.brut, args.yil, args.tavan)

        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif args.markdown:
            print("| Kalem | Tutar / Değer |")
            print("| :--- | :--- |")
            print(f"| **Giydirilmiş Brüt Ücret** | {res['giydirilmis_brut']:,.2f} TL |")
            print(f"| **Uygulanan Kıdem Tavanı** | {res['kidem_tavani']:,.2f} TL |")
            print(f"| **Esas Alınan Brüt** | {res['uygulanan_brut']:,.2f} TL |")
            print(f"| **Hizmet Yılı** | {res['calisma_yili']} Yıl |")
            print(f"| **Brüt Kıdem Tazminatı** | {res['brut_kidem']:,.2f} TL |")
            print(f"| **Damga Vergisi (‰7.59)** | -{res['damga_vergisi']:,.2f} TL |")
            print(f"| **Net Ödenecek Kıdem Taz.** | **{res['net_kidem_tazminati']:,.2f} TL** |")
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

if __name__ == "__main__":
    main()

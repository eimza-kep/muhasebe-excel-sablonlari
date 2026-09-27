import unittest
from calculate_smm import calculate_esmm_from_brut, calculate_esmm_from_net, calculate_kidem_tazminati, calculate_kdv_tevkifat

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

    def test_kdv_tevkifat(self):
        # Matrah: 100.000 TL, %20 KDV: 20.000 TL, 5/10 Tevkifat -> 10.000 TL Tevkif, 10.000 TL Tahsil
        res = calculate_kdv_tevkifat(100000, 0.20, 5, 10)
        self.assertEqual(res["matrah"], 100000.0)
        self.assertEqual(res["hesaplanan_kdv"], 20000.0)
        self.assertEqual(res["tevkif_edilen_kdv"], 10000.0)
        self.assertEqual(res["tahsil_edilen_kdv"], 10000.0)
        self.assertEqual(res["fatura_toplam"], 110000.0)
        self.assertEqual(res["kdv2_beyan_tutari"], 10000.0)

if __name__ == "__main__":
    unittest.main()

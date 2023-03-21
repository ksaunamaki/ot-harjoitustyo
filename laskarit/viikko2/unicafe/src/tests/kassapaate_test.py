import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.edullisen_hinta = 240
        self.maukkaan_hinta = 400

    def test_luotu_kassapaate_rahamaara_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_luotu_kassapaate_myydyt_oikein(self):
        self.assertEqual((self.kassapaate.edulliset + self.kassapaate.maukkaat), 0)

    def test_maukas_kateisosto_riittamaton_raha_toimii(self):
        palautus = self.kassapaate.syo_maukkaasti_kateisella(self.maukkaan_hinta-100)

        self.assertEqual(palautus, self.maukkaan_hinta-100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_maukas_kateisosto_tasaraha_toimii(self):
        palautus = self.kassapaate.syo_maukkaasti_kateisella(self.maukkaan_hinta)

        self.assertEqual(palautus, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000+self.maukkaan_hinta)

    def test_maukas_kateisosto_vaihtoraha_toimii(self):
        palautus = self.kassapaate.syo_maukkaasti_kateisella(self.maukkaan_hinta+100)

        self.assertEqual(palautus, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000+self.maukkaan_hinta)

    def test_maukas_kateisosto_myydyt_lounaat_kasvavat(self):
        self.kassapaate.syo_maukkaasti_kateisella(self.maukkaan_hinta)

        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_edullinen_kateisosto_riittamaton_raha_toimii(self):
        palautus = self.kassapaate.syo_edullisesti_kateisella(self.edullisen_hinta-100)

        self.assertEqual(palautus, self.edullisen_hinta-100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_edullinen_kateisosto_tasaraha_toimii(self):
        palautus = self.kassapaate.syo_edullisesti_kateisella(self.edullisen_hinta)

        self.assertEqual(palautus, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000+self.edullisen_hinta)

    def test_edullinen_kateisosto_vaihtoraha_toimii(self):
        palautus = self.kassapaate.syo_edullisesti_kateisella(self.edullisen_hinta+100)

        self.assertEqual(palautus, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000+self.edullisen_hinta)

    def test_edullinen_kateisosto_myydyt_lounaat_kasvavat(self):
        self.kassapaate.syo_edullisesti_kateisella(self.edullisen_hinta)

        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukas_korttiosto_riittamaton_raha_toimii(self):
        kortti = Maksukortti(self.maukkaan_hinta-100)
        tulos = self.kassapaate.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(kortti.saldo, self.maukkaan_hinta-100)
        self.assertEqual(tulos, False)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_maukas_korttiosto_kortti_toimii(self):
        kortti = Maksukortti(self.maukkaan_hinta)
        tulos = self.kassapaate.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(tulos, True)
        self.assertEqual(kortti.saldo, 0)

    def test_maukas_korttiosto_myydyt_lounaat_kasvavat(self):
        kortti = Maksukortti(self.maukkaan_hinta)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)
        
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_maukas_korttiosto_myydyt_kassa_ei_muutu(self):
        kortti = Maksukortti(self.maukkaan_hinta)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)
        
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_edullinen_korttiosto_riittamaton_raha_toimii(self):
        kortti = Maksukortti(self.edullisen_hinta-100)
        tulos = self.kassapaate.syo_edullisesti_kortilla(kortti)

        self.assertEqual(kortti.saldo, self.edullisen_hinta-100)
        self.assertEqual(tulos, False)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_edullinen_korttiosto_kortti_toimii(self):
        kortti = Maksukortti(self.edullisen_hinta)
        tulos = self.kassapaate.syo_edullisesti_kortilla(kortti)

        self.assertEqual(tulos, True)
        self.assertEqual(kortti.saldo, 0)

    def test_edullinen_korttiosto_myydyt_lounaat_kasvavat(self):
        kortti = Maksukortti(self.edullisen_hinta)
        self.kassapaate.syo_edullisesti_kortilla(kortti)
        
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_edullinen_korttiosto_myydyt_kassa_ei_muutu(self):
        kortti = Maksukortti(self.edullisen_hinta)
        self.kassapaate.syo_edullisesti_kortilla(kortti)
        
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_korttilataus_toimii(self):
        kortti = Maksukortti(0)
        self.kassapaate.lataa_rahaa_kortille(kortti, 100)
        
        self.assertEqual(kortti.saldo, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100100)

    def test_negatiivinen_korttilataus_toimii(self):
        kortti = Maksukortti(100)
        self.kassapaate.lataa_rahaa_kortille(kortti, -100)
        
        self.assertEqual(kortti.saldo, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

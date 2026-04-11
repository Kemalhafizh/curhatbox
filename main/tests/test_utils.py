from django.test import TestCase
from main.utils import sensor_kata, verify_recaptcha
from django.conf import settings

class UtilsTestCase(TestCase):
    """
    Test suite khusus untuk modul helper/utilitas independen
    seperti filter sensor kata dan integrasi third party (reCAPTCHA).
    """

    def test_sensor_kata_basic(self):
        """Memastikan fungsi dasar sensor kata berjalan."""
        text = "Dasar kamu anjing dan babi!"
        censored = sensor_kata(text)
        self.assertEqual(censored, "Dasar kamu ****** dan ****!")

    def test_sensor_kata_case_insensitive(self):
        """Memastikan filter kebal terhadap trik huruf besar/kecil (Alay)."""
        text = "Ini bAnGsAt banget sih, aSu"
        censored = sensor_kata(text)
        self.assertEqual(censored, "Ini ******* banget sih, ***")

    def test_sensor_kata_mixed_symbols(self):
        """Memastikan filter tidak merusak kata aman yang mirip."""
        text = "Makan di restoran yang asyik"
        # Kata "asyik" ada unsur "as" namun bukan "asu" yang terpisah
        censored = sensor_kata(text)
        self.assertEqual(censored, "Makan di restoran yang asyik")

    def test_sensor_kata_empty(self):
        """Memastikan fungsi tidak error jika diberi input kosong/None."""
        self.assertEqual(sensor_kata(""), "")
        self.assertEqual(sensor_kata(None), None)

    def test_verify_recaptcha_success_mock(self):
        """
        Memastikan logika reCAPTCHA v3 mengembalikan True untuk Test Key Google.
        (Test Key asli selalu lolos bypass bypass di utils.py)
        """
        # Dalam settings.py, RECAPTCHA_PUBLIC_KEY diset ke Test Key
        with self.settings(RECAPTCHA_PUBLIC_KEY="6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"):
            result = verify_recaptcha("dummy_token_karena_bypass")
            self.assertTrue(result)

    def test_verify_recaptcha_fail_no_token(self):
        """Memastikan gagal jika token kosong."""
        self.assertFalse(verify_recaptcha(""))
        self.assertFalse(verify_recaptcha(None))

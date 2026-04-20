from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from main.models import Profile, QnASession


class ViewsTestCase(TestCase):
    """
    Test suite untuk mensimulasikan rute HTTP dan respon Views.
    Memastikan perlindungan halaman khusus pengguna login bekerja.
    """

    def setUp(self):
        self.client = Client()

        # Buat user dan paksa generate profil via signal
        self.user = User.objects.create_user(
            username="kemal_test", password="password_super_kuat"
        )

    def test_dashboard_login_required(self):
        """Memastikan halaman dashboard diproteksi dari tamu (Guest)."""
        response = self.client.get(reverse("dashboard"))
        # Harus diarahkan ke halaman login
        self.assertEqual(response.status_code, 302)
        self.assertTrue("/login/" in response.url or "/accounts/login/" in response.url)

    def test_dashboard_accessible_for_logged_in_user(self):
        """Memastikan dashboard bisa diakses setelah Login berhasil."""
        # Login secara virtual
        self.client.login(username="kemal_test", password="password_super_kuat")

        response = self.client.get(reverse("dashboard"))
        # Harus sukses load halaman
        self.assertEqual(response.status_code, 200)

    def test_public_profile_accessible(self):
        """Memastikan URL Profil Publik berstatus 200 OK untuk umum."""
        # Ambil slug profil yang baru degenerate
        slug = self.user.profile.slug
        url = reverse("public_profile", kwargs={"slug": slug})

        response = self.client.get(url, HTTP_X_REAL_IP="127.0.0.1")
        self.assertEqual(response.status_code, 200)

    def test_inactive_qna_session_redirects(self):
        """
        Memastikan jika user mencoba mengakses sesi QnA yang ditutup,
        mereka akan dialihkan kembali ke profil utama dengan peringatan.
        """
        qna = QnASession.objects.create(
            user=self.user, title="Sudah Tutup", is_active=False
        )
        slug = self.user.profile.slug

        url = reverse("public_profile_qna", kwargs={"slug": slug, "qna_slug": qna.slug})
        response = self.client.get(url, HTTP_X_REAL_IP="127.0.0.1")

        # Harus diredirect (302) kembali ke profil publik biasa
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/{slug}/")

from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Profile, QnASession, Message
from django.core.files.uploadedfile import SimpleUploadedFile

class ModelsTestCase(TestCase):
    """
    Test suite untuk memverifikasi logika Model Database,
    termasuk pembuatan slug otomatis, sinyal on_save, dan logika relasional.
    """

    def setUp(self):
        # Set up data awal yang akan digunakan pada setiap test di bawahnya
        self.user1 = User.objects.create_user(username="testuser_satu", email="t1@mail.com", password="pwd")
        self.user2 = User.objects.create_user(username="testuser_dua", email="t2@mail.com", password="pwd")

    def test_profile_auto_created_on_user_creation(self):
        """Memastikan Profile otomatis dibuat via Signals saat User mendaftar."""
        self.assertTrue(Profile.objects.filter(user=self.user1).exists())
        self.assertTrue(Profile.objects.filter(user=self.user2).exists())

    def test_profile_slug_generation(self):
        """Memastikan Slug tervalidasi dan dihasilkan dengan aman."""
        profile1 = self.user1.profile
        self.assertEqual(profile1.slug, "testuser_satu")

        # Test user dengan karakter unik (simulasi)
        user_unik = User.objects.create_user(username="Bang Jago 123!", email="bj@mail.com", password="pwd")
        self.assertEqual(user_unik.profile.slug, "bang-jago-123")

    def test_qna_session_slug_generation(self):
        """Memastikan sesi QnA memiliki slug unik dan acak yang terisi otomatis."""
        qna = QnASession.objects.create(user=self.user1, title="Ask anything!")
        self.assertIsNotNone(qna.slug)
        self.assertEqual(len(qna.slug), 6) # Generate acak 6 karakter
        self.assertTrue(qna.is_active)

    def test_message_creation_logic(self):
        """Memastikan pembuatan pesan anonim berfungsi secara relasional."""
        qna = QnASession.objects.create(user=self.user1, title="Sesi Tanya Jawab")
        
        # Simulasi orang anonim mengirim pesan ke user1 lewat sesi QnA
        msg = Message.objects.create(
            recipient=self.user1,
            content="Ini pesan uji coba dari fans",
            sender_ip="192.168.1.1",
            qna_session=qna,
            is_disposable=True
        )

        self.assertEqual(msg.recipient.username, "testuser_satu")
        self.assertFalse(msg.is_read) # Default belum dibaca
        self.assertEqual(msg.qna_session.title, "Sesi Tanya Jawab")
        self.assertTrue(msg.is_disposable)

    def test_user_cascade_deletion(self):
        """
        Memastikan On_Delete CASCADE bekerja. Jika User dihapus,
        semua Profil, Sesi QnA, dan Pesan miliknya harus lenyap seketika.
        """
        qna = QnASession.objects.create(user=self.user1, title="Sesi Dihapus")
        Message.objects.create(recipient=self.user1, content="Pesan Sampah", qna_session=qna)

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Profile.objects.count(), 2)
        self.assertEqual(QnASession.objects.count(), 1)
        self.assertEqual(Message.objects.count(), 1)

        # Hapus user 1
        self.user1.delete()

        # Validasi pembersihan otomatis
        self.assertEqual(User.objects.count(), 1) # Sisa user2
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(QnASession.objects.count(), 0) # QnA user1 hilang
        self.assertEqual(Message.objects.count(), 0) # Pesan inbox user1 hilang

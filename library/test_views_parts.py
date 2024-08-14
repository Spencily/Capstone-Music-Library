from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase
from .forms import PartForm
from .models import Piece, Part


class TestPieceView(TestCase):
    """Test the piece view and context"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpassword"
        )
        self.piece = Piece(
            title="Test Title",
            composer="Test Composer",
            arranged_by="Test Arranger",
            genre="Test Genre",
            mc_location="Test Location",
            band_arrangement="Flexi-band",
        )
        self.piece.save()

        self.part = Part(
            piece=self.piece,
            instrument="Test Instrument",
            part_number=1,
            pdf_file=SimpleUploadedFile(
                "test.pdf", b"file_content", content_type="application/pdf"
            ),
        )
        self.part.save()

    def test_piece_view_upload_part(self):
        """Test the piece view with a new part upload"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("piece_view", args=[self.part.id]),
            {
                "instrument": "Test Instrument",
                "part_number": 2,
                "pdf_file": SimpleUploadedFile(
                    "test.pdf", b"file_content", content_type="application/pdf"
                ),
            },
        )
        self.assertRedirects(
            response,
            reverse("piece_view", args=[self.part.id]),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        part = Part.objects.get(pk=2)

        response = self.client.get(reverse("piece_view", args=[self.part.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/piece_view.html")
        self.assertEqual(self.piece, response.context["piece"])
        self.assertIn(part, response.context["piece"].parts.all())
        self.assertIsInstance(response.context["part_form"], PartForm)
        self.client.logout()


class TestPartView(TestCase):
    """Test the part view and context"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpassword"
        )
        self.piece = Piece(
            title="Test Title",
            composer="Test Composer",
            arranged_by="Test Arranger",
            genre="Test Genre",
            mc_location="Test Location",
            band_arrangement="Flexi-band",
        )
        self.piece.save()

        self.part = Part(
            piece=self.piece,
            instrument="Test Instrument",
            part_number=1,
            pdf_file=SimpleUploadedFile(
                "test.pdf", b"file_content", content_type="application/pdf"
            ),
        )
        self.part.save()

    def test_part_view_visible_pdf(self):
        """Test the part view with a visible pdf"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("part_view", args=[self.part.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/piece_view.html")
        self.assertEqual(self.part, response.context["part"])
        self.assertEqual(self.piece, response.context["piece"])
        self.assertIsInstance(response.context["part_form"], PartForm)

        content = response.content.decode("utf-8")
        self.assertIn("<embed", content, "The embed tag was not found in the response.")
        expected_src = reverse("part_pdf_view", args=[self.part.id])
        expected_embed_str = f'<embed src="{expected_src}'

        self.assertIn(
            expected_embed_str,
            content,
            f"The embed with src '{expected_src}' was not found in the response.",
        )
        self.client.logout()

    def test_part_view_upload_part(self):
        """Test the part view with a new part upload"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("part_view", args=[self.part.id]),
            {
                "instrument": "Test Instrument",
                "part_number": 2,
                "pdf_file": SimpleUploadedFile(
                    "test.pdf", b"file_content", content_type="application/pdf"
                ),
            },
        )
        self.assertRedirects(
            response,
            reverse("part_view", args=[self.part.id]),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        part = Part.objects.get(pk=2)

        response = self.client.get(reverse("part_view", args=[self.part.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/piece_view.html")
        self.assertEqual(self.part, response.context["part"])
        self.assertEqual(self.piece, response.context["piece"])
        self.assertIn(part, response.context["piece"].parts.all())
        self.assertIsInstance(response.context["part_form"], PartForm)
        self.client.logout()


class TestPartPdfView(TestCase):
    """Test the part pdf view and context"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpassword"
        )
        self.piece = Piece(
            title="Test Title",
            composer="Test Composer",
            arranged_by="Test Arranger",
            genre="Test Genre",
            mc_location="Test Location",
            band_arrangement="Flexi-band",
        )
        self.piece.save()

        self.part = Part(
            piece=self.piece,
            instrument="Test Instrument",
            part_number=1,
            pdf_file=SimpleUploadedFile(
                "test.pdf", b"file_content", content_type="application/pdf"
            ),
        )
        self.part.save()

    def test_part_pdf_view(self):
        """Test the part pdf view"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("part_pdf_view", args=[self.part.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertEqual(response.content, b"file_content")
        self.client.logout()


class TestPartEdit(TestCase):
    """Test the part edit view and context"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpassword")
        self.piece = Piece(
            title="Test Title",
            composer="Test Composer",
            arranged_by="Test Arranger",
            genre="Test Genre",
            mc_location="Test Location",
            band_arrangement="Flexi-band",
        )
        self.piece.save()

        self.part = Part(
            piece=self.piece,
            instrument="Test Instrument",
            part_number=1,
            pdf_file=SimpleUploadedFile(
                "test.pdf", b"file_content", content_type="application/pdf"
            ),
        )
        self.part.save()

    def test_part_edit_display_form(self):
        """Test the part edit view with the form displayed"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("part_edit", args=[self.part.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/piece_view.html")
        self.assertEqual(self.piece, response.context["piece"])
        self.assertIsInstance(response.context["part_form"], PartForm)
        self.client.logout()

    def test_part_edit_update_part(self):
        """Test the part edit view when updating a part"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("part_edit", args=[self.part.id]),
            {
                "instrument": "Test Instrument",
                "part_number": 2,
                "pdf_file": SimpleUploadedFile(
                    "test.pdf", b"file_content", content_type="application/pdf"
                ),
            },
        )
        self.assertRedirects(
            response,
            reverse("piece_view", args=[self.part.id]),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        part = Part.objects.get(pk=self.part.id)
        self.assertEqual(part.instrument, "Test Instrument")
        self.assertEqual(part.part_number, 2)
        self.assertEqual(part.pdf_file.read(), b"file_content")
        self.client.logout()

class TestPartDelete(TestCase):
    """Test the part delete view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpassword")
        self.piece = Piece(
            title="Test Title",
            composer="Test Composer",
            arranged_by="Test Arranger",
            genre="Test Genre",
            mc_location="Test Location",
            band_arrangement="Flexi-band",
        )
        self.piece.save()

        self.part = Part(
            piece=self.piece,
            instrument="Test Instrument",
            part_number=1,
            pdf_file=SimpleUploadedFile(
                "test.pdf", b"file_content", content_type="application/pdf"
            ),
        )
        self.part.save()

    def test_part_delete(self):
        """Test the part delete view"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("part_delete", args=[self.part.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Part.DoesNotExist):
            Part.objects.get(pk=self.part.id)
        self.client.logout()
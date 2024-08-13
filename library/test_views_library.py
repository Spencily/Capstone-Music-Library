from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase
from .forms import PieceForm, PartForm, SearchForm
from .models import Piece, Part


class TestLibraryView(TestCase):
    """Test the library view and context"""

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

    def test_library_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("library"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/library.html")
        self.assertIn(self.piece, response.context["pieces"])
        self.client.logout()

    def test_library_view_post(self):
        """Test to add new pieces to the library"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("library"),
            {
                "title": "Test Title 2",
                "composer": "Test Composer 2",
                "arranged_by": "Test Arranger 2",
                "genre": "Test Genre 2",
                "mc_location": "Test Location 2",
                "band_arrangement": "Flexi-band",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        piece = Piece.objects.get(title="Test Title 2")
        self.client.logout()

    def test_library_view_search(self):
        """Test the library view search"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("library"), {"query": "Test Title"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/library.html")
        self.assertIn(self.piece, response.context["pieces"])
        self.client.logout()

    def test_library_view_search_filter(self):
        """Test the library view search filter"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("library"), {"query": "Test Composer", "filter": "composer"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/library.html")
        self.assertIn(self.piece, response.context["pieces"])
        self.client.logout()

    def test_library_view_search_no_results(self):
        """Test the library view search with no results"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("library"), {"query": "No Results"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/library.html")
        self.assertNotIn(self.piece, response.context["pieces"])
        self.client.logout()

    def test_library_view_pagination(self):
        """Test the library view pagination"""
        self.client.login(username="testuser", password="testpassword")
        for i in range(0, 20):
            piece = Piece(
                title=f"Test Title {i}",
                composer=f"Test Composer {i}",
                arranged_by=f"Test Arranger {i}",
                genre=f"Test Genre {i}",
                mc_location=f"Test Location {i}",
                band_arrangement="Flexi-band",
            )
            piece.save()
        response = self.client.get(reverse("library"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/library.html")
        self.assertEqual(len(response.context["pieces"]), 10)
        self.client.logout()

    def test_library_view_pagination_next_page(self):
        """Test the library view pagination next page"""
        self.client.login(username="testuser", password="testpassword")
        for i in range(0, 15):
            piece = Piece(
                title=f"Test Title {i}",
                composer=f"Test Composer {i}",
                arranged_by=f"Test Arranger {i}",
                genre=f"Test Genre {i}",
                mc_location=f"Test Location {i}",
                band_arrangement="Flexi-band",
            )
            piece.save()
        response = self.client.get(reverse("library"), {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/library.html")
        self.assertEqual(len(response.context["pieces"]), 6)
        self.client.logout()


class TestLibraryPrintView(TestCase):
    """Test the library print view and context"""

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

    def test_library_print_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("library_print"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/library_print.html")
        self.assertIn(self.piece, response.context["pieces"])
        self.client.logout()


class TestPieceEditView(TestCase):
    """Test the piece edit view"""

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

    def test_piece_edit_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("piece_edit", args=[self.piece.id]),
            {
                "title": "Test Title Edited",
                "composer": "Test Composer Edited",
                "arranged_by": "Test Arranger Edited",
                "genre": "Test Genre Edited",
                "mc_location": "Test Location Edited",
                "band_arrangement": "Full-band",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.piece.refresh_from_db()
        self.assertEqual(self.piece.title, "Test Title Edited")
        self.assertEqual(self.piece.composer, "Test Composer Edited")
        self.assertEqual(self.piece.arranged_by, "Test Arranger Edited")
        self.assertEqual(self.piece.genre, "Test Genre Edited")
        self.assertEqual(self.piece.mc_location, "Test Location Edited")
        self.assertEqual(self.piece.band_arrangement, "Full-band")
        self.client.logout()

    def test_library_view_search(self):
        """Test the library view search"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("piece_edit", args=[self.piece.id]), {"query": "Test Title"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/library.html")
        self.assertIn(self.piece, response.context["pieces"])
        self.client.logout()

    def test_library_view_search_filter(self):
        """Test the library view search filter"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("piece_edit", args=[self.piece.id]),
            {"query": "Test Composer", "filter": "composer"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/library.html")
        self.assertIn(self.piece, response.context["pieces"])
        self.client.logout()

    def test_library_view_search_no_results(self):
        """Test the library view search with no results"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("piece_edit", args=[self.piece.id]), {"query": "No Results"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/library.html")
        self.assertNotIn(self.piece, response.context["pieces"])
        self.client.logout()

    def test_library_view_pagination(self):
        """Test the library view pagination"""
        self.client.login(username="testuser", password="testpassword")
        for i in range(0, 20):
            piece = Piece(
                title=f"Test Title {i}",
                composer=f"Test Composer {i}",
                arranged_by=f"Test Arranger {i}",
                genre=f"Test Genre {i}",
                mc_location=f"Test Location {i}",
                band_arrangement="Flexi-band",
            )
            piece.save()
        response = self.client.get(reverse("piece_edit", args=[self.piece.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/library.html")
        self.assertEqual(len(response.context["pieces"]), 10)
        self.client.logout()

    def test_library_view_pagination_next_page(self):
        """Test the library view pagination next page"""
        self.client.login(username="testuser", password="testpassword")
        for i in range(0, 15):
            piece = Piece(
                title=f"Test Title {i}",
                composer=f"Test Composer {i}",
                arranged_by=f"Test Arranger {i}",
                genre=f"Test Genre {i}",
                mc_location=f"Test Location {i}",
                band_arrangement="Flexi-band",
            )
            piece.save()
        response = self.client.get(
            reverse("piece_edit", args=[self.piece.id]), {"page": 2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/library.html")
        self.assertEqual(len(response.context["pieces"]), 6)
        self.client.logout()


class TestPieceDeleteView(TestCase):
    """Test the piece delete view"""

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

    def test_piece_delete_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("piece_delete", args=[self.piece.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Piece.DoesNotExist):
            Piece.objects.get(pk=self.piece.id)
        self.client.logout()

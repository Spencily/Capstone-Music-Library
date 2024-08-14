from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from library.models import Piece
from .models import Setlist
from .forms import SetForm


class TestSetlistListView(TestCase):
    """Tests for the setlist list view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.setlist = Setlist.objects.create(
            title="Test Title",
            created_by=self.user,
        )
        self.setlist.save()

    def test_setlist_list_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("setlist"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "setlist/setlist.html")
        self.assertContains(response, "Test Title")
        self.assertIn(self.setlist, response.context["setlists"])
        self.client.logout()

    def test_setlist_view_other_user(self):
        User.objects.create_user(username="otheruser", password="otherpassword")
        self.client.login(username="otheruser", password="otherpassword")
        response = self.client.get(reverse("setlist"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "setlist/setlist.html")
        self.assertNotIn(self.setlist, response.context["setlists"])
        self.client.logout()


class TestSetlistView(TestCase):
    """Tests for the setlist view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.setlist = Setlist.objects.create(
            title="Test Title",
            created_by=self.user,
        )
        self.setlist.save()

    def test_setlist_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("setlist_view", args=[self.setlist.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "setlist/setlist.html")
        self.assertContains(response, "Test Title")
        self.assertEqual(self.setlist, response.context["setlist"])
        self.client.logout()

    def test_setlist_view_other_user(self):
        User.objects.create_user(username="otheruser", password="otherpassword")
        self.client.login(username="otheruser", password="otherpassword")
        response = self.client.get(reverse("setlist_view", args=[self.setlist.id]))
        self.assertEqual(response.status_code, 404)
        self.client.logout()


class TestSetlistPrintView(TestCase):
    """Tests for the setlist print view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.setlist = Setlist.objects.create(
            title="Test Title",
            created_by=self.user,
        )
        self.setlist.save()

    def test_setlist_print_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("setlist_print", args=[self.setlist.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.client.logout()

    def test_setlist_print_view_other_user(self):
        User.objects.create_user(username="otheruser", password="otherpassword")
        self.client.login(username="otheruser", password="otherpassword")
        response = self.client.get(reverse("setlist_print", args=[self.setlist.id]))
        self.assertEqual(response.status_code, 404)
        self.client.logout()


class TestSetlistAddView(TestCase):
    """Tests for the setlist add view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.piece = Piece.objects.create(
            title="Test Title",
            composer="Test Composer",
            arranged_by="Test Arranger",
            genre="Test Genre",
            mc_location="Test Location",
            band_arrangement="Test Band Arrangement",
        )
        self.piece.save()

    def test_setlist_add_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("setlist_add"),
            {
                "title": "Test Title",
                "description": "Test Description",
                "pieces": (self.piece.id,),
            },
        )
        self.assertRedirects(
            response,
            reverse("setlist"),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        setlist = Setlist.objects.get(title="Test Title")

        response = self.client.get(reverse("setlist"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "setlist/setlist.html")
        self.assertIn(setlist, response.context["setlists"])
        self.client.logout()


class TestSetlistEditView(TestCase):
    """Tests for the setlist edit view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.piece = Piece.objects.create(
            title="Test Title",
            composer="Test Composer",
            arranged_by="Test Arranger",
            genre="Test Genre",
            mc_location="Test Location",
            band_arrangement="Test Band Arrangement",
        )
        self.piece.save()
        self.setlist = Setlist.objects.create(
            title="Test Title",
            description="Test Description",
            created_by=self.user,
        )
        self.setlist.pieces.add(self.piece)
        self.setlist.save()

    def test_setlist_edit_view_displays_form(self):
        """Test that the edit view displays the form"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("setlist_edit", args=[self.setlist.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "setlist/setlist_form.html")
        self.assertIsInstance(response.context["form"], SetForm)
        self.client.logout()

    def test_setlist_edit_view_update_set(self):
        """Test that the setlist is updated"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("setlist_edit", args=[self.setlist.id]),
            {
                "title": "New Title",
                "description": "New Description",
                "pieces": (self.piece.id,),
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.setlist.refresh_from_db()
        self.assertEqual(self.setlist.title, "New Title")
        self.assertEqual(self.setlist.description, "New Description")
        self.assertIn(self.piece, self.setlist.pieces.all())
        self.client.logout()


class TestSetlistDeleteView(TestCase):
    """Tests for the setlist delete view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.piece = Piece.objects.create(
            title="Test Title",
            composer="Test Composer",
            arranged_by="Test Arranger",
            genre="Test Genre",
            mc_location="Test Location",
            band_arrangement="Test Band Arrangement",
        )
        self.piece.save()
        self.setlist = Setlist.objects.create(
            title="Test Title",
            created_by=self.user,
        )
        self.setlist.pieces.add(self.piece)
        self.setlist.save()

    def test_setlist_delete_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("setlist_delete", args=[self.setlist.id]),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Setlist.DoesNotExist):
            Setlist.objects.get(title="Test Title")
        self.client.logout()

    def test_setlist_delete_view_other_user(self):
        User.objects.create_user(username="otheruser", password="otherpassword")
        self.client.login(username="otheruser", password="otherpassword")
        response = self.client.post(
            reverse("setlist_delete", args=[self.setlist.id]),
            follow=True,
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Setlist.objects.filter(title="Test Title").exists())
        self.client.logout()

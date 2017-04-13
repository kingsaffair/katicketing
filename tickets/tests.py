from django.test import TestCase, RequestFactory

from django.contrib.auth.models import User
from tickets.models import Guest

class GuestTestCase(TestCase):
    def setUp(self):
        self.bad_user = User.objects.create_user(
            username='dave', email='test@ox.ac.uk', password='oxf*rd'
        )
        self.college_user = User.objects.create_user(
            username='matt', email='me390@cam.ac.uk', password='correct horse battery staple'
        )
        self.uni_user = User.objects.create_user(
            username='tom', email='tre26@cam.ac.uk', password='t3ls3'
        )
        self.factory = RequestFactory()

    def test_bad(self):
        """
        This should test to make sure that only university members can buy
        tickets (even if they manage to get an account).
        """
        self.assertEqual(1,0)

    def test_college(self):
        """
        This should make sure that college members are entitled to 2 guest
        tickets and one member's ticket at the correct price.
        """
        self.assertEqual(1,0)

    def test_uni(self):
        """
        This should make sure that uni members are only entitled to a single
        ticket at the correct price.
        """
        self.assertEqual(1,0)

    # TODO: similar tests for the committee (simplify?)


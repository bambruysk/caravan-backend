from django.test import TestCase

# Create your tests here.
from caravan_routes.models import Pincode, Team, Game, Route


class TestPincode(TestCase):

    def setUp(self) -> None:
        self.game = Game.objects.create(name="TestGame", description="TestGame Description", )
        self.route = Route.objects.create(

        )

        self.pincode = Pincode.objects.create(
            text="ABCDEFG",
            team=Team.objects.create(name="TestTeam"),


        )
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

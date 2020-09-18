from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase, Client, LiveServerTestCase

# Create your tests here.
from rest_framework.test import APIClient

from caravan_routes.models import Game, GeoMap
from rest_framework.authtoken.models import Token

from scripts.geopoint_loader import make_default_points

TEST_GAME_NAME = "TestGame"
TEST_GAME_DESCRIPTION = "TestGameDescription"


def create_test_user() -> User:
    test_user_name = "test"
    test_user_passwd = "test"
    user = User.objects.create(username=test_user_name, password=test_user_passwd, is_superuser=False)
    return user


def get_user_token(user):
    token = Token.objects.get(user=user)
    return token


def create_map(game: Game):
    border_points = make_default_points()
    picture = File(open("tests/test_map.jpg", "rb"))
    return GeoMap.objects.create(
        name="TestMap",
        north_west=border_points["north_west"],
        north_east=border_points["north_east"],
        south_west=border_points["south_west"],
        south_east=border_points["south_east"],
        picture=picture,
        game=game)


def create_game():
    game = Game.objects.create(
        name=TEST_GAME_NAME,
        description=TEST_GAME_DESCRIPTION,
    )
    map = create_map(game)
    game.geomap = map
    game.save()
    return game


class UserCreateTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_test_user()
        cls.token = get_user_token(cls.user)

    def tearDown(self) -> None:
        super().tearDown()
        self.user.delete()

    def test_token(self):
        print(self.user)
        print(self.token)


class GameAPITest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = create_test_user()
        cls.token = get_user_token(cls.user)

    def setUp(self) -> None:
        super().setUp()
        print("Innit test")
        self.game = create_game()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self) -> None:
        self.game.delete()
        super().tearDown()

    def assertOneGameEqual(self):
        resp = Client().get("/game/", "")

    def test_game_creation(self):
        print ("------Game cretation test")
        games = Game.objects.all()
        for g in games:
            print(g.geomap.id)
        print ("------Game cretation test")


    def test_game_list(self):
        resp = self.client.get("/api/game/", "", format='json', Token=self.token)
        self.assertEqual(resp.status_code, 200, f"Server response {resp.status_code}")
        print(resp.content)

    def test_server(self):
        resp = self.client.get("/api/routes/", "", format='json')
        self.assertEqual(resp.status_code, 200, f"Server response {resp.status_code}")
        print(resp)

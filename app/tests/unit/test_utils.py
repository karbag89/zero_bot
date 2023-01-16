
import pytest

from tests.base import BaseTestCase

from helpers.db_helper import get_user, get_choice_id
from werkzeug.security import check_password_hash


class UsersTest(BaseTestCase):

    @pytest.mark.usefixtures('add_user')
    def test_users(self):
        telegram_name = "Zero_Bot"
        user = get_user(telegram_name)
        self.assertEqual(user.username, "Zero_ABC")
        self.assertTrue(check_password_hash(user.password, "Bot_123"))


    @pytest.mark.usefixtures('add_pictures')
    @pytest.mark.usefixtures('add_classes')
    def test_choice_id(self):
        picture_id = 3
        choice = "cat"
        choice_id = get_choice_id(picture_id, choice)
        self.assertEqual(choice_id, 2)

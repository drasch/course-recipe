from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTest(TestCase):
    def test_wait_for_db_ready(self):
        """Test waiting for the database when it's already available"""
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            gi.return_value = True
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, 1)  # why are we checking the call count?

    @patch("time.sleep", return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for the database when it's not ready the first time"""
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            ERROR_COUNT = 5
            gi.side_effect = [OperationalError] * ERROR_COUNT + [True]
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, ERROR_COUNT + 1)

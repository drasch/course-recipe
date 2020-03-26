import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    SLEEP_TIME = 1  # seconds to pause between checks for database

    def handle(self, *args, **options):
        """Handle command to wait for database"""
        self.stdout.write("Checking for database...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(self.SLEEP_TIME)

        self.stdout.write(self.style.SUCCESS("Database available!"))

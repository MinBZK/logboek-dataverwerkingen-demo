from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


USERS = (
    # username  bsn
    ("burger", "999995042"),
    ("burger02", "999993161"),
    ("burger03", "999993914"),
)
PASSWORD = "demo123"


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()

        for username, bsn in USERS:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email="", password=PASSWORD, bsn=bsn)

        self.stdout.write("Users loaded")

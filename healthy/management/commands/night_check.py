from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from healthy.utils import send_health_mail

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = User.objects.exclude(email="")

        for user in users:
            msg = f"Hi {user.username}, did you take extra diet today? YES or NO"
            send_health_mail(user, "Night Diet Check", msg)
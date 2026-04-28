from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from healthy.utils import send_health_mail

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = User.objects.exclude(email="")

        for user in users:
            msg = f"Good Morning {user.username} ☀️\nTime for exercise!"
            send_health_mail(user, "Morning Exercise Alert", msg)
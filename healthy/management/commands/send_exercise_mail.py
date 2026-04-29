from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from healthy.models import UserHealthPlan
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from healthy.utils import convert_table_to_html, send_health_mail

class Command(BaseCommand):
    help = "Send daily exercise mail"

    def handle(self, *args, **kwargs):
        today = datetime.now().strftime('%A')
        users = User.objects.exclude(email="")

        for user in users:
            plan = UserHealthPlan.objects.filter(user=user).first()
            if not plan:
                continue

            exercise_html = convert_table_to_html(plan.exercise_reply)

            html_message = f"""
            <html>
            <body style="font-family:Arial;max-width:600px;margin:auto">
                <h2>💪 {today} Exercise Plan</h2>
                {exercise_html}
                <p>Do it sincerely 💪</p>
            </body>
            </html>
            """

            send_health_mail(user, f"{today} Exercise Plan", html_message)
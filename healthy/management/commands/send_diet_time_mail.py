from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from healthy.models import UserHealthPlan, DietSchedule
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from healthy.utils import convert_table_to_html


class Command(BaseCommand):
    help = "Send diet mail according to user time"

    def handle(self, *args, **kwargs):
        now = datetime.now().time()
        today = datetime.now().strftime("%A, %d %b %Y")

        users = User.objects.exclude(email="")

        for user in users:
            try:
                schedule = DietSchedule.objects.get(user=user)
                plan = UserHealthPlan.objects.get(user=user)
            except:
                continue

            meal = None
            if now.hour == schedule.breakfast_time.hour and now.minute == schedule.breakfast_time.minute:
                meal = "Breakfast"
            elif now.hour == schedule.lunch_time.hour and now.minute == schedule.lunch_time.minute:
                meal = "Lunch"
            elif now.hour == schedule.dinner_time.hour and now.minute == schedule.dinner_time.minute:
                meal = "Dinner"

            if meal:
                diet_html = convert_table_to_html(plan.diet_reply)

                html_content = f"""
                <html>
                <head>
                <style>
                    body {{
                        font-family: Arial;
                    }}
                    .card {{
                        max-width:700px;
                        margin:auto;
                        padding:15px;
                    }}
                    table {{
                        width:100%;
                        border-collapse:collapse;
                    }}
                    th, td {{
                        border:1px solid #333;
                        padding:8px;
                        text-align:center;
                    }}
                    h2 {{
                        background:#4CAF50;
                        color:white;
                        padding:10px;
                    }}
                </style>
                </head>
                <body>

                <div class="card">
                    <h2>🥗 {meal} Diet Plan</h2>
                    <p>{today}</p>
                    {diet_html}
                </div>

                </body>
                </html>
                """

                msg = EmailMultiAlternatives(
                    subject=f"{meal} Time 🥗",
                    body="Your email client does not support HTML.",
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
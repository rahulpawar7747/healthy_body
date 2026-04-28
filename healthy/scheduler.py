from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.models import User
from .utils import send_health_mail
import datetime


def send_to_all(subject, message):
    users = User.objects.exclude(email="")
    for user in users:
        send_health_mail(user, subject, message)


def morning_exercise():
    send_to_all(
        "Morning Exercise Alert 💪",
        "Good Morning ☀️\nTime to do your daily exercise for 30 minutes!"
    )


def breakfast_alert():
    send_to_all(
        "Breakfast Time 🥗",
        "Time for your healthy breakfast. Avoid oily food!"
    )


def lunch_alert():
    send_to_all(
        "Lunch Time 🍛",
        "Have a balanced lunch as per your diet plan."
    )


def dinner_alert():
    send_to_all(
        "Dinner Time 🍲",
        "Take light dinner and avoid sugar."
    )


def night_confirmation():
    send_to_all(
        "Night Diet Confirmation 🌙",
        "Did you take any extra diet today?\n\nReply YES or NO to this email."
    )


def start():
    scheduler = BackgroundScheduler()

    scheduler.add_job(morning_exercise, 'cron', hour=7, minute=0)
    scheduler.add_job(breakfast_alert, 'cron', hour=8, minute=0)
    scheduler.add_job(lunch_alert, 'cron', hour=13, minute=30)
    scheduler.add_job(dinner_alert, 'cron', hour=21, minute=0)
    scheduler.add_job(night_confirmation, 'cron', hour=21, minute=30)

    scheduler.start()
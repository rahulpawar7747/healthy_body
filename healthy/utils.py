from django.core.mail import send_mail

def send_health_mail(user, subject, message):
    if user.email:  # only users with email
        send_mail(subject, message, None, [user.email])
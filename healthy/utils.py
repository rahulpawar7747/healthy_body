from django.core.mail import EmailMultiAlternatives
import markdown
from django.conf import settings


# def send_health_mail(user, subject, html_message):
#     if not user.email:
#         print("NO EMAIL FOUND")
#         return

#     try:
#         response = resend.Emails.send({
#             "from": "onboarding@resend.dev",
#             "to": user.email,
#             "subject": subject,
#             "html": html_message
#         })

#         print("EMAIL SENT SUCCESS:", response)

#     except Exception as e:
#         print("EMAIL ERROR:", str(e))

def send_health_mail(user, subject, html_message):
    print("printing user info",user, user.email)
    if not user.email:
        print("NO EMAIL FOUND FOR USER")
        print("NO EMAIL FOUND")
        return
    
    print("SENDING EMAIL TO:", user.email)
    try:
        html_content = markdown.markdown(html_message)

        email = EmailMultiAlternatives(
            subject,
            # html_message,
            "Your email client does not support HTML emails.",
            settings.EMAIL_HOST_USER,
            ['developer.deepak25@gmail.com']  # For testing, send to a fixed email
        )

        # email.attach_alternative(html_content, "text/html")
        email.attach_alternative(html_message, "text/html")
        email.send()

        print("EMAIL SENT SUCCESS")

    except Exception as e:
        print("EMAIL ERROR:", str(e))

def convert_table_to_html(text):
    html = markdown.markdown(text, extensions=["tables"])

    # EMAIL SAFE TABLE FORMATTING
    html = html.replace(
        "<table>",
        '<table border="1" cellpadding="6" cellspacing="0" width="100%" '
        'style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:14px;">'
    )

    html = html.replace(
        "<th>",
        '<th style="border:1px solid #000;padding:8px;background:#4CAF50;'
        'color:#fff;text-align:left;">'
    )

    html = html.replace(
        "<td>",
        '<td style="border:1px solid #000;padding:8px;vertical-align:top;text-align:left;">'
    )

    return html

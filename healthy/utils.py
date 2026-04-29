from django.core.mail import EmailMultiAlternatives
# import markdown
def send_health_mail(user, subject, html_message):
    if not user.email:
        return

    email = EmailMultiAlternatives(
        subject=subject,
        body="Your health plan is ready.",   # plain fallback text
        from_email="rahulrajput7747@gmail.com",    # yaha apna sender email likho
        to=[user.email]
    )

    # IMPORTANT: HTML attach karna zaroori hai
    email.attach_alternative(html_message, "text/html")
    email.send()

import markdown

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
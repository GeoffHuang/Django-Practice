from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import render_to_string


def send_email(message):
    email_subject = "New Poll"
    email_body = message

    email = EmailMessage(
        email_subject, email_body, settings.EMAIL_HOST_USER,
        [x[1] for x in settings.MANAGERS], [],
    )

    return email.send(fail_silently=False)

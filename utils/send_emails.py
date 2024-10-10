from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings


def send_email(subject: str, user, email_context, template: str):
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    text_content = render_to_string(f"{template}.txt", email_context)
    html_content = render_to_string(f"{template}.html", email_context)

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")

    email.send()

    return JsonResponse({"message": "Email sent successfully!"}, status=200)

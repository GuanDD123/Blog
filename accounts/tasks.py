from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


@shared_task
def user_registed(user_pk: int):
    user = get_user_model().objects.get(pk=user_pk)
    mail_sent = send_mail(
        subject="Welcome to our site!",
        message=f"Hi {user.username}, thanks for registering!",
        from_email=None,
        recipient_list=[user.email],
    )
    return mail_sent

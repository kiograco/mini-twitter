from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User

@shared_task
def send_follow_notification_email(follower_id, following_id):
    follower = User.objects.get(id=follower_id)
    following = User.objects.get(id=following_id)

    send_mail(
        subject=f"{follower.username} started following you!",
        message="You have a new follower!",
        from_email="noreply@example.com",
        recipient_list=[following.email],
    )
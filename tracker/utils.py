from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import RestSession
from datetime import timedelta

def send_reminders():
    three_days_ago = timezone.now() - timedelta(days=3)
    users = User.objects.all()

    for user in users:
        recent_sessions = RestSession.objects.filter(user=user, start_time__gte=three_days_ago)
        if not recent_sessions.exists() and user.email:
            send_mail(
                'Дзен помнит о вас 💚',
                'Мы заметили, что вы давно не отдыхали. Может быть, пора сделать дыхательное упражнение или медитацию?',
                'zen-tracker@example.com',
                [user.email],
                fail_silently=False,
            )

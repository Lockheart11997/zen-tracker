from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import RestSession
from datetime import timedelta
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings

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

def send_activation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = request.build_absolute_uri(
        reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
    )
    subject = 'Подтверждение регистрации'
    message = f'Здравствуйте! Пожалуйста, подтвердите свою регистрацию по ссылке: {activation_link}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


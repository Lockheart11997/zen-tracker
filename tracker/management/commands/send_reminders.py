from django.core.management.base import BaseCommand
from ...utils import send_reminders

class Command(BaseCommand):
    help = 'Отправляет email-напоминания пользователям, у которых не было сессий 3 дня'

    def handle(self, *args, **kwargs):
        send_reminders()
        self.stdout.write(self.style.SUCCESS('✅ Напоминания успешно отправлены!'))
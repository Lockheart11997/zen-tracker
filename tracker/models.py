from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class RestSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(null=True, blank=True)
    meditation = models.ForeignKey('Meditation', null=True, blank=True, on_delete=models.SET_NULL)
    breathing_exercise = models.ForeignKey('BreathingExercise', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.username} — {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None

    def clean(self):
        if self.end_time and self.end_time <= self.start_time:
            raise ValidationError("Время окончания должно быть позже времени начала.")

    def end_session(self):
        self.end_time = now()
        self.full_clean()
        self.save()
        self.update_statistics()

    def update_statistics(self):
        stats, created = Statistics.objects.get_or_create(user=self.user)
        session_duration = self.duration()
        if session_duration:
            stats.total_rest_time += session_duration
            if self.meditation:
                stats.total_meditation_time += session_duration
            if self.breathing_exercise:
                stats.total_breathing_time += session_duration
            stats.save()

    def get_session_title(self):
        if self.meditation:
            return self.meditation.title
        elif self.breathing_exercise:
            return self.breathing_exercise.title
        return "Без названия"

    def get_session_image(self):
        if self.meditation and self.meditation.image:
            return self.meditation.image.url
        elif self.breathing_exercise and self.breathing_exercise.image:
            return self.breathing_exercise.image.url
        return None


class Meditation(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='meditation_images/', null=True, blank=True)
    instructions = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Длительность в минутах", default=5)


    def __str__(self):
        return self.title

    def clean(self):
        if self.duration <= 0:
            raise ValidationError("Длительность медитации должна быть положительной.")


class BreathingExercise(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='meditation_images/', null=True, blank=True)
    instructions = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Длительность в минутах", default=5)

    def __str__(self):
        return self.title

    def clean(self):
        if self.duration <= 0:
            raise ValidationError("Длительность упражнения должна быть положительной.")


class RelaxationTip(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title

    def clean(self):
        if not self.title.strip():
            raise ValidationError("Заголовок не может быть пустым.")
        if not self.content.strip():
            raise ValidationError("Содержимое не может быть пустым.")


class Statistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_rest_time = models.DurationField(default=0)
    total_meditation_time = models.DurationField(default=0)
    total_breathing_time = models.DurationField(default=0)


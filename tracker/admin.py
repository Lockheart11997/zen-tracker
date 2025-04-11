from django.contrib import admin
from .models import *

admin.site.register(RestSession)
admin.site.register(RelaxationTip)
admin.site.register(Statistics)

@admin.register(Meditation)
class MeditationAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration')
    fields = ('title', 'description', 'instructions', 'duration', 'image')

@admin.register(BreathingExercise)
class BreathingExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration')
    fields = ('title', 'description', 'instructions', 'duration', 'image')
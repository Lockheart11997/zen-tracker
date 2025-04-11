from django import forms
from .models import RestSession

class RestSessionForm(forms.ModelForm):
    class Meta:
        model = RestSession
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 'class': 'form-control'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 'class': 'form-control'
            }),
        }
        labels = {
            'start_time': 'Начало сессии',
            'end_time': 'Завершение сессии',
        }




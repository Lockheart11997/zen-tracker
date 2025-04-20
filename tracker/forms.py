from django import forms
from .models import RestSession, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Обязательно введите ваш email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        def clean_email(self):
            email = self.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Пользователь с таким email уже существует.")
            return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birth_date', 'bio', 'avatar']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','placeholder': 'дд.мм.гггг'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_POST
from .models import RestSession, Meditation, BreathingExercise, RelaxationTip
from .forms import RestSessionForm
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import F, Sum
from django.utils import timezone
from datetime import timedelta
import random

class RestSessionListView(LoginRequiredMixin, ListView):
    model = RestSession
    template_name = 'restsession_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        return RestSession.objects.filter(user=self.request.user).select_related('meditation', 'breathing_exercise').order_by('-start_time')

class RestSessionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = RestSession
    template_name = 'restsession_detail.html'

    def test_func(self):
        return self.get_object().user == self.request.user or self.request.user.is_staff


class RestSessionCreateView(LoginRequiredMixin, CreateView):
    model = RestSession
    form_class = RestSessionForm
    template_name = 'restsession_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('restsession_list')


class RestSessionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RestSession
    form_class = RestSessionForm
    template_name = 'restsession_form.html'
    success_url = reverse_lazy('restsession_list')

    def form_valid(self, form):
        if 'finish_now' in self.request.POST and not form.instance.end_time:
            form.instance.end_time = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('restsession_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.get_object().user == self.request.user or self.request.user.is_staff


class RestSessionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RestSession
    template_name = 'restsession_confirm_delete.html'
    success_url = reverse_lazy('restsession_list')

    def test_func(self):
        return self.get_object().user == self.request.user or self.request.user.is_staff

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class MeditationListView(LoginRequiredMixin, ListView):
    model = Meditation
    template_name = 'meditation_list.html'
    context_object_name = 'meditations'

class MeditationDetailView(LoginRequiredMixin, DetailView):
    model = Meditation
    template_name = 'meditation_detail.html'
    context_object_name = 'meditation'

    def post(self, request, *args, **kwargs):
        meditation = self.get_object()
        session_id = request.POST.get('session_id')
        session = get_object_or_404(RestSession, pk=session_id, user=request.user)
        session.meditation = meditation
        session.save()
        return redirect('restsession_detail', pk=session.pk)


class BreathingListView(LoginRequiredMixin, ListView):
    model = BreathingExercise
    template_name = 'breathing_list.html'
    context_object_name = 'exercises'

class BreathingDetailView(LoginRequiredMixin, DetailView):
    model = BreathingExercise
    template_name = 'breathing_detail.html'
    context_object_name = 'exercise'

    def post(self, request, *args, **kwargs):
        exercise = self.get_object()
        session_id = request.POST.get('session_id')
        session = get_object_or_404(RestSession, pk=session_id, user=request.user)
        session.breathing_exercise = exercise
        session.save()
        return redirect('restsession_detail', pk=session.pk)

def create_rest_session(request):
    if request.method == 'POST':
        form = RestSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user

            # Проверка: только один вид отдыха должен быть выбран
            if session.meditation and session.breathing_exercise:
                form.add_error(None, 'Выберите только медитацию ИЛИ дыхательное упражнение.')
            elif not session.meditation and not session.breathing_exercise:
                form.add_error(None, 'Выберите хотя бы один вид отдыха.')
            else:
                session.save()
                return redirect('restsession_list')
    else:
        form = RestSessionForm()

    return render(request, 'restsession_form.html', {'form': form})

@login_required
def home_view(request):
    # Получение всех подсказок
    tips = RelaxationTip.objects.all()
    random_tip = random.choice(tips) if tips else None

    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    sessions = RestSession.objects.filter(user=request.user)
    active_sessions = sessions.filter(end_time__isnull=True).order_by('-start_time')
    completed_sessions = sessions.filter(end_time__isnull=False).order_by('-end_time')

    total_minutes = sessions.filter(
        end_time__isnull=False,
        start_time__gte=one_week_ago
    ).aggregate(
        total=Sum(F('end_time') - F('start_time'))
    )['total']

    if total_minutes:
        total_minutes = total_minutes.total_seconds() / 60
    else:
        total_minutes = 0

    return render(request, 'home.html', {
        'active_sessions': active_sessions,
        'completed_sessions': completed_sessions,
        'weekly_minutes': round(total_minutes),
        'random_tip': random_tip
    })

def select_exercise(request):
    return render(request, 'select_exercise.html')

@login_required
def start_meditation_session(request, pk):
    meditation = get_object_or_404(Meditation, pk=pk)
    RestSession.objects.create(
        user=request.user,
        meditation=meditation,
        start_time=timezone.now()
    )
    return redirect('restsession_list')

@login_required
def start_breathing_session(request, pk):
    exercise = get_object_or_404(BreathingExercise, pk=pk)
    RestSession.objects.create(
        user=request.user,
        breathing_exercise=exercise,
        start_time=timezone.now()
    )
    return redirect('restsession_list')

@require_POST
@login_required
def end_session_now(request, pk):
    session = get_object_or_404(RestSession, pk=pk, user=request.user)
    if session.end_time is None:
        session.end_time = timezone.now()
        session.save()
    return redirect('home')

@login_required
def statistics_view(request):
    user_sessions = RestSession.objects.filter(user=request.user)

    meditation_sessions = user_sessions.filter(meditation__isnull=False)
    meditation_count = meditation_sessions.count()

    breathing_sessions = user_sessions.filter(breathing_exercise__isnull=False)
    breathing_count = breathing_sessions.count()

    meditation_time = meditation_sessions.aggregate(total_time=Sum(F('end_time') - F('start_time')))['total_time']
    breathing_time = breathing_sessions.aggregate(total_time=Sum(F('end_time') - F('start_time')))['total_time']

    def convert_to_minutes(time_delta):
        if time_delta:
            return int(time_delta.total_seconds() / 60)  # Переводим в целые минуты
        return 0

    meditation_time_in_minutes = convert_to_minutes(meditation_time)
    breathing_time_in_minutes = convert_to_minutes(breathing_time)

    # Общие статистики
    total_sessions = user_sessions.count()
    total_time = user_sessions.aggregate(total_time=Sum(F('end_time') - F('start_time')))['total_time']
    total_time_in_minutes = convert_to_minutes(total_time)

    # Подаём данные в шаблон
    context = {
        'meditation_count': meditation_count,
        'breathing_count': breathing_count,
        'meditation_time': meditation_time_in_minutes,
        'breathing_time': breathing_time_in_minutes,
        'total_sessions': total_sessions,
        'total_time': total_time_in_minutes
    }

    return render(request, 'statistics.html', context)

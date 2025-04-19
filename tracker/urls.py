from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('select/', views.select_exercise, name='select_exercise'),
    path('statistics/', views.statistics_view, name='statistics'),

    path('session/<int:pk>/', views.RestSessionDetailView.as_view(), name='restsession_detail'),
    path('session/new/', views.RestSessionCreateView.as_view(), name='restsession_create'),
    path('session/<int:pk>/edit/', views.RestSessionUpdateView.as_view(), name='restsession_update'),
    path('session/<int:pk>/delete/', views.RestSessionDeleteView.as_view(), name='restsession_delete'),
    path('session/<int:pk>/end/', views.end_session_now, name='end_session_now'),

    path('meditations/', views.MeditationListView.as_view(), name='meditation_list'),
    path('meditations/<int:pk>/', views.MeditationDetailView.as_view(), name='meditation_detail'),
    path('meditations/<int:pk>/start/', views.start_meditation_session, name='start_meditation_session'),

    path('breathing/', views.BreathingListView.as_view(), name='breathing_list'),
    path('breathing/<int:pk>/', views.BreathingDetailView.as_view(), name='breathing_detail'),
    path('breathing/<int:pk>/start/', views.start_breathing_session, name='start_breathing_session'),
]

from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', RestSessionListView.as_view(), name='restsession_list'),
    path('session/<int:pk>/', RestSessionDetailView.as_view(), name='restsession_detail'),
    path('session/new/', RestSessionCreateView.as_view(), name='restsession_create'),
    path('session/<int:pk>/edit/', RestSessionUpdateView.as_view(), name='restsession_update'),
    path('session/<int:pk>/delete/', RestSessionDeleteView.as_view(), name='restsession_delete'),
    path('session/<int:pk>/end/', views.end_session_now, name='end_session_now'),
    path('select/', views.select_exercise, name='select_exercise'),
    path('meditations/', views.meditation_list, name='meditation_list'),
    path('meditations/<int:pk>/', views.meditation_detail, name='meditation_detail'),
    path('meditations/<int:pk>/start/', views.start_meditation_session, name='start_meditation_session'),
    path('breathing/', views.breathing_list, name='breathing_list'),
    path('breathing/<int:pk>/', views.breathing_detail, name='breathing_detail'),
    path('breathing/<int:pk>/start/', views.start_breathing_session, name='start_breathing_session'),
    path('statistics/', views.statistics_view, name='statistics'),
]

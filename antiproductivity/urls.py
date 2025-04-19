from django.contrib import admin
from django.urls import path, include
from tracker import views as tracker_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from tracker.views import activate_account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', tracker_views.register, name='register'),   # потому, что изменил страницу регистрации

    path('', include('tracker.urls')),
    path('sessions/', tracker_views.RestSessionListView.as_view(), name='restsession_list'),

    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # для картинок

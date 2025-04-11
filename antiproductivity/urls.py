from django.contrib import admin
from django.urls import path, include
from tracker import views as tracker_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', tracker_views.register, name='register'),
    path('', tracker_views.home_view, name='home'),
    path('', include('tracker.urls')),
    path('sessions/', tracker_views.RestSessionListView.as_view(), name='restsession_list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

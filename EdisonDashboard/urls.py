from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from configuration.views import *
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="homepage"),
    path('user/', include('users.urls')),
    path('edit/', include('graphics.urls')),
    path('api/', include('api.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),
    ]

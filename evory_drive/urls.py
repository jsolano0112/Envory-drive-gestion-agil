from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from src.views.views import custom_404_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('src.urls')),
    
]

handler404 = custom_404_view

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

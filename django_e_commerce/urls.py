from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('dashboard/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('product.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+\
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




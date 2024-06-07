from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.shortcuts import render

import config.settings as settings
from django.conf.urls.static import static


def page404(request, exception):
    return render(request, 'components/_error.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('market.urls')),
    path('', include('profiles.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page404


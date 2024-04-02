from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('words.urls')),
    path('admin/', admin.site.urls),
]

handler404 = 'words.views.page_not_found'
handler500 = 'words.views.server_error'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

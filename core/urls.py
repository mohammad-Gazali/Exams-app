from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('my-accounts/', include('accounts.urls')),


    # for google authentication
    path('accounts/', include('allauth.urls')),

    # for translating
    path('i18n/', include('django.conf.urls.i18n')),

    # for email vertification
    path('verification/', include('verify_email.urls')),

    # for ckeditor uploading images
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

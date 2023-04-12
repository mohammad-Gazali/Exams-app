from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # admin urls
    path('admin/', admin.site.urls),

    # my apps
    path('', include('main.urls')),
    path('my-accounts/', include('accounts.urls')),
    path('exams/', include('exams.urls')),


    # for google authentication
    path('accounts/', include('allauth.urls')),

    # for translating
    path('i18n/', include('django.conf.urls.i18n')),

    # for email vertification
    path('verification/', include('verify_email.urls')),

    # for ckeditor uploading images
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # TODO: Remove After Finishing Development
    # debug toolbar
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

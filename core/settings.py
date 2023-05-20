from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-w)d&do%u%21n6au6x%cmj-xwr3n8an1zn0#840j-j7o5mk!!-d"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # for human readable time
    "django.contrib.humanize",
    # my apps
    "main.apps.MainConfig",
    "accounts.apps.AccountsConfig",
    "exams.apps.ExamsConfig",
    "courses.apps.CoursesConfig",
    "blog.apps.BlogConfig",
    # for authentication with google
    "django.contrib.sites",
    # * ====== 3rd party libraries =======
    # all auth for google authentication
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # verifying emails
    "verify_email.apps.VerifyEmailConfig",
    # for google recaptcha protection
    "captcha",
    # for rich text editor
    "ckeditor",
    "ckeditor_uploader",
    # for phone number field
    "phonenumber_field",
    # TODO: Remove After Finishing Development
    # debug toolbar
    "debug_toolbar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # TODO: Remove After Finishing Development
    # debug toolbar
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # my context processor
                "main.context_processor.my_context",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# for postgresql database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'DB_NAME', 
#         'USER': 'DB_USER',
#         'PASSWORD': 'DB_PASSWORD',
#         'HOST': 'DB_HOST', 
#         'PORT': 'DB_PORT',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# * initial language
LANGUAGE_CODE = "en"

# * available languages code and its name
LANGUAGES = [
    ("ar", "العربية"),
    ("en", "English"),
]


TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# for auth process
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/my-accounts/login"


# for google authentication
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}


# for email sending

# ? for test sending emails
EMAIL_HOST = "sandbox.smtp.mailtrap.io"
EMAIL_HOST_USER = "f4eda1bd63acd9"
EMAIL_HOST_PASSWORD = "477b6fc5247f3a"
EMAIL_PORT = "2525"


# * Real Configration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_ID')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PW')
DEFAULT_FROM_EMAIL = "no_reply@test.com"


# for email vertification
VERIFICATION_SUCCESS_TEMPLATE = "registration/success.html"
VERIFICATION_FAILED_TEMPLATE = "registration/failed.html"
HTML_MESSAGE_TEMPLATE = "email/email_vertification.html"


# for recaptcha
RECAPTCHA_PUBLIC_KEY = "6LdSKPUkAAAAAD1LFMX85P-spSKo7CYGurT3zMV0"
RECAPTCHA_PRIVATE_KEY = "6LdSKPUkAAAAAL2Jb6Ht8BZl37HvM5UtKDE6aMzZ"
SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]


# for ckeditor package
CKEDITOR_UPLOAD_PATH = "ckeditor-uploads/"


CKEDITOR_CONFIGS = {
    "default": {
        "height": 100,
        "width": "100%",
    },
}

# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': 'Custom',
#         'toolbar_Custom': [
#             ['Bold', 'Italic', 'Underline'],
#             ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
#             ['Link', 'Unlink'],
#             ['RemoveFormat', 'Source']
#         ]
#     }
# }

# CKEDITOR_CONFIGS = {
#     'default': {
#         'skin': 'moono',
#         # 'skin': 'office2013',
#         'toolbar_Basic': [
#             ['Source', '-', 'Bold', 'Italic']
#         ],
#         'toolbar_YourCustomToolbarConfig': [
#             {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
#             {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
#             {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
#             {'name': 'forms','items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField']},
#             '/',
#             {'name': 'basicstyles',
#              'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
#             {'name': 'paragraph',
#              'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
#                        'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
#                        'Language']},
#             {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
#             {'name': 'insert',
#              'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
#             '/',
#             {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
#             {'name': 'colors', 'items': ['TextColor', 'BGColor']},
#             {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
#             {'name': 'about', 'items': ['About']},
#             '/',  # put this to force next toolbar on new line
#             {'name': 'yourcustomtools', 'items': [
#                 # put the name of your editor.ui.addButton here
#                 'Preview',
#                 'Maximize',

#             ]},
#         ],
#         'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
#         # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
#         # 'height': 291,
#         'width': '100%',
#         # 'filebrowserWindowHeight': 725,
#         # 'filebrowserWindowWidth': 940,
#         # 'toolbarCanCollapse': True,
#         # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
#         'tabSpaces': 4,
#         'extraPlugins': ','.join([
#             'uploadimage', # the upload image feature
#             # your extra plugins here
#             'div',
#             'autolink',
#             'autoembed',
#             'embedsemantic',
#             'autogrow',
#             # 'devtools',
#             'widget',
#             'lineutils',
#             'clipboard',
#             'dialog',
#             'dialogui',
#             'elementspath'
#         ]),
#     }
# }


# * CONSTANTS
G_WEBSITE_URL = "http://localhost:8000"
CONTACT_EMAIL = "contact@test.com"


# TODO: Remove After Finishing Development
# for debug toolbar
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

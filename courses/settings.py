import os
import django.conf.global_settings as DEFAULT_SETTINGS
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# GIT USERS: some information from this file has been scrubbed from the
# repository for privacy reasons. However, an effort has been made to publish
# all necessary information in order for this project to be setup without much
# reconstruction. Details of information have been noted where redactions have
# been made.

# SECRET_KEY is scrubbed

# SOCIAL_AUTH_GOOGLE_OAUTH2 KEY and SECRET are scrubbed
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['cnu.edu']
# SOCIAL_AUTH_FACEBOOK KEY and SECRET are scrubbed
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/account/error/'

DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['courses.gravitydevelopment.net']

INSTALLED_APPS = (
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-Party Apps
    'social.apps.django_app.default',
    'django_tables2',
    'tastypie',
    # Custom Apps
    'course',
    'schedule',
    'account',
    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

ROOT_URLCONF = 'courses.urls'

WSGI_APPLICATION = 'courses.wsgi.application'

DATABASES = {
    'default': {
        # Database connection details are scrubbed
}

# SMTP connection details are scrubbed
EMAIL_USE_TLS = True

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    BASE_DIR + '/courses/static/',
)

TEMPLATE_DIRS = (
    BASE_DIR + '/courses/templates/',
)

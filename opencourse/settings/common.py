import os
import django.conf.global_settings as DEFAULT_SETTINGS
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# GIT USERS: some information from this file has been scrubbed from the
# repository for privacy reasons. However, an effort has been made to publish
# all necessary information in order for this project to be setup without much
# reconstruction. Details of information have been noted where redactions have
# been made.

# SECRET_KEY scrubbed

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY scrubbed
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET scrubbed
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['cnu.edu']
# SOCIAL_AUTH_FACEBOOK_KEY scrubbed
# SOCIAL_AUTH_FACEBOOK_SECRET scrubbed
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/account/error/'

SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'hd': 'cnu.edu',
}

LOGIN_URL = '/account/'

DEBUG = False

TEMPLATE_DEBUG = DEBUG

MAINTENANCE_MODE = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/logs/app.log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'opencourse': {
            'handlers': ['file'],
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
}

ALLOWED_HOSTS = [
    '.opencourseproject.com',
]

SESSION_COOKIE_DOMAIN = '.opencourseproject.com'

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
    'djangosecure',
    'kronos',
    'maintenancemode',
    # Custom Apps
    'opencourse',
    'course',
    'schedule',
    'account',
    'api',
    'updates',
)

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'maintenancemode.middleware.MaintenanceModeMiddleware',
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
    'opencourse.context.report',
    'opencourse.context.api',
    'opencourse.context.school_info',
    'opencourse.context.domain',
)

ROOT_URLCONF = 'opencourse.urls'

WSGI_APPLICATION = 'opencourse.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SCHOOL_NAME = 'Christopher Newport University'
SCHOOL_ABBREVIATION = 'CNU'
SCHOOL_WEBSITE = 'http://cnu.edu'

STATIC_ROOT = BASE_DIR + '/static/'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '/static/'),
)

TEMPLATE_DIRS = (
    BASE_DIR + '/templates/',
)

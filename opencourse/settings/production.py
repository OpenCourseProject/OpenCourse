from __future__ import absolute_import
from .common import *

DATABASES = {
    'default': {
        # 'ENGINE' scrubbed
        # 'NAME' scrubbed
        # 'USER' scrubbed
        # 'PASSWORD' scrubbed
        # 'HOST' scrubbed
        # 'PORT' scrubbed
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 5
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

os.environ['wsgi.url_scheme'] = 'https'

EMAIL_USE_TLS = True
# EMAIL_HOST scrubbed
# EMAIL_PORT scrubbed
# EMAIL_HOST_USER scrubbed
# EMAIL_HOST_PASSWORD scrubbed
SERVER_EMAIL = 'admin@opencourseproject.com'
EMAIL_SUBJECT_PREFIX = '[OpenCourse] '

from .base import *

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/


MEDIA_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

HOST_NAME = 'localhost'
HOST_PORT = '8000'
SITE_URL = HOST_NAME + ':' + HOST_PORT

#  -------EMAIL----------
if 1:
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = '1025'
    DEFAULT_FROM_EMAIL = 'support.semisklad.com'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.mail.ru'
    EMAIL_PORT = '2525'
    EMAIL_HOST_USER = 'dingo_dnu@mail.ru'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    SERVER_EMAIL = EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = 'rm-02-01'

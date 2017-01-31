from .base import *

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = '1025'

HOST_NAME = 'localhost'
HOST_PORT = '8000'

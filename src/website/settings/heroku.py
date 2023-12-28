from .default import *

# SECURITY

# WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split(',')

# WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# HTTPS settings
SECURE_SSL_REDIRECT = True

# HSTS settings
SECURE_HSTS_SECONDS = 31536000  # year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


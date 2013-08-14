SITE_ID = 1
STATIC_URL = '/static/'
# ROOT_URLCONF = 'django_uuid_pk.tests.urls'
SECRET_KEY = ';klkj;okj;lkn;lklj;lkj;kjmlliuewhy2ioqwjdkh'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django_uuid_pk.sqlite',
        'HOST': '',
        'PORT': ''}}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)-8s: %(asctime)s %(name)10s: %(funcName)40s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
}

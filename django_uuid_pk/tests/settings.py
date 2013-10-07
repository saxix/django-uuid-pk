import os

SITE_ID = 1
STATIC_URL = '/static/'
SECRET_KEY =';pkj;lkj;lkjh;lkj;oi'
db = os.environ.get('DBENGINE', None)
if db == 'pg':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'django_uuid_pk',
            'HOST': '127.0.0.1',
            'PORT': '',
            'USER': 'postgres',
            'PASSWORD': '',
            'OPTIONS': {
                'autocommit': True, # same value for all versions of django (is the default in 1.6)
            }}}
elif db == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'django_uuid_pk',
            'HOST': '127.0.0.1',
            'PORT': '',
            'USER': 'aa',
            'PASSWORD': ''}}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'django_uuid_pk.sqlite',
            'HOST': '',
            'PORT': ''}}

INSTALLED_APPS = ('django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.sites',
                  'django_uuid_pk.tests')

ALLOWED_HOSTS = ('127.0.0.1',)

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

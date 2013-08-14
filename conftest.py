import os
import sys
from django.conf import settings


def pytest_configure(config):
    if not settings.configured:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'django_uuid_pk.tests.settings'

        settings.configure(INSTALLED_APPS=('django.contrib.auth',
                                           'django.contrib.contenttypes',
                                           'django.contrib.sessions',
                                           'django.contrib.sites',
                                           'django.contrib.auth',
                                           'django_uuid_pk.tests'),
                           SECRET_KEY = ';klkj;okj;lkn;lklj;lkj;kjmlliuewhy2ioqwjdkh',
                           DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                                                  'NAME': 'django_uuid_pk.sqlite',
                                                  'HOST': '',
                                                  'PORT': ''}})

    settings.ALLOWED_HOSTS = ('127.0.0.1',)

    test_db = os.environ.get('DBENGINE', 'sqlite')

    if test_db == 'postgres':
        settings.DATABASES['default'].update({
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',
            'NAME': 'django_uuid_pk',
            'OPTIONS': {'autocommit': True}
        })
    elif test_db == 'mysql':
        settings.DATABASES['default'].update({
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'root',
            'NAME': 'django_uuid_pk',
        })
    elif test_db == 'sqlite':
        settings.DATABASES['default'].update({
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        })


def runtests(args=None):
    import pytest

    if not args:
        args = []

    if not any(a for a in args[1:] if not a.startswith('-')):
        args.append('django_uuid_pk/tests')

    sys.exit(pytest.main(args))


if __name__ == '__main__':
    runtests(sys.argv)

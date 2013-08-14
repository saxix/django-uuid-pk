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
                                           'django_uuid_pk.tests'))

    settings.ALLOWED_HOSTS = ('127.0.0.1',)
    settings.SECRET_KEY = '123',

    test_db = os.environ.get('DBENGINE', 'sqlite')

    if test_db == 'postgres':
        settings.DATABASES['default'].update({
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',
            'NAME': 'django_uuid_pk',
            'OPTIONS': {'autocommit': True}
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

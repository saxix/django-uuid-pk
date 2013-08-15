#!/usr/bin/env python
import os
from setuptools import setup, find_packages
import django_uuid_pk as app

NAME = app.NAME
RELEASE = app.get_version()


def fread(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=NAME,
    version=RELEASE,
    url='https://github.com/saxix/django-uuid-pk',
    download_url='https://github.com/saxix/django-uuid-pk',
    author='sax',
    author_email='sax@os4d.org',
    description="Django UUIDField with full primary-key protocol support",
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['uuid'],
    zip_safe=False,
    platforms=['any'],
    command_options={
        'build_sphinx': {
            'version': ('setup.py', app.VERSION),
            'release': ('setup.py', app.VERSION)}
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Intended Audience :: Developers'],
    long_description=open('README.rst').read()
)

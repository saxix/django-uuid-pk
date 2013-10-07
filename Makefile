VERSION=2.0.0
BUILDDIR=~build
DJANGO_14=django==1.4.8
DJANGO_15=django==1.5.4
DJANGO_16=https://www.djangoproject.com/m/releases/1.6/Django-1.6b4.tar.gz
DJANGO_DEV=git+git://github.com/django/django.git

mkbuilddir:
	mkdir -p ${BUILDDIR}

install-deps:
	pip install -r django_uuid_pk/requirements.pip python-coveralls coverage

test:
	py.test -vv

clean:
	rm -fr ~build dist wfp_foodnet.egg-info .coverage .pytest MEDIA_ROOT MANIFEST *.egg .cache
	find . -name __pycache__ -prune | xargs rm -rf
	find . -name "*.py?" -prune | xargs rm -rf
	rm -rf pep8.out flake.out coverage.xml pytest.xml

fullclean: clean
	find . -name *.sqlite -prune | xargs rm -rf
	rm -fr .tox

coverage:
	py.test --cov=django_uuid_pk --cov-config=django_uuid_pk/tests/.coveragerc
ifdef BROWSE
	firefox ${BUILDDIR}/coverage/index.html
endif


init-db:
	@sh -c "if [ '${DBENGINE}' = 'mysql' ]; then mysql -e 'DROP DATABASE IF EXISTS django_uuid_pk;'; fi"
	@sh -c "if [ '${DBENGINE}' = 'mysql' ]; then pip install MySQL-python; fi"
	@sh -c "if [ '${DBENGINE}' = 'mysql' ]; then mysql -e 'create database IF NOT EXISTS django_uuid_pk;'; fi"

	@sh -c "if [ '${DBENGINE}' = 'pg' ]; then psql -c 'DROP DATABASE IF EXISTS django_uuid_pk;' -U postgres; fi"
	@sh -c "if [ '${DBENGINE}' = 'pg' ]; then psql -c 'CREATE DATABASE django_uuid_pk;' -U postgres; fi"
	@sh -c "if [ '${DBENGINE}' = 'pg' ]; then pip install -q psycopg2; fi"

ci: mkbuilddir
	@sh -c "if [ '${DJANGO}' = '1.4.x' ]; then pip install ${DJANGO_14}; fi"
	@sh -c "if [ '${DJANGO}' = '1.5.x' ]; then pip install ${DJANGO_15}; fi"
	@sh -c "if [ '${DJANGO}' = '1.6.x' ]; then pip install ${DJANGO_16}; fi"
	@sh -c "if [ '${DJANGO}' = 'dev' ]; then pip install ${DJANGO_DEV}; fi"
	@pip install coverage
	@python -c "from __future__ import print_function;import django;print('Django version:', django.get_version())"
	@echo "Database:" ${DBENGINE}

	py.test -vv --cov=django_uuid_pk --cov-report=html --cov-config=.coveragerc


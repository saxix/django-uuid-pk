VERSION=2.0.0
BUILDDIR=~build

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
	py.test --cov=django_uuid_pk --cov-report=html --cov-config=django_uuid_pk/tests/.coveragerc
ifdef BROWSE
	firefox ${BUILDDIR}/coverage/index.html
endif

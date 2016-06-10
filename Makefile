VIRTUALENV = virtualenv
VENV := $(shell echo $${VIRTUAL_ENV-.venv})
PYTHON = $(VENV)/bin/python
INSTALL_STAMP = $(VENV)/.install.stamp
TEMPDIR := $(shell mktemp -d)

.IGNORE: clean distclean maintainer-clean
.PHONY: all install virtualenv tests

OBJECTS = .venv .coverage

all: install
install: $(INSTALL_STAMP)
$(INSTALL_STAMP): $(PYTHON) setup.py
	$(VENV)/bin/pip install -U pip
	$(VENV)/bin/pip install -Ur dev-requirements.txt
	$(VENV)/bin/pip install -Ue .
	touch $(INSTALL_STAMP)

virtualenv: $(PYTHON)
$(PYTHON):
	virtualenv $(VENV)

build-requirements:
	$(VIRTUALENV) $(TEMPDIR)
	$(TEMPDIR)/bin/pip install -U pip
	$(TEMPDIR)/bin/pip install -Ue .
	$(TEMPDIR)/bin/pip freeze > requirements.txt

tests-once: install
	$(VENV)/bin/tox -e py27

tests:
	$(VENV)/bin/tox

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -fr
	find . -name '*flymake*' -delete

distclean: clean
	rm -fr *.egg *.egg-info/

maintainer-clean: distclean
	rm -fr $(OBJECTS) .tox/ dist/ build/

run-kinto: install
	$(VENV)/bin/kinto --ini config/kinto.ini migrate
	$(VENV)/bin/kinto --ini config/kinto.ini start

need-kinto-running:
	@curl http://localhost:8888/v1/ 2>/dev/null 1>&2 || (echo "Run 'make run-kinto' before starting tests." && exit 1)

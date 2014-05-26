# Some simple testing tasks (sorry, UNIX only).

PYTHON ?= python3
FLAKE=pyflakes3
PEP=pep8


doc:
	make -C docs html
	echo "open file://`pwd`/docs/_build/html/index.html"

pep:
	$(FLAKE) aiorest tests examples
	$(PEP) aiorest tests examples

test:
	$(PYTHON) runtests.py

vtest:
	$(PYTHON) runtests.py -v

testloop:
	$(PYTHON) runtests.py --forever

cov cover coverage:
	$(PYTHON) runtests.py --coverage

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f .coverage
	rm -rf coverage

.PHONY: all doc pep test vtest testloop cov clean

# Some simple testing tasks (sorry, UNIX only).

PYTHON ?= python3.3
FLAKE=pyflakes3


pep:
	$(FLAKE) aiorest tests

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

.PHONY: all pep test vtest testloop cov clean

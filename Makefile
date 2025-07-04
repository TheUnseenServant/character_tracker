# Makefile

SHELL = /usr/bin/bash

.PHONY:test
test:
	python -m unittest

coverage: test
	coverage run -m unittest
	coverage report -m 

clean:
	find . -type f -name "*.pyc" -exec rm {} \;
	find . -type f -name "*.swp" -exec rm {} \;

format: clean
	python -m black -l 79 .
	-flake8 --ignore E251,E266,W391,W503 --exclude venv

all: format coverage
	semgrep --config "p/default"


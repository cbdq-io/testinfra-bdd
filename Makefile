all: lint build test

build:
	PYTHONPATH=. python3 -m build
	PYTHONPATH=. gitchangelog > CHANGELOG.md

lint:
	yamllint -s .
	flake8

test:
	PYTHONPATH=.:.. pytest

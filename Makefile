all: build # test

build:
	PYTHONPATH=. python3 -m build
	PYTHONPATH=. gitchangelog > CHANGELOG.md

test:
	PYTHONPATH=.:.. pytest

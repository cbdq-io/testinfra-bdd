all: lint test build

build: changelog
	PYTHONPATH=. python3 -m build

changelog:
	PYTHONPATH=. gitchangelog > CHANGELOG.md

clean:
	rm -rf dist
	docker-compose -f tests/resources/docker-compose.yml down -t 0 -v

lint:
	docker run --rm -i hadolint/hadolint < tests/resources/sut/Dockerfile
	yamllint -s .
	flake8 --radon-no-assert
	bandit -r .

test:
	docker-compose -f tests/resources/docker-compose.yml up -d --build
	PYTHONPATH=.:.. pytest

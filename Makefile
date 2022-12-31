all: lint build test

build: changelog
	cut -d= -f1 requirements.txt > tests/resources/requirements-latest.txt
	PYTHONPATH=. python3 -m build

changelog:
	PYTHONPATH=. gitchangelog > CHANGELOG.md

clean:
	rm -rf dist
	docker-compose -f tests/resources/docker-compose.yml down -t 0 -v

lint:
	docker run --rm -i hadolint/hadolint < tests/resources/sut/Dockerfile
	yamllint -s .
	flake8 --radon-max-cc 5
	bandit -r .

test:
	docker-compose -f tests/resources/docker-compose.yml up -d --build
	docker-compose -f tests/resources/docker-compose.yml exec -T sut /usr/local/bin/install-dist-package.sh
	PYTHONPATH=.:.. pytest

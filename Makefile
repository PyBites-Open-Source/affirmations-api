.PHONY: setup
setup:
	python3.9 -m venv venv && source venv/bin/activate && pip install -r requirements/dev.txt

.PHONY: run
run:
	source venv/bin/activate && uvicorn affirmations.main:app --reload

.PHONY: lint
lint:
	flake8 --exclude venv

.PHONY: typing
typing:
	mypy affirmations tests

.PHONY: test
test:
	pytest

.PHONY: coverage
coverage:
	pytest --cov=affirmations --cov-report term-missing

.PHONY: ci
ci: lint typing coverage

.PHONY: precommit
precommit:
	pre-commit install

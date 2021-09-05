.PHONY: setup
setup:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements/dev.txt

.PHONY: lint
lint:
	flake8 --exclude venv

.PHONY: typing
typing:
	mypy affirmations tests

.PHONY: test
test:
	pytest

.PHONY: ci
ci: lint typing test

.PHONY: precommit
precommit:
	pre-commit install

.PHONY: run
run:
	uvicorn affirmations.main:app --reload

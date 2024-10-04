.PHONY: setup
setup:
	uv sync

.PHONY: run
run:
	uv run fastapi dev affirmations/main.py

.PHONY: typing
typing:
	uv run mypy affirmations tests

.PHONY: test
test:
	uv run pytest --cov=affirmations --cov-report term-missing

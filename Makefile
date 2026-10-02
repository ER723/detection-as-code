.PHONY: test lint

test:
	pytest -v

lint:
	ruff check .

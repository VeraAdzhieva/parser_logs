.PHONY lint test test-cov

lint:
	pre-commit run --all-files

test:
	pytest tests

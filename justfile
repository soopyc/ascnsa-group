dev:
	pdm run flask run --debug

check:
	pdm run ruff check
	pdm run ruff format --check

format:
	pdm run ruff format

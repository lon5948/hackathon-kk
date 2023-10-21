help:
	@echo "lint - Run isort, black and flake8."

lint:
	isort --line-length 79 --profile black .
	black --line-length 79 .
	flake8 --ignore=E203,E501,W503 --exclude venv
.PHONY: install format lint test dbt-parse docker-build ci

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi

format:
	black .

lint:
	flake8 . --exclude .git,.github,.venv,__pycache__,logs,data,batch/source,batch/landing,fraud_gold/target,fraud_gold/dbt_packages

test:
	pytest

dbt-parse:
	dbt deps --project-dir fraud_gold
	dbt parse --project-dir fraud_gold
	dbt compile --project-dir fraud_gold

docker-build:
	docker compose build

ci: lint test dbt-parse docker-build

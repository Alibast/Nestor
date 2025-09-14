.PHONY: run test api lint
run:
	python -m apps.cli

api:
	uvicorn apps.fastapi_app:app --reload --port 8000

test:
	pytest -q

ingest-jokes:
	python scripts/ingest_jokes.py --path data/jokes

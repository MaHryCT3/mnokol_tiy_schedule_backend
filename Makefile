run:
	uvicorn app:app --port 443

run-dev:
	uvicorn app:app --reload --port 443
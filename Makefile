run-production:
	uvicorn app:app --port 4430 --host 0.0.0.0

run-dev:
	uvicorn app:app --reload --port 443

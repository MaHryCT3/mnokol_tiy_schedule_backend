run-production:
	uvicorn app:app --port 443

run-dev:
	uvicorn app:app --reload --port 443

build:
	docker build -f '.\docker\fastapi\Dockerfile' -t "tiy-back"
.PHONY: help install run docker-build docker-up docker-down logs

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies using uv"
	@echo "  make run           - Run the Streamlit app locally"
	@echo "  make docker-build  - Build the Docker image"
	@echo "  make docker-up     - Run the app using Docker Compose"
	@echo "  make docker-down   - Stop Docker Compose services"
	@echo "  make logs          - View Docker Compose logs"

install:
	uv pip install -r requirements.txt

run:
	uv run streamlit run app.py

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

logs:
	docker-compose logs -f

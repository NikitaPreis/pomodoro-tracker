.DEFAULT_GOAL := help

HOST ?= 0.0.0.0
PORT ?= 8000

run: ## Run the application using uvicorn with provided arguments or defaults
	poetry run uvicorn main:app --host $(HOST) --port $(PORT) --reload

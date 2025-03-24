# Variables
FRONTEND_DIR := frontend
BACKEND_DIR := backend

# Frontend commands
.PHONY: test-frontend
test-frontend:
	cd $(FRONTEND_DIR) && npm test

.PHONY: lint-frontend
lint-frontend:
	cd $(FRONTEND_DIR) && npm run lint

.PHONY: format-frontend
format-frontend:
	cd $(FRONTEND_DIR) && npm run format

# Backend commands
.PHONY: test-backend
test-backend:
	cd $(BACKEND_DIR) && go test -v ./...

.PHONY: lint-backend
lint-backend:
	cd $(BACKEND_DIR) && golangci-lint run

.PHONY: format-backend
format-backend:
	cd $(BACKEND_DIR) && go fmt ./...

# Combined commands
.PHONY: test-all
test-all: test-backend test-frontend

.PHONY: lint-all
lint-all: lint-backend lint-frontend

.PHONY: format-all
format-all: format-frontend format-backend

.PHONY: lint-format-frontend
lint-format-frontend: lint-frontend format-frontend

.PHONY: lint-format-backend
lint-format-backend: lint-backend format-backend

.PHONY: lint-format-all
lint-format-all: lint-all format-all

# Default target
.PHONY: all
all: lint-format-all test-all

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  test-frontend      - Run frontend tests"
	@echo "  test-backend       - Run backend tests" 
	@echo "  test-all          - Run all tests"
	@echo "  lint-frontend      - Run frontend linting"
	@echo "  lint-backend       - Run backend linting"
	@echo "  lint-all          - Run all linting"
	@echo "  format-frontend    - Format frontend code"
	@echo "  format-backend     - Format backend code"
	@echo "  format-all        - Format all code"
	@echo "  lint-format-frontend - Lint and format frontend"
	@echo "  lint-format-backend  - Lint and format backend"
	@echo "  lint-format-all    - Lint and format everything"
	@echo "  all               - Run all tests, lint and format"
	@echo "  help              - Show this help message"

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
ifeq ($(OS),Windows_NT)
	cd $(BACKEND_DIR) && powershell ./scripts/run_tests.ps1
else
	cd $(BACKEND_DIR) && ./scripts/run_tests.sh
endif

.PHONY: lint-backend
lint-backend:
ifeq ($(OS),Windows_NT)
	cd $(BACKEND_DIR) && powershell ./scripts/lint.ps1
else
	cd $(BACKEND_DIR) && ./scripts/lint.sh
endif

# Combined commands
.PHONY: test-all
test-all: test-backend test-frontend

.PHONY: lint-all
lint-all: lint-backend lint-frontend

.PHONY: format-all
format-all: format-frontend

# Default target
.PHONY: all
all: lint-all test-all

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  test-frontend   - Run frontend tests"
	@echo "  test-backend    - Run backend tests"
	@echo "  test-all       - Run all tests"
	@echo "  lint-frontend   - Run frontend linting"
	@echo "  lint-backend    - Run backend linting"
	@echo "  lint-all       - Run all linting"
	@echo "  format-frontend - Format frontend code"
	@echo "  format-all      - Format all code"
	@echo "  all            - Run all linting and tests"
	@echo "  help           - Show this help message"

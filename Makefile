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

# Docker commands
.PHONY: docker-up
docker-up:
	docker-compose up -d

.PHONY: docker-clean
docker-clean:
	docker-compose down

.PHONY: docker-clean-all
docker-clean-all:
	docker-compose down -v --rmi all --remove-orphans

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

# Documentation commands
DOCS_DIR := docs
MERMAID_CHARTS_DIR := $(DOCS_DIR)/mermaid-charts
IMAGES_DIR := $(DOCS_DIR)/images

.PHONY: install-deps
install-deps:
	npm install -g @mermaid-js/mermaid-cli
	npm install -g mkdirp

.PHONY: create-dirs
create-dirs:
	mkdirp "$(IMAGES_DIR)"

.PHONY: generate-diagrams
generate-diagrams:
	mmdc -i "$(MERMAID_CHARTS_DIR)/backend.mmd" -o "$(IMAGES_DIR)/backend-flow.svg"
	mmdc -i "$(MERMAID_CHARTS_DIR)/frontend.mmd" -o "$(IMAGES_DIR)/frontend-flow.svg"
	mmdc -i "$(MERMAID_CHARTS_DIR)/overview.mmd" -o "$(IMAGES_DIR)/overview-flow.svg"

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
	@echo "  docker-up         - Start services with docker-compose in detached mode"
	@echo "  docker-clean      - Stop and remove containers defined in docker-compose"
	@echo "  docker-clean-all  - Clean everything: volumes, images, and orphaned containers"
	@echo "  install-deps      - Install dependencies for generating diagrams"
	@echo "  create-dirs       - Create directories for diagrams"
	@echo "  generate-diagrams  - Generate PNG diagrams from Mermaid files"
	@echo "  all               - Run all tests, lint and format"
	@echo "  help              - Show this help message"

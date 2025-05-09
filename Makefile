# Variables
FRONTEND_DIR := frontend
BACKEND_DIR := backend
STATS_DIR := stats

# Frontend commands

.PHONY: dev-frontend
dev-frontend:
	cd $(FRONTEND_DIR) && npm run dev

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

.PHONY: dev-backend
dev-backend:
	cd $(BACKEND_DIR) && go run cmd/main.go

.PHONY: test-backend
test-backend:
	cd $(BACKEND_DIR) && go test -v ./...

.PHONY: lint-backend
lint-backend:
	cd $(BACKEND_DIR) && golangci-lint run

.PHONY: format-backend
format-backend:
	cd $(BACKEND_DIR) && go fmt ./...

# Stats commands
ruff:
	cd $(STATS_DIR) && ruff check . --fix --unsafe-fixes && ruff format .

mypy:
	cd $(STATS_DIR) && mypy . --strict --ignore-missing-imports

run-stats:
	cd $(STATS_DIR) && python runner.py

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

# Makefile for Ask Me Bot Project

COMPOSE = docker-compose
PROJECT_NAME = ask_me_bot

.PHONY: help postgres init-db start all down build logs bash

help:
	@echo ""
	@echo "Available commands:"
	@echo "  make all         - Full startup: postgres → init-db → app + nginx"
	@echo "  make postgres    - Start only PostgreSQL container"
	@echo "  make init-db     - Initialize the database (idempotent)"
	@echo "  make start       - Start web_admin, ask_me_bot and nginx"
	@echo "  make down        - Stop and remove all containers"
	@echo "  make build       - Build all docker images"
	@echo "  make logs        - Show all logs"
	@echo "  make bash        - Open shell in ask_me_bot container"
	@echo ""

# Step 1: Start only the PostgreSQL container
postgres:
	$(COMPOSE) up -d postgres

# Step 2: Run database migration (create tables)
init-db:
	$(COMPOSE) run --rm init_db

# Step 3: Start the application and nginx
start:
	$(COMPOSE) up -d web_admin ask_me_bot nginx

# Step 4: All in one
all: postgres init-db start

# Stop and remove containers
down:
	$(COMPOSE) down

# Build images
build:
	$(COMPOSE) build

# Show logs
logs:
	$(COMPOSE) logs -f

# Bash into ask_me_bot container
bash:
	$(COMPOSE) exec ask_me_bot bash

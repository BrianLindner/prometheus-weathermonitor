
SHELL := bash

.PHONY: all
all: help

.PHONY: setup
setup: venv  ## Setup Virtual Environment

.PHONY: install-modules
install-modules: ## Install required modules (either global or venv if you are using)
	pip install -r requirements.txt

.PHONY: venv
venv: install-venv
	python3 -m venv .venv-weather

.PHONY: help
help: ## Display help information of available options
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

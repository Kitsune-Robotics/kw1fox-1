.PHONY: help clean run build


help: ## Show this help.
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run: ## For local development pipenv
	pipenv run flask --app MissionController/main.py --debug run


docker: build ## For local development (docker)
	# docker-compose -f docker-compose.yml build && docker-compose -f docker-compose.yml up
	docker-compose -f docker-compose.yml up


build: ## Build container locally
	# Generate tag
	echo TAG=$(shell git rev-parse --abbrev-ref HEAD | sed 's/[^a-zA-Z0-9]/-/g') > .env

	# Build
	docker-compose build --build-arg GIT_COMMIT=$(shell git describe --abbrev=8 --always --tags --dirty) --build-arg DEBUG=True

clean: ## Clean All
	git clean -fdx
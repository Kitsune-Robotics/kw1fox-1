.PHONY: help clean run build

# Help
help:
	@echo " help    -         Prints this help."
	@echo " clean   -         Shortcut for git clean -fdX"
	@echo " build   -         Builds the required containers locally"
	@echo " run     -         Build and run the app locally"
	@echo " docker  -         Build and run the app using docker"

# For local development pipenv
run:
	pipenv run flask --app MissionController/main.py --debug run

# For local development (docker)
docker: build
	# docker-compose -f docker-compose.yml build && docker-compose -f docker-compose.yml up
	docker-compose -f docker-compose.yml up

# Build container locally
build:
	# Generate tag
	echo TAG=$(shell git rev-parse --abbrev-ref HEAD | sed 's/[^a-zA-Z0-9]/-/g') > .env

	# Build
	docker-compose build --build-arg GIT_COMMIT=$(shell git describe --abbrev=8 --always --tags --dirty) --build-arg DEBUG=True


clean:
	git clean -fdx
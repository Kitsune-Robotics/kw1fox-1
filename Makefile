# Makefile

up:
	docker compose up -d --build

restart:
	docker-compose stop $(CONTAINER)
	docker-compose up -d --build $(CONTAINER)
	docker-compose logs -f $(CONTAINER)

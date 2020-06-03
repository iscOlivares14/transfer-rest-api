.PHONY: tests

all: deps static

create_new_migration:
	# this uses Flask Migrate (Alembic) to create a new migration file based on the 
	# models file
	docker exec -it core python3 manage.py db migrate

run_migrations:
	# this will execute any migrations that have not been run before
	docker exec -it core python3 manage.py db upgrade

docker_rebuild:
	docker-compose -f docker-compose.yml down
	docker-compose -f docker-compose.yml up -d --build

tests:
	# run the tests in the test directory
	docker-compose -f docker-compose.yml down
	docker-compose -f docker-compose.yml up -d
	# Run tests
	docker exec -it core pytest tests

up:
	docker-compose -f docker-compose.yml down
	docker-compose -f docker-compose.yml up -d

restart_app:
	touch requirements.txt

api_shell:
	# this gives you a shell inside the API container
	docker exec -it core bash

postgres_shell:
	# this gives you a shell inside the postgres container
	docker exec -it postgres bash



all: migrate test
migrate:
	docker exec -it addressbook-api python manage.py migrate
test:
	docker exec -it addressbook-api python manage.py test
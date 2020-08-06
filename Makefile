all: migrate test
migrate:
	docker exec -it addressbook-api python manage.py migrate
test:
	docker exec -it addressbook-api python manage.py test
show_urls:
	docker exec -it addressbook-api python manage.py show_urls
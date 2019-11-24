dev:
	docker-compose up

initdb:
	docker-compose run app python manage.py migrate

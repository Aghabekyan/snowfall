migrations:
	docker-compose run --rm issue_tracker python3 manage.py makemigrations

migrate:
	docker-compose run --rm issue_tracker python3 manage.py migrate

shell:
	docker-compose run --rm issue_tracker python3 manage.py shell

test:
	docker-compose run --rm issue_tracker python3 manage.py test

flake8:
	docker-compose run --rm issue_tracker flake8 .

format:
	./format_python.sh

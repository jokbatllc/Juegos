lint:
	ruff check . --fix
	isort .
	black .

test:
	pytest -q

run:
	python manage.py runserver

seed:
	python manage.py seed_lexicon --per-lang 200 --langs es,en,fr

users:
	python manage.py setup_roles && python manage.py create_demo_users

up:
	docker compose --env-file .env up --build

up-prod:
	docker compose -f docker-compose.prod.yml --env-file .env up --build -d

down:
	docker compose down

migrate:
	docker compose exec web python manage.py migrate

createsuperuser:
	docker compose exec web python manage.py createsuperuser

shell:
	docker compose exec web python manage.py shell

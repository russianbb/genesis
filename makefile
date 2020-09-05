close:
	@echo "--> Close Docker."
	docker-compose down

develop:
	@echo "--> Creating Docker."
	docker-compose build ## --no-cache

bash:
	docker-compose run --rm web bash

run:
	@echo "--> Running Docker."
	docker-compose up

test: ## Run all tests (pytest).
	@echo "--> Testing on Docker."
	# docker-compose run --rm web py.test $(path) -s --cov-report term --cov-report html
	docker-compose run --rm web bash -c "cd ../../. && py.test -s --cov-report term --cov-report html"

create-migrate:
	@echo "--> Creating migrations on Docker."
	docker-compose run --rm web python manage.py makemigrations $(name)

run-migrate:
	@echo "--> Running migrations on Docker."
	docker-compose run --rm web python manage.py migrate

open-test:
	open htmlcov/index.html

create-app:
	@echo "--> Creating new app on Docker."
	docker-compose run --rm web python manage.py startapp $(name)

create-superuser:
	@echo "--> Creating superuser on Docker."
	docker-compose run --rm web python manage.py createsuperuser

merge-migration:
	@echo "--> Merging Migration."
	docker-compose run --rm web python manage.py makemigrations --merge

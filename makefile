run:
	@echo "--> Running Docker."
	docker-compose up

run-debug:
	@echo "--> Running Debug Mode with IPDB"
	docker-compose run --service-ports web

close:
	@echo "--> Close Docker."
	docker-compose down

build:
	@echo "--> Creating Docker."
	docker-compose build ## --no-cache -t genesis -f docker/dev/dockerfile .

bash:
	docker-compose run --rm web bash

test: ## Run all tests (pytest).
	@echo "--> Testing on Docker."
	# docker-compose run --rm web py.test $(path) -s --cov-report term --cov-report html
	docker-compose run --rm web bash -c "cd ../../. && py.test -s --cov-report term --cov-report html"

django-makemigrations:
	@echo "--> Creating migrations on Docker."
	docker-compose run --rm web python manage.py makemigrations $(name)

django-migrate:
	@echo "--> Running migrations on Docker."
	docker-compose run --rm web python manage.py migrate

open-test:
	open htmlcov/index.html

django-create-app:
	@echo "--> Creating new app on Docker."
	docker-compose run --rm web python manage.py startapp $(name)

django-create-superuser:
	@echo "--> Creating superuser on Docker."
	docker-compose run --rm web python manage.py createsuperuser

django-merge-migration:
	@echo "--> Merging Migration."
	docker-compose run --rm web python manage.py makemigrations --merge

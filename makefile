run:
	@echo "--> Running Docker."
	docker-compose up

run-debug:
	@echo "--> Running Debug Mode with IPDB"
	docker-compose run --service-ports web

run-extras:
	@echo "--> Running Docker with Extras"
	docker-compose --profile extras up

close:
	@echo "--> Close Docker."
	docker-compose down

build:
	@echo "--> Creating Docker."
	docker-compose build

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

shell-plus:
	@echo "--> Run shell plus from django-extensions"
	docker-compose run web python manage.py shell_plus

shell:
	@echo "--> Run shell plus from django-extensions"
	docker-compose run web python manage.py shell

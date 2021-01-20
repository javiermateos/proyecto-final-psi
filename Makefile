DOCKER = sudo docker-compose
CMD = python3 manage.py

build:
	$(DOCKER) up --no-start 

run:
	$(DOCKER) up

stop:
	$(DOCKER) down -v

update_db:
	$(DOCKER) exec web $(CMD) makemigrations core
	$(DOCKER) exec web $(CMD) migrate

populate:
	@echo populate database
	$(DOCKER) exec web $(CMD) populate all 19-edat_psi.csv 19-edat_2_psi.csv

create_super_user:
	$(DOCKER) exec web $(CMD) shell -c "from core.models import Student; Student.objects.create_superuser('alumnodb', 'a@a.es', 'alumnodb')"

test_datamodel:
	$(DOCKER) exec web $(CMD) test core.tests_models

test_services:
	$(DOCKER) exec web $(CMD) test core.tests_services

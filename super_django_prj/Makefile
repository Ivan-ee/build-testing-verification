run:
	cd recipe_project && python manage.py runserver

migrations:
	cd recipe_project && python manage.py makemigrations

migrate:
	cd recipe_project && python manage.py migrate

test:
	cd recipe_project && python manage.py test

test-report:
	cd recipe_project && coverage run manage.py test

report:
	cd recipe_project && coverage report

report-html:
	cd recipe_project && coverage html

docker-migrate:
	docker exec super_django_prj-django-1 python manage.py migrate

docker-test:
	docker exec super_django_prj-django-1 python manage.py test

docker-lint:
	docker exec super_django_prj-django-1  flake8


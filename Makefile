venv_path := ~/.venv/demo
bin_path := ${venv_path}/bin
all:
	@echo "Available commands: \n\
		make installdeps : to install virtualenv and other dependent packages\n\
		make install : to install virtualenv, other dependent packages, and make migrations \n\
		make adminuser : creates a superuser to access the django admin \n\
		make dev : runs django development server \n\
		make run : run the django application \n\
		make shell : activate the virtualenv with all required packages available in the environment \n\
		make lint : runs linters on all project files and shows the changes \n\
		make test : run the test suite  \n\
		make coverage : runs tests and creates a report of the coverage \n\
 	"

installdeps:
	python3 -m pip install virtualenv
	python3 -m venv ${venv_path}
	@echo ${bin_path}
	${bin_path}/pip3 install -r requirements.txt
	${bin_path}/pip3 install -r requirements_dev.txt

install: installdeps
	${bin_path}/python3 manage.py makemigrations
	${bin_path}/python3 manage.py migrate

dev:
	${bin_path}/python3 manage.py runserver

run: install
	# the default settings file is development, it can be changed
	# for any of the others, please don't use development setting in production
	export DJANGO_SETTINGS_MODULE=microservice.settings;\
	${bin_path}/gunicorn microservice.wsgi:application --bind localhost:8000

shell:
	@echo 'To activate the venv use source ~/.venv/demo/bin/activate . Use deactivate to exit'

lint:
	# starts a pipenv shell, shows autopep8 diff and then fixes the files
	# does the same for isort
	@echo '---Running autopep8---'
	${bin_path}/autopep8 demo -r -d
	${bin_path}/autopep8 demo -r -i
	@echo '---Running isort---'
	${bin_path}/isort demo --diff
	${bin_path}/isort demo --atomic

coverage:
	@echo 'Running tests and making coverage files'
	${bin_path}/coverage run manage.py test
	${bin_path}/coverage report
	${bin_path}/coverage html
	@echo 'to see the complete report, open index.html on the htmlcov folder'

adminuser:
	@echo 'creating Django admin user'
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
	User.objects.create_superuser('admin', '', '$(password)')" \
	| ${bin_path}/python3 manage.py shell
	@echo 'Username: admin , Password: $(password)'

test:
	@echo 'Running tests'
	${bin_path}/python3 manage.py test

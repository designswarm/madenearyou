
## Vagrant

If you have Vagrant installed, then doing this should set up a Vagrant box based on [this](https://github.com/philgyford/vagrant-heroku-cedar-14-python):

	$ vagrant up

If all goes well, access the local dev site at [http://localhost:5000/](http://localhost:5000/). This code repository will be linked to `/vagrant` on the Vagrant machine.

If setting up the database from scratch, run initial migrations and set the Django admin superuser:

	$ vagrant ssh
	vagrant$ cd /vagrant
	vagrant$ ./manage.py migrate
	vagrant$ ./manage.py createsuperuser

If you need/want to log into the postgres database then this will connect as a superuser:

	$ vagrant ssh
	vagrant$ sudo -u postgres psql madenearyou

Or connect as the app's database user:

	$ vagrant ssh
	vagrant$ PGUSER=madenearyou PGPASSWORD=madenearyou psql -h localhost madenearyou

Sleep the Vagrant box with:

	$ vagrant suspend

Or, shut down the box using:

	$ vagrant halt

Wake/start it again with:

	$ vagrant up --provision

Server logs will be in a `gunicorn.log` in this repository's directory.

### Notes

The install script should do this, but I had an occasion when I was getting this error while running migrations:

	django.db.utils.ProgrammingError: permission denied to create extension "postgis"

So I had to:
	
	$ vagrant ssh
	vagrant$ sudo -u postgres psql madenearyou
	madenearyou=# CREATE EXTENSION postgis;
	madenearyou=# \q


## Heroku

Create your app on Heroku.

Add the "Heroku Postgres" Add-on.

In the top level of your checked-out code, add Heroku as a git remote (replacing `your-app-name` with your app's name):

	$ heroku git:remote -a your-app-name 

Set the buildpacks for Python and the stuff required for GeoDjango:

	$ heroku buildpacks:set heroku/python
	$ heroku buildpacks:add https://github.com/cyberdelia/heroku-geo-buildpack.git#1.3

Set the environment variables (replacing `your-secret-key-here` with one for your site ([eg, from here](http://www.miniwebtool.com/django-secret-key-generator/)):

	$ heroku config:set DJANGO_SETTINGS_MODULE=madenearyou.settings.heroku
	$ heroku config:set config:set DJANGO_SECRET_KEY=your-secret-key-here

Push code to the server:

	$ git push heroku master

Enable PostGIS on the database:

	$ heroku pg:psql
	=> CREATE EXTENSION postgis;
	=> \q

If setting up the database from scratch, run initial migrations and set the Django admin superuser:

	$ heroku run python manage.py migrate
	$ heroku run python manage.py createsuperuser


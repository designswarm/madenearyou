
## Vagrant

If you have Vagrant installed, then doing this should set up a Vagrant box based on [this](https://github.com/philgyford/vagrant-heroku-cedar-14-python):

	$ vagrant up

If all goes well, access the local dev site at [http://localhost:5000/](http://localhost:5000/).

Shut down the box using:

	$ vagrant halt

Start it again with:

	$ vagrant up --provision

Server logs will be in a `gunicorn.log` in this repository's directory.


## Heroku

	$ heroku pg:psql
	=> CREATE EXTENSION postgis;



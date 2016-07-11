# Made Near You

Instructions for setting up on Vagrant (for local development) and Heroku.

## Vagrant

If you have Vagrant installed, then doing this should set up a Vagrant box based on [this](https://github.com/philgyford/vagrant-heroku-cedar-14-python):

	$ vagrant up

If all goes well, start the dev server manually by:

	$ vagrant ssh
	vagrant$ /vagrant/manage.py runserver 0.0.0.0:5000
	
Access the local dev site at [http://localhost:5000/](http://localhost:5000/). 

This code repository will be linked to `/vagrant` on the Vagrant machine.

For the Recaptcha on the Add Producer form to work, [sign up](https://www.google.com/recaptcha/intro/index.html), add a key, and add these to `/home/vagrant/.virtualenvs/made-near-you/bin/postactivate`:

	export RECAPTCHA_PUBLIC_KEY='YOUR-KEY'
	export RECAPTCHA_PRIVATE_KEY='YOUR-PRIVATE-KEY'
	
Probably need to restart the server to pick them up.

### Database
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

### Controlling the VM

Sleep the Vagrant box with:

	$ vagrant suspend

Or, shut down the box using:

	$ vagrant halt

Wake/start it again with:

	$ vagrant up

Re-run the scripts (if you change something), with:

	$ vagrant provision

### Other notes

The install script should do this, but I had an occasion when I was getting this error while running migrations:

	django.db.utils.ProgrammingError: permission denied to create extension "postgis"

So I had to:
	
	$ vagrant ssh
	vagrant$ sudo -u postgres psql madenearyou
	madenearyou=# CREATE EXTENSION postgis;
	madenearyou=# \q


## Heroku

**NOTE:** Currently using [an updated fork of django-storages](https://github.com/syapse/django-storages/tree/boto3-new) because the default version [doesn't currently support boto3](https://github.com/jschneier/django-storages/pull/111) (Python 3 version of boto) as a backend. When it does, we can switch to the default version. Will probably involve changing `runtime.txt` to a different python version, pushing to Heroku, changing it back, pushing again (to delete all python modules and reinstall).

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

**AND** don't forget to run that `migrate` command whenever pushing code with new migrations to Heroku!

For the Recaptcha on the Add Producer form to work, [sign up](https://www.google.com/recaptcha/intro/index.html), add a key, and add then:

	$ heroku config:set RECAPTCHA_PUBLIC_KEY=YOUR-KEY
	$ heroku config:set RECAPTCHA_PRIVATE_KEY=YOUR-PRIVATE-KEY


### Media files

User-uploaded images will be stored in an Amazon S3 bucket. So, create an account on https://aws.amazon.com if you don't already have one.

I more-or-less followed [these instructions](http://pritishc.com/blog/2015/09/06/uploading-with-django-and-amazon-s3/) for making a new bucket, creating an IAM user with Access Key ID and Secret Access Key, and creating a policy to the bucket. This is my summary:

Go to https://console.aws.amazon.com and create an account or sign in.

Go to the Security Credentials section of your account and choose Users.

Create a new user. Click the 'Show Security Credentials' and note the user's Access Key ID and Secret Access Key.

When you get to the list of users, click your new user. Note the "User ARN" value.

Under the Services menu, go to S3.

Create a new bucket.

In the bucket's Properties, open the Permissions panel, then "Edit bucket policy". Paste the following into the window. Replace `BUCKETNAME` with the name of your bucket. And replace `arn:aws:iam::1234567890:user/USERNAME` with the User ARN value noted earlier. Save the policy.

	{
		"Version": "2012-10-17",
		"Statement": [
			{
				"Action": [
					"s3:GetObject"
				],
				"Effect": "Allow",
				"Principal": {
					"AWS": [
						"*"
					]
				},
				"Resource": [
					"arn:aws:s3:::BUCKETNAME/*"
				]
			},
			{
				"Action": [
					"s3:*"
				],
				"Effect": "Allow",
				"Principal": {
					"AWS": [
						"arn:aws:iam::1234567890:user/USERNAME"
					]
				},
				"Resource": [
					"arn:aws:s3:::BUCKETNAME",
					"arn:aws:s3:::BUCKETNAME/*"
				]
			}
		]
	}

(This gives anonymous users the ability to "get" objects (view images) and the named user the ability to perform any actions.)

Set Heroku config values as here, replacing the values with those for your bucket and user:

	$ heroku config:set AWS_ACCESS_KEY_ID=YOUR-ACCESS-KEY-ID
	$ heroku config:set AWS_SECRET_ACCESS_KEY=YOUR-SECRET-ACCESS-KEY
	$ heroku config:set AWS_STORAGE_BUCKET_NAME=your-bucket-name


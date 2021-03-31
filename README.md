# Made Near You

Instructions for setting up a local development environment using Docker, and the production server on Heroku.


## Local development

We use Docker for local development only, not for the live site.

### 1. Create a .env file

Create a `.env` file containing the below:

    export ALLOWED_HOSTS='*'

    DJANGO_SETTINGS_MODULE='madenearyou.settings.development'

    # For use in Django:
    DATABASE_URL='postgis://madenearyou:madenearyou@madenearyou_db:5432/madenearyou'

    # For use in Docker:
    POSTGRES_USER=madenearyou
    POSTGRES_PASSWORD=madenearyou
    POSTGRES_DB=madenearyou

    # See https://www.google.com/recaptcha/intro/index.html
	RECAPTCHA_PUBLIC_KEY='YOUR-KEY'
	RECAPTCHA_PRIVATE_KEY='YOUR-PRIVATE-KEY'

    MAPBOX_API_KEY='YOUR-KEY'

### 2. Set up a local domain name

Open your `/etc/hosts` file in a terminal window by doing:

    $ sudo vim /etc/hosts

Enter your computer's password. Then add this line somewhere in the file and save:

    127.0.0.1 www.madenearyou.test


### 3. Build the Docker containers

Download, install and run Docker Desktop.

In same directory as this README, build the containers:

    $ docker-compose build

Then start up the web and database containers:

    $ docker-compose up

There are two containers, the webserver (`madenearyou_web`) and the postgres server (`madenearyou_db`). All the repository's code is mirrored in the web container in the `/code/` directory.


### 4. Set up the database

Once that's running, showing its logs, open another terminal window/tab.

There are two ways we can populate the database. First we'll create an empty one,
and second we'll populate it with a dump of data from the live site.

#### 4a. An empty database

The `build` step will create the database and run the Django migrations.

Then create a superuser:

    $ ./scripts/manage.sh createsuperuser

(NOTE: The `manage.sh` script is a shortcut for a longer command that runs
Django's `manage.py` within the Docker web container.)

#### 4b. Use a dump from the live site

Log into postgres and drop the current (empty) database:

    $ docker exec -it madenearyou_db psql -U madenearyou -d postgres
    # drop database madenearyou with (FORCE);
	# create database madenearyou;
	# grant all privileges on database "madenearyou" to madenearyou;
    # \q

On Heroku, download a backup file of the live site's database and rename it to
something simpler. We'll use "heroku_db_dump" below.

Put the file in the same directory as this README.

Import the data into the database:

    $ docker exec -i madenearyou_db pg_restore --verbose --clean --no-acl --no-owner -U madenearyou -d madenearyou < heroku_db_dump

#### 5. Vist and set up the site

Then go to http://www.madenearyou.test:8000 and you should see the site.

Log in to the [Django Admin](http://www.madenearyou.test:8000/admin/), go to the "Sites"
section and change the one Site's Domain Name to `www.madenearyou.test:8000` and the
Display Name to "Made Near You".

## Ongoing work

Whenever you come back to start work you need to start the containers up again:

    $ docker-compose up

When you want to stop the server, in the terminal window/tab that's showing the logs, hit `Control` and `X` together.

You can check if anything's running by doing this, which will list any Docker processes:

    $ docker ps

Do this in the project's directory to stop containers:

    $ docker-compose stop

You can also open the Docker Desktop app to see a prettier view of what containers you have.

When the containers are running you can open a shell to the web server (exit with `Control` and `D` together):

    $ docker exec -it madenearyou_web sh

You could then run `.manage.py` commands within there:

    $ ./manage.py help

Or, use the shortcut command from *outside* of the Docker container:

    $ ./scripts/manage.sh help

Or you can log into the database:

    $ docker exec -it madenearyou_db psql -U madenearyou -d madenearyou

To install new python dependencies:

    $ docker exec -it madenearyou_web sh
    # pipenv install module-name


## Heroku

Create your app on Heroku.

Add the "Heroku Postgres" Add-on.

In the top level of your checked-out code, add Heroku as a git remote (replacing `your-app-name` with your app's name):

	$ heroku git:remote -a your-app-name

Set the buildpacks for Python and the [Heroku Geo Buildpack](https://github.com/heroku/heroku-geo-buildpack) required for GeoDjango:

	$ heroku buildpacks:set heroku/python
    $ heroku buildpacks:add --index 1 https://github.com/heroku/heroku-geo-buildpack.git

Set the environment variables (replacing `your-secret-key-here` with one for your site ([eg, from here](http://www.miniwebtool.com/django-secret-key-generator/)):

	$ heroku config:set DJANGO_SETTINGS_MODULE=madenearyou.settings.heroku
	$ heroku config:set DJANGO_SECRET_KEY=your-secret-key-here
    $ heroku config:set ALLOWED_HOSTS=madenearyou.herokuapp.com,madenearyou.org,www.madenearyou.org

Push code to the server:

	$ git push heroku master

Enable PostGIS on the database:

	$ heroku pg:psql
	=> CREATE EXTENSION postgis;
	=> \q

If setting up the database from scratch, run initial migrations and set the Django admin superuser:

	$ heroku run python manage.py migrate
	$ heroku run python manage.py createsuperuser

For the Recaptcha on the Add Producer form to work, [sign up](https://www.google.com/recaptcha/intro/index.html), add a key, and add then:

	$ heroku config:set RECAPTCHA_PUBLIC_KEY=YOUR-KEY
	$ heroku config:set RECAPTCHA_PRIVATE_KEY=YOUR-PRIVATE-KEY

Add the Mapbox API key:

    $ heroku config:set MAPBOX_API_KEY='YOUR-KEY


### Media files

User-uploaded images will be stored in an Amazon S3 bucket. So, create an account on https://aws.amazon.com if you don't already have one.

I more-or-less followed [these instructions](http://pritishc.com/blog/2015/09/06/uploading-with-django-and-amazon-s3/) for making a new bucket, creating an IAM user with Access Key ID and Secret Access Key, and creating a policy to the bucket. This is my summary:

Go to https://console.aws.amazon.com and create an account or sign in.

Go to the Security Credentials section of your account and choose Users.

Create a new user. Click the 'Show Security Credentials' and note the user's Access Key ID and Secret Access Key.

When you get to the list of users, click your new user. Note the "User ARN" value.

Under the Services menu, go to S3.

Create a new bucket.

In the bucket's Properties, open the Permissions panel, then "Add bucket policy". Paste the following into the window. Replace `BUCKETNAME` with the name of your bucket. And replace `arn:aws:iam::1234567890:user/USERNAME` with the User ARN value noted earlier. Save the policy.

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

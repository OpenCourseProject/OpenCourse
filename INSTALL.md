### Setup Instructions

These instructions are written with Ubuntu Linux 14.04 in mind. However, if you
are familiar with your operating system it should be no problem to setup elsewhere
and use this as a guide.

First things first:

    sudo apt-get update
    sudo apt-get upgrade

Install the necessary packages:

    sudo apt-get install git apache2 libapache2-mod-wsgi python python-dev libxml2-dev libxslt1-dev python-pip

I use (and suggest using) MySQL as your database, and instructions assume you do.
There are suitable alternatives but you're on your own for configuration.

    sudo apt-get install mysql-server libmysqlclient-dev

Install virtualenv:

    sudo pip install virtualenv

Create a new folder to work with. I'll be placing this in ```/var/www/site/```:

  cd /var/www/
  sudo mkdir site
  sudo chown ubuntu site
  cd site

Create a new virtual environment to work on and activate it:

  virtualenv env
  source ./env/bin/activate

Let's clone the project.

    git clone https://github.com/gravitylow/OpenCourse.git opencourse
    cd opencourse

Install the necessary pip libraries:

    pip install -r requirements.txt

The settings files are now located at ```opencourse/settings/```. It is important to note that by default the **development** settings are used. You can change this to production settings in the ```__init__.py``` file in this directory when you're ready.

Open ```common.py``` up using your favorite text editor because we have some work to do. Some private values have been removed from the settings file and have been noted in comments. You'll need to provide your own replacement for these.

First, populate the SECRET_KEY value with a sufficiently random secure text string. [See the Django documentation for this setting](https://docs.djangoproject.com/en/1.8/ref/settings/#secret-key).

Modify the ALLOWED_HOSTS setting to include your desired domain. Do similarly with the SESSION_COOKIE_DOMAIN setting.

If you want to use the Google OAuth login system, you'll need to [register an app](https://console.developers.google.com/project) with Google and, from your APIs & Auth / Credentials page, fill in the necessary fields. **Make sure you also enable the Google+ API from the APIs page or else you'll get login errors**. Here's a rundown of what you should have:

* SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'YOUR KEY'
* SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'YOUR SECRET'

You'll need to do similarly to use the Facebook integration. [Register an app](https://developers.facebook.com/apps/) with Facebook and, from your Dashboard, fill in the necessary fields. Here's a rundown of what you should have:

* SOCIAL_AUTH_FACEBOOK_KEY = 'YOUR KEY'
* SOCIAL_AUTH_FACEBOOK_SECRET = 'YOUR SECRET'

Now we'll need to configure the MySQL database we setup earlier. In the DATABASES section of your config, you should create the proper settings based on the [Django documentation](https://docs.djangoproject.com/en/1.8/ref/settings/#databases). Assuming you have an unchanged MySQL installation, you can fill these in right off the bat:

* 'ENGINE': 'django.db.backends.mysql',
* 'HOST': 'localhost',
* 'PORT': '3306',

Finally, to be able to send emails from the system, you'll need to provide SMTP server connection details. This will differ from host to host, so check with them to get your details.

Run the migrations to set up the database:

    python manage.py migrate

We'll do a quick test to make sure everything looks right:

    python manage.py runserver 0.0.0.0:80

You can now point your browser towards the server's public IP and (if all goes well), you will see the OpenCourse homepage. If you run into an error take a look to see what it is asking you to do - usually this will be installing a missing dependency. You can also check the apache2 log at ```/var/log/apache2/error.log``` for any setup errors once you've setup your virtual host. Feel free to open an issue with the error in question if it's not obvious.

From here, there's no step-by-step instructions. The data you'll serve depends on what you want your site to focus on. The copy you cloned has management commands setup at ```course/management/commands/``` that scrape data from the Schedule of Courses.

If you'd like to use these commands, you should run the kronos command to install the tasks as cron jobs:

    python manage.py installtasks

These scrapers will populate the database with information and keep it up-to-date as necessary. No manual processing should be necessary.

If you're using your own scrapers, you should replace these files, register the commands with kronos as shown, and make any necessary model changes to support the data.

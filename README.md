# flask-image-demo
A demo for my CS students on how to store and retrieve image files using
PostgreSQL, SQLAlchemy, and Flask.  This demo shows students how to store images both in
a database and on the filesystem using SQLAlchemy.  It is assumed that students know how to build a Flask app with a SQLAlchemy/PostgreSQL backend.

## Installation

First, create a Python 3.x virtual environment using virtualenv, like this:

```console
pyvenv-3.5 env
```

Virtual environments are a great way to move between different Python setups if you need to have multiple Python versions on your computer.  They also make migrating from one machine to another much easier.

Now, activate your newly created virtual environment:

```console
source .env
```

Sourcing this file activates your environment and gives you the environment variables APP_SETTINGS and DATABASE_URL.  Any time you want to run or modify code in this project, you'll need to do this to activate the environment.  The code uses the environment variable values to know whether to run in dev/test/production mode and where the database resides.

Now, install PostgreSQL and add
PostgreSQL's bin directory to your path, if you haven't done so already in a previously taken class.  Run psql and type the command `create
database imagedemo;`.  You can exit psql by typing `\q`.

Then, you can then build and run the app as follows:
```console
pip3 install -r requirements.txt
python3 manage.py db upgrade
python3 manage.py runserver
```

And finally, browse to [http://localhost:5000/](http://localhost:5000).

## Notes

Although this example shows how to serve images from both a database and from
the filesystem, it is generally thought to be better to serve images from
the filesystem in the interest of application performance.  Filesystems are
designed for that sort of thing.  Nonetheless, there are situations where it
may be necessary to store an image (or a file in general) in the database,
hence the existence of that feature in this demo application.

With knowledge comes a certain level of responsibility.  Take note!

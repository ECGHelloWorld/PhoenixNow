#TODO
* Make docs + tests For email, For wtf forms, Config.py, Add notes on db’s and relationships, Security page in docs explaining hashing and salt
* Config, Make secretkeys an env variable , Fix all of ali’s token code and email code that uses app.config and secret keys, Fix config stuff how to cleanly do it?, Change token key to secret key
* ~~Celery reset every morning NEEDS TO BE TESTED~~
* GET ACTUAL IPS FOR CHECKIN TESTING
* ~~Make page showing all users organized alphabetically with columns for days of the week.~~ Days blacked out if not on schedule, use checks for checkins
* Fix ali’s server str() around salt in model.py
* ~~Signin when verify~~
* ~~Add code to server to verify only official android app is used~~
* Two schedules, one that stays constant after being verified no matter what the user tries to do. Ie stays permanent once approved.
* Make unverified accounts delete if someone else tries to register with the same email.

# PhoenixNow
This app facilitates signins and roll calls for schools that aren't especially centralized.

The currently planned features are

* User accounts
* Signins by geographic locations
* Android support

# Setting up the dev environment
To run, follow instructions here http://phoenixnow.readthedocs.io/en/latest/running.html

# Planned Deployment Features

* TDD based development
* Dockerfiles for deployment and local development (allows for easier Windows
  development with Docker Toolbox)
* Fabric/Ansible for server setup and deployment of Dockerfiles
* Continuous testing integration

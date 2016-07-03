# PhoenixNow
This app facilitates signins and roll calls for schools that aren't especially centralized.

The currently planned features are

* User accounts
* Signins by geographic locations
* Android support

# Setting up the dev environment
These instructions assume that you're using a Debian-based Linux distribution

`sudo apt-get install build-essential pip3-python libffi-dev python-dev`

`sudo pip3 install -r requirements.txt`

To run, execute `python app.py`

# Planned Deployment Features

* TDD based development
* Dockerfiles for deployment and local development (allows for easier Windows
  development with Docker Toolbox)
* Fabric/Ansible for server setup and deployment of Dockerfiles
* Continuous testing integration

from fabric.api import *

env.hosts = ['phoenixnow.org']
env.user = 'ecg'
env.key_filename = '~/.ssh/id_rsa'

def build():
    sudo('docker-compose build')

def down():
    sudo('docker-compose down')

def up():
    sudo('docker-compose up -d')

def pull():
    run('git pull')

def deploy():
    with cd('~/PhoenixNow'):
        pull()
        build()
        down()
        up()

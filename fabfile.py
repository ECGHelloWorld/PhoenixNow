from fabric.api import run, sudo

env.hosts = ['phoenixnow.org']
env.user = ['ecg']

def build():
    sudo('docker-compose build')

def down():
    sudo('docker-compose down')

def up():
    sudo('docker-compose up')

def pull():
    run('git pull')

def deploy():
    with cd('~/PhoenixNow'):
        pull()
        build()
        down()
        up()

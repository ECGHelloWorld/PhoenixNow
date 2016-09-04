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

def restore_old_db():
    sudo('docker cp ~/mysql-dump-new.sql phoenixnow_db_1:/')
    sudo("docker exec -it phoenixnow_db_1 sh -c 'exec mysql -h172.18.0.2 -uroot -ppass < mysql-dump-new.sql'")

def db_access():
    sudo("docker exec -it phoenixnow_db_1 sh -c 'exec mysql -h172.18.0.2 -uroot -ppass'")

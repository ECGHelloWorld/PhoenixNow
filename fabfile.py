from fabric.api import *
import datetime

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

def backup_db():
    today = datetime.datetime.utcnow()
    today_str = today.strftime("%-m-%-d-%Y-%-H-%-M-%-S")
    sudo("docker exec phoenixnow_db_1 sh -c 'exec mysqldump --all-databases -uroot -ppass' > /home/ecg/backup-" + today_str +".sql")

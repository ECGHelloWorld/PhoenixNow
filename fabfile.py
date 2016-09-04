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

def mysql_restore_old_db():
    sudo('docker cp ~/mysql-dump-new.sql phoenixnow_db_1:/')
    sudo("docker exec -it phoenixnow_db_1 sh -c 'exec mysql -h172.18.0.2 -uroot -ppass < mysql-dump-new.sql'")

def mysql_db_access():
    sudo("docker exec -it phoenixnow_db_1 sh -c 'exec mysql -h172.18.0.2 -uroot -ppass'")

def mysql_backup_db():
    today = datetime.datetime.utcnow()
    today_str = today.strftime("%-m-%-d-%Y-%-H-%-M-%-S")
    sudo("docker exec phoenixnow_db_1 sh -c 'exec mysqldump --all-databases -uroot -ppass' > /home/ecg/backup-" + today_str +".sql")

def backup_db():
    sudo("docker exec -t phoenixnow_db_1 pg_dump -Upostgres postgres > /home/ecg/dump_`date +%d-%m-%Y_%H_%M_%S`.sql")

def list_backups():
    run("ls /home/ecg/ | grep dump")

def restore_backup(name):
    # fab restore_backup:name=sqlbackupname
    sudo("docker cp /home/ecg/" + name " phoenixnow_db_1:/")
    sudo("docker exec -it phoenixnow_db_1 sh -c 'exec psql -Upostgres < " + name)
    

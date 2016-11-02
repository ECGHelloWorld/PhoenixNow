from fabric.api import *
import datetime

env.hosts = ['phoenixnow.org']
env.user = 'ecg'
env.key_filename = '~/.ssh/id_rsa'

def build():
    with cd("/home/ecg/PhoenixNow/"):
        sudo('docker-compose build')

def down():
    with cd("/home/ecg/PhoenixNow/"):
        sudo('docker-compose down')

def up():
    with cd("/home/ecg/PhoenixNow/"):
        sudo('docker-compose up -d')

def pull():
    with cd("/home/ecg/PhoenixNow/"):
        run('git pull')

def deploy():
    pull()
    build()
    down()
    up()

def attach():
    sudo("docker attach phoenixnow_web_1 --sig-proxy=false")
    
def mysql_restore_old_db():
    sudo('docker cp /home/ecg/mysql-dump-new.sql phoenixnow_db_1:/')
    sudo("docker exec -it phoenixnow_db_1 sh -c 'exec mysql -h172.18.0.2 -uroot -ppass < mysql-dump-new.sql'")

def mysql_db_access():
    sudo("docker exec -it phoenixnow_db_1 sh -c 'exec mysql -h172.18.0.2 -uroot -ppass'")

def mysql_backup_db():
    today = datetime.datetime.utcnow()
    today_str = today.strftime("%-m-%-d-%Y-%-H-%-M-%-S")
    sudo("docker exec phoenixnow_db_1 sh -c 'exec mysqldump --all-databases -uroot -ppass' > /home/ecg/backup-" + today_str +".sql")

def cd_phoenixnow():
    cd("/home/ecg/PhoenixNow/")

def stop_web():
    with cd("/home/ecg/PhoenixNow/"):
        sudo("sudo docker-compose stop web")

def backup_db(name=None):
    if name is None:
        sudo("docker exec -t phoenixnow_db_1 pg_dump -Upostgres postgres > /home/ecg/dump_`date +%d-%m-%Y_%H_%M_%S`.sql")
    else:
        sudo("docker exec -t phoenixnow_db_1 pg_dump -Upostgres postgres > /home/ecg/dump_" + name + ".sql")

def list_backups():
    run("ls /home/ecg/ | grep dump")

def remove_postgres_db():
    sudo("docker exec -it phoenixnow_db_1 sh -c 'exec dropdb -Upostgres postgres'")

def create_postgres_db():
    sudo("docker exec -it phoenixnow_db_1 sh -c 'createdb -Upostgres postgres'")

def restore_backup(name):
    # fab restore_backup:name=sqlbackupname
    stop_web()
    remove_postgres_db()
    create_postgres_db()
    sudo("docker cp /home/ecg/" + name + " phoenixnow_db_1:/")
    sudo("docker exec -it phoenixnow_db_1 sh -c 'exec psql -Upostgres < " + name + "'")

def db_access():
    sudo("docker exec -it phoenixnow_db_1 sh -c 'exec psql -Upostgres'")

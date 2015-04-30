import os

from fabric.api import env, run, cd, sudo, local, lcd
from fabric.operations import run, get

try:
    from fabconf_local import *
except:
    pass


def set_host(host):
    env.curconfig = CONFIG[host]
    env.hosts = [env.curconfig['host']]


def rename_last():
    dump_path = os.path.expanduser(env.curconfig['dump_path'])
    db_name = '{}{}.sql'.format(dump_path, env.curconfig['db'])
    if os.path.exists(db_name):
        max_num = 0
        for filename in filter(lambda a: '{}{}'.format(dump_path, a).startswith(db_name), os.listdir(dump_path)):
            l = filename.split('.')
            try:
                if len(l) == 3 and int(l[2]) > max_num:
                    max_num = int(l[2])
            except ValueError:
                pass
        os.rename(db_name, '{}.{}'.format(db_name, max_num+1))


def backup():
    sudo('pg_dump -d {0} > /tmp/{0}.sql'.format(env.curconfig['db']), user=env.curconfig['db_user'])


def archive():
    with cd('/tmp'):
        run('tar cjf {0}.tar.bz2 {0}.sql'.format(env.curconfig['db']))
    env.curconfig['ext'] = 'tar.bz2'


def download():
    get('/tmp/{}.{}'.format(env.curconfig['db'], env.curconfig['ext']), env.curconfig['dump_path'])


def unarchive():
    with lcd(env.curconfig['dump_path']):
        local('tar xjf {}.tar.bz2'.format(env.curconfig['db']))


def restore():
    local('psql -U postgres -c "SELECT pid, (SELECT pg_terminate_backend(pid)) as killed from pg_stat_activity WHERE datname = \'{}\';"'.format(env.curconfig['local_db']))
    local('psql -U postgres -c "drop database {};"'.format(env.curconfig['local_db']))
    local('psql -U postgres -c "create database {};"'.format(env.curconfig['local_db']))
    local('psql -U postgres {} < {}{}.sql'.format(env.curconfig['local_db'], env.curconfig['dump_path'], env.curconfig['db']))


def update_db(with_archive=True):
    rename_last()
    backup()
    if with_archive:
        archive()
    download()
    if with_archive:
        unarchive()
    restore()

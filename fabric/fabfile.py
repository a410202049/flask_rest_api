#!/usr/bin/python
# -*- coding:utf-8 -*-


import datetime

from fabric.api import *
from fabric.contrib import console
from fabric import colors
from fabric import utils
from fabric.contrib.project import rsync_project

import fab_util

environments = {}

import fabconfig

exclude = ('redis_data', '.gitignore', '.git', '*.log', '*.pyc', 'fabric', 'tests', 'node_modules', 'venv')
environments.update(fabconfig.environments)


def e(name='dev', confirm='True'):
    confirm = confirm == 'True'
    print colors.yellow("Setting environment: %s" % name)
    if (not confirm) or console.confirm(u'Current env is %s, Do you wish to continue?' % name, default=False):
        env.update(environments[name])
        env.environment = name
    else:
        utils.abort(u'goodbye!')


def host_type():
    run('uname -s && whoami')


def backup_by_tar():
    """
    备份项目文件，并删除超过90天的备份文件。
    """
    with cd(env.remote_path):
        with prefix("cd .."):
            run("tar zcvf %(project)s.%(timestamp)s.tar.gz %(project)s/ %(exclude)s" % {
                "project": env.project_name, "timestamp": datetime.datetime.now().strftime("%Y%m%d%H%M%S"), "exclude": "".join(map(lambda e: ' --exclude ' + e, exclude)),
            })
            run("find ./%(project)s.*.tar.gz -ctime +90 -exec rm {} \;" % {"project": env.project_name})


def rsync():
    rsync_project(remote_dir=env.remote_path, local_dir=env.local_path,
                  delete=True, exclude=exclude)


def rsync_no_pass():
    fab_util.rsync_project(remote_dir=env.remote_path, local_dir=env.local_path,
                  delete=True, exclude=exclude)

def build(): 
    with cd(env.remote_path): 
        run(env.build)


def server_up():
    with cd(env.remote_path): 
        run(env.server_up)


def server_stop():
    with cd(env.remote_path): 
        run(env.server_stop)


def server_down():
    with cd(env.remote_path): 
        run(env.server_down)


def server_ps():
    with cd(env.remote_path): 
        run(env.server_ps)


def deploy_noback():
    rsync()
    build()
    server_up()
    server_ps()

def deploy():
    backup_by_tar()
    deploy_noback()

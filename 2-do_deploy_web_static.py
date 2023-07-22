#!/usr/bin/python3
""" 0x03. AirBnB clone - Deploy static, task"""
from fabric.api import env, put, run
from os import path

env.hosts = ['52.201.222.41', '174.129.54.185']
env.user = 'ubuntu'

def do_deploy(archive_path):
    if not path.exists(archive_path) or archive_path is None:
        return False

    f_name = path.basename(archive_path)
    d_name = f_name.split('.')[0]

    try:
        put(local_path=archive_path, remote_path='/tmp/')
        run('mkdir -p /data/web_static/releases/{}/'.format(d_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(f_name, d_name))
        run('rm /tmp/{}'.format(f_name))

        # Delete the existing directories if they exist
        run('rm -rf /data/web_static/releases/{}/web_static/images'.format(d_name))
        run('rm -rf /data/web_static/releases/{}/web_static/styles'.format(d_name))
        run('rm -rf /data/web_static/releases/{}/web_static/versions'.format(d_name))

        run('mv /data/web_static/releases/{}/web_static/* '.format(d_name) +
            '/data/web_static/releases/{}/'.format(d_name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(d_name))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(d_name))

        print('New version deployed!')
        return True
    except:
        return False


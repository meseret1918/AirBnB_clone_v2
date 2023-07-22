#!/usr/bin/python3
""" a Fabric script (based on the file 1-pack_web_static.py) that distributes..
    ..an archive to your web servers, using the function do_deploy: """

from fabric.api import env, put, run
from os.path import exists

# Define the web server IP addresses
env.hosts = ['52.201.222.41','174.129.54.185']

def do_deploy(archive_path):
    # Check if the archive file exists
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the /data/web_static/releases/<archive filename without extension> directory
        archive_filename = archive_path.split('/')[-1]
        archive_folder = '/data/web_static/releases/{}'.format(archive_filename.split('.')[0])
        run('mkdir -p {}'.format(archive_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, archive_folder))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current linked to the new version of your code
        run('ln -s {} /data/web_static/current'.format(archive_folder))

        return True
    except:
        return False


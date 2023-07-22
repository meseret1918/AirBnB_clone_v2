#!/usr/bin/env python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""
from fabric.api import env, put, run
from os.path import exists

# Define the web server IP addresses
env.hosts = ['52.201.222.41', '174.129.54.185']

def do_deploy(archive_path):
    # Check if the archive file exists
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the appropriate folder
        archive_filename = archive_path.split('/')[-1]
        release_folder = '/data/web_static/releases/{}'.format(archive_filename[:-4])
        run('mkdir -p {}'.format(release_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_folder))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move the contents of the extracted folder to the appropriate location
        run('mv {}/web_static/* {}'.format(release_folder, release_folder))

        # Remove the empty web_static folder
        run('rm -rf {}/web_static'.format(release_folder))

        # Delete the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new version of the code
        run('ln -s {} /data/web_static/current'.format(release_folder))

        print('New version deployed!')
        return True
    except:
        return False


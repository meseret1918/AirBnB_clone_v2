#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""

from fabric.api import env, put, run
from os.path import exists
env.hosts = ['52.201.222.41', '174.129.54.185']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        archive_filename = archive_path.split("/")[-1]
        folder_name = "/data/web_static/releases/{}".format(archive_filename.split(".")[0])
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, folder_name))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move the contents of the uncompressed folder to the parent folder
        run("mv {}/web_static/* {}/".format(folder_name, folder_name))
        run("rm -rf {}/web_static".format(folder_name))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server
        # linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
        run("ln -s {} /data/web_static/current".format(folder_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False


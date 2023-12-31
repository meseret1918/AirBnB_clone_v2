#!/usr/bin/python3

from fabric.api import local
from datetime import datetime

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_" + timestamp + ".tgz"
    archive_path = "versions/" + archive_name

    local("mkdir -p versions")
    result = local("tar -czvf {} web_static".format(archive_path))

    if result.failed:
        return None
    else:
        return archive_path

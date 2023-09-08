#!/usr/bin/python3
"""Fabric script that generates a compressed file (.tgz) from the contents
    of the web_static folder of your AirBnB Clone repo """
from fabric.api import env
from fabric.api import put
from fabric.api import run
from fabric.api import local
from datetime import datetime
from os import path

env.hosts = ['54.197.107.162', '35.153.79.164']
env.user = "ubuntu"


def do_pack():
    """ generate a compressed archive
    the function do_pack must return the archive path
    if the archive has been correctly generated
    otherwise, it should return None"""
    time_stamp = '%Y%m%d%H%M%S'
    _time = datetime.utcnow().strftime(time_stamp)
    _path = "versions/web_static_{}.tgz".format(_time)
    local("mkdir -p versions")
    local("tar -cvzf {} web_static".format(_path))
    if path.exists(_path):
        return _path
    else:
        return None


def do_deploy(archive_path):
    """ distributes an archive to web server
    Args:
        archive_path (path): path of the archive file
    """
    if not path.exists(archive_path) and path.isfile(archive_path):
        return False
    file_name = archive_path.split("/")[-1].split(".")[0]
    _path = "/data/web_static/releases/{}/web_static/*".format(file_name)
    try:
        put(archive_path, "/tmp/")
        run("sudo mkdir -p /data/web_static/releases/{}/".format(file_name))
        run("sudo tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/".
            format(file_name, file_name))
        run("sudo rm /tmp/{}.tgz".format(file_name))
        run("sudo mv {} /data/web_static/releases/{}/".format(_path,
                                                              file_name))
        run("sudo rm -rf /data/web_static/releases/{}/web_static".
            format(file_name))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(file_name))
        return True
    except:
        return False
    return True


def deploy():
    """[full deploy]
    """
    filepath = do_pack()
    if filepath is None:
        return False
    else:
        return do_deploy(filepath)

def do_clean(number=0):
    """Deletes out-of-date archives of the static files.
    Args:
        number (Any): The number of archives to keep.
    """
    archives = os.listdir('versions/')
    archives.sort(reverse=True)
    start = int(number)
    if not start:
        start += 1
    if start < len(archives):
        archives = archives[start:]
    else:
        archives = []
    for archive in archives:
        os.unlink('versions/{}'.format(archive))
    cmd_parts = [
        "rm -rf $(",
        "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
        " '/data/web_static/releases/web_static_.*'",
        " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1)
    ]
    run(''.join(cmd_parts))

#!/usr/bin/env python3

import os
import json
import socket
import getpass


# Variables
NAME = "clate"
VERSION = "dev"

TAG = "base"

WORKDIR = os.getcwd()
DOCKERDIR = "./docker"
DOCKERFILE = "{}/Dockerfile".format(DOCKERDIR)
DOCKERFILEDIR = "{}/dockerfile".format(DOCKERDIR)
DOCKERFRAMEWORK = "./framework"

DOCKERINIT = "{}/01_init.Dockerfile".format(DOCKERFILEDIR)
DOCKERUSER = "{}/02_user.Dockerfile".format(DOCKERFILEDIR)
DOCKERSETUP = "{}/03_setup.Dockerfile".format(DOCKERFILEDIR)
DOCKERNETWORK = "{}/04_network.Dockerfile".format(DOCKERFILEDIR)

DOCKERUSERDATA = "{}/userdata".format(DOCKERFILEDIR)
DOCKERNETWORKENV = "{}/network".format(DOCKERFILEDIR)

CONFIG_JSON = "./config.json"

CLATE_JSON = os.getenv("HOME") + '/.clate.json'
CLATE_EXEC = '/usr/local/bin/clate'


class UserInfo:
    def __init__(self):
        self.name = None
        self.install_path = None
        self.host_ip = None


def write_clate_json(clate_data):
    global CLATE_JSON

    clate_json = open(CLATE_JSON, 'w')
    clate_json.write(json.dumps(clate_data, sort_keys=True, indent=4))
    clate_json.close()


def mkdir(t_dir):
    try:
        os.makedirs(t_dir)
    except OSError as e:
        print(e)


def create_new_project(project_name, tag, port, vscode_path, uInfo):
    global TAG

    project_dirs = dict()
    if project_name == "clate":
        project_dirs['Workspace'] = os.path.dirname(
            os.path.abspath(__file__)) + '/'
    else:
        project_dirs['Workspace'] = os.path.dirname(
            os.path.abspath(__file__)) + '/' + project_name + '/'

    extension_dir = vscode_path + project_name + '/'
    project_dirs['extension'] = extension_dir
    mkdir(extension_dir)

    project_ports = dict()
    project_ports['ssh'] = str(port)

    clate_project = dict()
    clate_project['name'] = project_name
    clate_project['tag'] = tag
    clate_project['directory'] = project_dirs
    clate_project['port'] = project_ports

    ssh_config = """
Host {0}
    User {1}
    Hostname {2}
    Port {3}
""".format(project_name, uInfo.name, uInfo.host_ip, str(port))
    os.system("echo '{0}' >> ~/.ssh/config".format(ssh_config))

    return clate_project


def create_new_clate(uInfo):
    global VERSION

    print("create common and default project")

    # Common
    common_dict = dict()
    common_dict['user'] = uInfo.name
    common_dict['version'] = VERSION

    mkdir(uInfo.install_path)
    common_dict['install_path'] = uInfo.install_path
    vscode_path = uInfo.install_path + 'vscode-server/'
    mkdir(vscode_path)

    common_dict['host_ip'] = uInfo.host_ip

    # Clate
    clate_data = dict()
    clate_data['common'] = common_dict

    # Default project
    project_list = list()
    project_list.append(create_new_project(
        "clate", TAG, 5000, vscode_path, uInfo))
    project_list.append(create_new_project(
        "cpilot", 'cpp', 5100, vscode_path, uInfo))

    clate_data['project'] = project_list

    return clate_data


def clate_manager(uInfo):
    global CLATE_JSON

    clate_data = None

    # Project
    if os.path.exists(CLATE_JSON):
        print(".clate.json is already existed")
        clate_json = open(CLATE_JSON).read()
        clate_data = json.loads(clate_json)
    else:
        clate_data = create_new_clate(uInfo)

    write_clate_json(clate_data)

    # Install execute file
    if not os.path.exists(CLATE_EXEC):
        os.system("sudo ln -s {0}/clate /usr/local/bin".format(os.getcwd()))


def config(uInfo):
    # Build dockerfile
    config_json = open(CONFIG_JSON).read()
    config_info = json.loads(config_json)

    if config_info['ID'] == "USER_ID" \
            or config_info['UID'] == 'USER_ID_NUMBER' \
            or config_info['GROUP'] == 'GROUP_ID' \
            or config_info['GID'] == 'GROUP_ID_NUMBER':
        print("Please fill your info in config_info.json")
        return False

    # User info
    USER_ENV = """
# User info
ENV UID="{0}" \\\n\
    UNAME="{1}" \\\n\
    GID="{2}" \\\n\
    GNAME="{3}" \\\n\
    SHELL="/bin/bash" \\\n\
    HOME=/home/{1}\n
    """.format(config_info['UID'], config_info['ID'], config_info['GID'], config_info['GROUP'])

    user = open(DOCKERUSERDATA, "w")
    user.write(USER_ENV)
    user.close()

    # Network info
    host_ip = config_info['HOST_IP']
    if host_ip == "":
        host_ip = socket.gethostbyname(socket.gethostname())
    pwd = getpass.getpass("ssh password: ")
    NETWORK_ENV = """
ENV HOST={0} \
    PASSWORD={1}
    """.format(host_ip, pwd)

    network = open(DOCKERNETWORKENV, "w")
    network.write(NETWORK_ENV)
    network.close()

    uInfo.name = config_info['ID']
    given_path = config_info['INSTALL_PATH']

    from clate_core.clate_core import DirManager
    dirMgr = DirManager()
    uInfo.install_path = dirMgr.endSlash(given_path) + 'clate/'
    uInfo.host_ip = host_ip

    os.system("cat {0} > {1}".format(DOCKERINIT,         DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERUSERDATA,    DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERUSER,        DOCKERFILE))

    os.system("cat {0} >> {1}".format(DOCKERSETUP,       DOCKERFILE))

    os.system("cat {0} >> {1}".format(DOCKERNETWORKENV,  DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERNETWORK,     DOCKERFILE))

    return True


def check_running_image(tag):
    from clate_core.clate_core import Docker
    docker = Docker("clate")
    if docker.is_using_image(tag):
        print(
            "Cannot build new image. please stop containers from clate:{0}".format(tag))
        return 0

    return docker.get_current_image_id(tag)


def remove_dangling_image(tag, image_id):
    from clate_core.clate_core import Docker
    docker = Docker("clate")
    docker.remove_dangling_image(tag, image_id)


def install():
    # Build docker image
    global TAG
    global DOCKERDIR
    global NAME

    image_id = check_running_image(TAG)
    if image_id != 0:
        os.chdir(DOCKERDIR)
        ret = os.system("docker build . -t {0}:{1}".format(NAME, TAG))
        if ret == 256:
            print("install clate base failed")
            return False
        os.chdir(WORKDIR)
        remove_dangling_image(TAG, image_id)

    return True

def install_framework():
    config_json = open(CONFIG_JSON).read()
    config_info = json.loads(config_json)

    for k, v in config_info['FRAMEWORKS'].items():
        if v:
            tag = k.lower()
            image_id = check_running_image(tag)
            if image_id != 0:
                framework_path = DOCKERFRAMEWORK + '/' + k + '/'
                os.chdir(framework_path)
                os.system("docker build . -t {0}:{1}".format(NAME, tag))
                os.chdir(WORKDIR)
                remove_dangling_image(tag, image_id)


def cleanup():
    os.system("rm {0}".format(DOCKERUSERDATA))
    os.system("rm {0}".format(DOCKERNETWORKENV))
    os.system("rm {0}".format(DOCKERFILE))


if __name__ == "__main__":
    uInfo = UserInfo()

    if config(uInfo):
        clate_manager(uInfo)
        if install():
            install_framework()
        cleanup()

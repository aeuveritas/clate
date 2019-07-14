#!/usr/bin/env python3

import os
import json
import socket
import getpass


# Variables
NAME             = "clate"
VERSION          = "0.3"

DOCKERDIR        = "./docker"
DOCKERFILE       = "{}/Dockerfile".format(DOCKERDIR)
DOCKERFILEDIR    = "{}/dockerfile".format(DOCKERDIR)
DOCKERINIT       = "{}/01_init.Dockerfile".format(DOCKERFILEDIR)
DOCKERUSER       = "{}/02_user.Dockerfile".format(DOCKERFILEDIR)
DOCKERSETUP      = "{}/03_setup.Dockerfile".format(DOCKERFILEDIR)
DOCKERNETWORK    = "{}/04_network.Dockerfile".format(DOCKERFILEDIR)
DOCKERNODE    = "{}/05_node.Dockerfile".format(DOCKERFILEDIR)

DOCKERUSERDATA   = "{}/userdata".format(DOCKERFILEDIR)
DOCKERVERSION    = "{}/version".format(DOCKERFILEDIR)
DOCKERNETWORKENV = "{}/network".format(DOCKERFILEDIR)
CONFIG_JSON      = "./config.json"

CLATE_JSON       = os.getenv("HOME") + '/.clate.json'
CLATE_EXEC       = '/usr/local/bin/clate'

USER             = ""
INSTALL_PATH     = ""
VSCODE_PATH      = ""
HOST_IP          = None


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


def create_new_project(project_name, port):
    global VERSION
    global VSCODE_PATH

    project_dirs = dict()
    if project_name == "clate":
        project_dirs['Workspace'] = os.path.dirname(os.path.abspath(__file__)) + '/'
    else:
        project_dirs['Workspace'] = os.path.dirname(os.path.abspath(__file__)) + '/' + project_name + '/'

    project_ports = dict()
    project_ports['ssh'] = str(port)

    clate_project = dict()
    clate_project['name'] = project_name
    clate_project['version'] = VERSION
    clate_project['directory'] = project_dirs
    clate_project['port'] = project_ports
    clate_project['cmake'] = ''

    ssh_config = """
Host {0}
    User {1}
    Hostname {2}
    Port {3}
""".format(project_name, USER, HOST_IP, str(port))
    os.system("echo '{0}' >> ~/.ssh/config".format(ssh_config))

    return clate_project


def create_new_clate():
    global VERSION
    global USER
    global INSTALL_PATH
    global VSCODE_PATH
    global HOST_IP

    print("create common and default project")

    # Common
    common_dict = dict()
    common_dict['user'] = USER
    common_dict['default_version'] = VERSION

    mkdir(INSTALL_PATH)
    VSCODE_PATH = INSTALL_PATH + 'vscode-server/'
    mkdir(VSCODE_PATH)
    common_dict['extension'] = VSCODE_PATH

    common_dict['host_ip'] = HOST_IP

    # Clate
    clate_data = dict()
    clate_data['common'] = common_dict

    # Default project
    project_list = list()
    project_list.append(create_new_project("clate", 5000))
    project_list.append(create_new_project("cpilot", 5100))

    clate_data['project'] = project_list

    return clate_data


def clate_manager():
    global VERSION
    global CLATE_JSON

    clate_data = None

    # Project
    if os.path.exists(CLATE_JSON):
        print(".clate.json is already existed")
        clate_json = open(CLATE_JSON).read()
        clate_data = json.loads(clate_json)
    else:
        clate_data = create_new_clate()

    write_clate_json(clate_data)

    # Install execute file
    if not os.path.exists(CLATE_EXEC):
        os.system("sudo ln -s {0}/clate /usr/local/bin".format(os.getcwd()))


def config():
    global VERSION
    global USER
    global INSTALL_PATH
    global HOST_IP

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
    USER_ENV = \
    """
# User info
ENV UID="{0}" \\\n\
    UNAME="{1}" \\\n\
    GID="{2}" \\\n\
    GNAME="{3}" \\\n\
    SHELL="/bin/bash" \\\n\
    HOME=/home/{1}\n
    """.format(config_info['UID'], config_info['ID'], config_info['GID'], config_info['GROUP'])
    USER = config_info['ID']

    user = open(DOCKERUSERDATA, "w")
    user.write(USER_ENV)
    user.close()

    path = config_info['INSTALL_PATH']
    if path[-1] != '/':
        path += '/'
    INSTALL_PATH = path + 'clate/'

    # Version info
    VERSION_ENV = \
    """
# Version info
ENV CLATE_VERSION={0} \
    LLVM_VERSION={1}
    """.format(VERSION, config_info['VERSION']['LLVM'])

    version = open(DOCKERVERSION, "w")
    version.write(VERSION_ENV)
    version.close()

    # Network info
    HOST_IP = config_info['HOST_IP']
    if HOST_IP == "":
        HOST_IP = socket.gethostbyname(socket.gethostname())
    pwd = getpass.getpass("ssh password: ")
    NETWORK_ENV = \
    """
ENV HOST={0} \
    PASSWORD={1}
    """.format(HOST_IP, pwd)

    network = open(DOCKERNETWORKENV, "w")
    network.write(NETWORK_ENV)
    network.close()

    os.system("cat {0} > {1}".format(DOCKERINIT,         DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERUSERDATA,    DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERVERSION,     DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERUSER,        DOCKERFILE))

    os.system("cat {0} >> {1}".format(DOCKERSETUP,       DOCKERFILE))

    os.system("cat {0} >> {1}".format(DOCKERNETWORKENV,  DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERNETWORK,     DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERNODE,     DOCKERFILE))

    return True


def install():
    # Build docker image
    global VERSION
    from clate_core.clate_core import Docker
    docker = Docker("clate")
    if docker.is_using_image(VERSION):
        print("cannot build new image. please stop containers from clate:{0}".format(VERSION))
        return

    id = docker.get_current_image_id(VERSION)

    os.chdir(DOCKERDIR)
    os.system("docker build . -t {0}:{1}".format(NAME, VERSION))
    os.chdir("..")

    docker.remove_dangling_image(VERSION, id)


def cleanup():
    os.system("rm {0}".format(DOCKERUSERDATA))
    os.system("rm {0}".format(DOCKERVERSION))
    os.system("rm {0}".format(DOCKERNETWORKENV))
    os.system("rm {0}".format(DOCKERFILE))


if __name__ == "__main__":
    if config():
        clate_manager()
        install()
        cleanup()

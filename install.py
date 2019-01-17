#!/usr/bin/env python3

import os
import json

# Variables
NAME            = "clate"
VERSION         = "0.2"

DOCKERDIR       = "./docker"
DOCKERFILE      = "{}/Dockerfile".format(DOCKERDIR)
DOCKERFILEDIR   = "{}/dockerfile".format(DOCKERDIR)
DOCKERINIT      = "{}/01_init".format(DOCKERFILEDIR)
DOCKERUSER      = "{}/02_user".format(DOCKERFILEDIR)
DOCKERBASE      = "{}/03_cpp".format(DOCKERFILEDIR)
DOCKERVIM       = "{}/04_vim".format(DOCKERFILEDIR)
DOCKERTAG       = "{}/05_tag".format(DOCKERFILEDIR)
DOCKERPLUGIN    = "{}/06_plugin".format(DOCKERFILEDIR)
DOCKERSETUP     = "{}/07_setup".format(DOCKERFILEDIR)

DOCKERUSERDATA  = "{}/userdata".format(DOCKERFILEDIR)
USER_JSON       = "./user_info.json"

VIMDIR          = "{}/vim".format(DOCKERDIR)
VIMRCINIT       = "{}/init_init.vim".format(VIMDIR)
VIMRCPROC       = "{}/init_proc.vim".format(VIMDIR)
VIMRCACT        = "{}/init.vim".format(VIMDIR)
VIMPLUGININIT   = "{}/01_plugin_init.vim".format(VIMDIR)
VIMPLUGINADD    = "{}/02_plugin_add.vim".format(VIMDIR)
VIMPLUGINFIN    = "{}/03_plugin_fin.vim".format(VIMDIR)
VIMCONF         = "{}/04_conf.vim".format(VIMDIR)
VIMCMD          = "{}/05_command.vim".format(VIMDIR)

RUN_SCRIPT = "./docker/shell/run"
GLOBALRC = "artifact/gnu-global/globalrc"

COMMON_PATH = ""
CLATE_JSON = os.getenv("HOME") + '/.clate.json'


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


def clate_manager():
    global VERSION
    global COMMON_PATH
    global CLATE_JSON

    clate_data = None

    # Common
    share_dir = COMMON_PATH + 'Share/'
    mkdir(share_dir)

    snippet_dir = COMMON_PATH + 'Snippet/'
    mkdir(snippet_dir)
    ultisnips_dir = snippet_dir + 'UltiSnips/'
    mkdir(ultisnips_dir)
    os.system("cp ./docker/artifact/UltiSnips/cpp.snippets {0}".format(ultisnips_dir))
    os.system("cp ./docker/artifact/UltiSnips/python.snippets {0}".format(ultisnips_dir))

    config_dir = COMMON_PATH + 'Config/'
    mkdir(config_dir)
    version_dir = config_dir + '/' + VERSION
    mkdir(version_dir)
    os.system("sudo cp {0} {1}".format(VIMRCACT, version_dir))

    common_dict = dict()

    common_dirs = dict()
    common_dirs['Path'] = COMMON_PATH
    common_dirs['Share'] = share_dir
    common_dirs['Snippet'] = snippet_dir
    common_dirs['Config'] = config_dir

    common_dict['directory'] = common_dirs
    common_dict['default_version'] = VERSION

    # Project
    if os.path.exists(CLATE_JSON):
        clate_json = open(CLATE_JSON).read()
        clate_data = json.loads(clate_json)
    else:
        clate_dir = COMMON_PATH + 'Clate/'
        mkdir(clate_dir)

        clate_dirs = dict()
        clate_dirs['Workspace'] = os.path.dirname(os.path.abspath(__file__))

        clate_project = dict()
        clate_project['name'] = 'clate'
        clate_project['version'] = VERSION
        clate_project['directory'] = clate_dirs

        project_list = list()
        project_list.append(clate_project)

        clate_data = dict()
        clate_data['project'] = project_list

    clate_data['common'] = common_dict
    write_clate_json(clate_data)

    # Install execute file
    os.system("sudo cp clate /usr/local/bin")


def config():
    global COMMON_PATH
    # Build dockerfile
    user_info = open(USER_JSON).read()
    user = json.loads(user_info)

    if user['UID'] == "USER_ID" \
        or user['UID'] == 'USER_ID_NUMBER' \
        or user['GROUP'] == 'GROUP_ID' \
        or user['GID'] == 'GROUP_ID_NUMBER' \
        or user['COMMON_PATH'] == 'CLATE_DIRECTORY':
        print("Please fill your info in user_info.json")
        return False

    USER_ENV = \
    """
# User info
ENV UID="{0}" \\\n\
    UNAME="{1}" \\\n\
    GID="{2}" \\\n\
    GNAME="{3}" \\\n\
    SHELL="/bin/bash" \\\n\
    HOME=/home/{1}\n\
\n
    """.format(user['UID'], user['ID'], user['GID'], user['GROUP'])
    common = user['COMMON_PATH']
    if common[-1] != '/':
        common += '/'

    if not os.path.exists(common):
        mkdir(common)

    COMMON_PATH = common

    user = open(DOCKERUSERDATA, "w")
    user.write(USER_ENV)
    user.close()

    os.system("cat {0} > {1}".format(DOCKERINIT,        DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERUSERDATA,   DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERUSER,       DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERBASE,       DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERVIM,        DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERTAG,        DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERPLUGIN,     DOCKERFILE))
    os.system("cat {0} >> {1}".format(DOCKERSETUP,      DOCKERFILE))

    if os.path.exists(DOCKERDIR + '/' + GLOBALRC):
        os.system("echo 'COPY {0} $HOME/.globalrc' >> {1}".format(GLOBALRC, DOCKERFILE))
        os.system("echo 'RUN chown $UNAME:$GROUP $HOME -R' >> {0}".format(DOCKERFILE))

    # Build init vimrc
    os.system("cat {0} > {1}".format(VIMPLUGININIT,     VIMRCINIT))
    os.system("cat {0} >> {1}".format(VIMPLUGINFIN,     VIMRCINIT))

    # Build proc vimrc
    os.system("cat {0} > {1}".format(VIMPLUGININIT,     VIMRCPROC))
    os.system("cat {0} >> {1}".format(VIMPLUGINADD,     VIMRCPROC))
    os.system("cat {0} >> {1}".format(VIMPLUGINFIN,     VIMRCPROC))

    # Build proc vimrc
    os.system("cp {0} {1}".format(VIMRCPROC,            VIMRCACT))
    os.system("cat {0} >> {1}".format(VIMCONF,          VIMRCACT))
    os.system("cat {0} >> {1}".format(VIMCMD,           VIMRCACT))

    # Run shell script
    run = open(RUN_SCRIPT, 'w')
    run.write("""#!/bin/bash
rm ~/.config/nvim/init.vim
ln -s /Config/{}/init.vim ~/.config/nvim/init.vim
sudo -u $UNAME -H bash -c "cd /Workspace && nvim ~/README.md"
    """.format(VERSION))
    run.close()

    return True


def install():
    # Build docker image
    os.system("cp README.md ./docker/artifact/")
    os.chdir(DOCKERDIR)
    os.system("docker build . -t {0}:{1}".format(NAME, VERSION))
    os.chdir("..")


def cleanup():
    os.system("rm {0}".format(VIMRCINIT))
    os.system("rm {0}".format(VIMRCPROC))
    os.system("rm {0}".format(VIMRCACT))
    os.system("rm {0}".format(DOCKERUSERDATA))
    os.system("rm {0}".format(DOCKERFILE))
    os.system("rm {0}".format(RUN_SCRIPT))
    os.system("rm docker/artifact/README.md")


if __name__ == "__main__":
    if config():
        clate_manager()
        install()
        cleanup()

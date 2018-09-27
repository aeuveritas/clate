#!/usr/bin/env python

import os
import json

# Variables
NAME            = "clate"
VERSION         = "0.1"

DOCKERDIR       = "./docker"
DOCKERFILE      = "{}/Dockerfile".format(DOCKERDIR)
DOCKERFILEDIR   = "{}/dockerfile".format(DOCKERDIR)
DOCKERINIT      = "{}/init".format(DOCKERFILEDIR)
DOCKERBASE      = "{}/base".format(DOCKERFILEDIR)
DOCKERVIM       = "{}/vim".format(DOCKERFILEDIR)
DOCKERTAG       = "{}/tag".format(DOCKERFILEDIR)
DOCKERUSER      = "{}/user".format(DOCKERFILEDIR)
DOCKERPLUGIN    = "{}/plugin".format(DOCKERFILEDIR)
DOCKERSETUP     = "{}/setup".format(DOCKERFILEDIR)

DOCKERUSERDATA  = "{}/userdata".format(DOCKERFILEDIR)
USER_JSON       = "./user_info.json"

VIMDIR          = "{}/vim".format(DOCKERDIR)
VIMRCINIT       = "{}/init_init.vim".format(VIMDIR)
VIMRCPROC       = "{}/init_proc.vim".format(VIMDIR)
VIMRCACT        = "{}/init.vim".format(VIMDIR)
VIMPLUGININIT   = "{}/plugin_init.vim".format(VIMDIR)
VIMPLUGINADD    = "{}/plugin_add.vim".format(VIMDIR)
VIMPLUGINFIN    = "{}/plugin_fin.vim".format(VIMDIR)
VIMPLUGIN       = "{}/plugin.vim".format(VIMDIR)
VIMCONF         = "{}/conf.vim".format(VIMDIR)
VIMCMD          = "{}/command.vim".format(VIMDIR)

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
    os.system("sudo cp {0} {1}".format(VIMRCACT, config_dir))
    os.system("sudo cp {0} {1}init.origin.vim".format(VIMRCACT, config_dir))

    common_dict = dict()
    common_dict['Share'] = share_dir
    common_dict['Snippet'] = snippet_dir
    common_dict['Config'] = config_dir

    # Project
    if os.path.exists(CLATE_JSON):
        clate_json = open(CLATE_JSON).read()
        clate_data = json.loads(clate_json)
    else:
        debug_dir = COMMON_PATH + 'Debug/'
        mkdir(debug_dir)
        
        debug_dirs = dict()
        debug_dirs['Base'] = debug_dir
        debug_dirs['Workspace'] = os.path.dirname(os.path.abspath(__file__))

        debug_project = dict()
        debug_project['name'] = 'debug'
        debug_project['directory'] = debug_dirs

        project_list = list()
        project_list.append(debug_project)
        
        clate_data = dict()
        clate_data['path'] = COMMON_PATH
        clate_data['project'] = project_list

    clate_data['common'] = common_dict
    clate_data['version'] = VERSION
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
    os.system("rm docker/artifact/README.md")

if __name__ == "__main__":
    if config():
        clate_manager()
        install()
        cleanup()

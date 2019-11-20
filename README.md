# Clate
Development sever for VS Code in Docker

![clate](img/clate.png "clate")

# History
* v0.1
  - native vim + youcompleteme
* v0.2
  - neovim + coc.nvim + llvm + ccls
* v0.3
  - vs code server + llvm + ccls

# Installation
1. Install Python Docker SDK
```
$ pip3 install docker
```
1. You can find your information with **id** linux command.
```
$ id [YOUR_ID]
```
  - If you use root account
```
$ id root
 uid=0(root) gid=0(root) groups=0(root),0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
```
2. Fill config.json
  - INSTALL_PATH is a directory to keep vscode-sever for each project.
  - Set "true" for target framework.
  - If you failed to configure ssh environment, please find you ip address and fill HOST_IP out.
3. Copy your id_rsa.pub to clate/docker/ssh_key/
4. Run install.py

# Console
* **Clate** console helps to manage projects.
  - create, list, active, remove project.
```
[ INF ] clate - dev
     [C]reate new project
     [L]ist projects
     [A]ctivate project
    a[T]tach running project
     [E]dit project configs

    l[I]st running project
   st[O]p running project
     [D]elete proect

    e[X]it
[ ASK ] command: 
```

* **Clate** provides useful commands
```
usage: clate [-h] [-a ACTIVE] [-d DEBUG] [-t ATTACH] [-o STOP] [-l] [-i]

optional arguments:
  -h, --help            show this help message and exit
  -a ACTIVE, --active ACTIVE
                        active project
  -d DEBUG, --debug DEBUG
                        attach to running project as root
  -t ATTACH, --attach ATTACH
                        attach to running project
  -o STOP, --stop STOP  stop project
  -l, --listproject     list all projects
  -i, --listrunningproject
                        list running projects
```

# Connect to clate from VS Code
1. Open VS Code
2. Install extension: Remote - SSH
3. Open Remote-SSH menu in left bar
   
  ![remote-ssh](img/remote-ssh.png "remote-ssh")

4. Refresh connections
5. Click target project

# VS Code extension and Settings
* Extensions are independent among projects, because they are stored in independant directory in INSTALL_PATH.
* In project directory, .vscode directory will be created, and all settings will be there.

# Installed SW
* Ubuntu 18.04
* gcc 8.3.0
* llvm 9.0.0 (clang inclued)
* python 3.6.7
* node 10.16.0
* cmake 3.10.2

# Trouble shooting
* If VS Code machine and Docker machine is different
  1. Before install Clate, Copy id_ras.pub for VS Code machine to clate/docker/ssh_key/
  2. Install Clate
  3. Make .ssh/config in VS Code machine and write server info, like
```
Host PROJECT_NAME_1
    User YOUR_ID
    Hostname DOCKER.MACHINE.HOST.IP
    Port PROJECT_PORT_1

Host PROJECT_NAME_2
    User YOUR_ID
    Hostname DOCKER.MACHINE.HOST.IP
    Port PROJECT_PORT_2
```
* If you make lots of projects, ports can conflict. In that case, open .ssh/config and clean up legacy or conflicted project.
* If you want to make your own docker image based on Clate,
  1. Make a new directory in **framework** and write **Dockerfile**.
  2. Add the directory name in config.json and give **true**.
  3. Run install.py
  4. You will have docker image, clate:YOUR_FRAMEWORK_DIRECTORY_NAME


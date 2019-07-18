#!/usr/bin/env python3

import os
import json
import shutil
import argparse

import docker

CLATE_JSON = os.getenv("HOME") + '/.clate.json'


class Docker:
    def __init__(self, client="clate"):
        self._client = client
        self._docker = docker.from_env()

    def get_names(self):
        names = list()
        for container in self._docker.containers.list():
            if "{0}".format(self._client) in container.name:
                names.append(container.name.replace("{0}_".format(self._client), ""))

        return names

    def _traverse(self, name, func=None):
        target_name = "{0}_{1}".format(self._client, name)
        for container in self._docker.containers.list():
            if target_name == container.name:
                if func:
                    func(container)
                return True

        return False

    def is_running(self, name):
        return self._traverse(name)

    def stop(self, name):
        return self._traverse(name, lambda obj: obj.stop())

    def get_using_images(self):
        images = set()
        for container in self._docker.containers.list():
            images.add(str(container.image))

        return images

    def is_using_image(self, tag):
        target_image = "clate:{0}".format(tag)
        using_images = list(self.get_using_images())

        for image in using_images:
            if target_image in image:
                return True

        return False

    def get_current_image_id(self, tag):
        target_image = "clate:{0}".format(tag)

        id = None
        try:
            id = self._docker.images.get(target_image).id
        except Exception as e:
            pass

        return id

    def remove_dangling_image(self, tag, id):
        current_image_id = self.get_current_image_id(tag)

        if current_image_id != id:
            try:
                self._docker.images.remove(image=id, force=True)
            except Exception as e:
                pass

    def get_tag_list(self):
        tags = list()

        for image in self._docker.images.list():
            if len(image.tags) == 0:
                continue

            name, tag = image.tags[0].split(':')
            if name == "clate":
                tags.append(tag)

        return tags

    def remove_all_images(self):
        for image in self._docker.images.list():
            if len(image.tags) == 0:
                continue
            name, tag = image.tags[0].split(':')
            if name in ('clate', 'aeuveritas/clate'):
                self._docker.images.remove(image=image.tags[0], force=True)


class DirManager:
    def exist(self, new_dir):
        if os.path.exists(new_dir):
            return True
        return False

    def endSlash(self, new_dir):
        if new_dir[-1] != '/':
            new_dir += '/'
        return new_dir

    def mkDir(self, new_dir):
        try:
            os.makedirs(new_dir)
        except OSError as e:
            print(e)

    def rmDir(self, t_dir):
        try:
            shutil.rmtree(t_dir)
        except shutil.Error as e:
            print(e)

    def rmFile(self, t_file):
        try:
            os.remove(t_file)
        except OSError as e:
            print(e)


class Interactor:
    def __init__(self, dirMgr):
        self._dirMgr = dirMgr

    def menu(self):
        print('     \x1b[1;32;40m' + "[C]" + '\x1b[0m' + "reate new project")
        print('     \x1b[1;32;40m' + "[L]" + '\x1b[0m' + "ist projects")
        print('     \x1b[1;32;40m' + "[A]" + '\x1b[0m' + "ctivate project")
        print('    a\x1b[1;32;40m' + "[T]" + '\x1b[0m' + "tach running project")
        print('     \x1b[1;32;40m' + "[E]" + '\x1b[0m' + "dit project configs")
        print('')
        print('    l\x1b[1;32;40m' + "[I]" + '\x1b[0m' + "st running project")
        print('   st\x1b[1;32;40m' + "[O]" + '\x1b[0m' + "p running project")
        print('     \x1b[1;32;40m' + "[D]" + '\x1b[0m' + "elete proect")
        print('')
        print('    e\x1b[1;32;40m' + "[X]" + '\x1b[0m' + "it")

        cmd = ""
        try:
            cmd = input("[ ASK ] command: ")
        except (KeyboardInterrupt):
            cmd = "x"

        return cmd

    def print_list(self, items):
        for (i, item) in enumerate(items):
            print("{0:2}: {1}".format(i, item))

    def list_select(self, items):
        ret = -1
        if len(items) == 0:
            return ret

        self.print_list(items)

        try:
            num = int(input("[ ASK ] select: "))
            if num <= len(items) and num >= 0:
                ret = num
        except (TypeError, ValueError, KeyboardInterrupt):
            print("[ WAR ] wrong input")

        return ret

    def binary_select(self):
        try:
            confirm = input("[ ASK ] confirm(y/N): ")
            if confirm in ('y', 'Y'):
                return True
        except (TypeError, ValueError, KeyboardInterrupt):
            print("[ WAR ] wrong input")

        return False

    def fill_project(self, name_list, tag_list, port_list):
        try:
            project_name = input("[ ASK ] project name: ")

            if project_name in name_list:
                print("[ WAR ] already existed: {}".format(project_name))
                return None

            print("[ INF ] frameworks")
            for (idx, tag) in enumerate(tag_list):
                print("    {0}: {1}".format(idx, tag))
            val = int(input("[ ASK ] select framework: "))
            project_tag = tag_list[val]

            import readline
            import glob

            def complete(text, state):
                return (glob.glob(text+'*')+[None])[state]
            readline.set_completer_delims(' \t\n;')
            readline.parse_and_bind("tab: complete")
            readline.set_completer(complete)

            dirs = dict()
            project_path = input("[ ASK ] project directory: ")
            if not self._dirMgr.exist(project_path):
                print("[ WAR ] not existed: {}".format(project_path))
                return
            dirs['Workspace'] = self._dirMgr.endSlash(project_path)

            while True:
                need_more = input("[ ASK ] additonal directory(y/N): ")
                if need_more in ('y', 'Y'):
                    new_name = input("[ ASK ] directory name: ")

                    new_path = input("[ ASK ] directory path: ")
                    if not self._dirMgr.exist(new_path):
                        print("[ WAR ] not existed: {}".format(new_path))
                        continue

                    self._dirMgr.endSlash(new_path)
                    dirs[new_name] = new_path
                else:
                    break

            ports = dict()
            while True:
                project_port = None
                try:
                    project_port = int(input("[ ASK ] project ssh port: "))
                    if str(project_port) in port_list:
                        print("[ ERR ] already used port: {}".format(project_port))
                        continue
                except ValueError:
                    print("[ ERR ] port must be a number")
                    continue
                ports['ssh'] = str(project_port)
                break

            while True:
                need_more = input("[ ASK ] additonal port(y/N): ")
                if need_more in ('y', 'Y'):
                    host_port = int(input("[ ASK ] host port: "))
                    docker_port = int(input("[ ASK ] docker port: "))
                    ports[str(host_port)] = str(docker_port)
                else:
                    break

            return project_name, project_tag, dirs, ports
        except KeyboardInterrupt:
            pass

        return None


class Setting_Manager:
    def __init__(self):
        global CLATE_JSON
        self._json_file = CLATE_JSON

    def update(self):
        clate_json = open(self._json_file, 'r')
        data = json.loads(clate_json.read())
        clate_json.close()

        return data['common'], data['project']

    def flush(self, common, project):
        data = dict()
        data['common'] = common
        data['project'] = project

        clate_json = open(self._json_file, 'w')
        clate_json.write(json.dumps(data, sort_keys=True, indent=4))
        clate_json.close()


class Clate:
    def __init__(self, dirMgr, interactor, client="clate"):
        self._common = None
        self._project = None
        self._project_names = None
        self._ssh_ports = None

        self._client = client
        self._dirMgr = dirMgr
        self._interactor = interactor
        self._setting = Setting_Manager()
        self._docker = Docker(client)

        self._common, self._project = self._setting.update()
        self._build_project_names()
        self._build_ssh_ports()

        print("[ INF ] {0} - {1}".format(client, self._common['version']))

    def _build_project_names(self):
        del self._project_names
        self._project_names = list()
        for project in self._project:
            self._project_names.append(project['name'])

    def _build_ssh_ports(self):
        del self._ssh_ports
        self._ssh_ports = list()
        for project in self._project:
            self._ssh_ports.append(project['port']['ssh'])

    def console(self):
        is_finish = False

        while not is_finish:
            cmd = self._interactor.menu().lower()

            if cmd == 'c':
                self._create()
            elif cmd == 'l':
                self.show_projects()
            elif cmd == 'a':
                self._run()
            elif cmd == 't':
                self._attach()
            elif cmd == 'e':
                self._edit_config()
            elif cmd == 'o':
                self._stop()
            elif cmd == 'i':
                self.show_running_projects()
            elif cmd == 'd':
                self._delete()
            elif cmd == 'x':
                return
            else:
                print("[ WAR ] wrong command")

            print("")

    def _get_running_project(self):
        return self._docker.get_names()

    def show_running_projects(self):
        print('[ INF ] Running projects')
        names = self._get_running_project()
        self._interactor.print_list(names)

    def _edit_config(self):
        global CLATE_JSON
        os.system("vi {0}".format(CLATE_JSON))

    def _attach_project(self, project_name):
        docker_cmd = "docker exec -ti clate_{0} /bin/bash".format(project_name)
        os.system(docker_cmd)

    def _attach(self):
        names = self._get_running_project()
        num = self._interactor.list_select(names)

        if num != -1:
            project_name = names[num]
            self._attach_project(project_name)

    def attach(self, project_name):
        names = self._get_running_project()
        if project_name in names:
            self._attach_project(project_name)

    def show_projects(self):
        print('[ INF ] All projects')
        for idx, project in enumerate(self._project):
            print("{0:2}: {1}".format(idx, project['name']))

    def _build_project(self, name, tag, dirs, ports):
        project = dict()

        project['name'] = name
        project['tag'] = tag
        dirs['extension'] = self._common['install_path'] + 'vscode-server/' + name + '/'
        project['directory'] = dirs
        project['port'] = ports

        ssh_config = """
Host {0}
    User {1}
    Hostname {2}
    Port {3}
""".format(name, self._common['user'], self._common['host_ip'], ports['ssh'])
        os.system("echo '{0}' >> ~/.ssh/config".format(ssh_config))

        self._dirMgr.mkDir(dirs['extension'])

        return project

    def _create(self):
        tags = self._docker.get_tag_list()
        name, tag, dirs, ports = self._interactor.fill_project(self._project_names, tags, self._ssh_ports)
        new_project = self._build_project(name, tag, dirs, ports)

        self._project.append(new_project)
        self._build_project_names()
        self._build_ssh_ports()
        self._setting.flush(self._common, self._project)
        print("[ SUC ] created: {}".format(new_project))

    def _delete(self):
        project_num = self._interactor.list_select(self._project_names)

        if project_num != -1:
            if project_num == 0:
                print("[ WAR ] project - Clate is not earasable.")
            else:
                project_name = self._project_names[project_num]
                if not self._docker.is_running(project_name):
                    confirm = self._interactor.binary_select()
                    if confirm:
                        project = self._project[project_num]
                        self._dirMgr.rmDir(project['directory']['extension'])
                        del self._project[project_num]
                        self._build_project_names()
                        self._build_ssh_ports()
                        print("[ SUC ] deleted: {}".format(project_name))
                        self._setting.flush(self._common, self._project)
                    else:
                        print("[ WAR ] canceled")
                else:
                    print("[ WAR ] cannot delete, because it is still running: {}".format(project_name))

    def _run_project(self, project, is_debug=False):
        dockercmd = "docker run -td --rm "

        dockercmd += "--name {0}_{1} ".format(self._client, project['name'])

        for target, host in project['directory'].items():
            if target == 'extension':
                dockercmd += "-v {0}:/home/{1}/.vscode-server ".format(host, self._common['user'])
            else:
                dockercmd += "-v {0}:/{1} ".format(host, target)

        dockercmd += "--env CLATE_CLIENT={0} ".format(self._client)
        dockercmd += "--env PROJECT_NAME={0} ".format(project['name'])

        dockercmd += "-p {0}:22 ".format(project['port']['ssh'])

        for host, docker in project['port'].items():
            if host != 'ssh':
                dockercmd += "-p {0}:{1} ".format(host, docker)

        if is_debug:
            dockercmd += "--entrypoint /bin/bash "

        dockercmd += "clate:{0}".format(project['tag'])

        print("[ SUC ] docker cmd: {}".format(dockercmd))
        os.system(dockercmd)
        print("[ SUC ] activated: {0}".format(project['name']))

    def _select_project(self):
        return self._interactor.list_select(self._project_names)

    def _run(self):
        project_num = self._select_project()
        if project_num != -1:
            self._run_project(self._project[project_num])

    def run(self, project_name='clate', is_debug=False):
        idx = None
        try:
            idx = self._project_names.index(project_name)
        except ValueError:
            print("[ ERR ] no project: {0}".format(project_name))
            return

        self._run_project(self._project[idx], is_debug)

    def _stop_project(self, project_name):
        ret = self._docker.stop(project_name)
        if ret:
            print("[ SUC ] stopped: {}".format(project_name))
        else:
            print("[ WAR ] cannot find running clate: {}".format(project_name))

    def _stop(self):
        names = self._get_running_project()
        num = self._interactor.list_select(names)

        if num != -1:
            project_name = names[num]
            self._stop_project(project_name)

    def stop(self, project_name='clate'):
        try:
            self._project_names.index(project_name)
        except ValueError:
            print("[ ERR ] no project: {0}".format(project_name))
            return

        self._stop_project(project_name)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--active', help='active project', default=None)
    parser.add_argument('-d', '--debug', help='run project with debug mode', default=None)
    parser.add_argument('-t', '--attach', help='attach to running project', default=None)
    parser.add_argument('-o', '--stop', help='stop project', default=None)
    parser.add_argument('-l', '--listproject', help='list all projects', action='store_true')
    parser.add_argument('-i', '--listrunningproject', help='list running project', action='store_true')

    return parser.parse_args()


def check_param(params):
    cnt = 0

    if params.active:
        cnt += 1
    if params.debug:
        cnt += 1
    if params.listproject:
        cnt += 1
    if params.stop:
        cnt += 1
    if params.listrunningproject:
        cnt += 1
    if params.attach:
        cnt += 1

    if cnt > 1:
        print("[ ERR ] only 1 option is available.")
        return False

    return True


def clate_main(clate, params):
    if params.active:
        clate.run(params.active)
    elif params.debug:
        clate.run(params.debug, is_debug=True)
    elif params.listproject:
        clate.show_projects()
    elif params.stop:
        clate.stop(params.stop)
    elif params.listrunningproject:
        clate.show_running_projects()
    elif params.attach:
        clate.attach(params.attach)
    else:
        clate.console()

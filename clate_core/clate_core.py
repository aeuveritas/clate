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

    def is_using_image(self, version):
        target_image = "clate:{0}".format(version)
        using_images = list(self.get_using_images())

        for image in using_images:
            if target_image in image:
                return True

        return False

    def get_current_image_id(self, version):
        target_image = "clate:{0}".format(version)

        id = None
        try:
            id = self._docker.images.get(target_image).id
        except Exception as e:
            pass

        return id

    def remove_dangling_image(self, version, id):
        current_image_id = self.get_current_image_id(version)

        if current_image_id != id:
            try:
                image = self._docker.images.remove(image=id, force=True)
            except Exception as e:
                pass


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
        print(' dele\x1b[1;32;40m' + "[T]" + '\x1b[0m' + "e proect")
        print('     \x1b[1;32;40m' + "[E]" + '\x1b[0m' + "dit project configs")
        print('')
        print('     \x1b[1;32;40m' + "[G]" + '\x1b[0m' + "enerate compile_commands.json")
        print('')
        print('   st\x1b[1;32;40m' + "[O]" + '\x1b[0m' + "p running project")
        print('   li\x1b[1;32;40m' + "[S]" + '\x1b[0m' + "t running project")
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
            print("{0}: {1}".format(i, item))

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

    def fill_project(self, name_list, default_version, port):
        try:
            project_name = input("[ ASK ] project name: ")

            if project_name in name_list:
                print("[ WAR ] already existed: {}".format(project_name))
                return None

            import readline
            import glob

            def complete(text, state):
                return (glob.glob(text+'*')+[None])[state]
            readline.set_completer_delims(' \t\n;')
            readline.parse_and_bind("tab: complete")
            readline.set_completer(complete)

            project_path = input("[ ASK ] project directory: ")
            if not self._dirMgr.exist(project_path):
                print("[ WAR ] not existed: {}".format(project_path))
                return
            project_path = self._dirMgr.endSlash(project_path)

            dirs = dict()
            dirs['Workspace'] = project_path

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

            new_project = dict()
            new_project['name'] = project_name
            new_project['version'] = default_version
            new_project['directory'] = dirs
            new_project['port'] = port

            return new_project
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

        self._client = client
        self._dirMgr = dirMgr
        self._interactor = interactor
        self._setting = Setting_Manager()
        self._docker = Docker(client)

        self._common, self._project = self._setting.update()
        self._build_project_names()

        print("[ INF ] {0} - {1}".format(client, self._common['default_version']))

    def _build_project_names(self):
        del self._project_names
        self._project_names = list()
        for project in self._project:
            self._project_names.append(project['name'])

    def console(self):
        is_finish = False

        while not is_finish:
            cmd = self._interactor.menu().lower()

            if cmd == 'c':
                self._create()
            elif cmd == 'l':
                self.show()
            elif cmd == 'a':
                self._run()
            elif cmd == 't':
                self._delete()
            elif cmd == 'e':
                self._edit_config()
            elif cmd == 'g':
                self._compile()
            elif cmd == 'o':
                self._stop()
            elif cmd == 's':
                self._show_running_project()
            elif cmd == 'x':
                return
            else:
                print("[ WAR ] wrong command")

            print("")

    def _compile_project(self, project):
        try:
            project_dir = project['directory']['Workspace']
            cc_file = project_dir + 'compile_commands.json'
            if self._dirMgr.exist(cc_file):
                self._dirMgr.rmFile(cc_file)

            cmake_option = project['build']['cmake_option']
            cmd = "cmake -H{0} -B{0}/CLATE -DCMAKE_EXPORT_COMPILE_COMMANDS=YES {1}".format(project_dir, cmake_option)
            os.system(cmd)

            cmd = "cp {0}/CLATE/compile_commands.json {0}".format(project_dir)
            os.system(cmd)

            cmd = "rm -rf  {0}/CLATE".format(project_dir)
            os.system(cmd)
            print("[ SUC ] generate: compile_commands.json")
        except:
            print("[ WAR ] cannot generate: compile_commands.json")
            print("[ INF ] compile_commands.json is only available for cpp proejct with cmake")

    def _compile(self):
        project_num = self._select_project()
        if project_num != -1:
            self._compile_project(self._project[project_num])

    def _get_running_project(self):
        return self._docker.get_names()

    def _show_running_project(self):
        names = self._get_running_project()
        self._interactor.print_list(names)

    def _edit_config(self):
        global CLATE_JSON
        os.system("vi {0}".format(CLATE_JSON))

    def _stop(self):
        names = self._get_running_project()
        num = self._interactor.list_select(names)

        if num != -1:
            project_name = names[num]
            ret = self._docker.stop(project_name)
            if ret:
                print("[ SUC ] stopped: {}".format(project_name))
            else:
                print("[ WAR ] cannot find running clate: {}".format(project_name))

    def show(self):
        for idx, project in enumerate(self._project):
            print("{0:2}: {1}".format(idx, project['name']))


    def _create(self):
        self._common['last_port'] += 1
        new_project = self._interactor.fill_project(self._project_names, self._common['default_version'], self._common['last_port'])

        if new_project:
            self._project.append(new_project)
            self._build_project_names()
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
                        del self._project[project_num]
                        self._build_project_names()
                        print("[ SUC ] deleted: {}".format(project_name))
                        self._setting.flush(self._common, self._project)
                    else:
                        print("[ WAR ] canceled")
                else:
                    print("[ WAR ] cannot delete, because it is still running: {}".format(project_name))

    def _run_project(self, project, is_debug=False):
        dockercmd = "docker run -ti --rm "

        dockercmd += "--name {0}_{1} ".format(self._client, project['name'])

        for target, host in project['directory'].items():
            dockercmd += "-v {0}:/{1} ".format(host, target)

        dockercmd += "--env CLATE_CLIENT={0} ".format(self._client)
        dockercmd += "--env PROJECT_NAME={0} ".format(project['name'])

        version = project['version']
        if version in ('0.3', ):
            dockercmd += "-v {0}:/home/{1}/.vscode-server ".format(self._common['extension'], self._common['user'])
            dockercmd += "-p {0}:22 ".format(project['port'])
        elif version in ('0.2', ):
            dockercmd += "--env BUILD_CMD='{0}' ".format(project['build']['build_cmd'])
            dockercmd += "--env RUN_CMD='{0}' ".format(project['build']['run_cmd'])
            dockercmd += """--env CMAKE_CMD="{0}" """.format(project['build']['cmake_cmd'])
        else:
            print("[ WAR ] undefined version: {0}".format(version))

        if is_debug:
            dockercmd += "--entrypoint /bin/bash "

        dockercmd += "clate:{0}".format(project['version'])

        print("[ SUC ] run: {}".format(dockercmd))
        os.system(dockercmd)

    def _select_project(self):
        return self._interactor.list_select(self._project_names)

    def _run(self, is_debug=False):
        project_num = self._select_project()
        if project_num != -1:
            self._run_project(self._project[project_num], is_debug)

    def run(self, project_name='clate', is_debug=False):
        idx = None
        try:
            idx = self._project_names.index(project_name)
        except ValueError:
            print("[ WAR ] no project: {0}".format(project_name))
            return

        self._run_project(self._project[idx], is_debug)

    def compile(self, project_name='clate'):
        idx = None
        try:
            idx = self._project_names.index(project_name)
        except ValueError:
            print("[ WAR ] no project: {0}".format(project_name))
            return

        self._compile_project(self._project[idx])


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--active', help='active project', default=None)
    parser.add_argument('-g', '--generate', help='generate compile_commands.json', default=None)
    parser.add_argument('-d', '--debug', help='run project with debug mode', action='store_true')
    parser.add_argument('-l', '--list', help='list all projects', action='store_true')

    return parser.parse_args()


def check_param(params):
    cnt = 0

    if params.active:
        cnt += 1
    if params.generate:
        cnt += 1
    if params.debug:
        cnt += 1
    if params.list:
        cnt += 1

    if cnt > 1:
        print("[ ERR ] only 1 option is available.")
        return False

    return True


def clate_main(clate, params):
    if params.active:
        clate.run(params.active)
    elif params.generate:
        clate.compile(params.generate)
    elif params.debug:
        clate.run(is_debug=True)
    elif params.list:
        clate.show()
    else:
        clate.console()

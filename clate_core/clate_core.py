#!/usr/bin/env python3

import os
import json
import shutil

import docker

CLATE_JSON = os.getenv("HOME") + '/.clate.json'

AVAILABLE_VERSION = [
    '0.1',
    '0.2',
]


class Docker:
    def __init__(self):
        self._client = docker.from_env()

    def get_names(self):
        names = list()
        for container in self._client.containers.list():
            if "clate_" in container.name:
                names.append(container.name.replace("clate_", ""))

        return names

    def _traverse(self, name, func=None):
        target_name = "clate_{}".format(name)
        for container in self._client.containers.list():
            if target_name == container.name:
                if func:
                    func(container)
                return True

        return False

    def is_running(self, name):
        return self._traverse(name)

    def stop(self, name):
        return self._traverse(name, lambda obj: obj.stop())


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

    def menu(self, support_cpp):
        print('    \x1b[1;32;40m' + "[C]" + '\x1b[0m' + "reate new project")
        print('    \x1b[1;32;40m' + "[L]" + '\x1b[0m' + "ist projects")
        print('    \x1b[1;32;40m' + "[A]" + '\x1b[0m' + "ctivate project")
        print('dele\x1b[1;32;40m' + "[T]" + '\x1b[0m' + "e proect")
        print('chan\x1b[1;32;40m' + "[E]" + '\x1b[0m' + " version")
        print('')
        print('  st\x1b[1;32;40m' + "[O]" + '\x1b[0m' + "p running project")
        print('  li\x1b[1;32;40m' + "[S]" + '\x1b[0m' + "t running project")
        print('')
        if support_cpp:
            print('gene\x1b[1;32;40m' + "[R]" + '\x1b[0m' + "ate compile_commands.json")
            print('')
        print('   e\x1b[1;32;40m' + "[X]" + '\x1b[0m' + "it")

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

    def fill_project(self, name_list, default_version):
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

            clang = dict()
            clang['directory'] = 'CLATE'
            clang['option'] = '-DCMAKE_BUILD_TYPE=Debug'

            new_project = dict()
            new_project['name'] = project_name
            new_project['version'] = default_version
            new_project['directory'] = dirs
            new_project['clang'] = clang

            return new_project
        except KeyboardInterrupt:
            pass

        return None


class Setting_Manager:
    def __init__(self, json_file):
        self.json_file = json_file

    def update(self):
        clate_json = open(self.json_file, 'r')
        data = json.loads(clate_json.read())
        clate_json.close()

        return data['common'], data['project']

    def flush(self, common, project):
        data = dict()
        data['common'] = common
        data['project'] = project

        clate_json = open(self.json_file, 'w')
        clate_json.write(json.dumps(data, sort_keys=True, indent=4))
        clate_json.close()


class Clate:
    def __init__(self, json_file, dirMgr, interactor):
        self._common = None
        self._project = None
        self._project_names = None

        self._dirMgr = dirMgr
        self._interactor = interactor
        self._setting = Setting_Manager(json_file)
        self._docker = Docker()

        self._common, self._project = self._setting.update()
        self._build_project_names()

        print("[ INF ] Clate - {0}".format(self._common['default_version']))

    def _build_project_names(self):
        del self._project_names
        self._project_names = list()
        for project in self._project:
            self._project_names.append(project['name'])

    def console(self):
        is_finish = False

        while not is_finish:
            support_cpp = self._common['language']['CPP']
            cmd = self._interactor.menu(support_cpp).lower()

            if cmd == 'c':
                self._create()
            elif cmd == 'l':
                self._show()
            elif cmd == 'a':
                self._run()
            elif cmd == 't':
                self._delete()
            elif cmd == 'e':
                self._change_version()
            elif cmd == 'o':
                self._stop()
            elif cmd == 's':
                self._show_running_project()
            elif cmd == 'r' and support_cpp:
                self._compile()
            elif cmd == 'x':
                return
            else:
                print("[ WAR ] wrong command")

            print("")

    def _compile_project(self, project):
        try:
            project_dir = project['directory']['Workspace']
            compile_dir = project['clang']['directory']
            compile_option = project['clang']['option']
            cc_file = project_dir + 'compile_commands.json'
            if self._dirMgr.exist(cc_file):
                self._dirMgr.rmFile(cc_file)

            cmd = "cmake -H{0} -B{0}/{1} -DCMAKE_EXPORT_COMPILE_COMMANDS=YES {2}".format(project_dir, compile_dir, compile_option)
            os.system(cmd)

            cmd = "ln -s {0}/{1}/compile_commands.json {0}".format(project_dir, compile_dir)
            os.system(cmd)
            print("[ SUC ] generate: compile_commands.json")
        except:
            print("[ WAR ] cannot generate: compile_commands.json")

    def _compile(self):
        project_num = self._select_project()
        if project_num != -1:
            self._compile_project(self._project[project_num])

    def _get_running_project(self):
        return self._docker.get_names()

    def _show_running_project(self):
        names = self._get_running_project()
        self._interactor.print_list(names)

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

    def _show(self):
        print("COMMON")
        print(json.dumps(self._common, indent=4, sort_keys=True))
        print("PROJECT")
        print(json.dumps(self._project, indent=4, sort_keys=True))

    def _createTempDir(self, new_project):
        temp_dir = self._common['directory']['Path'] + 'Temp/' + new_project['name'] + '/'
        new_project['directory']['Temp'] = temp_dir
        self._dirMgr.mkDir(temp_dir)

    def _create(self):
        new_project = self._interactor.fill_project(self._project_names, self._common['default_version'])

        if new_project:
            self._createTempDir(new_project)
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
                        self._dirMgr.rmDir(self._project[project_num]['directory']['Temp'])
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

        dockercmd += "--name clate_{} ".format(project['name'])

        for target, host in project['directory'].items():
            dockercmd += "-v {0}:/{1} ".format(host, target)

        for target, host in self._common['directory'].items():
            dockercmd += "-v {0}:/{1} ".format(host, target)

        if is_debug:
            dockercmd += "--entrypoint /bin/bash "

        dockercmd += "clate:{0}".format(project['version'])

        print("[ SUC ] run: {}".format(dockercmd))
        os.system(dockercmd)

    def _select_project(self):
        return self._interactor.list_select(self._project_names)

    def _select_version(self):
        global AVAILABLE_VERSION
        return self._interactor.list_select(AVAILABLE_VERSION)

    def _run(self, is_debug=False):
        project_num = self._select_project()
        if project_num != -1:
            self._run_project(self._project[project_num], is_debug)

    def _change_version(self):
        project_num = self._select_project()
        if project_num != -1:
            project = self._project[project_num]
            if self._docker.is_running(project['name']):
                print("[ WAR ] cannot change version, because it is still running: {}".format(project['name']))
                return

            version_num = self._select_version()
            if version_num != -1:
                project['version'] = AVAILABLE_VERSION[version_num]
                self._setting.flush(self._common, self._project)

                print("[ SUC ] version is updated - project: {0}, version: {1}".format(project['name'], project['version']))

    def run(self, project_name='clate', is_debug=False):
        idx = None
        try:
            idx = self._project_names.index(project_name)
        except ValueError:
            print("[ WAR ] no project: {0}".format(project_name))
            return

        self._run_project(self._project[idx], is_debug)

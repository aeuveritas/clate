#!/usr/bin/env python3

import os
import json

from clate_core.clate_core import Docker
from clate_core.clate_core import DirManager


CLATE_EXE    = "/usr/local/bin/clate"
CLATE_JSON   = os.getenv("HOME") + '/.clate.json'


def main():
    dirMgr = DirManager()

    if dirMgr.exist(CLATE_JSON):
        clate_json = open(CLATE_JSON).read()
        clate_info = json.loads(clate_json)
        install_path = clate_info['common']['install_path']

        dirMgr.rmDir(install_path)
        dirMgr.rmFile(CLATE_JSON)

    if dirMgr.exist(CLATE_EXE):
        os.system("sudo rm -rf {0}".format(CLATE_EXE))

    docker = Docker("clate")
    docker.remove_all_images()

    print("clate is uninstalled")

if __name__ == '__main__':
    main()

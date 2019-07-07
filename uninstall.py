#!/usr/bin/env python3

import os
import json

CONFIG_JSON = "./config.json"
CLATE_JSON  = os.getenv("HOME") + '/.clate.json'

def main():
    config_json = open(CONFIG_JSON).read()
    common = json.loads(config_json)

    install_path = common['INSTALL_PATH']

    os.system("sudo rm /usr/local/bin/clate")
    os.system("rm -rf {}".format(install_path))
    os.system("rm -rf {}".format(CLATE_JSON))


if __name__ == '__main__':
    main()

#!/usr/bin/env python

import os
import json

USER_JSON       = "./user_info.json"
CLATE_JSON = os.getenv("HOME") + '/.clate.json'

def main():
    user_info = open(USER_JSON).read()
    user = json.loads(user_info)

    common = user['COMMON_PATH']

    os.system("sudo rm /usr/local/bin/clate")
    os.system("rm -rf {}".format(common))
    os.system("rm -rf {}".format(CLATE_JSON))

if __name__ == '__main__':
    main()

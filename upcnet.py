#!/usr/bin/python3
#!coding=utf-8
from net import *
from sys import argv

if __name__ == '__main__':
    if len(argv) > 1:
        if len(argv) > 2:
            print('Too many args')

        else:
            if argv[1] == 'reset':
                file_path = getpath()
                if os.path.exists(file_path):
                    os.remove(file_path)
                print('Reset successful')

            elif argv[1] == 'logout':
                logout()

            else:
                print('Wrong args')

    else:
        config_init()

        if online():
            print("Already online")  # 已经登录

        else:
            login()


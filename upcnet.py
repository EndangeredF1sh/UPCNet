from login import *
from getpass import getpass
from ping import ping


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            print('Too many args')

        else:
            argv = sys.argv[1]
            if argv == 'reset':
                file_path = getpath()
                if os.path.exists(file_path):
                    os.remove(file_path)
                print('Reset successful')

            elif argv == 'logout':
                logout()

            else:
                print('Wrong args')

    else:
        file_path = getpath()
        if not os.path.exists(file_path):
            str_tmp = input('School number: ')
            str_tmp = str_tmp + ' ' + getpass('Password: (Hidden)')
            str_tmp = str_tmp + ' ' + input('1.default\n2.unicom\n3.cmcc\n4.ctcc\n5.local\nCommunications number: ')
            file = open(file_path, 'wb')
            file.write(encode(str_tmp))  # 加密后的字符串写入二进制文件

        if ping("1.2.4.8"):
           print("Already online")  # 已经登录

        else:
            login()


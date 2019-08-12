import os
import sys

ver = sys.version_info

def Check_response():
    return True

def Check_module(module):
    modules = sys.modules.keys()
    if not module in modules:
        print('Cannot resolve ' + module)
        q = None
        question = 'Do you want to download module ' + module + '? (Y/N): '
        while not any([q == 'y', q == 'Y', q == 'n', q =='N']):
            try: q = raw_input(question)
            except NameError: q = input(question)

            if q == 'Y' or q == 'y':
                print('Downloading ' + module + '...')
                os.system('python -m pip install ' + module)
                
                if module in modules:
                    return True
                else:
                    print('Cannot download/install ' + module)
                    return False

            elif q == 'N' or q == 'n':
                print('Module ' + module + " hasn't been installed")
                quit()
    else:
        return True

def Check_pip():
    global ver
    ver = str(ver[0]) + str(ver[1])
    path_main = str('\Python' + ver)
    path = os.path.join(path_main, 'Scripts', 'pip.exe')
    if os.path.exists(path):
        return True

def main(args):
    global ver
    if not ver[:2] == (3,4) and not Check_pip():
        print("You don't have required python version")
        print("Go to a python official website to download latest versions. https://www.python.org/downloads")
        os.system('pause >NUL')
        quit()
    else:
        pass

    for arg in args:
        if Check_module(arg):
            print('Module ' + arg + ' installed and available.')
        else:
            print('An error appeared during module check. Error caused by module: ' + arg)

    print('Module checking done.')

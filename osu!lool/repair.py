import os
import sys

ver = sys.version_info
modules = sys.modules.keys()

def Check_response():
    return True

def Check_module(module):
    if not module in modules:
        print('Cannot resolve ' + module)
        return False
    else:
        return True
    
def Download_module(module):
    q = None
    question = 'Do you want to download module ' + module + '? (Y/N): '
    while not any([q == 'y', q == 'Y', q == 'n', q =='N']):
        try: q = raw_input(question)
        except NameError: q = input(question)

        if q == 'Y' or q == 'y':
            print('Downloading ' + module + '...')

            os.system('py -m pip install ' + module)

            if module in modules:
                return True
            else:
                print('Cannot download/install ' + module)
                return False

        elif q == 'N' or q == 'n':
            print('Module ' + module + " hasn't been installed")
            return

def Check_pip():
    path_main = sys.executable[:-11]
    path = os.path.join(path_main, 'Scripts', 'pip.exe')
    if os.path.exists(path):
        return True

def main(args):
    global ver
    if not ver[0] == 3 and not ver[1] >= 4 and not Check_pip():
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
            if not Download_module(arg):
                print('An error appeared during module check. Error caused by module: ' + arg)

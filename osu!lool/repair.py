def Check_response():
    """
    rtype: none
    returns: bool
    """
    return True

import os
import sys
from helper import ask

ver = sys.version_info
modules = sys.modules.keys()

def Check_module(module):
    """
    rtype: string
    returns: bool
    """
    if not module in modules:
        print('Cannot resolve ' + module)
        return False
    else:
        return True
    
def Download_module(module):
    """
    rtype: string
    returns: bool
    """
    if ask('Do you want to download module ' + module + '?'):
        print('Downloading ' + module + '...')

        os.system('py -m pip install ' + module)

        if module in modules:
            return True
        else:
            print('Cannot download/install ' + module)
            return False

    else:
        print('Module ' + module + " hasn't been installed")
        return True

def Check_pip():
    """
    rtype: none
    returns: bool
    """
    path_main = sys.executable[:-11]
    path = os.path.join(path_main, 'Scripts', 'pip.exe')
    if os.path.exists(path):
        return True

def main(args):
    """
    rtype: array
    returns: none
    """
    if not (ver[0] == 3) and (ver[1] >= 4): # and not Check_pip():
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
            Download_module(arg)
            if not Check_module(arg):
                print('An error appeared during module check. Error caused by module: ' + arg)

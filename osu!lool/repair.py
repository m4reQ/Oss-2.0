import os
import sys

def Check_response():
    return True

def Check_module(module):
    modules = s.modules.keys()
    if not module in modules:
        print('Cannot resolve ' + module)
        q = ''
        while not any([q == 'y'], [q == 'Y'], [q == 'n'], [q =='N']):
            q = input('Do you want to download module ' + module + '? (Y/N)')
            if q == 'Y' or q == 'y':
                if 'pip' in modules:
                    print('Downloading ' + module + '...')
                    os.system('python -m pip install ' + module)
                else:
                    print('Cannot download ' + module)      

            elif q == 'N' or q == 'n':
                print('module ' + module + " hasn't been installed")
                os.system('pause >NUL')
                quit()

def main():
    ver = sys.version_info
    if not sys.version_info[:2] == (3,4):
        print("You don't have required python version")
        print("Go to a python official website to download latest versions. https://www.python.org/downloads")
        os.system('pause >NUL')
        quit()
    else:
        pass

    Check_module('pygame')        
    
    modules = s.modules.keys()
    if 'pygame' in modules:
              print('All modules installed and available. Now you can safely launch the game.')

if __name__ == '__main__':
    main()
    quit()

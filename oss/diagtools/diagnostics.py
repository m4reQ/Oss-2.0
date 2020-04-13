#WARNING
#This module is quite old and probably could 
#not work in 100% as it should be. Be careful
#when using it.

try:
    import os
    import sys
    import ctypes
    import platform
    import requests
    import pygame
except ImportError as e:
    print(e)

dir = os.getcwd()
path = os.path.join(dir[:-10], 'oss')
sys.path.append(path)

log = {"system_ver": '',
       "python_ver": '',
       "screen_res": '',
       "CPU": '',
       "path": '',
       "pygame_ver": '',
       "graphics_info": ''}

def Get_sys_ver():
    name = os.name
    sys = platform.system()
    rel = platform.release()

    return '{}, {} {}'.format(name, sys, rel)

def Get_graph_info():
    if platform.system() == 'Windows':
        try:
            import wmi

            comp = wmi.WMI()
            gpu_info = comp.Win32_VideoController()[0]
            fgpu_info = 'Graphics card: {}'.format(gpu_info.Name)
            return fgpu_info
        except ImportError:
            return '---'
    else:
        return '---'

def Get_python_ver():
    ver = ''
    for e in sys.version_info:
        ver += '.' + str(e)
    ver = ver[1:]
    return str(ver)

def Get_screen_res():
    user32 = ctypes.windll.user32
    scrsize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
    res = 'Width: {} | Height: {}'.format(scrsize[0], scrsize[1])
    return res

def Gen_log():
    print('Generating log file...')
    with open('diaglog.txt', 'w+') as  f:
        f.write('')

    try:
        log['system_ver'] = Get_sys_ver()
        log['python_ver'] = Get_python_ver()
        log['path'] = '{} {}'.format(os.sys.path, os.popen('echo %path%').read())
        log['screen_res'] = Get_screen_res()
        log['CPU'] = str(platform.processor())
        log['pygame_ver'] = str(pygame.version.ver)
        try:
            log['sdl_driver'] = os.environ['SDL_VIDEODRIVER']
        except KeyError:
            log['sdl_driver'] = 'not set'
        log['graphics_info'] = Get_graph_info()
    except Exception:
        pass

    for key, val in log.items():
        with open('diaglog.txt', 'a') as f:
            f.write('{}: {}\n'.format(key, val))

if __name__ == '__main__':
    Gen_log()
    os.system("pause >NUL")

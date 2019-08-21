dont_check_net = False

try:
    import os
    import sys
    import ctypes
    import platform
except ImportError:
    dont_check_net = True

dir = os.getcwd()
path = os.path.join(dir[:-10], 'osu!lool')
sys.path.append(path)

log = {"System_ver": "",
       "Python_ver": "",
       "Screen_res": "",
       "CPU": "",
       "path": ""}

def Get_sys_ver():
    name = os.name
    sys = platform.system()
    rel = platform.release()
    
    ver = name + ", " + sys + rel
    return ver

def Get_python_ver():
    ver = ""
    for e in sys.version_info:
        ver += '.' + str(e)
    ver = ver[1:]
    return str(ver)

def Get_screen_res():
    user32 = ctypes.windll.user32
    scrsize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
    res = ('Width: ' + str(scrsize[0]) + ' Height: ' + str(scrsize[1]))
    return str(res)

def Get_cpu_inf():
    return str(platform.processor())

def Get_path():
    return str(os.sys.path) + " " + str(os.popen('echo %path%').read())

def Gen_log():
    print('Generating log file...')
    f = open('diaglog.txt', 'w+')
    
    log['System_ver'] = Get_sys_ver()
    log['Python_ver'] = Get_python_ver()
    log['path'] = Get_path()
    log['Screen_res'] = Get_screen_res()
    log['CPU'] = Get_cpu_inf()  

    for key, val in log.items():
        f.write(str(key + ": " + val + "\n"))
    f.close()

if __name__ == '__main__':
    Gen_log()
    exit()

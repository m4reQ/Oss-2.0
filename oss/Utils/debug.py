ENABLE = False

def Enable():
    global ENABLE
    ENABLE = True

    print("[INFO]<debug> Debugging enabled.")

def Log(message, logLevel, sender):
    if not ENABLE:
        return
    
    print("[{}]<{}> {}".format(logLevel, sender, message))

class LogLevel:
    Info = "INFO"
    Warning = "WARNING"
    Error = "ERROR"
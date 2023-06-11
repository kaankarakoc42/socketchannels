import json

def responseGenerator(socket):
    while True:
        received = socket.recv(1024).decode("utf8")
        while "\r\n" in received:
            index = received.index("\r\n")
            message = received[:index]
            received = received[index + 2:]
            #print("received",json.loads(message))
            yield json.loads(message)
            
            
def send(socket,channel,data={}):
    data.update({"channel":channel})
    socket.send((json.dumps(data)+"\r\n").encode("utf8"))
    #print("sended",(json.dumps(data)+"\r\n").encode("utf8"))
    
'''
def auto_get_args(defaults):
    def finner(func):
        args = func.__code__.co_varnames[:func.__code__.co_argcount]
        keys = defaults.keys()
        def sinner():
            r = []
            for i in args:
                if i in keys:
                    r.append(defaults[i])
                else:
                    r.append(None) 
            return func(*r)
        return sinner
    return finner
'''
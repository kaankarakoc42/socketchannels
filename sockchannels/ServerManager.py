import socket
import threading
try:
 from .utils import *
except:
    from utils import *
    import os
    os.system("title server")
        
class ServerManager:
      
    def __init__(self):
        self.channels = {}
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.run = True
        
    def channel(self,channel_name):
        def get_func(func):
            self.channels.update({channel_name:func})       
        return get_func


    def handle_client(self,socket):
        try:
            self.gen = responseGenerator(socket)
            while self.run:
                data = next(self.gen)
                self.channels[data["channel"]](socket,data)
        except Exception as e:
            print("connection closed",socket,"\n",e)
            
            


    def mainloop(self):
        self.server.bind(("localhost",1234))
        self.server.listen()
        while self.run:
            socket,_=self.server.accept()
            threading.Thread(target=self.handle_client,args=[socket]).start()

if __name__ == "__main__":
    import time
    app = ServerManager()
    @app.channel("pong")
    def send_back(server,data):
        print("pong",data)
        send(server,"ping")
        time.sleep(0.4)

    @app.channel("ping")
    def send_back(server,data):
        print("ping",data)
        send(server,"pong")
        time.sleep(0.4)
        
    app.mainloop()
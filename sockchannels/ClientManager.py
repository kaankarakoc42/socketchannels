import socket
import threading
try:
 from .utils import *
except:
    from utils import *
    import os
    os.system("title client")
    
class ClientManager:
      def __init__(self) -> None:
          self.channels = {} 
      
      def channel(self,channel_name):
          def get_func(func):
              self.channels.update({channel_name:func})       
          return get_func
      
      def handle_server(self,socket):
           self.gen = responseGenerator(socket)
           while 1:
             data = next(self.gen)
             self.channels[data["channel"]](socket,data)

             
      def createClient(self):
          client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
          client.connect(("localhost",1234))
          threading.Thread(target=self.handle_server,args=[client]).start()
          return client
      
if __name__ == "__main__":
    client = ClientManager()
    @client.channel("ping")
    def test(client,data):
        print("ping",data)
        send(client,"pong",{"a":"selam dostum"})

    @client.channel("pong")
    def send_back(client,data):
        print("pong")
        send(client,"ping",data)

    client1 = client.createClient()
    send(client1,"pong")
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
class OrderConsumer(WebsocketConsumer):
    def connect(self):        
        self.accept()

    def disconnect(self, code):
        pass
    
    def receive(self, text_data):
        print(text_data)
       
    
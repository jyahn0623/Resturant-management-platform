from channels.generic.websocket import WebsocketConsumer
import json

class RMSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print(self.scope['url_route']['kwargs'].keys())

    def disconnect(self, code): # code argu가 없으면 오류
        print("연결 해제")

    def receive(self, text_data): #text_data가 아니면 오류
        data = json.loads(text_data)
        print(data['name'])

        send_data = {
            'name' : '안주영',
            'age' : 25,
        }
        
        self.send(json.dumps(send_data))

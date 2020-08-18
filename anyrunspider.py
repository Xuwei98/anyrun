import json
import logging
import random
import string
import websocket
from typing import Callable

import time

class AnyRunSpider:

    def send_message(self, msg: dict) -> None:
        self._con.send(json.dumps([json.dumps(msg)]))

    def send_message_plus(self, name: str, params: list = None) -> None:
        if not params:
            params = []
        self.send_message({'msg': 'sub', 'id': AnyRunSpider.generate_token(17), 'name': name, 'params': params})

    def send_1(self):
        b = [{'msg': 'connect', 'version': '1', 'support': ['1', 'pre2', 'pre1']}, {'msg': 'method', 'method': 'host', 'params': [], 'id': '1'}, {'msg': 'method', 'method': 'checkDevelopment', 'params': [], 'id': '2'}, {'msg': 'method', 'method': 'getPrefix', 'params': [], 'id': '3'}]
        for i in b:
            # print(type(i))
            self.send_message(i)

    def send_2(self):
        self.send_message_plus('meteor.loginServiceConfiguration')
        self.send_message_plus('meteor_autoupdate_clientVersions')
        self.send_message_plus('activeTasks')
        self.send_message_plus('settings')
        self.send_message_plus('teams')
        self.send_message_plus('files.avatars')
        self.send_message_plus('statisticsDayVeridct')
        self.send_message_plus('statisticsDayCountry')
        self.send_message_plus('statisticsDayTags')
        self.send_message_plus('statisticsDayTime')
        self.send_message_plus('statisticsDayIOC')
        self.send_message_plus('publicTasks',[
            20,0,{
                'isPublic':True,
                'hash':'',
                'runtype':[],
                'verdict':[],
                'ext':[],
                'tag':'',
                'significant':False}])
        self.send_message_plus('changeLog')
        self.send_message_plus('activeTasksCounter')
        self.send_message_plus('interestingTask')
    
    @staticmethod
    def generate_id() -> int:
        return random.randint(100,999)

    @staticmethod
    def generate_token(num) -> str:
        words = string.ascii_lowercase +  "0123456789"
        return ''.join(random.choice(words) for _ in range(num))

    #wss://app.any.run/sockjs/631/vag1wp6e/websocket
    @staticmethod
    def generate_url(num) -> str:
        print("Generate Url! ")
        url = "wss://app.any.run/sockjs/{id}/{token}/websocket".format(id = AnyRunSpider.generate_id(),token = AnyRunSpider.generate_token(num))
        print(url)
        return url

    def run_forever(self):
        self._con.run_forever()

    def _on_open(self):
        self.send_1()
        time.sleep(3)
        self.send_2()



    def on_error(self, error) -> None:
        if not isinstance(KeyboardInterrupt, type(error)):
            print('Connection error occurs')
            
    
    def on_close(self) -> None:
        print("Connection closed")

    def on_message(self, message) -> None:
        if len(message) > 1:
            message = json.loads(message[1:])[0]
            message = json.loads(message)
            if 'msg' in message and message['msg'] == 'ping':
                # print("Send pong!")
                self.send_message({"msg": "pong"})
            elif self._on_message_cb:
                self._on_message_cb(message)

    def __init__(self, on_message_cb: Callable[[dict], None], enable_trace=False):
        self._on_message_cb = on_message_cb
        self._url = self.generate_url(8)
        websocket.enableTrace(enable_trace)
        self._con = None
    def connect(self):
        self._con = websocket.WebSocketApp(
            url = self._url,
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close
        )
        self._con.on_open = self._on_open

    pass


def callback(msg: dict) -> None:
    if(len(str(msg)) > 400 and len(str(msg)) < 10000):
        print("===================")
        print(msg)

if __name__ == "__main__":
    client = AnyRunSpider(
        on_message_cb=callback,
        enable_trace=False
    )
    client.connect()
    client.run_forever()
from phone_verify.backends.base import BaseBackend
from requests.auth import HTTPBasicAuth as Auth
import requests
import re

class SimClient:
    def __init__(self, url, username, password):
        self.url = url
        self.auth = Auth(username, password)

        self.post = requests.post


    def send_message(self, number, message):
        number = re.search('(\d+)', number).group()
        
        data = {
              'to_mobile':[int(number)],
              'message': message,
              'message_type': 0
              }
        try:
                 
           self.res = self.post(self.url, auth=self.auth, json=data)
           return self.res

        except Exception as e:
            print(e)
            raise ValueError(e)

        
class SmsToClient:
    def __init__(self, url, token_key):
        self.url = url
        self.headers = { 'Authorization': 'Bearer {}'.format(token_key)}

        self.post = requests.post


    def send_message(self, number, message):
        number = re.search('(\d+)', number).group()
        
        data = {
              'to': "+" + number,
              'message': message,
              }
        try:
                 
           self.res = self.post(self.url, headers=self.headers, json=data)
           return self.res

        except Exception as e:
            print(e)
            raise ValueError(e)

 
class VoicegateBackend(BaseBackend):
    def __init__(self, **options):
        super(VoicegateBackend, self).__init__(**options)
        options = { key.lower(): value for key, value in options.items()}
        
        self._url = options.get('url', None)
        self._secret = options.get('secret', None)
        self._user = options.get('username',None)

        self.client = SimClient(self._url, self._user, self._secret)
        self.exception_class = ValueError

    def send_sms(self, number, message):
        self.client.send_message(number, message)
        return self.client.res

    def send_bulk_sms(self, numbers, message):
        for number in numbers:
            self.send_sms(number=number, message=message)

class SmsToBackend(BaseBackend):
    def __init__(self, **options):
        super(SmsToBackend, self).__init__(**options)
        options = { key.lower(): value for key, value in options.items()}
        
        self._url = options.get('url', None)
        self._token = options.get('token', None)

        self.client = SmsToClient(self._url, self._token)
        self.exception_class = ValueError

    def send_sms(self, number, message):
        self.client.send_message(number, message)
      
        return self.client.res

    def send_bulk_sms(self, numbers, message):
        for number in numbers:
            self.send_sms(number=number, message=message)

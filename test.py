import json
import os

import requests

'''
res = requests.get("http://127.0.0.1:8000/users/")
users = res.json()
for i in users:
    print(i["user"])
'''

data = {
  'username': 'admin',
  'password': 'root',
}

res = requests.post(url='http://tele2-api.herokuapp.com/login', data=json.dumps(data))
token = res.json()["token"]
data = {"value": token}
res = requests.get(url='http://tele2-api.herokuapp.com/docs#/default/login_login_post', data=json.dumps(data))
print(res)
res = requests.get(url='http://tele2-api.herokuapp.com/protected')
print(res.text)


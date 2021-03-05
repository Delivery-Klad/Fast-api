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
print(token)
data = {"value": token}
headers = {"Authorization": f"Bearer {token}"}
res = requests.get(url='http://tele2-api.herokuapp.com/protected', headers=headers)
print(res.text)


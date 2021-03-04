import os

import requests

'''
res = requests.get("http://127.0.0.1:8000/users/")
users = res.json()
for i in users:
    print(i["user"])


data = {
  "username": "string",
  "name": "string",
  "surname": "string",
  "group": "string",
  "user_id": 0
}
res = requests.post(url='http://127.0.0.1:8000/users/insert', data=data)
print(res.text)
'''

os.environ['API_USER'] = 'admin'
os.environ['API_HASH'] = '$2b$12$fJu8zmcNwADuQScxq1wa0O8moTHC4KIUmCJ48FxeTjZIUXY0ogbma'

print(os.environ.get("API_USER"))

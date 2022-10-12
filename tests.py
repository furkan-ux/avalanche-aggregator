
import json
import requests



url = "http://159.223.29.67:5000/transactions/save"
headers = {"Content-Type": "application/json"}
json_data = {"id":"testtest123","key":"zort","txn":"mort"}
urlreq = requests.post(url,headers=headers,json=json_data)

print(urlreq.text)
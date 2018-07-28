import json
import requests
r = requests.get('http://msftconnect.com')
magic_start=r.text.find('magic')+14
magic=r.text[magic_start:magic_start+16]
print(magic)
# manual URL encoding of JSON
data = "4Tredir=http%3A%2F%2Fmsftconnect.com%2F&magic="+magic+"&username=wifi&password=wifi"
r = requests.post('https://webhook.site/1209e150-34dc-4782-af5d-3b40129ff000', data=data, headers={"content-type":"application/x-www-form-urlencoded"})
print(r.text)

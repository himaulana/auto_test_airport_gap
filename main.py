import requests
# from pprint import pprint

response = requests.get('https://airportgap.com/api/airports')
print(response.json())
# pprint(response.json())
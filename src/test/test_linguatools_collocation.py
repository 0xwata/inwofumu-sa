import requests
import json
apiurl = 'https://lt-collocation-test.herokuapp.com/todos/?query=boy&lang=en&min_sg=0'
response = requests.get(apiurl)
json_data = json.loads(response.text)
print(json_data)

print(len(json_data))
for row in json_data:
    print(row["collocation"])

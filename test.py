import json

json_data = {"domain": "domain", "fetch_mode": "subdomain", "competitors": ['asd', 'asdfasdf'],
             "date_min": "date_min", "date_max": "date_max", "date_interval": "weekly"}

print(json.dumps(json_data))

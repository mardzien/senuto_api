import requests
from user_data import auth

header = {
    "Authorization": f"Bearer {auth.get_token()}"
}

url = "https://api.senuto.com/api/visibility_analysis/reports/exports/domain_keywords/download?id=92e7d92dd9629e2f69348fbc627b90af"
# url2 = "https://api.senuto.com/api/visibility_analysis/reports/exports/domain_keywords/download"  418
# url2 = "https://api.senuto.com/api/visibility_analysis/reports/exports/domain_keywords/downloads"  404
url2 = "https://api.senuto.com/api/visibility_analysis/reports/exports/domain_keywords"     # 401

resp = requests.get(url)
resp2 = requests.get(url2, headers=header, params={'domain': 'medjol.pl'})

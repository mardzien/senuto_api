import requests
import json
from user_data import auth

urls = {
    "auth": "https://api.senuto.com//api/users/token.json",
    "getDomainStatistics": "https://api.senuto.com/api/visibility_analysis/reports/dashboard/getDomainStatistics",
    "getTopCompetitors": "https://api.senuto.com/api/visibility_analysis/reports/domain_competitors/getTopCompetitors",
    "getImportantKeywords":
        "https://api.senuto.com/api/visibility_analysis/reports/domain_keywords/getImportantKeywords",
    "getPositionsHistoryChartData":
        "https://api.senuto.com/api/visibility_analysis/reports/domain_positions/getPositionsHistoryChartData",
    "getKeywordsWithDecreasedPositions":
        "https://api.senuto.com/api/visibility_analysis/reports/domain_keywords/getKeywordsWithDecreasedPositions",
    "getKeywordStatistics":
        "https://api.senuto.com/api/keywords_analysis/reports/keyword_details/getStatistics"
}


header = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Bearer {auth.get_token()}"
}


def get_domain_statistics(domain, fetch_mode="subdomain"):
    domain_statistics = requests.get(urls['getDomainStatistics'], headers=header,
                                     params={'domain': domain, "fetch_mode": fetch_mode})

    domain_data = json.loads(domain_statistics.text)
    statistics = ['top3', 'top10', 'top50', 'visibility', 'visibility_no_brand']
    statistics_dict = {'domain': domain}
    for element in statistics:
        value = domain_data['data']['statistics'][element]['recent_value']
        statistics_dict[element] = value
    return statistics_dict


def get_top_level_domain_statistics(domain):
    domain_statistics = requests.get(urls['getDomainStatistics'], headers=header,
                                     params={'domain': domain, "fetch_mode": "topLevelDomain"})

    domain_data = json.loads(domain_statistics.text)
    statistics = ['top3', 'top10', 'top50', 'visibility', 'visibility_no_brand']
    statistics_dict = {'domain': domain}
    for element in statistics:
        value = domain_data['data']['statistics'][element]['recent_value']
        statistics_dict[element] = value
    return statistics_dict

def get_top_competitors(number_of_competitors, domain):
    competitors = requests.post(urls['getTopCompetitors'], headers=header,
                                data={"fetch_mode": "subdomain", "domain": domain, "limit": number_of_competitors})
    competitors_data = json.loads(competitors.text)
    list_of_competitors = []
    for i in range(number_of_competitors):
        competitor = competitors_data['data'][i]['domain']
        list_of_competitors.append(competitor)
    return list_of_competitors


def get_important_keywords(domain):
    keywords = requests.post(urls['getImportantKeywords'], headers=header,
                             data={"fetch_mode": "subdomain", "domain": domain})
    keywords_data = json.loads(keywords.text)
    count_keywords = len(keywords_data['data'])
    list_of_keywords = []
    for i in range(count_keywords):
        keyword = keywords_data['data'][i]['keyword']
        list_of_keywords.append(keyword)
    return list_of_keywords


def get_keywords_with_decreased_positions(domain, limit=50):
    keywords_with_decreased_positions = requests.get(urls['getKeywordsWithDecreasedPositions'], headers=header,
                                                     params={'domain': domain, "fetch_mode": "subdomain",
                                                             'limit': limit})
    keywords_data = json.loads(keywords_with_decreased_positions.text)
    #################
    ### To nie działa, wypluwa: 'params': {'domain': {'_required': 'This field is required'},
    ###'fetch_mode': {'_required': 'This field is required'}}}}
    #################
    return keywords_data


def get_positions_history_chart_data(domain, date_min, date_max, competitors=[]):
    positions_history = requests.get(urls['getPositionsHistoryChartData'], headers=header,
                                     params={"domain": domain, "fetch_mode": "subdomain", "competitors": competitors,
                                             "date_min": date_min, "date_max": date_max, "date_interval": "weekly"})

    positions_history_data = json.loads(positions_history.text)
    ####################
    ### Tutaj format daty w jsonie jest taki, że nie wiem jak wyciągnąć dane z dokładnej daty.
    ####################
    return positions_history_data


def get_keyword_statistics(keyword):
    keyword_statistics = requests.get(urls['getKeywordStatistics'], headers=header,
                                      params={"country_id": "1", "keyword": keyword})

    keyword_data = json.loads(keyword_statistics.text)
    keyword_dict = {'keyword': keyword}
    try:
        value = keyword_data["data"]["searches"]
        keyword_dict["searches"] = value
    except:
        keyword_dict["searches"] = 0
    return keyword_dict


print(get_top_level_domain_statistics("zdrowie.tvn.pl"))

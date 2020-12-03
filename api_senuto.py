import requests
import json
from user_data import auth

urls = {
    "auth":
        "https://api.senuto.com//api/users/token.json",
    "getDomainStatistics":
        "https://api.senuto.com/api/visibility_analysis/reports/dashboard/getDomainStatistics",
    "getTopCompetitors":
        "https://api.senuto.com/api/visibility_analysis/reports/domain_competitors/getTopCompetitors",
    "getImportantKeywords":
        "https://api.senuto.com/api/visibility_analysis/reports/domain_keywords/getImportantKeywords",
    "getPositionsHistoryChartData":
        "https://api.senuto.com/api/visibility_analysis/reports/domain_positions/getPositionsHistoryChartData",
    "getKeywordsWithDecreasedPositions":
        "https://api.senuto.com/api/visibility_analysis/reports/domain_keywords/getKeywordsWithDecreasedPositions",
    "getKeywordsWithIncreasedPositions":
        "https://api.senuto.com/api/visibility_analysis/reports/domain_keywords/getKeywordsWithIncreasedPositions",
    "getKeywordStatistics":
        "https://api.senuto.com/api/keywords_analysis/reports/keyword_details/getStatistics",
    "getKeywordsPropositions":
        "https://api.senuto.com/api/keywords_analysis/reports/keyword_details/getKeywordsPropositions"
}

exports = {
    "getDomainKeywords":
    "https://api.senuto.com/api/visibility_analysis/reports/exports/domain_keywords/getImportantKeywords",
    "getKeywordsWithDecreasedPositions":
    "https://api.senuto.com/api/visibility_analysis/reports/exports/domain_keywords/getKeywordsWithDecreasedPositions",
    "getKeywordsWithIncreasedPositions":
    "https://api.senuto.com/api/visibility_analysis/reports/exports/domain_keywords/getKeywordsWithIncreasedPositions",
    "rangeCompare":
    "https://api.senuto.com/api/visibility_analysis/tools/exports/range_compare/getData"
}


monitoring = {
    "getCompetitorMatrix":
        "https://api.senuto.com/api/ExcelReports/reportCompetitorsMatrix"

}


header = {
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


def get_top_competitors(domain, number_of_competitors=10):
    competitors = requests.post(urls['getTopCompetitors'], headers=header,
                                data={"fetch_mode": "subdomain", "domain": domain, "limit": number_of_competitors})
    competitors_data = json.loads(competitors.text)

    list_of_competitors = []
    for i in range(number_of_competitors):
        competitor = competitors_data['data'][i]['domain']
        list_of_competitors.append(competitor)
    return list_of_competitors


def get_important_keywords_export(domain, file_path):
    data = requests.post(exports['getDomainKeywords'], headers=header,
                         data={'domain': domain, "fetch_mode": "subdomain"})
    text = json.loads(data.text)
    url = text['data']['downloadUrl']
    download = requests.get(url)
    with open(f'{file_path}/{domain}_keywords.xlsx', 'wb') as fh:
        fh.write(download.content)


def get_incresed_pocitions_keywords_export(domain, file_path):
    data = requests.post(exports['getKeywordsWithIncreasedPositions'], headers=header,
                         data={'domain': domain, "fetch_mode": "subdomain"})
    text = json.loads(data.text)
    url = text['data']['downloadUrl']
    download = requests.get(url)
    with open(f'{file_path}/{domain}_increased_keywords.xlsx', 'wb') as fh:
        fh.write(download.content)


def get_decresed_pocitions_keywords_export(domain, file_path):
    data = requests.post(exports['getKeywordsWithDecreasedPositions'], headers=header,
                         data={'domain': domain, "fetch_mode": "subdomain"})
    text = json.loads(data.text)
    url = text['data']['downloadUrl']
    download = requests.get(url)
    with open(f'{file_path}/{domain}_decreased_keywords.xlsx', 'wb') as fh:
        fh.write(download.content)


def get_range_compare_export(domain, file_path, date_min, date_max):
    ### jest konflikt między obiektem json a zagnieżdżonym słownikiem w pythonie- stąd taka konwersja
    json_data = {'domain': domain,
                 "date_min": date_min,
                 "range_min_pos": {
                    "range": [1, 10],
                    "gte": 1,
                    "lte": 10
                 },
                 "date_max": date_max,
                 "range_max_pos": {
                     "range": [11, 50],
                     "gte": 11,
                     "lte": 50
                 },
                 }

    sorted_data = sorted([date_min, date_max])
    if sorted_data[0] == date_min:
        compare = "decreased"
    else:
        compare = "increased"

    data = requests.post(exports['rangeCompare'], headers=header,
                         data=json.dumps(json_data))
    text = json.loads(data.text)
    url = text['data']['downloadUrl']
    download = requests.get(url)
    with open(f'{file_path}/{domain}_{compare}_keywords.xlsx', 'wb') as fh:
        fh.write(download.content)


# błędna metoda w dokumentacji! jest get, zamiast post
def get_keywords_with_decreased_positions(domain, dates: list, limit=10):
    """
    :param domain:
    :param dates: supposed to be in format: "YYYY-MM-01"
    :param limit:
    :return:
    """
    accumulated_data = []
    page_index = 1
    while True:
        keywords_with_decreased_positions = requests.post(urls['getKeywordsWithDecreasedPositions'], headers=header,
                                                          data={'domain': domain, "fetch_mode": "subdomain",
                                                                'limit': limit, 'page': page_index,
                                                                'order': {'dir': 'asc', 'prop': 'searches'}})
        keywords_data = json.loads(keywords_with_decreased_positions.text)
        # print(keywords_data)
        try:
            accumulated_data.extend(keywords_data['data'])
        except KeyError as exc:
            print(f"""Problem with extracting data for {urls['getKeywordsWithDecreasedPositions']}.
                  Domain: {domain}, page index: {page_index}""")
            raise exc
        # break
        if keywords_data.get('pagination', {}).get('has_next_page'):
            page_index += 1
        elif keywords_data.get('pagination', {}).get('page_count') == page_index:
            break
        else:
            break

    # post processing of server data
    # print(accumulated_data)
    result = []
    for keyword_data in accumulated_data:
        all_monthly_positions = keyword_data.get("monthly_positions", {})
        monthly_positions = {date: all_monthly_positions[date] for date in dates if date in all_monthly_positions}

        processed_dict = {
            "keyword": keyword_data["keyword"],
            "monthly_positions": monthly_positions
        }
        result.append(processed_dict)

    return result


# zmienna = get_keywords_with_decreased_positions("optibuy.com", dates=["2020-01-01", "2020-02-01"])
# print(len(zmienna))


def get_keywords_with_increased_positions(domain, fetch_mode="topLevelDomain",  limit=10):
    keywords_with_increased_positions = requests.post(urls['getKeywordsWithIncreasedPositions'], headers=header,
                                                      data={"domain": domain, "fetch_mode": fetch_mode,
                                                            "limit": 50})
    keywords_data = json.loads(keywords_with_increased_positions.text)

    return keywords_data


def get_positions_history_chart_data(domain, date_min, date_max, fetch_mode="subdomain"):
    raw_data = {"domain": domain,
                "date_interval": "weekly",
                "fetch_mode": fetch_mode,
                "date_min": date_min,
                "date_max": date_max, }
    positions_history = requests.get(urls['getPositionsHistoryChartData'], headers=header, params=raw_data, )
    position_history_data = json.loads(positions_history.text)
    position_history = position_history_data['data'][0]['data']
    return position_history


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


def get_keyword_propositions(keyword, country_id=1):
    keyword_propositions_response = requests.post(urls['getKeywordsPropositions'], headers=header,
                                                  data={"keyword": keyword, "country_id": country_id})

    keyword_propositions_data = json.loads(keyword_propositions_response.text)

    try:
        proposition = keyword_propositions_data['data'][0]['keyword']
        searches = keyword_propositions_data['data'][0]['searches']
    except:
        proposition = 'brak propozycji'
        searches = 0

    return keyword, proposition, searches


def get_keyword_propositions2(keyword, country_id=1):
    keyword_propositions_response = requests.post(urls['getKeywordsPropositions'], headers=header,
                                                  data={"keyword": keyword, "country_id": country_id})
    try:
        keyword_propositions_data = json.loads(keyword_propositions_response.text)
    except:
        keyword_propositions_data = None
    propositions = []
    searches = []
    for i in range(5):
        try:
            propositions.append(keyword_propositions_data['data'][i]['keyword'])
            searches.append(keyword_propositions_data['data'][i]['searches'])
        except:
            propositions.append('brak propozycji')
            searches.append(0)

    return keyword, propositions[0], searches[0], propositions[1], searches[1], propositions[2], searches[2],\
           propositions[3], searches[3], propositions[4], searches[4]


def get_competitors_matrix(project_id, date_min, date_max, file_path):

    json_data = {
        "project_id": project_id,
        "date_min": date_min,
        "date_max": date_max,
    }

    data = requests.post(monitoring['getCompetitorMatrix'], headers=header,
                         data=json.dumps(json_data))
    text = json.loads(data.text)
    print(text)
    url = text['data']['downloadUrl']
    download = requests.get(url)
    with open(f'{file_path}/{date_min}-{date_max}_competitors_matrix.xlsx', 'wb') as fh:
        fh.write(download.content)

import requests
import time
import json
import openpyxl
import api_senuto


def get_important_keywords(domain, limit=100):
    with requests.Session() as session:
        accumulated_data = []
        page_index = 1
        while True:
            start = time.time()
            important_keywords = session.post(api_senuto.urls['getImportantKeywords'], headers=api_senuto.header,
                                              data={'domain': domain, "fetch_mode": "subdomain",
                                                    'limit': limit, 'page': page_index})
            keywords_data = json.loads(important_keywords.text)
            stop = time.time()
            delta = stop - start
            print(f"Dobra wiadomość: pobieranie danych zajęło: {delta}s.")
            # print(keywords_data)
            try:
                accumulated_data.extend(keywords_data['data'])
            except KeyError as exc:
                print(f"""Problem with extracting data for {api_senuto.urls['getImportantKeywords']}.
                      Domain: {domain}, page index: {page_index}""")
                raise exc
            # break
            if keywords_data.get('pagination', {}).get('has_next_page'):
                page_index += 1
                print(f'Page no: {page_index} of {keywords_data["pagination"]["page_count"]}')
            # elif keywords_data.get('pagination', {}).get('page_count') == page_index:
            #     break
            else:
                break
        print("Data loaded")
        # return accumulated_data
        # post processing of server data
        print(accumulated_data)

        result = []
        for data in accumulated_data:
            # if 1 <= data["last_position"] <= 10:
            processed_dict = {
                "keyword": data["keyword"],
                "url": data["url"],
                "searches": data["searches"],
                "last_position": data["last_position"],
                "position_yesterday": data["position_yesterday"],
            }
            result.append(processed_dict)
    return result


get_important_keywords('florimex.info.pl')


session = requests.Session()


def get_important_keywords_data(domain, limit=10000):
    page_index = 1
    first_page = session.post(api_senuto.urls['getImportantKeywords'], headers=api_senuto.header,
                              data={'domain': domain, "fetch_mode": "subdomain", 'limit': limit,
                                    'page': page_index}).json()

    yield first_page
    num_pages = first_page['pagination']['page_count']

    for page_index in range(2, num_pages + 1):
        next_page = session.post(api_senuto.urls['getImportantKeywords'], headers=api_senuto.header,
                                 data={'domain': domain, "fetch_mode": "subdomain", 'limit': limit,
                                 'page': page_index}).json()

        yield next_page

acumulated_data = []
for page in get_important_keywords_data("izielnik.pl"):
    acumulated_data.append(page)

    print(acumulated_data)


def generate_domain_raport(domain):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    columns = "ABCDE"
    column_names = ['keyword', 'url', 'searches', 'last_position', 'position_yesterday']
    ### Tworzenie 1 wiersza w arkuszu
    for i, column in enumerate(columns):
        sheet[f"{column}1"] = column_names[i]

    data = get_important_keywords(domain)
    for i, row in enumerate(data):
        for j, column in enumerate(columns):
            sheet[f"{column}{i + 2}"] = row[column_names[j]]
    workbook.save(f"data/raport/{domain}.xlsx")
    print(f"Raport generated for: {domain}")


def generate_multiple_raports(domains):
    for domain in domains:
        generate_domain_raport(domain)
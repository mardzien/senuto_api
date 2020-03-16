import openpyxl
from api_senuto import get_keyword_statistics

src = """def get_keyword_statistics(keyword):
    keyword_statistics = requests.get(urls['getKeywordStatistics'], headers=header,
                                      params={"country_id": "1", "keyword": keyword})

    keyword_data = json.loads(keyword_statistics.text)
    keyword_dict = {'keyword': keyword}
    try:
        value = keyword_data["data"]["searches"]
        keyword_dict["searches"] = value
    except:
        keyword_dict["searches"] = 0
    return keyword_dict"""

# compiled = compile(src, "tekst", "eval")

def get_domains_from_file(file_name):
    domain_list = []
    with open(file_name, encoding="utf-8") as file:
        for line in file.read().splitlines():
            domain_list.append(line)
    return domain_list


def generate_keywords_statistics(keywords_list):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    columns = "AB"
    column_names = ['keyword', 'searches']
    ### Tworzenie 1 wiersza w arkuszu
    for i, column in enumerate(columns):
        sheet[f"{column}1"] = column_names[i]

    for i, keyword in enumerate(keywords_list):
        statistics_dict = get_keyword_statistics(keyword)
        for j, column in enumerate(columns):
            sheet[f"{column}{i+2}"] = statistics_dict[column_names[j]]

    workbook.save("data/keywords.xlsx")


keyword_list = get_domains_from_file('data/keywords.txt')
print(generate_keywords_statistics(['Auchan najnowsza gazetka', 'Biedronka promocja']))

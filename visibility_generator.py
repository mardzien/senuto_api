import openpyxl
### pip install openpyxl
from api_senuto import get_domain_statistics, get_top_competitors


def get_domains_from_file(file_name):
    """
    :param file_name: plik powinien zawierać nazwy domen- każda domena w nowej linii
    :return: lista domen
    """
    domain_list = []
    with open(file_name, encoding="utf-8") as file:
        for line in file.read().splitlines():
            domain_list.append(line)
    return domain_list


def generate_domain_statistics(domains, name):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    columns = "ABCDE"
    column_names = ['domain', 'top3', 'top10', 'top50', 'visibility']
    ### Tworzenie 1 wiersza w arkuszu
    for i, column in enumerate(columns):
        sheet[f"{column}1"] = column_names[i]

    for i, domain in enumerate(domains):
        try:
            statistics_dict = get_domain_statistics(domain)
        except:
            try:
                statistics_dict = get_domain_statistics(domain, fetch_mode="topLevelDomain")
            except:
                statistics_dict = {'domain': domain, 'top3': 0, 'top10': 0, 'top50': 0, 'visibility': 0}
        for j, column in enumerate(columns):
            sheet[f"{column}{i + 2}"] = statistics_dict[column_names[j]]

    ### Nazwa pliku w folderze data
    workbook.save(f"data/{name}.xlsx")


### załadowanie pliku do listy
# domain_list = get_domains_from_file("data/domains.txt")
domain_list = get_top_competitors("medjol.pl", 11)
### generowanie pliku ze statystykami
print(domain_list)
generate_domain_statistics(domain_list, "medjol_competitors")

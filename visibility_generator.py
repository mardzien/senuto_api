import openpyxl
from api_senuto import get_domain_statistics


def get_domains_from_file(file_name):
    domain_list = []
    with open(file_name, encoding="utf-8") as file:
        for line in file.read().splitlines():
            domain_list.append(line)
    return domain_list


# domain_list = ['medjol.pl', 'wapteka.pl', 'medifem.pl']


def generate_domain_statistics(*domains):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    columns = "ABCDE"
    column_names = ['domain', 'top3', 'top10', 'top50', 'visibility']
    ### Tworzenie 1 wiersza w arkuszu
    for i, column in enumerate(columns):
        sheet[f"{column}1"] = column_names[i]

    for i, domain in enumerate(domains):
        statistics_dict = get_domain_statistics(domain)
        for j, column in enumerate(columns):
            sheet[f"{column}{i+2}"] = statistics_dict[column_names[j]]

    workbook.save("data.xlsx")


domain_list = get_domains_from_file('data/plik.txt')
print(*domain_list)
lista = ['hellozdrowie.pl']
generate_domain_statistics(*lista)

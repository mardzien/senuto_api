import openpyxl
from api_senuto import get_important_keywords


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


domains_list = get_domains_from_file('data/domains.txt')
print(domains_list)
generate_multiple_raports(domains_list)

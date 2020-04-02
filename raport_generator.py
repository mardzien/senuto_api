
import json
import requests
import api_senuto
import numpy as np
import pandas as pd
import glob
import xlrd


def get_domains_from_file(file_name):
    """
    :param file_name: plik powinien zawierać nazwy domen- każda domena w nowej linii
    :return: lista domen
    """
    domains = []
    with open(file_name, encoding="utf-8") as file:
        for line in file.read().splitlines():
            domains.append(line)
    return domains


file_path='data/raport'


def get_multiple_important_keywords_export(domains, file_path):
    for domain in domains:
        api_senuto.get_important_keywords_export(domain, file_path)


# domains = get_domains_from_file('data/domains.txt')
# get_multiple_important_keywords_export(domains, 'data/raport')


def create_full_report(file_path):
    files = glob.glob(f'{file_path}*.xlsx')
    wynikowy = pd.DataFrame()
    wynikowy.to_excel('output.xlsx')
    for file in files:
        name = file[:file.index('.')]
        dataframe = pd.read_excel(file)
        wynikowy = wynikowy.append(dataframe[['Słowo kluczowe', 'Śr. mies. liczba wyszukiwań']])
        with pd.ExcelWriter('output.xlsx', engine='openpyxl', mode='a') as writer:
            dataframe.to_excel(writer, sheet_name=name)

    wynik = wynikowy.drop_duplicates(ignore_index=True)

    with pd.ExcelWriter('output.xlsx', engine='openpyxl', mode='a') as writer:
        wynik.to_excel(writer, sheet_name='zbiorczy')






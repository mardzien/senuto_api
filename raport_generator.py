import pandas as pd
import glob
import time
import xlrd
import api_senuto

file_path = 'data/raport'


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

"""funkcja zaimportowana z pliku api_senuto pobiera export z aplikacji senuto i zapisuje go do pliku excel
funkcja poniżej obsługuje listę domen i zwraca wiele plików do podanej ścieżki"""


def get_multiple_important_keywords_export(domains, file_path):
    for domain in domains:
        api_senuto.get_important_keywords_export(domain, file_path)


"""
Do tej funkcji potrzeba zainstalować moduły:
numpy, pandas, xlrd?, 
"""


def create_full_report(file_path):
    full_time_start = time.time()
    files = glob.glob(f'{file_path}/*.xlsx')
    wynikowy = pd.DataFrame()
    wynikowy.to_excel(f'{file_path}/output.xlsx')
    for file in files:
        start = time.time()
        name = file[file.index('\\')+1:file.index('.')]
        dataframe = pd.read_excel(file)
        wynikowy = wynikowy.append(dataframe[['Słowo kluczowe', 'Śr. mies. liczba wyszukiwań']])
        with pd.ExcelWriter(f'{file_path}/output.xlsx', engine='openpyxl', mode='a') as writer:
            dataframe.to_excel(writer, sheet_name=name)
        stop = time.time()
        delta = stop - start
        print(f"Do raportu dodano plik: {name} w czasie: {delta}")

    wynik = wynikowy.drop_duplicates(ignore_index=True)

    ### dodanie arkusza zbiorczego do pliku output.xlsx
    with pd.ExcelWriter(f'{file_path}/output.xlsx', engine='openpyxl', mode='a') as writer:
        wynik.to_excel(writer, sheet_name='zbiorczy')
    full_time_stop = time.time()
    full_delta = full_time_stop - full_time_start
    print(f"Wygenerowana cały raport w czasie: {full_delta}")


create_full_report(file_path)

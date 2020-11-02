import datetime
import json
import api_senuto
import pandas as pd


def get_date():
    """
    :return: funkcja zwraca tuplę z 4 elementami typu string:
    1- aktualna data
    2- data z pierwszym dniem aktualnego miesiąca
    3- data z pierwszym dniam poprzedniego miesiąca
    4- data z pierwszym dniam, obeznym miesiącem i poprzednim rokiem
    """
    today = datetime.date.today()
    this_month_date = datetime.date(today.year, today.month, 1)
    if today.month == 1:
        last_month_date = datetime.date(today.year - 1, 12, 1)
    else:
        last_month_date = datetime.date(today.year, today.month - 1, 1)
    last_year_date = datetime.date(today.year - 1, today.month, 1)

    today = f"{today}"
    this_month_date = f"{this_month_date}"
    last_month_date = f"{last_month_date}"
    last_year_date = f"{last_year_date}"

    return today, this_month_date, last_month_date, last_year_date


def load_to_list(filename):
    result = []
    with open(filename, encoding='utf-8') as fh:
        for line in fh:
            clean_line = line.replace("\n", "")
            result.append(f'{clean_line}')
    return result


def load_to_string(filename):
    result = ''
    with open(filename, encoding='utf-8') as fh:
        for line in fh:
            clean_line = line.replace("\n", "")
            result += f'{clean_line}, '
    result = result[:-2]
    return result


def write_list_to_file(input_list, filename):
    with open(filename, 'w', encoding='utf-8') as fh:
        for phrase in input_list:
            fh.write(f"{phrase}\n")


# Załadowanie listy domen
domain_list = load_to_list('Input/domains.txt')


def get_visibility_history(domains, date_min, date_max):
    result_df = pd.DataFrame()
    for domain in domains:
        temp_df = pd.read_json(json.dumps(api_senuto.get_positions_history_chart_data(domain, date_min, date_max)))
        temp_df['domena'] = f"{domain}"
        temp_df.reset_index(inplace=True)
        temp_df.rename(columns={'index': 'data'}, inplace=True)
        temp_df.set_index('domena', inplace=True)
        result_df = result_df.append(temp_df)

    writer = pd.ExcelWriter('history_chart.xlsx', engine='xlsxwriter')
    result_df.to_excel(writer, sheet_name='Historia widoczności')
    writer.save()


get_visibility_history(domains=domain_list, date_min=get_date()[2], date_max=get_date()[0])

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
    citys = []
    with open(filename, encoding='utf-8') as fh:
        for line in fh:
            clean_line = line.replace("\n", "")
            citys.append(f'{clean_line}')
    return citys


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

print(get_date())


# Liczba słów kluczowych w TOP3 TOP10 TOP50


# Wyciągnięcie 3 najważniejszych konkurendów z Senuto
competitors = load_to_list('data/domains.txt')


json_data = {"domain": "domain", "fetch_mode": "subdomain", "competitors": competitors,
             "date_min": "date_min", "date_max": "date_max", "date_interval": "weekly"}


print(api_senuto.get_positions_history_chart_data("wyborcza.pl", get_date()[2], get_date()[0]))
print(competitors)

result_df = pd.DataFrame()
for competitor in competitors:
    temp_df = pd.read_json(json.dumps(api_senuto.get_positions_history_chart_data(competitor, get_date()[2], get_date()[0])))
    result_df = result_df.append(temp_df)

writer = pd.ExcelWriter('history_chart.xlsx', engine='xlsxwriter')
result_df.to_excel(writer, sheet_name='Podstawowe informacje')
writer.save()

# df_1 = pd.read_json(json.dumps(api_senuto.get_positions_history_chart_data("wyborcza.pl", get_date()[1], get_date()[0])))
# writer = pd.ExcelWriter('history_chart.xlsx', engine='xlsxwriter')
# df_1.to_excel(writer, sheet_name='Podstawowe informacje')
# writer.save()


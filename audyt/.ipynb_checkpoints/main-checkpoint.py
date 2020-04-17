"""
Input: domena.pl

Output:

1. Liczba słów kluczowych w TOP3 TOP10 TOP50
2. Najważniejsi konkurenci, na podstawie wspólnych słów kluczowych to:
3. Słowa kluczowe, które dają najwięcej ruchu:
4. W stosunku do poprzedniego roku: (jak się zmieniła liczba słów w TOP3, TOP10, TOP50):
5. Słowa kluczowe, na których warto się skupić to: (słowa z pozycji 11-15):
6. Słowa kluczowe, które weszły do TOP10 w ostatnim miesiącu to:
7. Słowa kluczowe, które wypadły z TOP10 to:
"""
import api_senuto
import datetime
import requests
import pandas as pd
import openpyxl


domain = "medjol.pl"


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


print(get_date()[1])


# Liczba słów kluczowych w TOP3 TOP10 TOP50


# Wyciągnięcie 3 najważniejszych konkurendów z Senuto
api_senuto.get_top_competitors(domain, 4)

# api_senuto.get_incresed_pocitions_keywords_export(domain, "data")
# api_senuto.get_decresed_pocitions_keywords_export(domain, "data")
# api_senuto.get_important_keywords_export(domain, "data")

# tak się tworzy listę fraz które wypadły z TOP 10 od 1 dnia ostatniego miesiąca do dzisiaj
# żeby stworzyć listę fraz, które wpadły do top 10 wystarczy zamienić daty miejscami.
# api_senuto.get_range_compare_export(domain, "data", get_date()[2], get_date()[0])
# print(get_date()[3], get_date()[0])
# print(api_senuto.get_positions_history_chart_data("medjol.pl", get_date()[3], get_date()[0]))


def generate_audit(domain):
    df_1 = pd.DataFrame(api_senuto.get_domain_statistics(domain))
    writer = pd.ExcelWriter('audit.xlsx', engine='xlsxwriter')
    df_1.to_excel(writer, sheet_name='Podstawowe informacje')
    writer.save()


generate_audit('medjol.pl')
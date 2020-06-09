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
import xlsxwriter


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


print(sorted(get_date()))


# Liczba słów kluczowych w TOP3 TOP10 TOP50


# Wyciągnięcie 3 najważniejszych konkurendów z Senuto
api_senuto.get_top_competitors(domain, 4)

# api_senuto.get_incresed_pocitions_keywords_export(domain, "data")
# api_senuto.get_decresed_pocitions_keywords_export(domain, "data")
# api_senuto.get_important_keywords_export(domain, "data")

# tak się tworzy listę fraz które wypadły z TOP 10 od 1 dnia ostatniego miesiąca do dzisiaj
# żeby stworzyć listę fraz, które wpadły do top 10 wystarczy zamienić daty miejscami.
# api_senuto.get_range_compare_export(domain, "data", get_date()[2], get_date()[0])
# api_senuto.get_range_compare_export(domain, "data", get_date()[0], get_date()[2])
# print(get_date()[3], get_date()[0])
# print(api_senuto.get_positions_history_chart_data("medjol.pl", get_date()[3], get_date()[0]))


def generate_audit(domain):
    ### podstawowe dane domeny
    
    df_1 = pd.DataFrame(api_senuto.get_domain_statistics(domain), index=[0])
    df_1.set_index(['domain'], inplace=True)
    writer = pd.ExcelWriter('audit.xlsx', engine='xlsxwriter')
    df_1.to_excel(writer, sheet_name='Podstawowe informacje')
    df_2 = pd.DataFrame(api_senuto.get_top_competitors(domain, 4))
    df_2.to_excel(writer, sheet_name='Konkurencja')
    df_keywords = pd.read_excel(f'data/{domain}_keywords.xlsx')
    df_3 = df_keywords.head(50)
    df_3.set_index(['Słowo kluczowe'], inplace=True)
    df_3.to_excel(writer, sheet_name='Frazy dające najwięcej ruchu')
    df_4 = df_keywords[(df_keywords['Pozycja dziś'] > 10) & (df_keywords['Pozycja dziś'] < 16)]
    df_4.set_index(['Słowo kluczowe'], inplace=True)
    df_4.to_excel(writer, sheet_name='Frazy na pozycji 11-15')
    df_5 = pd.read_excel(f'data/{domain}_decreased_keywords.xlsx')
    df_5.set_index(['Słowo kluczowe'], inplace=True)
    df_5.to_excel(writer, sheet_name='Wypadły z TOP10')
    df_6 = pd.read_excel(f'data/{domain}_increased_keywords.xlsx')
    df_6.set_index(['Słowo kluczowe'], inplace=True)
    df_6.to_excel(writer, sheet_name='Wpadły do TOP10')

    writer.save()


generate_audit('winkhaus.pl')

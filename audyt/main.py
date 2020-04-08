"""
Input: domena.pl

Output:

Liczba słów kluczowych w TOP3 TOP10 TOP50

Najważniejsi konkurenci, na podstawie wspólnych słów kluczowych to:

Słowa kluczowe, które dają najwięcej ruchu:

W stosunku do poprzedniego roku: (jak się zmieniła liczba słów w TOP3, TOP10, TOP50): Słowa kluczowe, na których warto się skupić to: (słowa z pozycji 11-15):

Słowa kluczowe, które weszły do TOP10 w ostatnim miesiącu to:

Słowa kluczowe, które wypadły z TOP10 to:
"""
import api_senuto
import datetime


domain = "medjol.pl"


def get_date():
    """
    :return: funkcja zwraca tuplę z 4 elementami:
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

api_senuto.get_domain_statistics(domain)
api_senuto.get_top_competitors(domain, 4)


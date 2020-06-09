import api_senuto
import files
import json


products = files.load_file_to_list("input/produsts.txt")


def create_propositions(products):
    output = {'produkt': {}, 'fraza': {}, 'wyszukania': {}, }
    counter = 1
    for i, product in enumerate(products):
        output['produkt'][f'{i}'], output['fraza'][f'{i}'], output['wyszukania'][f'{i}'] = api_senuto.get_keyword_propositions(product)
        # zabezpieczenie: pliki będą zapisywane co 10k fraz
        if i != 0 and i % 10000 == 0:
            with open(f'output/data{counter}.txt', 'w') as fh:
                json.dump(output, fh)
            counter += 1
            # zliczenie i reset słownika wynikowego
            output = {'produkt': {}, 'fraza': {}, 'wyszukania': {}, }
    # zapisanie pozostałych fraz do pliku
    with open(f'output/data{counter}.txt', 'w') as fh:
        json.dump(output, fh)


create_propositions(products)

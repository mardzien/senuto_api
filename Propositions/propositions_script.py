import api_senuto
import files
import json


products = files.load_file_to_list("Input/produsts.txt")


def create_propositions(products):
    output = {'produkt': {}, 'fraza': {}, 'wyszukania': {}, }
    counter = 1
    for i, product in enumerate(products):
        output['produkt'][f'{i+1}'], output['fraza'][f'{i+1}'], output['wyszukania'][f'{i+1}'] = api_senuto.get_keyword_propositions(product)
        # zabezpieczenie: pliki będą zapisywane co 10k fraz
        print(product, i)
        if i != 0 and i % 10000 == 0:
            with open(f'output/data{counter}.json', 'w', encoding='utf8') as fh:
                json.dump(output, fh, ensure_ascii=False)
            counter += 1
            # zliczenie i reset słownika wynikowego
            output = {'produkt': {}, 'fraza': {}, 'wyszukania': {}, }
    # zapisanie pozostałych fraz do pliku
    with open(f'output/data{counter}.json', 'w', encoding='utf8') as fh:
        json.dump(output, fh, ensure_ascii=False)


def create_propositions2(products):
    output = {'produkt': {}, 'fraza1': {}, 'wyszukania1': {}, 'fraza2': {}, 'wyszukania2': {}, 'fraza3': {},
              'wyszukania3': {}, 'fraza4': {}, 'wyszukania4': {}, 'fraza5': {}, 'wyszukania5': {}}
    counter = 1
    for i, product in enumerate(products):
        output['produkt'][f'{i+1}'], output['fraza1'][f'{i+1}'], output['wyszukania1'][f'{i+1}'], \
            output['fraza2'][f'{i+1}'], output['wyszukania2'][f'{i+1}'], output['fraza3'][f'{i+1}'], \
            output['wyszukania3'][f'{i+1}'], output['fraza4'][f'{i+1}'], output['wyszukania4'][f'{i+1}'], \
            output['fraza5'][f'{i+1}'], output['wyszukania5'][f'{i+1}'] = api_senuto.get_keyword_propositions2(product)
        # zabezpieczenie: pliki będą zapisywane co 10k fraz
        print(product, i)
        if i != 0 and i % 10000 == 0:
            with open(f'output/data{counter}.json', 'w', encoding='utf8') as fh:
                json.dump(output, fh, ensure_ascii=False)
            counter += 1
            # zliczenie i reset słownika wynikowego
            output = {'produkt': {}, 'fraza1': {}, 'wyszukania1': {}, 'fraza2': {}, 'wyszukania2': {}, 'fraza3': {},
                      'wyszukania3': {}, 'fraza4': {}, 'wyszukania4': {}, 'fraza5': {}, 'wyszukania5': {}}
    # zapisanie pozostałych fraz do pliku
    with open(f'output/data{counter}.json', 'w', encoding='utf8') as fh:
        json.dump(output, fh, ensure_ascii=False)


create_propositions2(products)

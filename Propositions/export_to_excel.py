import pandas as pd
import glob


df = pd.DataFrame()
files = glob.glob('Output/*.json')
for file in files:
    with open(file, encoding='utf8') as json_file:
        text = json_file.read()
        print(text)
        df = df.append(pd.read_json(text))

df.to_excel('Output/product_propositions.xlsx')

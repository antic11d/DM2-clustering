import pandas as pd

explore_path = '../data/non_dropna/'

sample_folders = ['GSM2560245', 'GSM2560246', 'GSM2560247', 'GSM2560248',
                  'GSM2560249', 'GSM3087619', 'GSM3087622', 'GSM3087624',
                  'GSM3087626', 'GSM3169075',  # 'GSM3374613', 'GSM3374614',
                  'GSM3478791', 'GSM3478792', 'GSM3892570', 'GSM3892571',
                  'GSM3892572', 'GSM3892573', 'GSM3892574', 'GSM3892575',
                  'GSM3892576']

filenames = [explore_path + 'prep_' + x + '.csv' for x in sample_folders]

null_cols = []

for fname in filenames:
    df = pd.read_csv(fname)
    print(f'\n{fname}:')
    print(f'\tShape: {df.shape}')
    for col in df.columns:
        uniques = df[col].unique()
        if len(uniques) == 1:
            if uniques[0] == 0:
                print(f'\tnull column: {col}')
                null_cols.append(col)
        if len(uniques) == 2:
            print(f'\t two uniques: {col} -> {uniques}')

print(f'{null_cols}')

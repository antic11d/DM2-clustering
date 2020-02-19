import pandas as pd

groups = [['GSM3478791.csv'],
          ['GSM3087619.csv', 'GSM3478792.csv', 'GSM3892570.csv',
           'GSM3892571.csv', 'GSM3169075.csv'],

          ['GSM3087622.csv', 'GSM3087624.csv', 'GSM3087626.csv'],

          ['GSM3892572.csv', 'GSM3892573.csv', 'GSM3892574.csv',
           'GSM3892575.csv', 'GSM3892576.csv'],

          ['GSM2560245.csv', 'GSM2560246.csv', 'GSM2560247.csv',
           'GSM2560248.csv', 'GSM2560249.csv']]

ensg_save_map = {
    '../data/1000-1/': '../data/1000-1-ensg/',
    '../data/1-1000/': '../data/1-1000-ensg/',
}

explore_folders = ['../data/1000-1/', '../data/1-1000/']

common_human_list = pd.read_csv('../../Projekat_1/common_human_list.csv')
ENSG_ID = list(common_human_list['ENSG_ID'])


def drop_incorrect_ensg(group, explore, i):
    print(f'Group {i + 1}:')
    for file in group:
        print(f'\tFile: {file}')
        try:
            df = pd.read_csv(explore + file)

            if 'Unnamed: 0' in df.columns:
                df.drop(['Unnamed: 0'], axis=1, inplace=True)
            df[df['Index'].isin(ENSG_ID)].to_csv(ensg_save_map[explore]+file, index=False)

        except:
            print(f'Exception while parsing {file}')


def main():
    for explore in explore_folders:
        print(f'{explore}\n')
        for i, group in enumerate(groups):
            drop_incorrect_ensg(group, explore, i)


if __name__ == '__main__':
    main()
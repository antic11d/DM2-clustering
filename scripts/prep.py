import pandas as pd
import os

prefix = '../../Projekat_1/'

sample_folders = ['GSM2560245', 'GSM2560246', 'GSM2560247', 'GSM2560248',
                  'GSM2560249', 'GSM3087619', 'GSM3087622', 'GSM3087624',
                  'GSM3087626', 'GSM3169075',  # 'GSM3374613', 'GSM3374614',
                  'GSM3478791', 'GSM3478792', 'GSM3892570', 'GSM3892571',
                  'GSM3892572', 'GSM3892573', 'GSM3892574', 'GSM3892575',
                  'GSM3892576']


def get_filename(folder):
    path = os.path.join(prefix, folder)
    csv = [file for file in os.listdir(path) if file.endswith('.csv')]
    filename = csv[0]
    return filename


def get_csv_files(folder):
    csv = [file for file in os.listdir(folder) if file.endswith('.csv')]
    return csv


sample_paths = [os.path.join(prefix+x, get_filename(x)) for x in sample_folders]


def drop_rows(df, threshold=1.0):
    percentage = threshold / 100.0

    df.drop(df[(df.iloc[:, 1:] > 0).sum(axis=1) / (len(df.columns)-1) < percentage].index, inplace=True)


def preprocess(fpath, save_path):
    df = pd.read_csv('../data/drop-1-percent/'+fpath)

    print(f'\t\t Original shape: {df.shape}')

    # drop rows containing fewer than threshold percents of columns > 0
    drop_rows(df)

    # columns = df['Index']
    # df = df.T

    print(f'\t\t After parsing shape: {df.shape}')

    df.to_csv(save_path)
    print(f'\t\t Data saved on path: {save_path}')


def main():
    n_samples = len(sample_paths)
    for i in range(n_samples):
        print(f'{i + 1}/{n_samples} -> {(i + 1) / n_samples:.2f}\t\t Parsing {sample_folders[i]}.')
        preprocess(sample_paths[i], '../data/drop-1-percent/'+sample_folders[i]+'.csv')
    # preprocess(sample_paths[0], '../data/drop-1-p-t/'+sample_paths[0])


if __name__ == '__main__':
    main()

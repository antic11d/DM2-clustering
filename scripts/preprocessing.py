import pandas as pd
import os

root = '../../Projekat_1/'
sample_folders = ['GSM2560245', 'GSM2560246', 'GSM2560247', 'GSM2560248',
                  'GSM2560249', 'GSM3087619', 'GSM3087622', 'GSM3087624',
                  'GSM3087626', 'GSM3169075',  # 'GSM3374613', 'GSM3374614',
                  'GSM3478791', 'GSM3478792', 'GSM3892570', 'GSM3892571',
                  'GSM3892572', 'GSM3892573', 'GSM3892574', 'GSM3892575',
                  'GSM3892576']

# GSM3374614, GSM3374613 nemaju Index, izgleda da su vec obradjene?

uzorci_data = pd.read_csv(os.path.join(root, 'uzorci.seminarski.csv'))

common_hlist_data = pd.read_csv(os.path.join(root, 'common_human_list.csv'))


def get_sample_genome(sample_id):
    sample_filter = uzorci_data['SAMPLE'] == sample_id
    uzorci_seminarski_data_sample = uzorci_data[sample_filter]
    genome = uzorci_seminarski_data_sample['GENOME'].values[0]
    return genome


def get_filename(folder):
    path = os.path.join(root, folder)
    CSV_Files = [file for file in os.listdir(path) if file.endswith('.csv')]
    filename = CSV_Files[0]
    return filename


def read_data(sample, sample_genomes, dropna=True):
    filename = get_filename(sample)
    path = os.path.join(root, sample)
    sample_data = pd.read_csv(os.path.join(path, filename))
    common_hlist_ENSG = common_hlist_data.loc[:, ['ENSG_ID', sample_genomes[sample]]]

    sample_data_filtered_ENSG = sample_data.set_index('Index').join(common_hlist_ENSG.set_index('ENSG_ID'), how='left')

    if dropna:
        sample_data = sample_data_filtered_ENSG.dropna()
    else:
        sample_data = sample_data_filtered_ENSG

    num_cols = sample_data.shape[1]

    new_columns = [str(sample)[3:] + '_' + str(i) for i in range(1, num_cols)] + ['gene']
    sample_data.columns = new_columns
    sample_data.to_csv(f'../data/non_dropna/prep_{sample}.csv')


def main():
    sample_genomes = {}

    n_samples = len(sample_folders)

    for i in range(n_samples):
        sample_genomes[sample_folders[i]] = get_sample_genome(sample_folders[i])

    print('Up and running!')
    for i in range(n_samples):
        read_data(sample_folders[i], sample_genomes, dropna=False)
        print(f'{i+1}/{n_samples} -> {(i+1)/n_samples:.2f}...\t Done with parsing {sample_folders[i]}.')

    print('All done!')


if __name__ == '__main__':
    main()

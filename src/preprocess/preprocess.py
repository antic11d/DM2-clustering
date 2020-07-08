import pandas as pd
import os
import re
import csv
import argparse

# Relative path to folder containing samples
prefix = '../../Projekat_1/'

groups = [
    ['GSM3087619', 'GSM3478792', 'GSM3892570', 'GSM3892571', 'GSM3169075'],
    ['GSM3087622', 'GSM3087624', 'GSM3087626'],
    ['GSM3892572', 'GSM3892573', 'GSM3892574', 'GSM3892575', 'GSM3892576'],
    ['GSM2560245', 'GSM2560246', 'GSM2560247', 'GSM2560248', 'GSM2560249']
]


def join(p1, p2):
    return os.path.join(p1, p2)


def get_filename(data_path, folder):
    path = join(data_path, folder)
    csv = [file for file in os.listdir(path) if file.endswith('.csv')]
    filename = csv[0]
    return filename



def transpose(data, sample):
    data_t = data.set_index('Index').transpose()
    data_t.index = new_index(data_t.shape, sample)
    return data_t


def new_index(shape, sample):
    index = [str(sample) + '_' + str(i + 1) for i in range(shape[0])]
    return index


# Dropping ensg_ids which are not ni common_human_list
def drop_invalid_ensg(df, ensg_ids):
    return df[df['Index'].isin(ensg_ids)]


# Dropping genes after transposing
# threshold is in percents
def drop_genes(df, threshold):
    print(f'\tDropping genes...')
    percentage = threshold / 100.0

    dropping = df.columns[(df > 0).sum() / len(df.columns) < percentage]
    df.drop(columns=dropping, inplace=True)


# Dropping cells in raw data
# threshold_1 = min number of positive values
# threshold_2 = min sum
def drop_cells(df, threshold_1, threshold_2):
    columns = df.columns[1:]
    dropping = columns[((df.iloc[:, 1:] > 0).sum() < threshold_1) | (df.iloc[:, 1:].sum() < threshold_2)]
    df.drop(columns=dropping, inplace=True)


def prepare(data_path, sample, threshold_1, threshold_2, ensg_ids):
    print(f'\tParsing {sample}')
    data = pd.read_csv(join(data_path, sample) + '/' + get_filename(data_path, sample))

    data = drop_invalid_ensg(data, ensg_ids)

    drop_cells(data, threshold_1, threshold_2)

    data = transpose(data, sample)

    return data


def prepare_genome_sample(path):
    genome_sample = pd.read_csv(join(path, 'SCT-10x-Metadata_readylist_merged-PBMC-tasks-short-Bgd.csv'))
    genome_values = genome_sample['GENOME']
    sample_keys = genome_sample['SAMPLE']

    return dict(zip(sample_keys, genome_values))


def prepare_genome_to_human_map(data_path):
    common_human_list = pd.read_csv(join(data_path, 'common_human_list.csv'))
    ENSG_IDs = list(common_human_list['ENSG_ID'])

    keys = common_human_list['ENSG_ID']
    mapping_columns = ['hg19', 'hg38', 'Ensembl_GRCh38.p12_rel94']
    maps = []
    for column in mapping_columns:
        maps.append(dict(zip(keys, common_human_list[column])))

    return maps, ENSG_IDs


# ensg0000123456_#LYL1 ide u
# E123456#LYL1
def extract(ensg):
    search_part = ensg[4:]
    hit = re.search('0+', search_part)
    result = 'E' + search_part[hit.end():]
    return result


def map_genome_to_human(columns, maps, genome_to_human_csv_mapping, genome_value):
    return [extract(column) + maps[genome_to_human_csv_mapping[genome_value]][column] for column in columns]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', help='Absolute path for the original data file')
    parser.add_argument('--save_path', help='Absolute save path for the preprocessed file')
    parser.add_argument('--cell_thresh1', help='Threshold for cells - minimum of positive values', type=float)
    parser.add_argument('--cell_thresh2', help='Threshold for cells - minimum sum', type=float)
    parser.add_argument('--gene_drop', help='Threshold for genes', type=float)
    args = parser.parse_args()

    sample_to_genome_mapping = prepare_genome_sample(args.data_path)

    maps, ensg_ids = prepare_genome_to_human_map()
    genome_to_human_csv_mapping = {
        'hg19': 2,
        'hg38': 2,
        'GRCh38': 2,
        'GRCh38 version 90': 2
    }

    for i, group in enumerate(groups):

        group_id = f'group_{i + 1}'
        print(group_id)
        dfs = [prepare(args.data_path, sample, args.cell_thresh1, args.cell_thresh2, ensg_ids) for sample in group]

        resulting = pd.concat(dfs, sort=False)
        drop_genes(resulting, args.gene_drop)

        genome_value = sample_to_genome_mapping[group[0]]

        resulting.columns = map_genome_to_human(resulting.columns, maps, genome_to_human_csv_mapping, genome_value)
        print(f'\tShape after parsing: {resulting.shape}')

        os.mkdir(join(args.save_path, group_id))

        print(f'\tSaving columns: {args.save_path}/{group_id}/columns_{i+1}.csv')

        out = csv.writer(open(f'{args.save_path}/{group_id}/columns_{i+1}.csv', "w"), delimiter=',', quoting=csv.QUOTE_ALL)
        out.writerow(resulting.columns)

        print(f'\tSaving data on the path {args.save_path}/{group_id}/data.csv')
        resulting.to_csv(join(args.save_path, group_id) + '/data.csv')


if __name__ == '__main__':
    main()

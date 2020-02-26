import pandas as pd
import os

# Relative path to folder containing samples
prefix = '../../Projekat_1/'

groups = [['GSM3087619'],
          ['GSM3087619', 'GSM3478792', 'GSM3892570', 'GSM3892571', 'GSM3169075'],
          ['GSM3087622', 'GSM3087624', 'GSM3087626'],
          ['GSM3892572', 'GSM3892573', 'GSM3892574', 'GSM3892575', 'GSM3892576'],
          ['GSM2560245', 'GSM2560246', 'GSM2560247', 'GSM2560248', 'GSM2560249']]


def join(p1, p2):
    return os.path.join(p1, p2)


def get_filename(folder):
    path = join(prefix, folder)
    csv = [file for file in os.listdir(path) if file.endswith('.csv')]
    filename = csv[0]
    return filename


common_human_list = pd.read_csv(join(prefix, 'common_human_list.csv'))
genome_sample = pd.read_csv(join(prefix, 'SCT-10x-Metadata_readylist_merged-PBMC-tasks-short-Bgd.csv'))

ENSG_IDs = list(common_human_list['ENSG_ID'])


def transpose(data, sample):
    data_t = data.set_index('Index').transpose()
    data_t.index = new_index(data_t.shape, sample)
    return data_t


def new_index(shape, sample):
    index = [str(sample) + '_' + str(i + 1) for i in range(shape[0])]
    return index


# Dropping ENSG_IDs which are not ni common_human_list
def drop_invalid_ensg(df):
    return df[df['Index'].isin(ENSG_IDs)]


# Dropping genes in raw data
# currently unused
def drop_rows(df, threshold):
    percentage = threshold / 100.0
    df.drop(df[(df.iloc[:, 1:] > 0).sum(axis=1) / (len(df.columns) - 1) < percentage].index, inplace=True)


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


def prepare(sample):
    print(f'\tParsing {sample}')
    data = pd.read_csv(join(prefix, sample) + '/' + get_filename(sample))

    data = drop_invalid_ensg(data)

    # drop cells
    drop_cells(data, 500, 1000)

    # transpose
    data = transpose(data, sample)

    return data


def prepare_genom_sample(genome_sample):
    genome_values = genome_sample['GENOME']
    sample_keys = genome_sample['SAMPLE']

    return dict(zip(sample_keys, genome_values))


def test_mapping(sample_to_genome_mapping):
    for i, group in enumerate(groups):
        print('Group: {}'.format(i))
        found_genomes = set([])
        for gsm in group:
            genome_value = sample_to_genome_mapping[gsm]
            print(genome_value)
            found_genomes.add(genome_value)
            if len(found_genomes) > 2:
                print('Unable to join group{}'.format(i))
                break

    print('Able to map')


def map_columns(columns, genome_value):
    return [column + '_' + genome_value + '_CCT3' for column in columns]


def prepare_genome_to_human_map():
    keys = common_human_list['ENSG_ID']
    mapping_columns = ['hg19', 'hg38', 'Ensembl_GRCh38.p12_rel94']
    maps = []
    for column in mapping_columns:
        maps.append(dict(zip(keys, common_human_list[column])))

    return maps


def map_genome_to_human(columns, maps, genome_to_human_csv_mapping, genome_value):
    return [column + '_' + maps[genome_to_human_csv_mapping[genome_value]][column] for column in columns]


def main():
    sample_to_genome_mapping = prepare_genom_sample(genome_sample)
    test_mapping(sample_to_genome_mapping)

    maps = prepare_genome_to_human_map()
    genome_to_human_csv_mapping = {'hg19': 0, 'GRCh38': 2,
                                   'GRCh38 version 90': 2}

    for i, group in enumerate(groups):

        group_id = f'group_{i + 1}'
        print(group_id)
        dfs = [prepare(sample) for sample in group]

        # at this point we have list with dropped invalid genes, and cells
        # then, we should concat all dataframes in dfs list
        # after concat, genes should be dropped
        # lastly, that big df should be saved on disk, in folder named after group, group_1, group_2 etc.

        resulting = pd.concat(dfs, sort=False)
        drop_genes(resulting, 1.0)

        genome_value = sample_to_genome_mapping[group[0]]
        print(resulting.columns)
        resulting.columns = map_genome_to_human(resulting.columns, maps, genome_to_human_csv_mapping, genome_value)
        print(resulting.columns)
        os.mkdir(join('../data', group_id))
        print(f'\tShape after parsing: {resulting.shape}')
        print(f'\tSaving on path ../data/{group_id}/data.csv')
        resulting.to_csv(join('../data', group_id) + '/data.csv')

        # TODO remove break when preprocessing all groups
        break


if __name__ == '__main__':
    main()

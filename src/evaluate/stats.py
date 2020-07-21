import pandas as pd
import argparse
import os


def calculate_stats(df, save_path):
    labels = df['label'].unique()
    label_counts = df['label'].value_counts()
    sample_counts = df['sample'].value_counts()

    sample_counts.to_csv(os.path.join(save_path, 'sample_counts.csv'))
    label_counts.to_csv(os.path.join(save_path, 'label_counts.csv'))

    for label in labels:
        tmp = df.loc[df['label'] == label]['sample'].value_counts()
        tmp.to_csv(os.path.join(save_path, f'cluster_{label}.csv'))

# Should be refactored
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples_path', help='Absolute path for samples files')
    parser.add_argument('--algorithm', help='Name of the algorithm which should be evaluated')
    args = parser.parse_args()

    distances = ['cosine']
    methods = [3, 5]

    paths = [os.path.join(args.samples_path, f'group_{i}/data_{i}.csv') for i in range(1, 5)]
    print(paths)

    for i, path in enumerate(paths):
        df = pd.read_csv(path)
        stats_df = pd.DataFrame(columns=['sample', 'label', 'cluster'])
        stats_df['sample'] = df['Unnamed: 0'].apply(lambda x: x[:x.find('_')])
        for distance in distances:
            for method in methods:
                save_prefix = f'../results/{args.algorithm}/data-{i+1}/{distance}_{method}'
                labels_df = pd.read_csv(os.path.join(save_prefix, f'labels.csv'))
                stats_df['label'] = labels_df['labels']
                calculate_stats(stats_df, save_prefix)   

if __name__ == '__main__':
    main()
    
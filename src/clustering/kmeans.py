from sklearn.cluster import KMeans
import pandas as pd
from os.path import join as join
import utils
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples_folder', help='Absolute path for data folder')
    parser.add_argument('--save_folder', help='Absolute path for saving folder')
    args = parser.parse_args()

    sample_paths = [join(args.samples_folder, f'data_{i}.csv') for i in [2, 3, 4, 1]]

    Path(args.save_folder).mkdir(exist_ok=True)
    save_pref = [join(args.save_folder, f'data_{i}') for i in [2, 3, 4, 1]]

    for i, sample in enumerate(sample_paths):
        df = pd.read_csv(sample)
        df.index = df['Unnamed: 0']
        df = df.drop('Unnamed: 0', axis=1)

        for n in [2, 3, 4]:
            cluster_type = f'kmeans_{n}'
            folder = join(save_pref[i], cluster_type)
            print(folder)
            Path(folder).mkdir(exist_ok=True)
            
            kmeans = KMeans(n_clusters=n).fit(df)
            
            labels = kmeans.labels_
            utils.save_labels(labels, join(folder, 'labels.csv'))
            utils.save_clusters_tsne(df, labels, 2, join(folder, f'kmeans_{n}.jpg'))
    
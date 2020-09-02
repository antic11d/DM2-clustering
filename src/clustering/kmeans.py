from sklearn.cluster import KMeans
import pandas as pd
from pathlib import Path
from utils import *
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_folder', required=True, help='Absolute path for data folder')
    parser.add_argument('--output_folder', required=True, help='Absolute path for saving folder')
    parser.add_argument('--p', type=int, default=15, help='Value for dendogram depth')
    args = parser.parse_args()

    sample_paths, save_pref = get_paths(args.data_folder, args.output_folder)

    # Should be determined based on data and previous research
    n_clusters = [2, 3, 4]

    for i, sample in enumerate(sample_paths):
        df = pd.read_csv(sample)
        df.index = df['Unnamed: 0']
        df = df.drop('Unnamed: 0', axis=1)

        for n in n_clusters:
            cluster_type = f'kmeans_{n}'
            
            folder = save_pref[i]  / cluster_type
            folder.mkdir(exist_ok=True, parents=True)
            
            kmeans = KMeans(n_clusters=n).fit(df)
            
            labels = kmeans.labels_
            csv_path = folder / 'labels.csv'
            save_labels(labels, csv_path)

            tsne_save = folder / f'{cluster_type}'
            save_clusters_tsne(df, labels, 2, tsne_save)
    
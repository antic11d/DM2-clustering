from sklearn.cluster import DBSCAN
import pandas as pd
from pathlib import Path
from utils import *
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_folder', required=True, help='Absolute path for data folder')
    parser.add_argument('--output_folder', required=True, help='Absolute path for saving folder')
    args = parser.parse_args()

    sample_paths, save_pref = get_paths(args.data_folder, args.output_folder)

    # Should be determined based on data and previous research
    metrics = ['jaccard', 'cosine']
    min_neighbors = [3, 5]

    for i, sample in enumerate(sample_paths):
        df = pd.read_csv(sample)
        df.index = df['Unnamed: 0']
        df = df.drop('Unnamed: 0', axis=1)

        for metric in metrics:
            eps = dbscan_knee(df, save_pref[i], metric)

            for min_pts in min_neighbors:
                cluster_type = f'{metric}_{min_pts}'
                folder = save_pref[i]  / cluster_type
                folder.mkdir(exist_ok=True, parents=True)
                db = DBSCAN(eps=eps, min_samples=min_pts, metric=metric).fit(df)

                labels = db.labels_
                csv_path = folder / 'labels.csv'
                save_labels(labels, csv_path)

                tsne_save = folder / f'{cluster_type}'
                save_clusters_tsne(df, labels, 2, tsne_save)

    

if __name__ == '__main__':
    main()
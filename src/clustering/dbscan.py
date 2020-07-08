from sklearn.cluster import DBSCAN
import pandas as pd
from os.path import join as join
import utils
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples_folder', help='Absolute path for data folder')
    parser.add_argument('--save_folder', help='Absolute path for saving folder')
    parser.add_argument('--save_path', help='Absolute path for saving report csv')
    args = parser.parse_args()

    sample_paths = [f'{args.samples_folder}/data_{i}.csv' for i in range(1, 5)]

    Path(args.save_folder).mkdir(exist_ok=True)
    save_pref = [join(args.save_folder, f'data_{i}') for i in range(1, 5)]

    for i, sample in enumerate(sample_paths):
        df = pd.read_csv(sample)
        df.index = df['Unnamed: 0']
        df = df.drop('Unnamed: 0', axis=1)

        for metric in ['jaccard']:
            eps = utils.dbscan_knee(df, save_pref[i], metric)

            for min_pts in [3, 5]:
                cluster_type = f'{metric}_{min_pts}'
                folder = join(save_pref[i], cluster_type)
                print(folder)
                Path(folder).mkdir(exist_ok=True)

                print('dbscan')
                db = DBSCAN(eps=eps, min_samples=min_pts, metric=metric).fit(df)
                labels = db.labels_

                tsne_save = join(folder, f'{cluster_type}')
                utils.save_clusters_tsne(df, labels, 2, tsne_save)  
                
                utils.save_clusters_pca(df, labels, tsne_save)
        print(f'{sample} Done!')
    

if __name__ == '__main__':
    main()
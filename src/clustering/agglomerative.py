import pandas as pd
import scipy.cluster.hierarchy as shc 
import scipy.spatial.distance as ssd
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
    distances = ['cosine', 'jaccard']
    methods = ['average', 'ward']

    for i, sample in enumerate(sample_paths):
        df = pd.read_csv(sample)
        df.index = df['Unnamed: 0']
        df = df.drop('Unnamed: 0', axis=1)   
    
        for distance in distances:
            dist_matrix = ssd.pdist(df.values, metric=distance)
            
            for link in methods:
                Z = shc.linkage(dist_matrix, method=link)
                coph, _ = shc.cophenet(Z, dist_matrix)
                
                cluster_type = f'{distance}_{link}'
                plt_title = f'data_{i}, shape:{df.shape}:\n{cluster_type}, coph={coph}'
                
                folder = save_pref[i]  / cluster_type
                folder.mkdir(exist_ok=True, parents=True)
                
                dendro_save = folder / f'{args.p}_dendro.jpg'
                fancy_dendrogram(
                    Z,
                    truncate_mode='lastp',
                    p=args.p,
                    show_contracted=True,
                    title=plt_title,
                    save_path=dendro_save
                )
                
                elbow_save = folder / f'{cluster_type}_elbow.jpg'
                labels = elbow_agglo(Z, elbow_save)
                
                csv_path = folder / 'labels.csv'
                save_labels(labels, csv_path)
                
                tsne_save = folder / f'{cluster_type}'
                save_clusters_tsne(df, labels, 2, tsne_save)

if __name__ == "__main__":
    main()

from sklearn.cluster import SpectralClustering
import pandas as pd
from os.path import join as join
from pathlib import Path
import utils
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples_folder', help='Absolute path for data folder')
    parser.add_argument('--save_folder', help='Absolute path for saving folder')
    args = parser.parse_args()

    sample_paths = [f'{args.samples_folder}/data_{i}.csv' for i in [2, 3, 4, 1]]

    Path(args.save_folder).mkdir(exist_ok=True)
    save_pref = [join(args.save_folder, f'data_{i}') for i in [2, 3, 4, 1]]
    
    for i, sample in enumerate(sample_paths):
        df = pd.read_csv(sample_paths[i])
        df.index = df['Unnamed: 0']
        df = df.drop('Unnamed: 0', axis=1) 
        for n in n_clusters[i]:
            cluster_type = f'discretize_{n}'
            folder = join(save_pref[i], cluster_type)
            Path(folder).mkdir(exist_ok=True)
            
            spectral = SpectralClustering(n_clusters=n, 
                                        assign_labels='discretize', 
                                        random_state=0,
                                        affinity='nearest_neighbors').fit(df.values)
            labels = spectral.labels_
            utils.save_labels(labels, join(folder, 'labels.csv'))
            utils.save_clusters_tsne(df, labels, 2, join(folder, f'spectral_{n}_tsne.jpg'))

if __name__ == "__main__":
    main()    
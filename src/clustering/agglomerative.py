import pandas as pd
import scipy.cluster.hierarchy as shc 
import scipy.spatial.distance as ssd
from os.path import join as join
from pathlib import Path
import utils

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples_folder', help='Absolute path for data folder')
    parser.add_argument('--save_folder', help='Absolute path for saving folder')
    parser.add_argument('--p', help='Value for dendogram depth')
    args = parser.parse_args()

    sample_paths = [f'{args.samples_folder}/data_{i}.csv' for i in range(1, 5)]

    Path(args.save_folder).mkdir(exist_ok=True)
    save_pref = [join(args.save_folder, f'data_{i}') for i in range(1, 5)]

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
                
                
                folder = join(save_pref[i], cluster_type)
                Path(folder).mkdir(exist_ok=True)
                
                dendro_save = join(folder, f'{p}_dendro.jpg')
                utils.fancy_dendrogram(
                    Z,
                    truncate_mode='lastp',
                    p=p,
                    show_contracted=True,
                    title=plt_title,
                    save_path=dendro_save
                )
                
                elbow_save = join(folder, f'{cluster_type}_elbow.jpg')
                labels = utils.elbow_agglo(Z, elbow_save)
                
                csv_path = join(folder, f'data_{i+1}_{cluster_type}.csv')
                utils.save_labels(labels, csv_path)
                
                tsne_save = join(folder, f'{cluster_type}')
                utils.save_clusters_tsne(df, labels, 2, tsne_save)

if __name__ == "__main__":
    main()

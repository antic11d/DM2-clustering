from sklearn.cluster import SpectralClustering
import pandas as pd
from os.path import join as join
from pathlib import Path
import utils

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples_folder', help='Absolute path for data folder')
    parser.add_argument('--save_folder', help='Absolute path for saving folder')
    parser.add_argument('--save_path', help='Absolute path for saving report csv')
    args = parser.parse_args()

    sample_paths = [f'{args.samples_folder}/data_{i}.csv' for i in range(1, 5)]

    Path(args.save_folder).mkdir(exist_ok=True)
    save_pref = [join(args.save_folder, f'data_{i}') for i in range(1, 5)]
    
    df = pd.read_csv(sample_paths[3])
    df.index = df['Unnamed: 0']
    df = df.drop('Unnamed: 0', axis=1)   

    for n in [3, 4]:
        for labels_type in ['discretize', 'kmeans']:
            cluster_type = f'{labels_type}_{n}'

            plt_title = f'data_4, shape:{df.shape}:\n{cluster_type}'

            folder = join(save_pref[3], cluster_type)
            print(folder)
            Path(folder).mkdir(exist_ok=True)

            labels = SpectralClustering(n_clusters=n,
                                        assign_labels=labels_type,
                                        n_jobs=-1).fit_predict(df.values)

            tsne_save = join(folder, f'{cluster_type}')
            utils.save_clusters_tsne(df, labels, 2, tsne_save)

if __name__ == "__main__":
    main()    
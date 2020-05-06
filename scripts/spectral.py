from sklearn.cluster import SpectralClustering
import pandas as pd
import matplotlib.pyplot as plt
from os.path import join as join
import os
from sklearn.decomposition import PCA
import numpy as np
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap
from sklearn.manifold import TSNE

def save_clusters_tsne(df, labels, n_components, save_path):
    n = len(set(labels))
    
    tsne = TSNE(n_components, 
                perplexity=50,  
                n_iter=300)
    tsne_data = pd.DataFrame(tsne.fit_transform(df))
    
    fig = plt.figure(figsize=(15, 15))
    if n_components == 3:
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(tsne_data[0], 
                   tsne_data[1], 
                   tsne_data[2], 
                   c=labels,
                   cmap=ListedColormap(sns.color_palette('Set1', n).as_hex()))
    else:
        ax = fig.add_subplot(111)
        ax.scatter(tsne_data[0], 
                   tsne_data[1],
                   c=labels,
                   cmap=ListedColormap(sns.color_palette('Set1', n).as_hex()))
    
    plt.savefig(f'{save_path}_tsne_{n_components}.jpg')
    plt.close()

if __name__ == "__main__":
    sample_paths = [f'/sbgenomics/project-files/data_{i}.csv' for i in range(1, 5)]

    save_pref = [join('./spectral_sklearn', f'data_{i}') for i in range(1, 5)]
    # for i, sample in enumerate(sample_paths):
    # df = sns.load_dataset('iris')
    # df = df.drop('species', axis=1)
    df = pd.read_csv(sample_paths[3])
    df.index = df['Unnamed: 0']
    df = df.drop('Unnamed: 0', axis=1)   

    # print(f'{sample}')

    for n in [3, 4]:
        for labels_type in ['discretize', 'kmeans']:
            cluster_type = f'{labels_type}_{n}'

            plt_title = f'data_4, shape:{df.shape}:\n{cluster_type}'

            folder = join(save_pref[3], cluster_type)
            print(folder)
            try:
                os.mkdir(folder)
            except:
                pass


            labels = SpectralClustering(n_clusters=n,
                                        assign_labels=labels_type,
                                        n_jobs=-1).fit_predict(df.values)


            save_path = join(folder, f'{cluster_type}')
            save_clusters_pca(df, labels, save_path)

            tsne_save = join(folder, f'{cluster_type}')
            save_clusters_tsne(df, labels, 2, tsne_save)
    #         break
    #     break
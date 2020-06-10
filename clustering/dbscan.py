from sklearn.cluster import DBSCAN
import scipy.spatial.distance as ssd
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
from sklearn.neighbors import NearestNeighbors
from kneebow.rotor import Rotor

def save_clusters_tsne(df, labels, n_components, save_path):
    n = len(set(labels))
    
    tsne = TSNE(n_components, 
                perplexity=50,  
                n_iter=300)
    tsne_data = pd.DataFrame(tsne.fit_transform(df))
    tsne_data['labels'] = labels
    
#     colors = ListedColormap(sns.color_palette('Set1', n).as_hex())
    
    fig = plt.figure(figsize=(15, 15))
    sns.scatterplot(
        x=0,
        y=1,
        hue='labels',
        palette=sns.color_palette('Set1', n),
        data=tsne_data,
        legend='full'
    ) 
    plt.savefig(f'{save_path}_tsne_{n_components}.jpg')
    plt.close()

def knee(X, save_path, metric):
    neigh = NearestNeighbors(n_neighbors=3, metric=metric) 
    nbrs = neigh.fit(X) 
    distances, indices = nbrs.kneighbors(X)  
    distances = np.sort(distances, axis=0) 
    distances = distances[:,1] 
    rotor = Rotor()
    data = np.hstack((np.array(range(df.shape[0])).reshape(-1, 1), distances.reshape(-1, 1)))
    rotor.fit_rotate(data)
    eps = distances[rotor.get_elbow_index()]
    plt.plot(distances)
    plt.title(f'eps={eps}')
    plt.savefig(f'{save_path}_knee_{metric}.jpg')
    plt.close()
    return eps

if __name__ == '__main__':
    sample_paths = [f'/sbgenomics/project-files/data_{i}.csv' for i in range(1, 5)]

    save_pref = [join('./dbscan_sklearn', f'data_{i}') for i in range(1, 5)]

    for i, sample in enumerate(sample_paths):
    #     df = sns.load_dataset('iris')
#     df = df.drop('species', axis=1)
        df = pd.read_csv(sample)
        df.index = df['Unnamed: 0']
        df = df.drop('Unnamed: 0', axis=1)

        try:
            for metric in ['jaccard']:
                eps = knee(df, save_pref[i], metric)

                for min_pts in [3, 5]:
                    cluster_type = f'{metric}_{min_pts}'
                    folder = join(save_pref[i], cluster_type)
                    print(folder)
                    try:
                        os.mkdir(folder)
                    except:
                        pass

                    print('dbscan')
                    db = DBSCAN(eps=eps, min_samples=min_pts, metric=metric).fit(df)
                    labels = db.labels_

                    tsne_save = join(folder, f'{cluster_type}')
                    save_clusters_tsne(df, labels, 2, tsne_save)  
                    
                    save_clusters_pca(df, labels, tsne_save)
    #             break
        except:
            print('error')
            pass
        print(f'{sample} Done!')
    #     break
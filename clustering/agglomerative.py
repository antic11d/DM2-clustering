import pandas as pd
import scipy.cluster.hierarchy as shc 
import scipy.spatial.distance as ssd
import matplotlib.pyplot as plt
from os.path import join as join
import os
from sklearn.decomposition import PCA
import numpy as np
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap
from sklearn.manifold import TSNE

def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    title = kwargs.pop('title', None)
    save_path = kwargs.pop('save_path', None)
    
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    plt.figure(figsize=(20, 10))
    ddata = shc.dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title(f'{title} p={p}')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
            
    plt.savefig(save_path)
    plt.close()
    return ddata


def save_clusters_pca(df, labels, save_path):
    n = len(set(labels))
    
    pca = PCA(n_components=3).fit(df)
    pca_data = pd.DataFrame(pca.transform(df))
    explained_var = sum(pca.explained_variance_ratio_)
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(pca_data[0], 
               pca_data[1], 
               pca_data[2], 
               c=labels,
               cmap=ListedColormap(sns.color_palette('Set1', n).as_hex()))
    plt.legend(labels)
    
    plt.title(f'explained_variance={explained_var}')
    plt.savefig(save_path)
    plt.close()

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

def save_labels(labels, save_path):
    lb_df = pd.DataFrame(labels, columns=['labels'])
    lb_df.to_csv(path_or_buf=save_path)

def elbow_method(Z, save_path):
    plt.figure(figsize=(15, 15))
    last = Z[:, 2]
    last_rev = last[::-1]
    idxs = np.arange(1, len(last) + 1)
    plt.plot(idxs, last_rev)

    acceleration = np.diff(last, 2)  # 2nd derivative of the distances
    acceleration_rev = acceleration[::-1]
    plt.plot(idxs[:-2] + 1, acceleration_rev)
    
    p = acceleration_rev.argmax() + 2
    
    plt.title(f'{p} clusters')
    
    plt.savefig(save_path)
    plt.close()
    
    return shc.fcluster(Z, p, criterion='maxclust')

if __name__ == "__main__":
    distances = ['cosine', 'jaccard']
    methods = ['average', 'ward']
    sample_paths = [f'/sbgenomics/project-files/data_{i}.csv' for i in range(1, 5)]

    save_pref = [join('./agl_scipy', f'data_{i}') for i in range(1, 5)]
    p = 15

    for i, sample in enumerate(sample_paths):
#     df = sns.load_dataset('iris')
#     df = df.drop('species', axis=1)
    df = pd.read_csv(sample)
    df.index = df['Unnamed: 0']
    df = df.drop('Unnamed: 0', axis=1)   
    
    print(f'{sample}')
    
    for distance in distances:
        dist_matrix = ssd.pdist(df.values, metric=distance)
        
        for link in methods:
            Z = shc.linkage(dist_matrix, method=link)
            coph, _ = shc.cophenet(Z, dist_matrix)
            
            cluster_type = f'{distance}_{link}'
            plt_title = f'data_{i}, shape:{df.shape}:\n{cluster_type}, coph={coph}'
            
            
            folder = join(save_pref[i], cluster_type)
            try:
                os.mkdir(folder)
            except:
                pass
            
#             dendro_save = join(folder, f'{p}_dendro.jpg')
#             fancy_dendrogram(
#                 Z,
#                 truncate_mode='lastp',
#                 p=p,
#                 show_contracted=True,
#                 title=plt_title,
#                 save_path=dendro_save
#             )
            
            elbow_save = join(folder, f'{cluster_type}_elbow.jpg')
            labels = elbow_method(Z, elbow_save)
            
            csv_path = join(folder, f'data_{i+1}_{cluster_type}.csv')
            save_labels(labels, csv_path)
            
#             tsne_save = join(folder, f'{cluster_type}')
#             save_clusters_tsne(df, labels, 2, tsne_save)
            
#             save_clusters_tsne(df, labels, 3, tsne_save)

#             break
            print(f'\t\t{link}')
        print(f'\tDone! {distance}')
#         break
#     break
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import scipy.cluster.hierarchy as shc 
from sklearn.neighbors import NearestNeighbors
from kneebow.rotor import Rotor
import numpy as np
from pathlib import Path

def get_paths(data_folder, output_folder):
    sample_paths = list(Path(data_folder).glob('*.csv'))

    Path(output_folder).mkdir(exist_ok=True)
    save_pref = [Path(output_folder, path.parts[-1][:path.parts[-1].rfind('.csv')]) for path in sample_paths]
    return sample_paths, save_pref

def dbscan_knee(X, save_path, metric):
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

def elbow_agglo(Z, save_path):
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
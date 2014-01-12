print(__doc__)

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

def readFile(filepath):
    data = []
    file = open(filepath, 'r')
    
    while True:
        readLine = file.readline();
        if not readLine:
            # EOF reached
        	   break
        pass
        strData = readLine.split('\t');
        row = [int(strData[0]),int(strData[1]),int(strData[2]),int(strData[3])]
        data = data + [row];
    
    return data

##############################################################################
# Generate sample data

X = StandardScaler().fit_transform( readFile("Plotpath.txt") )
print X

##############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.33, min_samples=5).fit(X)
core_samples = db.core_sample_indices_
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)

"""
##############################################################################
# Plot result
import pylab as pl

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = pl.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'
        markersize = 6
    class_members = [index[0] for index in np.argwhere(labels == k)]
    cluster_core_samples = [index for index in core_samples
                            if labels[index] == k]
    for index in class_members:
        x = X[index]
        if index in core_samples and k != -1:
            markersize = 14
        else:
            markersize = 6
        pl.plot(x[0], x[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=markersize)

pl.title('Estimated number of clusters: %d' % n_clusters_)
pl.show()"""
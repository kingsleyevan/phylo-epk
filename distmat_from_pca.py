# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import scipy.spatial as sp

evecs = np.loadtxt("20131101_manicphylo-filter-vcfs-smartpca_shortnames_noleucopus.evec", usecols=range(1,10))
names = np.loadtxt("20131101_manicphylo-filter-vcfs-smartpca_shortnames_noleucopus.evec", usecols=([0]), dtype=str)
hab = np.loadtxt("/Users/evan/Desktop/pero_tail_length/subspp_hab.csv", usecols=([2]), dtype=str)
subspp = np.loadtxt("/Users/evan/Desktop/pero_tail_length/subspp_hab.csv", usecols=([1]), dtype=str)

dmat = sp.distance.pdist(evecs)
sq_dmat = sp.distance.squareform(dmat)


# <codecell>

from sklearn.metrics import euclidean_distances
from sklearn import manifold
from sklearn import preprocessing
import matplotlib.pyplot as mp


seed = np.random.RandomState(seed=3)

print np.std(evecs,axis=0),np.std(preprocessing.normalize(evecs),axis=0)

similarities = euclidean_distances(preprocessing.normalize(evecs))

mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed, dissimilarity="precomputed", n_jobs=1)



mf = mds.fit(similarities)
mf_for_R = mf.embedding_

X,Y = zip(*mf.embedding_)


#mp.scatter(X,Y)
#mp.show()




# <codecell>

%load_ext rmagic
%Rpush mf_for_R
%Rpush names
%Rpush hab
%Rpush subspp

# <codecell>

%%R -w 1024 -h 768

manic <- data.frame(mf_for_R)
manic$names <- names

#hab <- c('f','n','n','n','f','n','f','n','n','n','f','f','n','n','f','f','f','n','f','f','n','n','n','n','n','n','n','n','n','n','f','f','f','f','f','f','f','f','n','n','f','f','n','n','n','n','n','n','f','f','f','f','f','f','f','f','f','n','n','n','n','n','n','n','n','n','f','f','f','f','f','f','f')

o <- order(manic$names)
manic_sorted <- data.frame(manic$names[o], manic$X1[o], manic$X2[o], hab, subspp)



library(ggplot2)
mds_plot_subspp <- ggplot(manic_sorted, aes(manic.X1.o., manic.X2.o.)) + geom_text(aes(label=subspp), fontface=3, size=4, colour=factor(manic_sorted$hab))
print(mds_plot_subspp)

mds_plot_names <- ggplot(manic_sorted, aes(manic.X1.o., manic.X2.o.)) + geom_text(aes(label=manic.names.o.), fontface=3, size=4, colour=factor(manic_sorted$hab))
print(mds_plot_names)

print(manic_sorted)


# <codecell>

from cogent.phylo import distance, nj
import dendropy

!sumtrees.py --help


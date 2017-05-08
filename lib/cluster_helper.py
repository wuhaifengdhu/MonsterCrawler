#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from sklearn.cluster import KMeans
from store_helper import StoreHelper
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.cluster as cluster
import hdbscan
import time
sns.set_context('poster')
sns.set_color_codes()
plot_kwds = {'alpha': 0.25, 's': 80, 'linewidths': 0}


class ClusterHelper(object):
    @staticmethod
    def cluster_vector(vector_list):
        cluster_number = 3
        np_array = np.array(vector_list)
        k_means = KMeans(n_clusters=cluster_number, random_state=0).fit(np_array)
        length = len(k_means.labels_)
        clusters = [[str(j) for j in range(length) if k_means.labels_[j] == i] for i in range(cluster_number)]
        for i in range(len(clusters)):
            print ("Cluster %i has %i position, position: %s" % (i, len(clusters[i]), str(clusters[i])))

    @staticmethod
    def plot_clusters(data, algorithm, args, kwds):
        start_time = time.time()
        labels = algorithm(*args, **kwds).fit_predict(data)
        end_time = time.time()
        print ('\t'.join([str(i) for i in labels]))
        palette = sns.color_palette('deep', np.unique(labels).max() + 1)
        colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
        plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
        frame = plt.gca()
        frame.axes.get_xaxis().set_visible(False)
        frame.axes.get_yaxis().set_visible(False)
        plt.title('Clusters found by {}'.format(str(algorithm.__name__)), fontsize=24)
        plt.text(-0.5, 0.7, 'Clustering took {:.2f} s'.format(end_time - start_time), fontsize=14)

    @staticmethod
    def run_script(vector_list):
        ClusterHelper.plot_clusters(np.array(vector_list), hdbscan.HDBSCAN, (), {'min_cluster_size': 15})


if __name__ == '__main__':
    _vector_list = StoreHelper.load_data("../data/vectors.dat")
    ClusterHelper.cluster_vector(_vector_list)
    # ClusterHelper.run_script(_vector_list)

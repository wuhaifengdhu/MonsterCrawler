#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from sklearn.cluster import KMeans
from store_helper import StoreHelper
from dict_helper import DictHelper
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import MeanShift, estimate_bandwidth, Birch
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
        ClusterHelper.print_label(k_means.labels_, cluster_number)

    @staticmethod
    def print_label(label, index_list, cluster_number=None):
        if cluster_number is None:
            label_dict = DictHelper.dict_from_count_list(label)
            print("\t".join([str(i) for i in label]))
            print(label_dict)
            print("max cluster number: %i" % max(label_dict))
            print("min cluster number: %i" % min(label_dict))
            position_tag = {}
            for i in range(len(label)):
                DictHelper.append_dic_key(position_tag, label[i], int(index_list[i]))
            for key, value in position_tag.items():
                print ("%s: %s" % (key, value))
            StoreHelper.store_data(position_tag, 'position_tag.dat')
            StoreHelper.save_file(position_tag, 'position_tag.txt')
        else:
            length = len(label)
            clusters = [[str(j) for j in range(length) if label[j] == i] for i in range(cluster_number)]
            for i in range(len(clusters)):
                print("Cluster %i has %i position, position: %s" % (i, len(clusters[i]), str(clusters[i])))

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

    @staticmethod
    def mean_shift_cluster(vector_list):
        np_array = np.array(vector_list)
        bandwidth = estimate_bandwidth(np_array, quantile=0.2, n_samples=500)
        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(np_array)
        ClusterHelper.print_label(ms.labels_)

    @staticmethod
    def birch_cluster(vector_list, index_list):
        np_array = np.array(vector_list, dtype=float)
        brc = Birch(branching_factor=50, threshold=0.05, compute_labels=True)
        brc.fit(np_array)
        label = brc.predict(np_array)
        ClusterHelper.print_label(label, index_list)


if __name__ == '__main__':
    # _vector_list = StoreHelper.load_data("../data/vectors.dat")
    # ClusterHelper.mean_shift_cluster(_vector_list)
    # ClusterHelper.birch_cluster(_vector_list)
    # ClusterHelper.run_script(_vector_list)
    position_dict = StoreHelper.load_data("../data/position_vector_01.dat", {})
    _vector_list = position_dict.values()
    _index_list = position_dict.keys()
    ClusterHelper.birch_cluster(_vector_list, _index_list)

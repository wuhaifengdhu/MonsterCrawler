#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from sklearn.cluster import KMeans
from store_helper import StoreHelper
import numpy as np


class ClusterHelper(object):
    @staticmethod
    def cluster_vector(vector_list):
        cluster_number = 2
        np_array = np.array(vector_list)
        k_means = KMeans(n_clusters=cluster_number, random_state=0).fit(np_array)
        length = len(k_means.labels_)
        clusters = [[str(j) for j in range(length) if k_means.labels_[j] == i] for i in range(cluster_number)]
        for i in range(len(clusters)):
            print ("Cluster %i has %i position, position: %s" % (i, len(clusters[i]), str(clusters[i])))


if __name__ == '__main__':
    _vector_list = StoreHelper.load_data("../data/vectors.dat")
    ClusterHelper.cluster_vector(_vector_list)
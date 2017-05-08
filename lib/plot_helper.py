#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn import datasets
from store_helper import StoreHelper


class PlotHelper(object):
    @staticmethod
    def plot_k_means(vector_list, cluster_number=3):
        np_array = np.array(vector_list)
        k_means = KMeans(n_clusters=cluster_number, random_state=0).fit(np_array)
        X = np.asarray(vector_list)
        y = np.asarray(k_means.labels_)
        # print type(X), X.shape
        # print type(y), y.shape

        fig = plt.figure(1, figsize=(8, 6))
        plt.clf()
        ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
        plt.cla()

        # for label in range(cluster_number):
        #     name = "cluster %i" % label
        #     ax.text3D(X[y == label, 33].mean(),
        #               X[y == label, 99].mean(),
        #               X[y == label, 112].mean(), '',
        #               horizontalalignment='center',
        #               bbox=dict(alpha=.5, edgecolor='w', facecolor='w'))

        # y = np.choose(y, [0, 1, 2]).astype(np.float)
        ax.scatter(X[:, 15], X[:, 17], X[:, 23], c=y)

        ax.w_xaxis.set_ticklabels([])
        ax.w_yaxis.set_ticklabels([])
        ax.w_zaxis.set_ticklabels([])
        ax.set_xlabel('Petal width')
        ax.set_ylabel('Sepal length')
        ax.set_zlabel('Petal length')
        plt.show()


if __name__ == '__main__':
    _vector_list = StoreHelper.load_data("../data/vectors.dat")
    PlotHelper.plot_k_means(_vector_list)


#!/usr/bin/python
# -*- coding: utf-8 -*-


class DistanceHelper(object):
    @staticmethod
    def compute_distance(vector_a, vector_b):
        if len(vector_a) != len(vector_b):
            print ("Error: vector length do not equal %d compare with %d" % (len(vector_a), len(vector_b)))
            return 0
        cross_sum = a_sum = b_sum = 0
        for i in range(len(vector_a)):
            cross_sum += vector_a[i] * vector_b[i]
            a_sum += vector_a[i] * vector_a[i]
            b_sum += vector_b[i] * vector_b[i]
        if a_sum == 0 or b_sum == 0:
            print ("warn: one of vector is 0")
            return 0
        return cross_sum / ((a_sum * b_sum) ** 0.5)
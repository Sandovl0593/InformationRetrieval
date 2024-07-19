import pandas as pd
import os
import numpy as np
from rtree import index

class RtreeKNN:
    def init(self, data, index_name, dimension, m):
        p = index.Property()
        p.dimension = dimension
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        p.buffering_capacity = m

        data_file = f'{index_name}.data'
        index_file = f'{index_name}.index'
        if os.path.exists(data_file):
            os.remove(data_file)
            print(f"Removed existing data file: {data_file}")
        if os.path.exists(index_file):
            os.remove(index_file)
            print(f"Removed existing index file: {index_file}")

        self.idx = index.Index(index_name, properties=p)

        if data is not None:
            self.data = data
            self._build_index()

    def _build_index(self):
        for i in range(len(self.data)):
            point = tuple(self.data.iloc[i])
            bounding_box = point + point
            self.idx.insert(i, bounding_box)

    def knn_search(self, query_vector, K):
        query_point = tuple(query_vector)
        bounding_box = query_point + query_point
        neighbors = list(self.idx.nearest(bounding_box, K, objects=True))

        # Calculate Euclidean distance for each neighbor
        def euclidean_distance(point1, point2):
            return np.sqrt(np.sum((np.array(point1) - np.array(point2)) ** 2))

        result = []
        for neighbor in neighbors:
            point = tuple(self.data.iloc[neighbor.id])
            distance = euclidean_distance(query_point, point)
            result.append((neighbor.id, distance))

        return result
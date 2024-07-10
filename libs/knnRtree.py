import numpy as np
import rtree

# Knn search with rtree
def knn_rtree_search(query_vector, data, K):
    p = rtree.index.Property()
    p.dimension = query_vector.shape[0]
    idx = rtree.index.Index(properties=p)
    for index, row in data.iterrows():
        idx.insert(index, row['MFCC_Vector'])
    
    neighbors = list(idx.nearest(query_vector, num_results=K))
    return [(np.linalg.norm(
                query_vector - data.loc[neighbor]['MFCC_Vector']
            ), data.loc[neighbor]) for neighbor in neighbors]


def range_rtree_search(query_vector, data, radius, sort_results=True):
    p = rtree.index.Property()
    p.dimension = query_vector.shape[0]
    idx = rtree.index.Index(properties=p)
    for index, row in data.iterrows():
        idx.insert(index, row['MFCC_Vector'])
    
    results = list(idx.intersection(query_vector, radius))
    # Ordenar los resultados por distancia si sort_results es True
    if sort_results:
        results.sort(key=lambda x: np.linalg.norm(query_vector - data.loc[x]['MFCC_Vector']))

    return [(np.linalg.norm(query_vector - data.loc[result]['MFCC_Vector']), data.loc[result]
            ) for result in results]


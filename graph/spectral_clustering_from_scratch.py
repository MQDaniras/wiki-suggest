import numpy as np
import networkx as nx
from sklearn.cluster import SpectralClustering
import pickle
import glob
# from utils.pickle_dump import pickle_dump
filepath:str = "/work3/s204163/wiki/"
extension:str = "pkl"

def edge_list(G):

    # Get the edge list with weights
    edge_list_with_weights = [(u, v, d['weight']) for u, v, d in G.edges(data=True)]

    # Print the edge list
    return edge_list_with_weights


def adjacency_matrix(edge_list):
    
    # construct the pairwise distance matrix
    #A = pairwise_distances(X, metric='euclidean')

    # Number of nodes (assuming nodes are labeled from 0 to n-1)
    # n_nodes = len(edge_list)
    set_nodes = set()
    [(set_nodes.add(x),set_nodes.add(y)) for x,y,_ in edge_list] # add nodes to set_nodes
    n_nodes = len(set_nodes)
    
    # Constructing the similarity matrix 
    A = np.zeros((n_nodes, n_nodes))
    pos = {n:i for i,n in enumerate(set_nodes)} # fix if node is string/doesn't start at 0
    
    for node1, node2, weight in edge_list:
        A[pos[node1], pos[node2]] = weight
        A[pos[node2], pos[node1]] = weight  
    
    return A


# spectral clustering with the given epsilon, the distance critera for two pooints to be considered in the same cluster
def spectral_clustering(G):
    output_path = "/work3/s204163/wiki/test/"
    
    edge_list_G = edge_list(G)
    # print(edge_list(G))
    n = len(edge_list_G)
    
     # create the similarity matrix
    A = adjacency_matrix(edge_list_G)
    # pickle_dump(A,"test/A")
    # full_path = filepath + "test/A"
    # n_exist = len(glob.glob(full_path+"*"))
    # with open(f"{full_path}_{n_exist}.{extension}") as handle:
        # pickle.dump(A, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    # Compute the sum of weights for each node
    degree_sums = np.sum(A, axis=1)
    # raise Exception(degree_sums)

    # Create the degree matrix as a diagonal matrix
    D = np.diag(degree_sums)
    D = np.linalg.pinv(D)**(1/2)
    
    # create the normalized Laplacian matrix
    L = np.identity(A.shape[0]) - D @ A @ D
    # pickle_dump(L,"test/L")
    # full_path = filepath + "test/L"
    # n_exist = len(glob.glob(full_path+"*"))
    # with open(f"{full_path}_{n_exist}.{extension}") as handle:
        # pickle.dump(L, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    # print(L)
    # print(nx.linalg.normalized_laplacian_matrix(G)) # Ens
    
    # computing the eigenvector for the second-smallest eigenvalue
    eigval_sorted = np.linalg.eig(L)[0].argsort() # indices of sorted eigenvalues
    eigvecs = np.linalg.eig(L)[1] # matrix of eigenvectors
    z_eigvec = eigvecs[:,eigval_sorted][:,1] # eigenvec w.r.t. second smallest eigenvalue
    
    z_eigvec[z_eigvec >= 0] = 1
    z_eigvec[z_eigvec < 0] = 0
    
    return z_eigvec



# # Create an undirected graph
# Gx = nx.Graph()
# # Add nodes, you can add as many as you need
# Gx.add_nodes_from([1, 2, 3, 4, 5])
# # Add edges with weights
# # The tuple is (node1, node2, weight)
# Gx.add_weighted_edges_from([(1, 2, 1), (1, 3, 1), 
#                            (2, 4, 1), (3, 4, 1), 
#                            (4, 5, 1), (1, 5, 1), (2,3,1), (1,7,1), (4,9,1),(9,7,1)])

print("Begin")
if __name__ == "__main__":
    path = "/work3/s204163/wiki/test/subgraph_001.pkl"
    # path = "/work3/s204163/wiki/test/subgraph_005.pkl"
    # path = "/work3/s204163/wiki/test/subgraph_010.pkl"
    with open(path, "rb") as f:
        G: nx.Graph = pickle.load(f)
    print("Loaded subgraph_1%")
    # print("Loaded subgraph_5%")
    # print("Loaded subgraph_10%")
    

    print("Spectral-customs:",spectral_clustering(G))

    # clustering = SpectralClustering(n_clusters=2, assign_labels='kmeans', random_state=0, affinity="precomputed")
    # clustering.fit(adjacency_matrix(edge_list(Gx)))
    # print("Spectral-sklearn:",clustering.labels_)
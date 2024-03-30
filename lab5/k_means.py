import numpy as np

def initialize_centroids_forgy(data, k):
    # Random initialization
    indices = np.random.choice(data.shape[0], k, replace=False)
    return data[indices]

def initialize_centroids_kmeans_pp(data, k):
    # KMeans++ initialization
    centroids = []
    centroids.append(data[np.random.randint(data.shape[0])])
    for _ in range(1, k):
        distances = np.array([min([np.linalg.norm(x - c) for c in centroids]) for x in data])
        prob = distances / distances.sum()
        cumulative_prob = prob.cumsum()
        r = np.random.rand()
        for j, p in enumerate(cumulative_prob):
            if r < p:
                i = j
                break
        centroids.append(data[i])
    return np.array(centroids)

def assign_to_cluster(data, centroids):
    return np.argmin(np.linalg.norm(data[:, np.newaxis] - centroids, axis=2), axis=1)

def update_centroids(data, assignments):
    return np.array([data[assignments == k].mean(axis=0) for k in range(len(np.unique(assignments)))])

def mean_intra_distance(data, assignments, centroids):
    return np.sqrt(np.sum((data - centroids[assignments])**2))

def k_means(data, num_centroids, kmeansplusplus=False):
    # Centroids initialization
    if kmeansplusplus:
        centroids = initialize_centroids_kmeans_pp(data, num_centroids)
    else: 
        centroids = initialize_centroids_forgy(data, num_centroids)

    assignments = assign_to_cluster(data, centroids)
    for i in range(100):  # Maximum number of iterations = 100
        # print(f"Intra distance after {i} iterations: {mean_intra_distance(data, assignments, centroids)}")
        new_centroids = update_centroids(data, assignments)
        new_assignments = assign_to_cluster(data, new_centroids)
        if np.array_equal(new_assignments, assignments):  # Stop if nothing changed
            break
        else:
            assignments = new_assignments
            centroids = new_centroids

    return assignments, centroids, mean_intra_distance(data, assignments, centroids)

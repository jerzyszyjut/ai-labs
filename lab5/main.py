from k_means import k_means
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Useful learning resource
# https://www.kaggle.com/code/khotijahs1/k-means-clustering-of-iris-dataset

def load_iris():
    data = pd.read_csv("data/iris.data", names=["sepal_length", "sepal_width", "petal_length", "petal_width", "class"])
    classes = data["class"].to_numpy()
    features = data.drop("class", axis=1).to_numpy()
    return features, classes

def evaluate(clusters, labels):
    for cluster in np.unique(clusters):
        labels_in_cluster = labels[clusters==cluster]
        print(f"Cluster: {cluster}")
        for label_type in np.unique(labels):
            print(f"Num of {label_type}: {np.sum(labels_in_cluster==label_type)}")
    
def clustering(kmeans_pp):
    data = load_iris()
    features, classes = data
    intra_class_variance = []
    best_assignments, best_centroids, best_error = None, None, np.inf
    for i in range(100):
        assignments, centroids, error = k_means(features, 3, kmeans_pp)
        #evaluate(assignments, classes)
        intra_class_variance.append(error)
        if error < best_error:
            best_assignments, best_centroids, best_error = assignments, centroids, error

    colors = ["red", "green", "blue"]
    for cluster in np.unique(best_assignments):
        plt.scatter(features[best_assignments==cluster, 0], features[best_assignments==cluster, 1], c=colors[cluster])
    for centroid in best_centroids:
        plt.scatter(centroid[0], centroid[1], c="black", s=100)
    
    plt.legend(list(np.unique(classes)) + ["Centroid"])
    plt.show()

    print(f"Mean intra-class variance: {np.mean(intra_class_variance)}")

if __name__=="__main__":
    clustering(kmeans_pp = True)
    # clustering(kmeans_pp = False)

import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
from time import time
from sklearn import metrics
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.metrics import normalized_mutual_info_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans, AffinityPropagation, estimate_bandwidth, MeanShift, SpectralClustering, \
    AgglomerativeClustering, DBSCAN

#加载digits  data
np.random.seed(42)
digits = load_digits()
data = scale(digits.data)
n_samples, n_features = data.shape
n_digits = len(np.unique(digits.target))
labels = digits.target
sample_size = 300
print("n_digits: %d, \t n_samples %d, \t n_features %d"
      % (n_digits, n_samples, n_features))
print(82 * '_')
print('init\t\ttime\tnmi\thomo\tcompl')

#评估
def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0),
             #metrics.normalized_mutual_info_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_)))

#kmeans
bench_k_means(KMeans(init='k-means++', n_clusters=n_digits, n_init=10),name="k-means++", data=data)
bench_k_means(KMeans(init='random', n_clusters=n_digits, n_init=10),name="random", data=data)
# in this case the seeding of the centers is deterministic, hence we run the
# kmeans algorithm only once with n_init=1
pca = PCA(n_components=n_digits).fit(data)
bench_k_means(KMeans(init=pca.components_, n_clusters=n_digits, n_init=1),name="PCA-based",data=data)

#AffinityPropagation
bench_k_means(AffinityPropagation(),name="AffinityPropagation", data=data)

# MeanShift
bandwidth = estimate_bandwidth(data, quantile=0.1)
bench_k_means(MeanShift(bandwidth=bandwidth, bin_seeding=True),name="MeanShift",data=data)

# ward hierarchical clustering
bench_k_means(AgglomerativeClustering(n_clusters=10, linkage='ward'),name="ward hierarchical clustering",data=data)

# AgglomerativeClustering
bench_k_means(AgglomerativeClustering(),name="AgglomerativeClustering",data=data)

# DBSCN
bench_k_means(DBSCAN(),name="DBSCAN()",data=data)

print(82 * '_')
reduced_data = PCA(n_components=2).fit_transform(data)

# Visualize the results on PCA-reduced data  way1
# example:meanshift

bandwidth = estimate_bandwidth(reduced_data, quantile=0.07)
meanshift = MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(reduced_data)
result = meanshift.labels_
centroids = meanshift.cluster_centers_
labels_unique = np.unique(result)
n_clusters_ = len(labels_unique)
plt.figure(1)
plt.clf()
colors = cycle('bgrcmybgrcmybgrcmybgrcmy')
for k, col in zip(range(n_clusters_), colors):
    my_members = result == k
    cluster_center = centroids[k]
    plt.plot(reduced_data[my_members, 0], reduced_data[my_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=5)
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()

# Visualize the results on PCA-reduced data  way2
# example:kmeans
kmeans = KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
kmeans.fit(reduced_data)  # 对降维后的数据进行kmeans
result = kmeans.labels_
plt.figure(2)
plt.clf()
plt.scatter(reduced_data[:, 0], reduced_data[:, 1],c=result)
centroids = kmeans.cluster_centers_   #得到各类中心点
#聚类中心
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
plt.show()

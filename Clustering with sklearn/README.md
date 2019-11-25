实验四                      
==============
实验题目 
---------------
Clustering with sklearn

编程环境 
---------------
anaconda + Spyder  
Win10 + python3.7  

实验任务
---------------  
### -- Datasets
      • sklearn.datasets.load_digits
      • sklearn.datasets.fetch_20newsgroups
  ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-1.png)
  ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-2.png)

### -- 测试sklearn中以下聚类算法在以上两个数据集上的聚类效果
  ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-3.png)
  
### -- Evaluation
    – labels_true and labels_pred
        • >>> from sklearn import metrics
        • >>> labels_true = [0, 0, 0, 1, 1, 1]
        • >>> labels_pred = [0, 0, 1, 1, 2, 2]      
    – Normalized Mutual Information (NMI)
        • >>> metrics.normalized_mutual_info_score(labels_true, labels_pred) 
    – Homogeneity: each cluster contains only members of a single class
        • >>> metrics.homogeneity_score(labels_true, labels_pred) 
    – Completeness: all members of a given class are assigned to the same cluster
        • >>> metrics.completeness_score(labels_true, labels_pred)

digits手写数字数据集
--------------- 
实验要求采用digits数据集，我们先对这个数据集进行一个初步的了解：  
手写数字数据集包含1797个0-9的手写数字数据，每个数据由8 * 8 大小的矩阵构成，矩阵中值的范围是0-16，代表颜色的深度。
我们先加载一下数据，了解一下数据的维度，并以图像的形式展示一些第一个数据：  

    import matplotlib.pyplot as plt
    from sklearn.datasets import load_digits
    digits = load_digits()
    print(digits.data.shape)
    print(digits.target.shape)
    print(digits.images.shape)
    plt.matshow(digits.images[0])
    plt.show()
可以看到数据维度和第一张手写数字：
(1797, 64)
(1797,)
(1797, 8, 8)  
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-5.png)     

实验步骤
--------------- 
### 一、 K-means聚类digits数据集  
在sklearn官网中提供的K-means对digits的聚类的demo代码中运行出来的结果如下：（https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_digits.html）   

   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-7.png)    
从库sklearn.datasets中加载digits数据集，数据集的介绍见上面。数据集是分好label的，存在digits.target中，同时我们可
以提取出数据集的样本数，每个样本的维度，分别存储在n_samples n_features中，输出这三个变量，可以得到：  
                              
      n_digits: 10     n_samples： 1797    n_features： 64  
     
对官网代码进行改动，使用不同的评分方法来计算score表示聚类后类别的准确性，下面再分别用三种k-means聚类的方式来调用
这段评分代码，得到不同的score：  

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

其中K-means函数参数详解见链接：https://blog.csdn.net/weixin_44707922/article/details/91954734

由此得到init=random，k-means++，pca下各个方式的score :  
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-8.png)

### 二、可视化聚类结果
在上面步骤中k-means聚类和评估已经全部完成了，但是为了更好可视化输出，我们可以进行操作：使用pca降维至两维，再进行聚类   
理由：  
     1.散点图中的数据点是两位的  
     2.在2维的基础上再次k-means聚类是因为已经聚类高维数据映射到二维空间的prelabel可能分散不过集中，影响可视化效果。  
    
     reduced_data = PCA(n_components=2).fit_transform(data)
     kmeans = KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
     kmeans.fit(reduced_data)  # 对降维后的数据进行kmeans
     result = kmeans.labels_
得到各个类的中心点：  
     
     centroids = kmeans.cluster_centers_
定义输出的变化范围和输出的效果：  

     #窗口
     plt.imshow(Z, interpolation='nearest',
                extent=(xx.min(), xx.max(), yy.min(), yy.max()),
                cmap=plt.cm.Paired,
                aspect='auto', origin='lower')
     #降维后的数据点
     plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
     #聚类中心
     plt.scatter(centroids[:, 0], centroids[:, 1],
                 marker='x', s=169, linewidths=3,
                 color='w', zorder=10)

### 三、修改demo可视化效果
聚类后的结果应该是不同类以不同的颜色来表明，所以在修改的时候我用不同颜色来表示不同的聚类点，最后再加上聚类中心，会有更加直观
的结果：

    plt.scatter(reduced_data[:, 0], reduced_data[:, 1],c=kmeans.labels_)    
    
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-9.png) 
 
 ### 四、使用不同的方法对digits数据集聚类
有了前一部分的探索，使用其他的聚类方法处理起来就会相对轻松，下面我们分别来看这几种方法的聚类和评估结果：  
#### 1、AffinityPropagation
使用AffinityPropagation的核心算法如下所示：  

    af = AffinityPropagation().fit(reduced_data)
    result = af.labels_
按照demo模型形式，绘制出来的效果如下：
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-10.png)   

![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-11.jpg) 

修改可视化效果后如下：
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-12.jpg) 

#### 2、MeanShift
    bandwidth = estimate_bandwidth(reduced_data, quantile=0.1)#经过测试，在quantile=0.1的情况下得到的结果是最好的
    bench_k_means(MeanShift(bandwidth=bandwidth, bin_seeding=True),name="MeanShift",data=data)
    meanshift = MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(reduced_data)
使用demo的效果本身就很好，如下：
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-6.png) 
 
与 K-means 聚类不同的是，Mean-Shift 不需要选择聚类的数量，因为mean-shift 自动发现它。这是一个很大的优点。事实上聚类中心
向着有最大密度的点收敛也是我们非常想要的，因为这很容易理解并且很适合于自然的数据驱动的场景。缺点是滑窗尺寸/半径“r“的选择需
要仔细考虑。
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-16.gif) 

 下图展示了所有滑动窗口从端到端的整个过程。每个黑色的点都代表滑窗的质心，每个灰色的点都是数据点。
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-17.gif) 

#### 3、SpectralClustering  
    pca = PCA(n_components=n_digits).fit_transform(data)#要使用数据降维是因为高维情况在建图过程存在数据缺失
    bench_k_means(SpectralClustering(n_clusters=10),name="spectralcluster",data=pca)
    
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-14.png) 
这个聚类是没有聚类中心的。

#### 4、ward hierarchical clustering
    ward = AgglomerativeClustering(n_clusters=10, linkage='ward')
    ward.fit(data)
其他的聚类方法可视化效果都类似，这里不再一一可视化。

#### 5、AgglomerativeClustering
    clustering = AgglomerativeClustering().fit(data)
    
#### 6、DBSCN
    db = DBSCAN().fit(data)
    result = db.labels_
  
 ### 五、不同聚类方法的指标对比：
 
    init		time	nmi	homo	compl
    k-means++	0.60s	0.625	0.602	0.650
    random   	0.26s	0.689	0.669	0.710
    PCA-based	0.06s	0.680	0.667	0.695
    AffinityPropagation	6.43s	0.616	0.932	0.460
    MeanShift	0.51s	0.008	0.004	0.212
    ward hierarchical clustering	0.51s	0.796	0.758	0.836
    AgglomerativeClustering	0.20s	0.378	0.239	0.908
    DBSCAN() 	0.62s	0.000	0.000	1.000
   
结论分析与体会
---------------   
对比这几种方法，感觉k-means算法相对较好，尽管在种子选点的方式上存在随机性，对异常偏离值不太敏感，但这个算法的逻辑和原理，对
聚类的测定和迭代方法使它成为最经典，也是首选的聚类方法，在各个评价指标上都有一个相对较好的结果，而且速度比较快，计算量少。其
他方法各有优劣，如AP和sc的时间复杂性较高，存在准确度上有较大的偏差，无法求得聚类中心等问题。

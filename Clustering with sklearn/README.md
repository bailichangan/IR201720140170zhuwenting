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
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-4.png)  
可以看到数据维度和第一张手写数字：
(1797, 64)
(1797,)
(1797, 8, 8)
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-5.png) 
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework4-6.png)   

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

### 二、可视化聚类
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

### 三、对demo可视化效果的修改/另一种形式展示



2、MAP评价
MAP在Precision@K的基础上进行，主要步骤为：  

     一、考虑每个相关docid在测试结果中的位置，K1,K2, … KR；  
     二、为K1,K2 , … KR计算Precision@K；
     三、求这R个P@K的平均值AvgPrec，得到AP；
     四、MAP即为多个查询的AP的均值；
 ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-11.png)   
 
 可以得到MAP评价结果如下：  
 
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-12.png)   
.......    
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-13.png) 

3、MRR评价  
MRR相比其他两个较为简单，只需考虑第一个相关文档出现的位置就可以，步骤为：  

     一、考虑第一个相关文档的名次位置
     二、计算排名分数为1/k，即RR
     三、MRR即为RR的均值  
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-14.png)   

可以得到MRR评价结果如下：  

![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-15.png)    
.......    
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-16.png)  

4、NDCG评价  
NDCG基于两个假设：  

      • 高度相关的文档比边缘相关的文档更加有用
      • 文档的排名越低，对用户越无用  
      
具体步骤为：  

    一、给每一个真实相关的doc，附一个gain
    二、计算第n级的CG
    三、做一个discount的log运算，意为对测试结果的排名做一个惩罚（高rel，但rank不够靠前也很拉低评分），得到DCG
    四、标准化，得到IDCG,进而计算NDCG
    五、对每个query的NDCG求均值，得到最后的NDCG
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-17.png)  

可以得到NDCG评价结果如下：  

![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-18.png)    
.......   
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-19.png)   
   
结论分析与体会
---------------   
MAP可以在每个召回率水平上提供单指标结果，在众多指标中，MAP被证明具有非常好的区别性和稳定性。NDCG是针对非二值情况下的指标
同指标P@K一样，基于前K个检索结果进行计算。NDCG相对于MAR和MRR指标公式更复杂，所以计算方式存在差异的可能性更大。除了C是进
行累加没有什么争议以外，N、D、G三项计算都可能存在差别。

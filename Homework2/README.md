实验二                          
==============
实验题目 
---------------
Ranked retrieval model 

编程环境 
---------------
anaconda + Spyder  
Win10 + python3.7

实验任务
---------------
### – 在Homework1.1的基础上实现最基本的Ranked retrieval model  
      • Input：a query (like Ron Weasley birthday)
      • Output: Return the top K (e.g., K = 10) relevant tweets.  
### • Use SMART notation: lnc.ltc  
      • Document: logarithmic tf (l as first character), no idf and cosine normalization
      • Query: logarithmic tf (l in leftmost column), idf (t in second column), no normalization
### • 改进Inverted index  
      • 在Dictionary中存储每个term的DF
      • 在posting list中存储term在每个doc中的TF with pairs (docID, tf)  
### • 选做
      • 支持所有的SMART Notations  
  
### 1、向量相似度的基本算法  
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework2-8.png) 
   
### 2、不同tf-idf方法的SMART系统记号   
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework2-9.png)  

实验步骤
---------------
### 一、对推特数据的处理
       1、 打开推特的文本数据发现数据具有较好的结构性，信息主要有userName、clusterNo、text、timeStr、tweetId、errorC
       ode、textCleaned、relevance这些部分的信息，除了下图红色标注的，对于我们的检索任务而言，其它信息都是冗余的，我们
       首先需要提取出userName、text、tweetId三部分信息来建立inverted index的postings。 
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.5.png)   
   
       2、 按行读取每条tweet后调用tokenize_tweet方法对其进行处理,并进行分词后对单词的大写统一变小写、单复数和动词形式统
       一等处理。使用TextBlob工具包，处理后的推特如下所示：
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.6.png)  
   
       3、然后进行分词等处理后的推特如下：  
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.7.png)  
   
       4、最后再构建postings，采用字典结构，其中将每个term作为键值，后面跟着包含该term的[tweetid,tf_wght_doc]。
       具体实现步骤为：
         （1）先逐行读取文本内容，用cnt_line计算文档总数，同时记录下每个term在该文档中出现的次数即tf_raw_doc，
              进而求取tf_wght_doc，再利用tf_wght_doc求该篇文档的权重平方和。 
         （2）为postings中的每个term添加含有该term的tweetid和对应的tf_wght_doc项，即[tweetid,tf_wght_doc]
              同时计算出现该term的文档数目即df,以便后面计算idf。
       代码如下：
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework2-6.png)  
   
       postings输出结果如下：
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework2-4.png)  
   
   ### 二、对查询的输入进行处理
         对查询进行和tweet同样的分词等处理，保持一致性
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework2-10.png)   
    
   ### 三、Use SMART notation: lnc.ltc
         本次实验采用lnc.ltc的权重计算机制，query采用了对数tf计算方法、idf权重因子，document采用了对数tf计算方法、没有
         采用idf因子（同时基于效率和效果的考虑）及余弦归一化方法，对于每个查询词项term，根据term的贡献依次反复更新score
         数组。具体代码实现如下：
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework2-5.png)   
   
         其中tf_wght_query是query的tf，document_frequency[term]是query的idf，两者相乘是query的权重，te[0]、te[1]对应
         于postings中的[tweetid,tf_wght_doc]          
                 
 ### 四、 查询，可以返回排序最靠前的10个结果
           先对query进行和tweet同样的分词等处理，再调用第三步的lnc_ltc函数计算所有文档的得分，用sort排序选出分数（相似度）
           最高的K篇文档。
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework2-7.png)     
     
     
 结果展示
---------------
### 一、input a query: like Ron Weasley birthday
 ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework2-1.png)  
 
### 二、input a query: Boko Haram Kidnapped French tourists
 ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework2-2.png)   
 
### 三、input a query: China Achebe death
 ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework2-3.png) 
  
  
  结论分析与体会
  ---------------  
  本次实验将每篇文档和一个文本查询分别表示成一个向量，希望在给定查询时能从文档集合中返回得分最高的K篇文档，与实验一不同的是
  需要考虑文档和查询向量的相似度。如果使用向量相似度的基本算法计算权重时可能需要浮点数，这会造成空间的浪费，可以通过如下两步
  来缓解空间浪费问题，第一步如果使用Inverted intex的话，则不必事先计算出idf的值，只需要将N/df存储在term对应的倒排记录表的
  头部就已经足够，求query权重时再计算每个term的idf即可。第二步，在每个Postings中存储词项频率tf。此次实验我就采取了第二步，
  构建postings时为postings中的每个term添加含有该term的tweetid和对应的tf_wght_doc项，即[tweetid,tf_wght_doc]。
  此次实验采用lnc.ltc的权重计算机制，query采用了对数tf计算方法、idf权重因子，document采用了对数tf计算方法、没有采用idf因子
 （同时基于效率和效果的考虑）及余弦归一化方法，对于每个查询词项term，根据term的贡献依次反复更新score数组。
 

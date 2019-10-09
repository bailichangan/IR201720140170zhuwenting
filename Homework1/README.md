实验一                          
==============
实验题目 
---------------
Inverted index and Boolean Retrieval Model  

编程环境 
---------------
anaconda + Spyder  
Win10 + python3.7

实验任务
---------------
### 1. 使用我们介绍的方法，在tweets数据集上构建inverted index; 
        实现Boolean Retrieval Model，使用TREC 2014 test topics进行测试； 
### 2.Boolean Retrieval Model：
        • Input：a query (like Ron and Weasley)
        • Output: print the qualified tweets.
        • 支持and, or ,not；查询优化可以选做；
### 注意：
        对于tweets与queries使用相同的预处理；  
        
实验步骤
---------------
### 一、对推特数据的处理
       1、 打开推特的文本数据发现数据具有较好的结构性，信息主要有userName、clusterNo、text、timeStr、tweetId、errorCode、
       textCleaned、relevance这些部分的信息，但是除了红色标注的，对于我们的检索任务而言，其它的都是冗余的，我们首先需要集中
       提取出红色的三部分信息来建立inverted index的postings。     
       2、 按行读取每条tweet后调用tokenize_tweet方法对其进行处理,并进行分词后对单词的统一变小写、单复数和动词形式统一等处理
       使用TextBlob工具包，处理后的推特如下所示：
       3、然后进行分词等处理后的推特如下：
       4、最后再构建postings，采用字典结构，其中将每个单词作为键值，后面跟着包含该单词的tweet的tweetid列表。  
       
### 二、对查询的输入进行处理
       1、对输入的查询进行语义逻辑的识别，判断是什么样的布尔查询。
       在本次实验中，针对单个and、or、not（A and B、A or B、A not B）三种布尔查询进行了实现，并在此基础上对双层逻辑的如
       A and B and C、A or B or C、(A and B) or C、(A or B) and C的实现，并作为功能拓展实现了对一般输入语句进行的排序
       查询，可以返回排序最靠前的若干个结果。
       如下所示：(用查询的单词在该文档中出现的个数/总数作为简单的排序分数)
       其中merge合并列表时采用同时遍历的方法，降低复杂度为O(x+y)，如下merge2_and所示：  
       
### 三、实验结果展示
      1、A and B、A or B、A not B：
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.1.png)
      2、A and B and C、A or B or C、(A and B) or C、(A or B) and C：
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.2.png)
      3、一般的语句查询：
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.3.png)  

![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.4.png)  

结论分析与体会
---------------



       

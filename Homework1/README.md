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
       

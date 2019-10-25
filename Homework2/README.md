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
   
       4、最后再构建postings，采用字典结构，先逐行读取文本内容，记录下每个term在该文档中出现的次数即tf_raw_doc，进而求取tf_wght_doc，其中将每个term作为键值，后面跟着包含该term的[tweetid,tf_wght_doc]。 
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.8.png)
   

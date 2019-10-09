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
       1、 打开推特的文本数据发现数据具有较好的结构性，信息主要有userName、clusterNo、text、timeStr、tweetId、errorC
       ode、textCleaned、relevance这些部分的信息，除了下图红色标注的，对于我们的检索任务而言，其它信息都是冗余的，我们
       首先需要提取出userName、text、tweetId三部分信息来建立inverted index的postings。 
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.5.png)   
   
       2、 按行读取每条tweet后调用tokenize_tweet方法对其进行处理,并进行分词后对单词的大写统一变小写、单复数和动词形式统
       一等处理。使用TextBlob工具包，处理后的推特如下所示：
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.6.png)   
       
       3、然后进行分词等处理后的推特如下：  
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.7.png)  
   
       4、最后再构建postings，采用字典结构，其中将每个单词作为键值，后面跟着包含该单词的tweet的tweetid列表。 
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.8.png)
       
### 二、对查询的输入进行处理
       1、对输入的查询进行语义逻辑的识别，判断是什么样的布尔查询。
       在本次实验中，针对单个and、or、not（A and B、A or B、A not B）三种布尔查询进行了实现，并在此基础上对双层逻辑的如
       A and B and C、A or B or C、(A and B) or C、(A or B) and C的实现，并作为功能拓展实现了对一般输入语句进行的排序
       查询，可以返回排序最靠前的若干个结果。
       如下所示：(用查询的单词在该文档中出现的个数/总数作为简单的排序分数)
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.9.png)  
   ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/1.10.png)
   
       其中merge合并列表时采用同时遍历的方法，我们对每个有序表都维护一个位置指针，并让两个指针同时在两个列表中后移，每一步
       我们都比较两个位置所指向的两个文档id，如果两者一样，则将该id输出到结果表中，然后同时将两个指针后移一位.如果两个文档
       id不同，则将较小的id所对应的指针后移，降低复杂度为O(x+y)。 
       
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
构建inverted index首先需要将每篇文档转换成一个个词条的列表，然后进行语言学的预处理，产生归一化的词条作为词项，最后将所有文档按
照其中出现的词项来建立inverted index。根据inverted index的模型可以完成布尔查询的基本要求，复杂的布尔查询也可以在基本的and、or
、not逻辑基础实现上通过嵌套实现，最后通过用查询的单词在该文档中出现的个数/总数作为简单的排序检索，没有计算文档和查询的相似度，结
果比较粗糙，需要进一步评估。在本次inverted index模型中没有考虑tf、idf和文档length等信息，还需要进一步完善来满足更高级的应用需求
另外，在查询时还可以通过组织查询的处理过程来使处理的工作量最小，达到优化查询的目的。


       

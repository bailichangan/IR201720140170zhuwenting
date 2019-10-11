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

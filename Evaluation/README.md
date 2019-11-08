实验三                       
==============
实验题目 
---------------
IR Evaluation

编程环境 
---------------
anaconda + Spyder  
Win10 + python3.7  

实验任务
---------------  
### --实现以下指标评价，并对HW1.2检索结果进行评价
      • Mean Average Precision (MAP)
      • Mean Reciprocal Rank (MRR)
      • Normalized Discounted Cumulative Gain (NDCG)
  ![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-1.png)

相关知识
--------------- 
### 一、Mean average precision(MAP)：  
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-4.png)  
其中，N 表示相关文档总数，position(i) 表示第 i 个相关文档在检索结果列表中的位置。  
MAP（Mean Average Precision）即多个查询的平均正确率（AP）的均值，从整体上反映模型的检索性能。    
   
### 二、Mean reciprocal rank (MRR) ：
1、RR（reciprocal rank）
倒数排名，指检索结果中第一个相关文档的排名的倒数。
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-2.png)  
2、MRR（mean reciprocal rank）
多个查询的倒数排名的均值，公式如下：
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-3.png)  
ranki 表示第 i 个查询的第一个相关文档的排名。  

### 三、nDCG  
在MAP计算公式中，文档只有相关不相关两种，而在nDCG中，文档的相关度可以分多个等级进行打分。  
1、Cumulative Gain(CG)：  
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-5.png)    
2、Discounted cumulative gain(DCG)：  
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-6.png)  
3、Ideal DCG(IDCG)：
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-7.png)   
4、Normalize DCG(nDCG)：  
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-8.png)   

实验步骤
--------------- 
1、由qrels.txt和result.txt分别获得qrels_dict和test_dict
![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-9.png)    

![image](https://github.com/bailichangan/IR201720140170zhuwenting/blob/master/img-folder/Homework3-10.png)   

2、MAP评价
MAP在Precision@K的基础上进行，主要步骤为：
     一、考虑每个相关docid在测试结果中的位置，K1,K2, … KR；
     二、为K1,K2 , … KR计算Precision@K；
     三、求这R个P@K的平均值AvgPrec，得到AP；
     四、MAP即为多个查询的AP的均值；
 
   

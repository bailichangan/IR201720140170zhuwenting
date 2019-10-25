import math
from textblob import TextBlob
from textblob import Word
from collections import defaultdict

postings = defaultdict(dict)
document_frequency = defaultdict(int)
score = defaultdict(float)
cosine = defaultdict(dict)

def lnc_ltc(query):
    unique_query = set(query)
    for term in unique_query:
        tf_raw_query = query.count(term)
        tf_wght_query = 1 + math.log(tf_raw_query, 10)  # query的tf

        for te in postings[term]:
            tweetid = te[0]
            score[tweetid] += tf_wght_query * document_frequency[term] * te[1] / cosine[te[0]]
            #document_frequency[term]：idf_query  log N/df  te[1]  tf_wght_doc
            #cosine[te[0]] = math.sqrt(pow(tf_wght_doc, 2))


def rank_search():
    str = token(input("Search query >> "))
    lnc_ltc(str)

    ans = sorted(score.items(), key=lambda x: x[1], reverse=True)
    i = 0
    print("Return the top 10 relevant tweets:")
    while i < 10:
        print(ans[i])
        i = i + 1
    print("All relevant tweets:")
    print(ans)


# 对查询进行和tweet同样的分词等处理，保持一致性
def token(doc):
    doc = doc.lower()
    terms = TextBlob(doc).words.singularize()
    result = []
    for word in terms:
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")
        result.append(expected_str)

    return result

# 处理tweets数据集，用于下面get_postings
def tokenize_tweet(document):
    global uselessTerm
    uselessTerm = ["username", "text", "tweetid"]
    document = document.lower()
    a = document.index("username")
    b = document.index("clusterno")
    c = document.rindex("tweetid") - 1
    d = document.rindex("errorcode")
    e = document.index("text")
    f = document.index("timestr") - 3
    # 提取用户名、tweet内容和tweetid三部分主要信息
    document = document[c:d] + document[a:b] + document[e:f]

    terms = TextBlob(document).words.singularize()
    result = []
    for word in terms:
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")
        if expected_str not in uselessTerm:
            result.append(expected_str)

    return result

# 读取数据集（document),构建存储tf 的postings
def get_postings():
    global postings
    f = open(r"C:\Users\43498\PycharmProjects\Homework2\tweets.txt")
    lines = f.readlines()  # 逐行读取文本内容,返回行的列表
    cnt_line = 0 #初始化文档总数
    for line in lines:
        line = tokenize_tweet(line)  #处理数据
        tweetid = line[0]  # 在处理的文本集中取出tweetid单独存储
        line.pop(0)  # 删除id
        cosine[tweetid] = 0
        for te in line:
            tf_raw_doc = line.count(te)  # 记录tf_raw (document)
            tf_wght_doc = 1+math.log(tf_raw_doc,10)   #tf
            if te in postings.keys():
                postings[te].append([tweetid,tf_wght_doc])  #为每个词项的postings添加tf
                document_frequency[te]=document_frequency[te]+1    #出现te的所有文档数目即df
                cosine[tweetid]=cosine[tweetid]+pow(tf_wght_doc,2) #文档的权重平方和
            else:#该term还未创建postings
                postings[te] = [[tweetid,tf_wght_doc]]
                document_frequency[te] = 1
                cosine[tweetid] = cosine[tweetid]+tf_wght_doc*tf_wght_doc
        cnt_line = cnt_line + 1  #cnt_line计算文档总数
        #print(cnt_line)

    for te in document_frequency:
        document_frequency[te]=math.log(cnt_line/document_frequency[te],10)   #idf
    for tw in cosine:
        cosine[tw]=math.sqrt(cosine[tw])    #权重的平方和开根号，余弦归一化的倒数
        




def main():
    get_postings()

    while True:
        rank_search()

if __name__ == "__main__":
    main()

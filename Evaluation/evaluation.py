import math
import numpy as np

#input qrels.txt,output qrels_dict
def generate_tweetid_gain(file_name):
    qrels_dict = {}
    with open(file_name, 'r', errors='ignore') as f:
        for line in f:
            ele = line.strip().split(' ')
            if ele[0] not in qrels_dict:
                qrels_dict[ele[0]] = {}

            if int(ele[3]) > 0:
                qrels_dict[ele[0]][ele[2]] = int(ele[3])
    return qrels_dict
#input result.txt,output test_dict
def read_tweetid_test(file_name):
    test_dict = {}
    with open(file_name, 'r', errors='ignore') as f:
        for line in f:
            ele = line.strip().split(' ')
            if ele[0] not in test_dict:
                test_dict[ele[0]] = []
            test_dict[ele[0]].append(ele[1])
    return test_dict

def MAP_eval(qrels_dict, test_dict, k = 100):
    AP_result = []
    for query in qrels_dict:
        test_result = test_dict[query]
        true_list = set(qrels_dict[query].keys())
        length_use = min(k, len(test_result))
        if length_use <= 0:
            print('query ', query, ' not found test list')
            return []
        P_result = []
        i = 0
        i_retrieval_true = 0


        for doc_id in test_result[0: length_use]:
            i += 1
            if doc_id in true_list:
                i_retrieval_true += 1
                P_result.append(i_retrieval_true / i)

        if P_result:
            AP = np.sum(P_result) / len(true_list)
            print('query:', query, ',AP:', AP)
            AP_result.append(AP)
        else:
            print('query:', query, ' not found a true value')
            AP_result.append(0)
    return np.mean(AP_result)

def MRR_eval(qrels_dict, test_dict, k = 100):
    RR_result = []
    for query in qrels_dict:
        test_result = test_dict[query]
        true_list = set(qrels_dict[query].keys())

        length_use = min(k, len(test_result))
        if length_use <= 0:
            print('query ', query, ' not found test list')
            return []
        P_result = []
        i = 0


        for doc_id in test_result[0: length_use]:
            i += 1
            if doc_id in true_list:
                i_retrieval_true = 1
                P_result.append(i_retrieval_true / i)
                break

        if P_result:
            RR = np.sum(P_result)/1.0
            print('query:', query, ',RR:', RR)
            RR_result.append(RR)
        else:
            print('query:', query, ' not found a true value')
            RR_result.append(0)
    return np.mean(RR_result)

def NDCG_eval(qrels_dict, test_dict, k = 100):
    NDCG_result = []
    for query in qrels_dict:
        test_result = test_dict[query]
        # calculate DCG just need to know the gains of groundtruth
        true_list = list(qrels_dict[query].values())
        true_list = sorted(true_list, reverse=True)
        i = 1
        DCG = 0.0
        IDCG = 0.0

        length_use = min(k, len(test_result), len(true_list))
        if length_use <= 0:
            print('query ', query, ' not found test list')
            return []
        for doc_id in test_result[0: length_use]:
            i += 1
            rel = qrels_dict[query].get(doc_id, 0)
            DCG += (pow(2, rel) - 1) / math.log(i, 2)
            IDCG += (pow(2, true_list[i - 2]) - 1) / math.log(i, 2)
        NDCG = DCG / IDCG
        print('query', query, ', NDCG: ', NDCG)
        NDCG_result.append(NDCG)
    return np.mean(NDCG_result)

def evaluation():
    k = 100
    # query relevance file
    file_qrels_path = 'qrels.txt'
    # qrels_dict = {query_id:{doc_id:gain, doc_id:gain, ...}, ...}
    qrels_dict = generate_tweetid_gain(file_qrels_path)
    # ur result, format is in function read_tweetid_test, or u can write by ur own
    file_test_path = 'result.txt'
    # test_dict = {query_id:[doc_id, doc_id, ...], ...}
    test_dict = read_tweetid_test(file_test_path)
    MAP = MAP_eval(qrels_dict, test_dict, k)
    print('MAP', ' = ', MAP, sep='')
    MRR = MRR_eval(qrels_dict, test_dict, k)
    print('MRR', ' = ', MRR, sep='')
    NDCG = NDCG_eval(qrels_dict, test_dict, k)
    print('NDCG', ' = ', NDCG, sep='')
if __name__ == '__main__':
    evaluation()


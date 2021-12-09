from scipy.spatial.distance import cosine
import numpy as np
from gensim.models import Word2Vec,KeyedVectors

emb_dict = dict()
with open('emb/services_embedding.emb', 'r') as f:
    lines = f.readlines()
    for line in lines[1:]:
        list = line.split(' ')
        emb_dict[list[0]] = list[1:]
trained_w2v_model = KeyedVectors.load_word2vec_format('emb/services_embedding.emb')

def get_topN_serv_by_emb(emb,topN=10):
    list = trained_w2v_model.similar_by_vector(emb,topn=topN)
    servs = [t[0] for t in list]
    return servs

def get_top_N_serv_by_chosen_serv(chosen_serv,topN=10):
    average_pooling_emb = np.array(np.zeros(128))
    for serv in chosen_serv:
        chosen_serv_emb = np.array(emb_dict[serv],dtype='float64')
        average_pooling_emb = np.add(chosen_serv_emb,average_pooling_emb)
    average_pooling_emb = average_pooling_emb * [1/len(chosen_serv)]
    recommand_serv = get_topN_serv_by_emb(average_pooling_emb,topN=len(chosen_serv)+topN)
    recommand_serv = [x for x in recommand_serv if x not in chosen_serv][:10]
    return recommand_serv


if __name__ == '__main__':
    servs = get_top_N_serv_by_chosen_serv(['3248','1238','11111','39','5'],topN=10)
    print(servs)

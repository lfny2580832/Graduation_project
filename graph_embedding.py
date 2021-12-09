import random
from deepwalk import graph
from gensim.models import Word2Vec

NUM_WALKS = 10
WALK_LENGTH = 80
DIMENSION = 128
WINDOW_SIZE = 5

str_graph = []
attr_graph = []

def load_graph():
    global str_graph,attr_graph
    str_graph = graph.load_adjacencylist('adjlist/structure_graph.adjlist')
    print("Number of str_graph nodes: {}".format(len(str_graph.nodes())))
    attr_graph = graph.load_adjacencylist('adjlist/attribute_graph.adjlist')
    print("Number of attr_graph nodes: {}".format(len(attr_graph.nodes())))

def get_random_walks(G, num_walks, wlength):
    walks = graph.build_deepwalk_corpus(G, num_paths=num_walks, path_length=wlength, alpha=0,
                                        rand=random.Random(1))
    print("shit")
    print(walks[0])
    return walks

def filter_walks(walks, node_num):
    filter_walks = []
    for walk in walks:
        if int(walk[0]) <= node_num:
            fwalks = [nid for nid in walk if int(nid) <= node_num]
            filter_walks.append(fwalks)
    return filter_walks

def train_gat2vec(nwalks, wlength, dsize, wsize):
    global str_graph,attr_graph
    print("Random Walks on Structural Graph")
    walks_structure = get_random_walks(str_graph, nwalks, wlength)
    print("Random Walks on Attribute Graph")
    walks_attribute = get_random_walks(attr_graph, nwalks, wlength * 2)
    walks = filter_walks(walks_attribute, len(str_graph.nodes()))  # 19396个服务
    walks = walks_structure + walks
    print("Learning Representation")
    model = Word2Vec([list(map(str, walk)) for walk in walks],
                     size=dsize, window=wsize, min_count=0, sg=1,
                     workers=4)
    fname = 'emb/services_embedding.emb'
    model.wv.save_word2vec_format(fname)
    print("Learned Representation Saved")

if __name__ == "__main__":
    load_graph()
    train_gat2vec(NUM_WALKS,WALK_LENGTH,DIMENSION,WINDOW_SIZE)
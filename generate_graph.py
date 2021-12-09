import collections
from random import choice
import random
import jsonlines

serv_deliver_set = set()  # 送样方式不限/不限、检测机构上门采样、快递邮寄、客户亲自送样
serv_period_set = set()  # 1-3天、3-7天、7-15天、15-30天/1-3个月/半年内/一年内/一年以上/不限
serv_company_employees_set = set()  # 少于10人、10-50人、50-100人、100-200人、200-500人、500人以上
# 这三种set需要跑代码得到
serv_company_labs_set = set()  # 0-10、10-50、50-100、100以上
serv_location_set = set()
serv_range_set = set()

serv_deliver_dict = {
    '不限':20000,
    '检测机构上门采样':20001,
    '快递邮寄':20002,
    '客户亲自送样':20003
}

serv_period_dict = {
    '1-7天':20004,
    '7-30天':20005,
    '1-3个月':20006,
    '半年内':20007,
    '一年内':20008,
    '其他':20009
}
serv_company_employees_dict = {
    '少于10人':20010,
    '10-50人':20011,
    '50-100人':20012,
    '100-200人':20013,
    '200-500人':20014,
    '500人以上':20015
}
serv_range_dict = {} # 20016开始
serv_location_dict = {} # 20041开始
serv_company_labs_dict = {} # 20121开始，20125结束

# 根据概率生成数字
def num_of_prob(sequence, probability):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(sequence, probability):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item

# 生成一个结构图邻接表
def generate_adjlist(begin,end):
    with open('adjlist/structure_graph.adjlist', 'a') as f:
        adjlist = collections.defaultdict(set)
        for id in range(begin,end,1):
            if num_of_prob([0,1], [0.9,0.1]):
                # 添加邻居后，有p的概率再添加一个邻居，最多10个邻居
                for i in range(1,10,1):
                    p = 0.5
                    if not num_of_prob([0,1], [1-p,p]):
                        break
                    else:
                        neighbor = choice([i for i in range(begin,end) if i != id])
                        adjlist[id].add(neighbor)
        # 变成无向图
        for key in list(adjlist.keys()):
            for value in adjlist[key]:
                adjlist[value].add(key)
        # 输出到文件
        for id in range(begin,end,1):
            f.write(str(id))
            if id in adjlist.keys():
                for value in adjlist[id]:
                    f.write(' ' + str(value))
            f.write('\n')

def generate_attr_adjlist():
    with open('services_data/services_reset.txt', 'r') as f1, open('adjlist/attribute_graph.adjlist', 'a') as f2:
        adjlist = collections.defaultdict(set)
        for json_obj in jsonlines.Reader(f1):
            id = json_obj['serv_id']
            deliver_vertex = serv_deliver_dict[json_obj['serv_deliver']]
            adjlist[id].add(deliver_vertex)
            adjlist[deliver_vertex].add(id)

            period_vertex = serv_period_dict[json_obj['serv_period']]
            adjlist[id].add(period_vertex)
            adjlist[period_vertex].add(id)

            range_vertex = serv_range_dict[json_obj['serv_range']]
            adjlist[id].add(range_vertex)
            adjlist[range_vertex].add(id)

            employees_vertex = serv_company_employees_dict[json_obj['serv_company_employees']]
            adjlist[id].add(employees_vertex)
            adjlist[employees_vertex].add(id)

            location_vertex = serv_location_dict[json_obj['serv_location'][1]]
            adjlist[id].add(location_vertex)
            adjlist[location_vertex].add(id)

            labs_vertex = serv_company_labs_dict[json_obj['serv_company_labs']]
            adjlist[id].add(labs_vertex)
            adjlist[labs_vertex].add(id)

        for id in adjlist.keys():
            f2.write(str(id))
            for neighbor in adjlist[id]:
                f2.write(' ' + str(neighbor))
            f2.write('\n')

# 将service输出为dict{id:[a1 a2 a3]}
def extract_attribute():
    with open('services_data/services_reset.txt', 'r') as f1:
        for json_obj in jsonlines.Reader(f1):
            serv_deliver_set.add(json_obj['serv_deliver'])
            serv_period_set.add(json_obj['serv_period'])
            serv_range_set.add(json_obj['serv_range'])
            serv_company_employees_set.add(json_obj['serv_company_employees'])
            serv_location_set.add(json_obj['serv_location'][1])
            serv_company_labs_set.add(json_obj['serv_company_labs'])

def range_to_vertex():
    vertex = 20016
    for range in serv_range_set:
        serv_range_dict[range] = vertex
        vertex += 1
    # print(str(serv_range_dict))

def location_to_vertex():
    vertex = 20041
    for location in serv_location_set:
        serv_location_dict[location] = vertex
        vertex += 1
    # print(str(serv_location_dict))

def labs_to_vertex():
    vertex = 20121
    for labs in serv_company_labs_set:
        serv_company_labs_dict[labs] = vertex
        vertex += 1
    # print(str(serv_company_labs_dict))

if __name__ == '__main__':
    generate_adjlist(1,19397)
    extract_attribute()
    range_to_vertex()
    location_to_vertex()
    labs_to_vertex()
    # 所需属性当做vertex的dict已经准备完成
    generate_attr_adjlist()
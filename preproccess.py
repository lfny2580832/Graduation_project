import json
import jsonlines

def reset_labs_and_deliver():
    with open('services_data/services_new.txt', 'r+') as f1, open('services_data/services_reset.txt', 'a') as f2:
        for json_obj in jsonlines.Reader(f1):
            # 重设labs字段
            labs = int(json_obj['serv_company_labs'])
            if labs <= 10 and labs >= 0:
                json_obj['serv_company_labs'] = '0-10个'
            elif labs <= 50 and labs >= 11:
                json_obj['serv_company_labs'] = '10-50个'
            elif labs <= 100 and labs >= 51:
                json_obj['serv_company_labs'] = '50-100个'
            elif labs <= 200 and labs >= 101:
                json_obj['serv_company_labs'] = '100-200个'
            else:
                json_obj['serv_company_labs'] = '大于200个'

            # 重设送样方式字段
            if json_obj['serv_deliver'] == '送样方式不限':
                json_obj['serv_deliver'] = '不限'

            # 重设period字段
            period = json_obj['serv_period']
            if period == ('1-3天' or '3-7天'):
                json_obj['serv_period'] = '1-7天'
            elif period == ('7-15天' or '15-30天'):
                json_obj['serv_period'] = '7-30天'
            elif period == ('1-3个月'):
                json_obj['serv_period'] = '1-3个月'
            elif period == ('半年内'):
                json_obj['serv_period'] = '半年内'
            elif period == ('一年内'):
                json_obj['serv_period'] = '一年内'
            else:
                json_obj['serv_period'] = '其他'

            f2.write(json.dumps(json_obj, ensure_ascii=False) + '\n')

def reset_id():
    map = dict()
    index = 1
    with open('services_data/services.txt', 'r+') as f1,open('services_data/services_new.txt', 'a') as f2:
        for json_obj in jsonlines.Reader(f1):
            id = json_obj['serv_id']
            if id in map:
                # 略过重复，不写入新文件
                continue
            map[id] = 1
            json_obj['serv_id'] = index
            index = index + 1
            # 写入新文件
            f2.write(json.dumps(json_obj,ensure_ascii=False) + '\n')

if __name__ == '__main__':
    reset_labs_and_deliver()
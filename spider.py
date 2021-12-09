import time
import requests
from bs4 import BeautifulSoup
import re
import json

json_file = open('services_data/services.txt', 'a', encoding='utf-8')
stop = False

def constrct_url():
    return 0;

def get_service_from_url(service_id):
    print("%d开始爬取" % service_id,end='')
    target = 'https://www.woyaoce.cn/service/info-%d.html' % (service_id)
    headers = get_headers()
    try:
        req = requests.get(url=target,headers=headers)
    except Exception as e:
        print(" 服务端关闭了socket，休息60s继续爬")
        print(repr(e))
        time.sleep(60)
        get_service_from_url(service_id)
        return
    req.encoding = 'utf-8'
    if(req.status_code == 403):
        print(" 被网站ban了，想办法吧")
        global stop
        stop = True
        return
    soup = BeautifulSoup(req.text, 'lxml')
    # 检测服务名称、检测项目、一级标签、送样方式、检测周期、服务地点在description中
    serv_des = soup.find('div',class_='jieshao fl')
    if not serv_des:
        print(' 这个id没有检测服务信息')
        time.sleep(0.5)
        return;
    serv_title = serv_des.find('p',class_='f18b fl').string
    serv_contents = []
    for content in serv_des.find('p',class_='dpl f14 nr1').find_all('span'):
        serv_contents.append(content.string)
    serv_standard = []
    for standard in serv_des.find_all('span',class_='fl biaoqian ml10 mt3'):
        serv_standard.append(standard.string)
    serv_tags = serv_des.find_all('span',class_='dpl bq-1 ml10')
    serv_deliver = serv_tags[0].string
    serv_period = serv_tags[1].string
    serv_range = serv_tags[2].string.split("：")[1]
    serv_company = soup.find('p', class_='f14b gs-name').string
    serv_company_employees = soup.find('span', class_='f12 dpl fl c6 ml6').string
    serv_company_labs = soup.find_all('span', class_='f12 dpl fl c6 ml6',string=re.compile('独立实验室'))[0].string
    serv_company_labs = re.findall("\d+",serv_company_labs)
    if(len(serv_company_labs) > 0):
        serv_company_labs = serv_company_labs[0]
    else:
        serv_company_labs = 0
    serv_company_services = soup.find('span',class_='f20 c3').string
    #为了拿三级分类，三级分类在公司下的该服务详情页中，因此先构建公司-服务详情页url
    service_company_id = soup.find_all('a',href=re.compile("/member/"))[1].get('href').split("/")[-2]
    target_company_service = "https://www.woyaoce.cn/member/%s/service-%d.html" % (service_company_id,service_id)
    req2 = requests.get(url=target_company_service)
    req2.encoding = 'utf-8'
    soup2 = BeautifulSoup(req2.text, 'lxml')
    #从第一个meta content字符串"xxx、xxx、一级分类-二级分类-三级分类领域检测"中提取分类
    serv_category = soup2.find('meta').get('content')
    if(not serv_category):
        print(" 网站规律性抽风反爬，休息65s继续爬")
        # save_wrongID_to_file(service_id)
        time.sleep(65)
        get_service_from_url(service_id)
        return
    serv_category = serv_category.split("、")[-1][-5::-1][::-1].split("-")
    serv_location = soup2.find('div',class_='sild_left_list')
    if(not serv_location):
        print(" 位置信息出错，网站问题，略过")
        return
    serv_location = serv_location.find(string=re.compile('所在地区')).next_element.string.split(' ')

    json_obj = {
        "serv_id":service_id,
        "serv_title":serv_title,
        "serv_items":serv_contents,
        "serv_deliver":serv_deliver,
        "serv_period":serv_period,
        "serv_range":serv_range,
        "serv_company":serv_company,
        "serv_company_services":serv_company_services,
        "serv_company_employees":serv_company_employees,
        "serv_company_labs":serv_company_labs,
        "serv_category":serv_category,
        "serv_location":serv_location
    }
    json_str = json.dumps(json_obj,ensure_ascii=False)
    print(" 已存")
    save_service_to_file(json_str)
    time.sleep(0.5)

def get_headers():
    headers = {
        'Host': 'www.woyaoce.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-User': '?1',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Cookie': 'Hm_lvt_bbfe67df9882ce9c614f879578ca6e52=1637591795; 3i=2021112222363597; ASP.NET_SessionId=xzsdd3lu31f1tstrwje34j4d; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217d4813c5a37ee-006af5007d3ea8-1c306851-2764800-17d4813c5a4ae5%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217d4813c5a37ee-006af5007d3ea8-1c306851-2764800-17d4813c5a4ae5%22%7D; _jzqa=1.1542214760470276000.1637671457.1637671457.1637671457.1; _jzqc=1; _jzqx=1.1637671457.1637671457.1.jzqsr=woyaoce%2Ecn|jzqct=/news/interviewlist-1%2Ehtml.-; _qzja=1.965000312.1637671457147.1637671457147.1637671457147.1637671457147.1637671457147.0.0.0.1.1; _qzjc=1; uniqueVisitorId=fba0f46c-ea66-9083-7729-dadd33e5444d; www.echatsoft.com_529370_encryptVID=MyrmElp%2B9yDATLmUo6Su%2BQ%3D%3D; www.echatsoft.com_529370_chatVisitorId=1877703020; echat_firsturl=https%3A%2F%2Fwww.woyaoce.cn%2Fmember%2FT137351%2F; echat_firsttitle=%E6%81%BA%E6%97%B6%E6%B5%A6%EF%BC%88%E4%B8%8A%E6%B5%B7%EF%BC%89%E6%A3%80%E6%B5%8B%E6%8A%80%E6%9C%AF%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8_%E6%88%91%E8%A6%81%E6%B5%8B; HMF_CI=45c546e2da27e733a7107d0b6dba05380c6d5b5e1733f2f64a03785bda5ef37f09; _Jo0OQK=70EB8235ACC44E17186991F04770CE034EFE07D90558E219B28E203134DF2EC12E08C532E813CA5C723526FF17A52F99D16700B37AAC7A57E67101953034A196393BFCAF11C6ABA202A47ECF43BAA78857D47ECF43BAA78857D04121802CC2FF256GJ1Z1Qg==; ValidCodeValue=2ZT4; Hm_lpvt_bbfe67df9882ce9c614f879578ca6e52=1638001555'
    }
    return headers

def save_service_to_file(json_str):
    global json_file
    json_file.write(json_str+'\n')

def save_wrongID_to_file(service_id):
    wrongID_file = open('wrongID.txt', 'a')
    wrongID_file.write(str(service_id)+' ')
    wrongID_file.close()

def start_to_fetch():
    global json_file
    # get_service_from_url(15697)
    for service_id in range(5508,10000,1):
        global stop
        if(stop == True):
            print("停止爬虫")
            break;
        get_service_from_url(service_id)
    json_file.close()

def fetch_from_wroingID():
    with open('wrongID.txt') as file:
        content = file.read().split(' ')

if __name__ == '__main__':
    start_to_fetch()

import spider

def fetch_from_wroingID():
    with open('wrongID.txt') as file:
        id_list = file.read().split(' ')
    for id in id_list:
        spider.get_service_from_url(id)

if __name__ == '__main__':
    fetch_from_wroingID()

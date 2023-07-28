import requests
from bs4 import BeautifulSoup

def inf():
    url = 'https://free-proxy-list.net/'
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    return url, headers


def get_proxy():
    url, headers = inf()
    r = requests.get(url=url, headers=headers)
    columb = []
    proxy_list = []
    if r.status_code == 200:
        responce = r.text
        soup = BeautifulSoup(responce, 'lxml')
        get_table = soup.find('table', class_='table table-striped table-bordered')
        get_columb = get_table.find('thead').find('tr').find_all('th')
        get_proxy = get_table.find('tbody').find_all('tr')
        for item in get_columb:
            columb.append(item.text)
        
        for item in get_proxy:
            ip = item.find_all('td')[0].text
            port = item.find_all('td')[1].text
            https = item.find_all('td')[6].text
           # print(f'{ip}:{port} - {https}')
            proxy_list.append({
                'ip':ip,
                'port':port,
                'https':https
            })
    else:
        print('connection refused')
    return proxy_list

def proxy_checker():
    proxy_list = get_proxy()
    pst = []
    i = 0
    valid = 0
    for item in proxy_list:
        ip = item['ip']
        port = item['port']
        proxies = {
            'http':f'http://{ip}:{port}',
            'https':f'http://{ip}:{port}'
        }
        try:
            r = requests.get('http://api.ipify.org/', proxies=proxies)
            i += 1
            print(f'[{i}/{len(proxy_list)}]{ip}:{port} - is worked')
            pst.append(f'{ip}:{port}')
            valid +=1
        except:
            i +=1
            print(f'[{i}/{len(proxy_list)}]{ip}:{port} - is not worked')
    print('{v} proxy finded')
    print('writing to file lists.txt ...')
    with open('lists.txt', 'w') as file:
        for item in pst:
            file.write(item+'\n')
    print('writing is ended')
proxy_checker()
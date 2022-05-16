import re

import requests
from bs4 import BeautifulSoup

from common.log_out import log_err
from dbs.pipelines import MongoPipeline

url = 'https://www.amazon.cn/gp/navigation/ajax/generic.html?ajaxTemplate=hamburgerMainContent&pageType=Gateway&hmDataAjaxHint=1&navDeviceType=desktop&isSmile=0&isPrime=0&isBackup=false&hashCustomerAndSessionId=c1368cb93a0501cba54d54678f330e56a2505085&isExportMode=false&languageCode=zh_CN&environmentVFI=AmazonNavigationCards%2Fdevelopment%40B6077969839-AL2_x86_64&secondLayerTreeName=apparel_shoes%2Bcomputer_office%2Bhome_kitchen%2Bbeauty_pca%2Bkindle_ebook%2Bsports_outdoor%2Bgrocery%2Bbaby_toy%2Bphones_elec%2Bjewelry_watch%2Bhome_improvement%2Bvideo_game%2Bmusical_instrument%2Bcamera'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'downlink': '1.35',
    'ect': '3g',
    'Host': 'www.amazon.cn',
    'Pragma': 'no-cache',
    'rtt': '600',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Cookie': 'session-id=457-2023666-8893122; i18n-prefs=CNY; ubid-acbcn=457-3495621-5265355; session-token=LnaDz5YhFmr2qIsNfwo9qrSuJKpcXOZZwnetCv5fDogrpp5jt6ypcivhBKw3o/j4Lty4fDOnoSS/2kjnx5lth2Sh8wVBVF5NzJceR6ZZKd6zNvrVSeMECCDLXvTqzf2w4YkVAYh38z2L0XVvgyaN2w4M5x8FKb97K5JlpcFbljCHSGpun62OAbzGAY2e2dC2; session-id-time=2082729601l; csm-hit=adb:adblk_no&t:1650267938953&tb:TXVFXG64F0VZGVF9Y9G4+s-QYS179Y56PGCYD4JTGH4|1650267938953'
}


def get_category():
    resp = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    for ul in soup.find_all('ul'):
        try:
            category_1 = ul.find_all('li')[1].get_text()
            for li in ul.find_all('li')[2:]:
                try:
                    category_2 = li.get_text()
                    category_2_link = li.find('a').get('href')
                    if not str(category_2_link).startswith('https://www.amazon.cn'):
                        category_2_link = 'https://www.amazon.cn' + category_2_link
                    if '全部' not in category_2:
                        data = {
                            'category_1': category_1,
                            'category_2': category_2,
                            'category_2_link': category_2_link
                        }
                        MongoPipeline('categories').insert_item(data)
                except:
                    pass
        except:
            pass


def count_items(category_link):
    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'session-id=457-2023666-8893122; i18n-prefs=CNY; ubid-acbcn=457-3495621-5265355; session-token=I1qW2imZvZhT+PJQShMXYHZh8hEoHeXUtW84iINy9fOX6NIICJj/RdQDEsqPHLz2kHuZWeyJOQvoSF7uCNOJ4mxjtdbe/w0CrGENI8MUISLg9+67F5hl7bhNJKSPOILEbj/z0tyLLBRLABhKfNANIFL3Gb7Sp1YZ470MRtrDu7vdAePN8td66z2L2TlI6ums; session-id-time=2082787201l; csm-hit=adb:adblk_no&t:1650269013727&tb:s-09VAGM492ZE16QSMR0XE|1650269013587',
            'downlink': '1.35',
            'ect': '3g',
            'Host': 'www.amazon.cn',
            'Pragma': 'no-cache',
            'rtt': '750',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
        }
        resp = requests.get(url=category_link, headers=headers)
        if resp.status_code == 200:
            try:
                _text = re.search('超过 ?(\d+,\d+|\d+) ?个|超过 ?(\d+,\d+|\d+) ?条|共 ?(\d+,\d+|\d+) ?个|共 ?(\d+,\d+|\d+) ?条',
                                  str(resp.text), re.S).group(0)
                if _text:
                    _text = re.search('\d+', _text.replace(',', '')).group(0)
                    if _text:
                        _count = int(_text)
                        print('re', _count)
                        MongoPipeline('categories').update_item({'category_2_link': None},
                                                                {'category_2_link': category_link, 'count': _count})
            except Exception as error:
                log_err(error)
    except Exception as error:
        log_err(error)


count_sum = []
for num, i in enumerate(MongoPipeline('categories').find({'$nor': [{'count': None}]})):
    count_sum.append(i['count'])

print(sum(count_sum))

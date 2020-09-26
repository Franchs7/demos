#!/usr/bin/env python
import requests
from pyquery import PyQuery as pq


def switch_ip(ip):
    list1 = ip.split('.')
    list2 = []
    for item in list1:
        item = bin(int(item))
        item = item[2:]
        list2.append(item.zfill(8))

    v2 = ''.join(list2)
    return int(v2, base=2)


def is_edu_id(ip):
    """
    :param: ip ip地址
    :return: True 属于教育网IP False 不属于教育网IP
    """

    response = requests.get('http://ipcn.chacuo.net/view/i_CERNET')
    d = pq(response.text)
    items = d('.list dd').items()
    ip_list = []
    for item in items:
        ip_list.append(item.children().text())


    for ip_item in ip_list:
        start = ip_item.split(' ',1)[0].strip()
        end = ip_item.split(' ',1)[1].strip()
        if switch_ip(ip)<switch_ip(end) and switch_ip(ip)>switch_ip(start):
            return True
    return False

def is_ipv4(ip: str) -> bool:
    """
    检查ip是否合法
    :param: ip ip地址
    :return: True 合法 False 不合法
    """

    return True if [1] * 4 == [x.isdigit() and 0 <= int(x) <= 255 for x in ip.split(".")] else False


if __name__ == '__main__':
    print(is_edu_id('192.168.1.1'))
    # print(is_ipv4("192.168.1.1"))
    print(is_edu_id('222.201.17.1'))
    print(11111111111111111111111111)


### ---xxx--- 表示该步骤得出的结果
def switch_ip(ip)
    list1 = ip.split('.')
    list2 = []
    for item in list1:
        item = bin(int(item))
        item = item[2:]

        # 将IP地址地址的每个字段转换成八位，不足的在每段前补0.
        list2.append(item.zfill(8))

    # 将4段8位二进制连接起来，变成32个0101的样子.
    v2 = ''.join(list2)
    return int(v2,base=2)

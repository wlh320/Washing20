#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" FUCK shlunan's shit-like app and its fucking QRCode ! """
import requests
import json
import hashlib
import urllib.parse as parse
from datetime import datetime

URL = 'http://webapi.shlunan.cn/Home/ApiWashingRoomMachineList'

# this.sign = SignUtils.sign("address=" + Util.ToURLEncoded(this.name) + "page=" + "1" + "pageSize=" + "" + "timeStamp=" + this.time + "token=" + "b38449c7e6e24f6d85a6402bbe740b84");

def get_sign(address):
    param_str = 'address='+parse.quote(address)+'page=1pageSize=timeStamp='+str(int(datetime.now().timestamp()))+'token=b38449c7e6e24f6d85a6402bbe740b84'
    secret = '*%#^5KYTRFV4538f.cjley$^POI234de'
    str1 = str.lower(param_str)
    str2 = secret + str1

    md5 = hashlib.md5()
    md5.update(str2.encode('utf-8'))
    return str.upper(md5.hexdigest())


def get_machine_status(address):
    params = {
        'token':'b38449c7e6e24f6d85a6402bbe740b84',
        'page':1,
        'timeStamp': int(datetime.now().timestamp()),
        'address': address,
        'pageSize':''
    }
    params['sign'] = get_sign(address)
    res = requests.post(URL, data=params)
    return json.loads(res.text)


def parse_json(data):
    if not (data['success'] == 1 and data['msg'] == 'ok'):
        print('获取数据失败')
    else:
        data = data['data']
        address = data['WashingRoom']['Address']
        total_num = data['RecordTotal']
        machine_list = data['MachineList']
        print(address + ':')
        print('共 ' + str(total_num) + ' 台洗衣机')

        for machine in machine_list:
            mid = machine['MachineSn']
            status = machine['MachineStatusMsg']
            time = machine['RemainingTimeL']
            print('编号:' + str(mid) + '\t状态:' + status + '\t剩余:' + str(time) + ' 分钟')


def main():
    address = '同济大学嘉定校区二十号楼'
    wm_data = (get_machine_status(address))
    parse_json(wm_data)

if __name__ == '__main__':
    main()

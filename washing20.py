#!/usr/bin/python3
# -*- coding:utf-8 *-*
"""监视20号楼的洗衣机状态"""
import re
import requests
WM_20 = [3908, 3927, 3948, 3958]

def is_ready(mach_no):
    """获取状态"""
    status_url = "http://www.iskyct.com/www/Uwash/scan/OptionSelect.jsp?MACHINE_CD="
    status_url += str(mach_no)
    req = requests.get(status_url)
    return "功能选择" in req.text


def get_time(mach_no):
    """获取剩余时间"""
    root_url = "http://www.iskyct.com/www/Uwash/shopsearch/shopdetail.jsp?SHOP_CD=629&YuyueFlg=0"
    content = requests.get(root_url).text
    pat_str = '<span><b>' + str(mach_no) + r'号</b>\s*<br>(\d\d:\d\d)'
    pattern = re.compile(pat_str)
    time = re.findall(pattern, content)
    time = time[0] if len(time) == 1 else '00:00'
    return time


if __name__ == '__main__':
    for wm_no in WM_20:
        status = is_ready(wm_no)
        if status:
            print(wm_no, "号可以使用")
        else:
            print(wm_no, "号已被占用,", "剩余时间", get_time(wm_no))

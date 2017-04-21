#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2016-10-26 16:54:43
# Author     : cc
# Description:

import os
import time
from automateMac import *

'''---config---'''
nsecond = 1
totaltime = 1800
appname = "test"
bundleid = "com.apple.dt.Instruments"
systemlog = "systeminfo.log"
graphlog = "graphinfo.log"
instrument = get_appref(bundleid)
'''-----*------'''


# 将文件重命名为其最后修改时间
def log_bak(filelist):
    for file in filelist:
        if os.path.exists(file):
            createtime = os.stat(file).st_mtime
            str_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(createtime))
            old_name = os.path.splitext(file)
            new_name = old_name[0] + "(" + str_time  + ")" + old_name[1]
            os.rename(file, new_name)


# nsecond间隔收集cpu数据
def collect_systeminfo(sampletime = nsecond, ntimes = totaltime):
    start_time = time.time()
    if ntimes == -1:
        ntimes = float("inf")
         
    sysfile = open(systemlog, "a")
    jump_page(instrument, 0)
    time.sleep(0.2)
    
    now_time = time.time()
    while now_time - start_time < ntimes:
        try:
            sysinfo = get_systeminfo(instrument, appname)
            sysfile.write('\t'.join(sysinfo))
            sysfile.write('\n')
            now_time = time.time()
            time.sleep(sampletime)
        except Exception:
            continue
    sysfile.close()
 
 
# 收集gpu数据
def collect_graphinfo():
    graphfile = open(graphlog, "a")
    jump_page(instrument, 1)
    time.sleep(0.2)
    
    grapinfolist = get_graphinfo(instrument)
    for info in grapinfolist:
        graphfile.write('\t'.join(info))
        graphfile.write('\n')
    graphfile.close()

    
# 主流程
def main():
    log_bak([systemlog, graphlog])
    start_record()
    collect_systeminfo()
    stop_record()
    collect_graphinfo()


if __name__ == "__main__":
    main()


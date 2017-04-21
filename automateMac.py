#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2016-10-26 15:42:50
# Author     : cc
# Description:

import time
import platform

if platform.system() != 'Windows':

    import atomac

    
    def get_group(self, match = None):
        return self._convenienceMatch('AXGroup', 'AXRoleDescription', match)
        
    atomac.NativeUIElement.group = get_group
    
    
    def get_splitgroup(self, match = None):
        return self._convenienceMatch('AXSplitGroup', 'AXRoleDescription', match)
        
    atomac.NativeUIElement.splitgroup = get_splitgroup

    
    def get_outline(self, match = None):
        return self._convenienceMatch('AXOutline', 'AXRoleDescription', match)
        
    atomac.NativeUIElement.outline = get_outline
  

    def get_row(self, match = None):
        return self._convenienceMatch('AXRow', 'AXRoleDescription', match)
        
    atomac.NativeUIElement.row = get_row
  

    def get_scollarea(self, match = None):
        return self._convenienceMatch('AXScrollArea', 'AXRoleDescription', match)
        
    atomac.NativeUIElement.scollarea = get_scollarea


    def get_table(self, match = None):
        return self._convenienceMatch('AXTable', 'AXRoleDescription', match)
        
    atomac.NativeUIElement.table = get_table
    
    
    def get_statictext(self, match = None):
        return self._convenienceMatch('AXStaticText', 'AXRoleDescription', match)
        
    atomac.NativeUIElement.text = get_statictext


    def get_toolbars(self, match = None):
        return self._convenienceMatch('AXToolbar', 'AXRoleDescription', match)
        
    atomac.NativeUIElement.toolbars = get_toolbars

  
    def get_checkboxs(self, match = None):
        return self._convenienceMatch('AXCheckBox', 'AXRoleDescription', match)
        
    atomac.NativeUIElement.checkboxs = get_checkboxs  


    # 打开指定序列的控件页面：1-Activity；2-gpu
    def jump_page(instrument, index):
        page_group = instrument.windows()[0].group()[0].splitgroup()[0]
        page_obj = page_group.group()[0].outline()[0].row()[index].table()[0].row()[1]
        # 第一次点击只到app窗口，第二次点击才到控件分页
        page_obj.clickMouseButtonLeft(page_obj.AXPosition)
        time.sleep(0.1)
        page_obj.clickMouseButtonLeft(page_obj.AXPosition)
    

    def get_systeminfo(instrument, appname):
        systeminfo = []
        s_splitgroup = instrument.windows()[0].group()[0].splitgroup()[0]
     
        datalist = s_splitgroup.splitgroup()[0].scollarea()[0].table()[0].row()
        for i in datalist:
            data = i.text()
            if data[1].AXValue == appname:
                for j in data:
                    systeminfo.append(j.AXValue)
                return systeminfo
                
        
    def get_graphinfo(instrument):
        graphlist = []
        g_splitgroup = instrument.windows()[0].group()[0].splitgroup()[0]
        
        datalist = g_splitgroup.splitgroup()[0].scollarea()[0].table()[0].row()
        for i in datalist:
            data = i.text()
            values = []
            for j in data:
                values.append(j.AXValue)
            graphlist.append(values)
        # 如果不是从0开始，则逆序    
        if datalist[0].text()[0].AXValue != '0':
            graphlist.reverse()
        
        return graphlist


    def get_appref(bundleid):
        instrument = atomac.getAppRefByBundleId(bundleid)
        return instrument
    
    
    # 开始instruments记录
    def start_record():
        # atomac.launchAppByBundleId("com.apple.dt.Instruments")
        # time.sleep(2)
        instrument = atomac.getAppRefByBundleId("com.apple.dt.Instruments")
        recordbutton = instrument.windows()[0].toolbars()[0].checkboxs()[0]
        recordbutton.Press()
        return instrument
        
     
    # 停止记录
    def stop_record():
        start_record()
           
    
# windows上安装atomac失败，便于调试其他函数
else:
    def start_record():
        pass
    def stop_record():
        pass
    def get_systeminfo(instrument, appname):
        return ['1','2','3']
    def get_graphinfo(instrument):
        return [['1','2','3']]
    def get_appref(bundleid):
        pass
    def jump_page(a, b):
        pass
        
if __name__ == "__main__":
    #print(get_graphinfo("aa"))
    instrument = atomac.getAppRefByBundleId("com.apple.dt.Instruments")
    print(get_systeminfo(instrument, "test"))
        
    

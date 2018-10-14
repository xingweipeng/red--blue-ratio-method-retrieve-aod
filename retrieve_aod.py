# -*- coding: utf-8 -*-
"""
Created on Thu May 17 16:59:41 2018

@author: xwp
"""

import correct
import bisect
#import time
#time_start=time.time()

def retrive(blue_app,red_app,asol,azi,avis,rb):#the parametres including blue/red apparent reflectance,three sun-satellite geometry angles,the ratio of surface reflectance
    ratio_list, aot_list, residua_list = [], [], []
    aot=0.01
    while aot < 2.5:
        blue_sur = correct.blue(blue_app, asol, azi, avis, aot)
        red_sur = correct.red(red_app, asol, azi, avis, aot)
        # print "blue=",blue_sur,"red=",red_sur
        if blue_sur > 0 and red_sur > 0:
            # residua=rb*red_sur-blue_sur#if residul >0 then interpolate aot
            ratio = red_sur / blue_sur
            ratio_residual = ratio - rb
            ratio_list.append(ratio)
            residua_list.append(ratio_residual)
            aot_list.append(aot)
            # print aot,ratio,ratio_residual
        aot = aot + 0.05#以0.05步长递增，步长越小耗时越长
    # print aot_list,'\n',ratio_list,'\n',residua_list
    if  len( ratio_list)>1:#条件判断，最小残差小于0，最大残差大于0
        if max(ratio_list) > rb and min(ratio_list) < rb:#条件判断，运算得出的ratio范围
            # rb_up_pos = bisect.bisect_left(residua_list, 0)
            # rb_down_pos = rb_up_pos - 1  # the position of  boundry of ratio
            t = 0
            while 1 > 0:#a new method for searching mid point
                left = residua_list[t]
                right = residua_list[t + 1]
                if left * right < 0:
                    rb_up_pos = t + 1
                    rb_down_pos = t
                    break
                t = t + 1
            aod_down_up_value = [aot_list[rb_down_pos], aot_list[rb_up_pos]]
            rb_interval = abs(ratio_list[rb_down_pos] - ratio_list[rb_up_pos])
            aod_retrive = aod_down_up_value[0] * abs(rb - ratio_list[rb_up_pos])/rb_interval+aod_down_up_value[1]*abs(rb-ratio_list[rb_down_pos])/rb_interval
            #print aod_retrive
        elif rb<min(ratio_list):
            aod_retrive = -0.1
        elif rb>max(ratio_list):
            aod_retrive = -2.5

    else:
        aod_retrive = -99
    return aod_retrive


# -*- coding: utf-8 -*-
"""
Created on Thu May 17 16:59:41 2018

@author: xwp
"""

import acr_blue
import acr_red

#the input vector contains [blue_app geometry aod]
def blue(blue_app,sun_zen,re_azi,sat_zen,aot):
    geometry_aod=[sun_zen,re_azi,sat_zen,aot]
    parametre=acr_blue.look_up_interpolat(geometry_aod)
    path, tgm, tt, sa = parametre[0], parametre[1], parametre[2], parametre[3]
    y=blue_app/tgm/tt-path/tt
    acref = y/(1+y * sa)
    return acref


def red(red_app,sun_zen,re_azi,sat_zen,aot):
    geometry_aod=[sun_zen,re_azi,sat_zen,aot]
    parametre=acr_red.look_up_interpolat(geometry_aod)
    path, tgm, tt, sa = parametre[0], parametre[1], parametre[2], parametre[3]
    y=red_app/tgm/tt-path/tt
    acref = y/(1+y * sa)
    return acref

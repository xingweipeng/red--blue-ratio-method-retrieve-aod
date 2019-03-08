# -*- coding: utf-8 -*-
import numba as nb
import datetime
import numpy as np
import bisect
import math
import os
import datetime
import  time
from numba import jit
x1_dims,x2_dims,x3_dims=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85],[0.01,15,30,45,60,75,90,105,120,135,150,165,180],[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85]#三个维度分别是sun_zenith，relative_azimuth，sat_zenith
x4_dims = [0.001, 0.05, 0.1, 0.3, 0.5, 0.8, 1, 1.2, 1.5, 1.8, 2, 2.5]  # aod维度
x1_dims=np.array(x1_dims)
x2_dims=np.array(x2_dims)
x3_dims=np.array(x3_dims)
x4_dims=np.array(x4_dims)
martix_blue = np.loadtxt('lut_blue_whole.txt', dtype=float)  # 输入的蓝查找表
blue_vector = martix_blue[:, 0:4]
blue_vector = blue_vector.tolist()
blue_tgm_lut = martix_blue[:, 4:5]  # gas透过率
#blue_tgm_lut = blue_tgm_lut.tolist()
blue_path_lut = martix_blue[:, 7:8]  # 输出值程辐射
#blue_path_lut = blue_path_lut.tolist()
blue_tt_lut = martix_blue[:, 5:6]  # 总透过率
#blue_tt_lut = blue_tt_lut.tolist()
blue_sa_lut = martix_blue[:, 6:7]  # 半球反照率
#blue_sa_lut = blue_sa_lut.tolist()

martix_red = np.loadtxt('lut_red_whole.txt', dtype=float)  # 输入的蓝查找表
red_vector = martix_red[:, 0:4]
red_tgm_lut = martix_red[:, 4:5]  # gas透过率
red_path_lut = martix_red[:, 7:8]  # 输出值程辐射
red_tt_lut = martix_red[:, 5:6]  # 总透过率
red_sa_lut = martix_red[:, 6:7]  # 半球反照率

@jit(nopython=True)
def blue_look_up_interpolat(in_blue_vector):
    #in_blue_vector=np.array(in_blue_vector)
    x1_up_pos = np.searchsorted(x1_dims, in_blue_vector[0])
    x1_down_pos = x1_up_pos - 1
    x2_up_pos = np.searchsorted(x2_dims, in_blue_vector[1])
    x2_down_pos = x2_up_pos - 1
    x3_up_pos = np.searchsorted(x3_dims, in_blue_vector[2])
    x3_down_pos = x3_up_pos - 1
    x4_up_pos = np.searchsorted(x4_dims, in_blue_vector[3])
    x4_down_pos = x4_up_pos - 1
    x1_down_up_pos = [x1_dims[x1_down_pos], x1_dims[x1_up_pos]]  # 第一维度上下界的值
    x1_down_up_pos=np.array(x1_down_up_pos)
    x2_down_up_pos = [x2_dims[x2_down_pos], x2_dims[x2_up_pos]]  # 第二维度上下界的值
    x2_down_up_pos=np.array(x2_down_up_pos)
    x3_down_up_pos = [x3_dims[x3_down_pos], x3_dims[x3_up_pos]]  # 第三维度上下界的值
    x3_down_up_pos=np.array(x3_down_up_pos)
    x4_down_up_pos = [x4_dims[x4_down_pos], x4_dims[x4_up_pos]]  # 第四维度上下界的值
    x4_down_up_pos=np.array(x4_down_up_pos)
    num=0
    blue_path_interp_value,blue_tgm_interp_value,blue_blue_sa_interp_value,sa_interp_value=0,0,0,0
    for i in [0, 1]:
        for j in [0, 1]:
            for k in [0, 1]:
                for h in [0, 1]:
                   # index_pos = blue_vector.index([x1_down_up_pos[i], x2_down_up_pos[j], x3_down_up_pos[k], x4_down_up_pos[h]])  # 临近向量的index
                    temp_vector=[x1_down_up_pos[i], x2_down_up_pos[j], x3_down_up_pos[k], x4_down_up_pos[h]]
                    x1,x2,x3,x4= temp_vector[0],temp_vector[1],temp_vector[2],temp_vector[3]
                    L1,L2,L3,L4= np.where(x1_dims == x1),np.where(x2_dims == x2),np.where(x3_dims == x3),np.where(x4_dims == x4)
                    index_pos = L1[0] * 12 * 13 * 18 + L3[0] * 12 * 13 + L2[0] * 12 + L4[0]
                    index_poso=index_pos[0]


                    # neighbour[num]=y_lut[index_pos]*abs(in_blue_vector[1]-x1_down_up_pos[i-1])*
                    weight_1 = abs(in_blue_vector[0] - x1_down_up_pos[i - 1]) / 5.0
                    weight_2 = abs(in_blue_vector[1] - x2_down_up_pos[j - 1]) / 15.0
                    weight_3 = abs(in_blue_vector[2] - x3_down_up_pos[k - 1]) / 5.0
                    weight_4 = abs(in_blue_vector[3] - x4_down_up_pos[h - 1]) / abs(x4_dims[x4_up_pos] - x4_dims[x4_down_pos])

                    tgm_value = weight_1 * weight_2 * weight_3 * weight_4 * blue_tgm_lut[index_poso][0]
                    path_value = weight_1 * weight_2 * weight_3 * weight_4 * blue_path_lut[index_poso][0]
                    tt_value = weight_1 * weight_2 * weight_3 * weight_4 * blue_tt_lut[index_poso][0]
                    sa_value = weight_1 * weight_2 * weight_3 * weight_4 * blue_sa_lut[index_poso][0]
                    blue_path_interp_value+=path_value
                    blue_tgm_interp_value+=tgm_value
                    blue_blue_sa_interp_value+=tt_value
                    sa_interp_value+=sa_value
    return blue_path_interp_value, blue_tgm_interp_value,blue_blue_sa_interp_value, sa_interp_value  # 小数点后三位

@jit(nopython=True)
def red_look_up_interpolat(in_red_vector):
    #in_red_vector=np.array(in_red_vector)
    x1_up_pos = np.searchsorted(x1_dims, in_red_vector[0])
    x1_down_pos = x1_up_pos - 1
    x2_up_pos = np.searchsorted(x2_dims, in_red_vector[1])
    x2_down_pos = x2_up_pos - 1
    x3_up_pos = np.searchsorted(x3_dims, in_red_vector[2])
    x3_down_pos = x3_up_pos - 1
    x4_up_pos = np.searchsorted(x4_dims, in_red_vector[3])
    x4_down_pos = x4_up_pos - 1
    x1_down_up_pos = [x1_dims[x1_down_pos], x1_dims[x1_up_pos]]  # 第一维度上下界的值
    x1_down_up_pos=np.array(x1_down_up_pos)
    x2_down_up_pos = [x2_dims[x2_down_pos], x2_dims[x2_up_pos]]  # 第二维度上下界的值
    x2_down_up_pos=np.array(x2_down_up_pos)
    x3_down_up_pos = [x3_dims[x3_down_pos], x3_dims[x3_up_pos]]  # 第三维度上下界的值
    x3_down_up_pos=np.array(x3_down_up_pos)
    x4_down_up_pos = [x4_dims[x4_down_pos], x4_dims[x4_up_pos]]  # 第四维度上下界的值
    x4_down_up_pos=np.array(x4_down_up_pos)
    num=0
    red_path_interp_value,red_tgm_interp_value,red_red_sa_interp_value,sa_interp_value=0,0,0,0
    for i in [0, 1]:
        for j in [0, 1]:
            for k in [0, 1]:
                for h in [0, 1]:
                    temp_vector=[x1_down_up_pos[i], x2_down_up_pos[j], x3_down_up_pos[k], x4_down_up_pos[h]]
                    x1,x2,x3,x4= temp_vector[0],temp_vector[1],temp_vector[2],temp_vector[3]
                    L1,L2,L3,L4= np.where(x1_dims == x1),np.where(x2_dims == x2),np.where(x3_dims == x3),np.where(x4_dims == x4)
                    index_pos = L1[0] * 12 * 13 * 18 + L3[0] * 12 * 13 + L2[0] * 12 + L4[0]
                    index_poso=index_pos[0]
                    weight_1 = abs(in_red_vector[0] - x1_down_up_pos[i - 1]) / 5.0
                    weight_2 = abs(in_red_vector[1] - x2_down_up_pos[j - 1]) / 15.0
                    weight_3 = abs(in_red_vector[2] - x3_down_up_pos[k - 1]) / 5.0
                    weight_4 = abs(in_red_vector[3] - x4_down_up_pos[h - 1]) / abs(x4_dims[x4_up_pos] - x4_dims[x4_down_pos])


                    tgm_value = weight_1 * weight_2 * weight_3 * weight_4 * red_tgm_lut[index_poso][0]
                    path_value = weight_1 * weight_2 * weight_3 * weight_4 * red_path_lut[index_poso][0]
                    tt_value = weight_1 * weight_2 * weight_3 * weight_4 * red_tt_lut[index_poso][0]
                    sa_value = weight_1 * weight_2 * weight_3 * weight_4 * red_sa_lut[index_poso][0]
                    red_path_interp_value+=path_value
                    red_tgm_interp_value+=tgm_value
                    red_red_sa_interp_value+=tt_value
                    sa_interp_value+=sa_value
    return red_path_interp_value, red_tgm_interp_value,red_red_sa_interp_value, sa_interp_value  #f


@jit(nopython=True)
def blue_acr(blue_app, sun_zen, re_azi, sat_zen, aot):
    geometry_aod = [sun_zen, re_azi, sat_zen, aot]
    geometry_aod = np.array(geometry_aod)
    parametre= blue_look_up_interpolat(geometry_aod)
    path, tgm, tt, sa = parametre[0], parametre[1], parametre[2], parametre[3]
    y = blue_app / tgm / tt - path / tt
    blue_acref = y / (1 + y * sa)
    return blue_acref

@jit(nopython=True)
def red_acr(red_app, sun_zen, re_azi, sat_zen, aot):
    geometry_aod = [sun_zen, re_azi, sat_zen, aot]
    geometry_aod = np.array(geometry_aod)
    parametre= red_look_up_interpolat(geometry_aod)
    path, tgm, tt, sa = parametre[0], parametre[1], parametre[2], parametre[3]
    y = red_app / tgm / tt - path / tt
    red_acref = y / (1 + y * sa)
    return red_acref


@jit(nopython=True)	
def retrive(blue_app,red_app,asol,azi,avis,rb):#输入参数包括蓝、红表观反射率、三个角度、红蓝地表比值

	ratio_list, aot_list, residua_list = [], [], []#三个空列表
	aot=0.001
	aot_max=2.5
	aot_min=0.001
	ratio_pre_residual=0
	#max_aod_rb=correct.red(red_app, asol, azi, avis, aot_max)/correct.blue(blue_app, asol, azi, avis, aot_max)
	#min_aod_rb=correct.red(red_app, asol, azi, avis, aot_min)/correct.blue(blue_app, asol, azi, avis, aot_min)
	m_number=-1
	while aot < 2.5:
		blue_sur = blue_acr(blue_app, asol, azi, avis, aot)
		red_sur = red_acr(red_app, asol, azi, avis, aot)
		if blue_sur <0:
			aod_retrive = -1#出现异常值，对该像素不再反演
			break
		else:
			ratio = red_sur / blue_sur
			ratio_residual =ratio - rb
			ratio_sign=ratio_pre_residual*ratio_residual
			#print ratio,ratio_pre_residual,ratio_sign,m_number
			ratio_pre_residual=ratio_residual
			ratio_list.append(ratio)
			residua_list.append(ratio_residual)
			aot_list.append(aot)
			if ratio_sign<0:
				rb_up_pos =m_number + 1
				rb_down_pos = m_number
				aod_down_up_value = [aot_list[rb_down_pos], aot_list[rb_up_pos]]
				rb_interval = abs(ratio_list[rb_down_pos] - ratio_list[rb_up_pos])
				aod_retrive = aod_down_up_value[0] * abs(rb - ratio_list[rb_up_pos])/rb_interval+aod_down_up_value[1]*abs(rb-ratio_list[rb_down_pos])/rb_interval
				break
		aot = aot + 0.1#以0.05步长递增，步长越小耗时越长
		m_number=m_number+1

	else:aod_retrive = -99#出现异常值，对该像素不再反演
	return aod_retrive	
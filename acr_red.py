# -*- coding: utf-8 -*-
"""
Created on Thu May 17 16:59:41 2018

@author: xwp
"""
import numpy as np
import bisect
x1_dims,x2_dims,x3_dims=[55,60,65,70,75,80,85],[0.01,15,30,45,60,75,90],[30,35,40,45,50,55,60]#三个维度分别是sun_zenith，relative_azimuth，sat_zenith
x4_dims=[0.001,0.05,0.1,0.3,0.5,0.8,1,1.2,1.5,1.8,2,2.5]#dim=11,aod维度
martix=np.loadtxt('lut_red.txt',dtype=float)#输入的蓝查找表
x1_dim,x2_dim,x3_dim,x4_dim=7,7,6,12#这个其实没用
vector=[]
tgm_lut,path_lut,tt_lut,sa_lut=[],[],[],[]#对应大气校正的四个参数
for i in range(0,len(martix)):
    vector.append([martix[i,0],martix[i,1],martix[i,2],martix[i,3]])#输入的向量组包含三个角度和aod
    tgm_lut.append(martix[i,4])#gas透过率
    path_lut.append(martix[i,7])#输出值程辐射
    tt_lut.append(martix[i,5])#总透过率
    sa_lut.append(martix[i,6])#半球反照率
    


#neighbour=[]
#def look_up_interpolat(in_vector):
def look_up_interpolat(in_vector):
	x1_up_pos=bisect.bisect_left(x1_dims,in_vector[0])
	x1_down_pos=x1_up_pos-1
	x2_up_pos=bisect.bisect_left(x2_dims,in_vector[1])
	x2_down_pos=x2_up_pos-1
	x3_up_pos=bisect.bisect_left(x3_dims,in_vector[2])
	x3_down_pos=x3_up_pos-1
	x4_up_pos=bisect.bisect_left(x4_dims,in_vector[3])
	x4_down_pos=x4_up_pos-1
	x1_down_up_pos=[x1_dims[x1_down_pos],x1_dims[x1_up_pos]]#第一维度上下界的值
	x2_down_up_pos=[x2_dims[x2_down_pos],x2_dims[x2_up_pos]]#第二维度上下界的值
	x3_down_up_pos=[x3_dims[x3_down_pos],x3_dims[x3_up_pos]]#第三维度上下界的值
	x4_down_up_pos=[x4_dims[x4_down_pos], x4_dims[x4_up_pos]]# 第四维度上下界的值

	num=0
	path_interp_value,tgm_interp_value,tt_interp_value,sa_interp_value=[],[],[],[]
	for i in [0,1]:
	 for j in [0,1]:
	  for k in [0,1]:
	   for h in [0,1]:
		   index_pos=vector.index([x1_down_up_pos[i],x2_down_up_pos[j],x3_down_up_pos[k],x4_down_up_pos[h]])#临近向量的index
		   #neighbour[num]=y_lut[index_pos]*abs(in_vector[1]-x1_down_up_pos[i-1])*
		   weight_1=abs(in_vector[0]-x1_down_up_pos[i-1])/5.0
		   weight_2=abs(in_vector[1]-x2_down_up_pos[j-1])/15.0
		   weight_3=abs(in_vector[2]-x3_down_up_pos[k-1])/5.0
		   weight_4=abs(in_vector[3]-x4_down_up_pos[h-1])/abs(x4_dims[x4_up_pos]-x4_dims[x4_down_pos])
		  
		   #print weight_1,weight_2,weight_3,weight_4,weight_1*weight_2*weight_3*weight_4,'index_pos:',index_pos 
		   tgm_value=weight_1*weight_2*weight_3*weight_4*tgm_lut[index_pos]
		   path_value=weight_1*weight_2*weight_3*weight_4*path_lut[index_pos]
		   tt_value=weight_1*weight_2*weight_3*weight_4*tt_lut[index_pos]
		   sa_value=weight_1*weight_2*weight_3*weight_4*sa_lut[index_pos]
		   
		   path_interp_value.append(path_value)
		   tgm_interp_value.append(tgm_value)
		   tt_interp_value.append(tt_value)
		   sa_interp_value.append(sa_value)
		   num=num+1
	return sum(path_interp_value),sum(tgm_interp_value),sum(tt_interp_value),sum(sa_interp_value)#小数点后三位
   

#print look_up_interpolat([80,15,30.1,0.1])
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 16:59:41 2018

@author: xwp
"""
import numpy as np
import bisect
x1_dims,x2_dims,x3_dims=[55,60,65,70,75,80,85],[0.01,15,30,45,60,75,90],[30,35,40,45,50,55,60]#three demison including sun_zenith，relative_azimuth，sat_zenith
x4_dims=[0.001,0.05,0.1,0.3,0.5,0.8,1,1.2,1.5,1.8,2,2.5]
martix=np.loadtxt('lut_blue.txt',dtype=float)#input LUT of blue band
x1_dim,x2_dim,x3_dim,x4_dim=7,7,6,12
vector=[]
tgm_lut,path_lut,tt_lut,sa_lut=[],[],[],[]#four parametre for atmosphere correction
for i in range(0,len(martix)):
    vector.append([martix[i,0],martix[i,1],martix[i,2],martix[i,3]])
    tgm_lut.append(martix[i,4])#global gas transmittance
    path_lut.append(martix[i,7])#top reflectance
    tt_lut.append(martix[i,5])#total transmittance
    sa_lut.append(martix[i,6])#sing. scat. albedo
    


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
	x1_down_up_pos=[x1_dims[x1_down_pos],x1_dims[x1_up_pos]]#the boundry of a dimension
	x2_down_up_pos=[x2_dims[x2_down_pos],x2_dims[x2_up_pos]]
	x3_down_up_pos=[x3_dims[x3_down_pos],x3_dims[x3_up_pos]]
	x4_down_up_pos=[x4_dims[x4_down_pos], x4_dims[x4_up_pos]]

	num=0
	path_interp_value,tgm_interp_value,tt_interp_value,sa_interp_value=[],[],[],[]
	for i in [0,1]:
	 for j in [0,1]:
	  for k in [0,1]:
	   for h in [0,1]:
		   index_pos=vector.index([x1_down_up_pos[i],x2_down_up_pos[j],x3_down_up_pos[k],x4_down_up_pos[h]])#the nearest index
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
	return sum(path_interp_value),sum(tgm_interp_value),sum(tt_interp_value),sum(sa_interp_value)
   

#print look_up_interpolat([80,15,30.1,0.1])
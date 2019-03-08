# -*- coding: utf-8 -*-
import  numpy as np
import retrieve_numba
import math
import os
import datetime

starttime = datetime.datetime.now()
blue=np.loadtxt('selet_b1.txt')#load band1 albedo
red=np.loadtxt('selet_b3.txt')#load band3 albedo
sun_zen=np.loadtxt('selet_soz.txt')
sat_zen=np.loadtxt('selet_saz.txt')
razi=np.loadtxt('selet_raz.txt')
ratio=np.loadtxt('selet_rb.txt')#load ratio data
path=os.getcwd()
splite=path.split('\\')
folder=splite[2]
outputfilename='aod_output'
i=0
aot_result=[]
falseline=[]
print ('像元数目=',len(blue))
while i<len(ratio):
    blueapp,redapp,asol=blue[i],red[i],sun_zen[i]
    azi,avis,rb=razi[i],sat_zen[i],ratio[i]
    print ('number=',i)  
    print(blueapp,redapp,asol,azi,avis,rb),'number=',i
    aot=retrieve_numba.retrive(blueapp,redapp,asol,azi,avis,rb)#obtain AOD
    aot_result.append(aot)
    print ('aot=',aot)
    i=i+1



#print aot_result
np.savetxt(outputfilename,aot_result,fmt='%1.4f')

endtime = datetime.datetime.now()

print ('消耗的时间',endtime - starttime)
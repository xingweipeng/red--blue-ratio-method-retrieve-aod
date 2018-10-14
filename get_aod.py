import  numpy as np
import retrieve_aod
import math
#input=np.loadtxt('invector_1.txt')
blue=np.loadtxt('blue.txt')
red=np.loadtxt('red.txt')
sun_zen=np.loadtxt('sun_zenith.txt')
sat_zen=np.loadtxt('sat_zenith.txt')
razi=np.loadtxt('relative_azi.txt')
ratio=np.loadtxt('rb.txt')
i=0
aot_result=[]
falseline=[]
while i<len(blue):
    blueapp,redapp,asol=blue[i],red[i],sun_zen[i]
    azi,avis,rb=razi[i],sat_zen[i],ratio[i]
	
    # if math.isnan(rb)==True or math.isnan(blueapp)==True or  math.isnan(redapp)==True:
	  # falsepos=i
	  # falseline.append(falsepos)
      # print 'wrong'
    print(blueapp,redapp,asol,azi,avis,rb),'number=',i
    aot=retrieve_aod.retrive(blueapp,redapp,asol,azi,avis,rb)
    aot_result.append(aot)
    print 'aot=',aot
    i=i+1



#print aot_result
np.savetxt("aot_result.txt",aot_result,fmt='%1.4f')
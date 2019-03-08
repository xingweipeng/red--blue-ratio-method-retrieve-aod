# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from mpl_toolkits.basemap import Basemap
import gdal
import numpy as np
import matplotlib
import  time
import  os

rootpath=os.getcwd()

def add_map(rows,columns):#the rows and columns need to be set as 726,1120
    m = Basemap(projection='cyl', llcrnrlat=17.5, llcrnrlon=73, urcrnrlat=53.9, urcrnrlon=136.1)#lowest and highest  latitude, lowest and highest longititude
    lons, lats = m.makegrid(rows, columns)
    x, y = m(lons, lats)
    shp_path=rootpath+'\\shapfile\\china'
    m.readshapefile(shp_path, 'china.shp', color='grey')#input china shapfile
    m.drawparallels(np.arange(50., 15, -10.), labels=[1, 0, 0, 0],dashes=[1,8],fontsize=10)
    m.drawmeridians(np.arange(60., 140., 10.), labels=[0, 0, 0, 1],dashes=[1,8],fontsize=10)





def main():
    aot_file=np.loadtxt('aod_output')
    x=np.loadtxt('clear_x.txt',dtype=int)
    x=x-np.ones(len(x))
    x=x.astype(int)
    y= np.loadtxt('clear_y.txt',dtype=int)
    y=y - np.ones(len(y))
    y=y.astype(int)
    blank_mask=np.zeros([726,1120])
    n=0
    for t in aot_file:
        blank_mask[x[n],y[n]]=t
        n=n+1
    print ('n=',n)
    aot_values= blank_mask
    aot_values=aot_values.astype(float)
    aot_values[aot_values <= 0] =np.nan

    fig = plt.figure()
    plt_ax = plt.subplot(111, projection=ccrs.PlateCarree())
    aot_values = aot_values[::-1]
    extent = [79.967, 136.0573, 17.4946, 53.8614]
    cs=plt_ax.imshow(aot_values, transform=ccrs.PlateCarree(), vmin=0, vmax=1, extent=extent, cmap='RdYlBu_r')
    add_map(726, 1120)

#get the boundary of figure
    left, bottom, width, height = plt_ax.get_position().bounds
    cba_position = fig.add_axes([width/4, bottom - 0.06, width/1.5, 0.025])
    cbar = fig.colorbar(cs, cax=cba_position, orientation='horizontal', extend='both')
    cbar.set_label('AOD at 550nm', size=16, family='Times New Roman')
    plt.show()



if __name__ == '__main__':
        main()

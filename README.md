# red--blue-ratio-method-retrieve-aod
A method to retrieve aod from Himawari-8 satellite's visible bands.It is based on the ratio of  surface reflectance ratio,similiar to the method suggested in Shobha Kondragunta's paper"An enhanced VIIRS aerosol optical thickness (AOT) retrieval algorithm over land using a global surface reflectance ratio database".
Lut_red_whole.txt,lut_blue_whole.txt are lookup tables derived from 6s model,whose columns consist of sun_zenith, relative_azimuth, sat_zenith, and 4 parametres to correct atmosphericly.rb.txt is the ratio data of surface reflectance of red band and blue band,which are obtained from MOD09.red.txt and blue.txt are apparent reflectance data from MODIS red band(620-670 nm)  and blue band(459-479 nm).

Numba, matplotlib and numpy library are needed to install. pre_process_for_H8.m is used for pre-process.retrieve_numba.py is the library of retrievel library. get_aod.py is used to retrieve AOD values.draw_AOD_map.py is to show AOD map.
Sample himawari-8 data is in test-data folder.

Compared with old version, this one can retrieve AOD at a very high speed on ordinary PC with the help of numba.
If you want more detail information ,contact me through e-mail 919487406@qq.com.

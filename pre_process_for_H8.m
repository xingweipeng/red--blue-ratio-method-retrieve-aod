load('.\test data\ancillary data\china_region.mat')% this data is to indicate the pixel located in China
load('.\test data\ancillary data\ratio_dataset.mat')%the red-blue ratio dataset
load('.\test data\ancillary data\land_flag.mat');%this data is to indicate land/water flag
load('.\test data\ancillary data\elevation.mat');%this data  represent elevation, the unit is meter


orign_H8_name='.\test data\Himawari-8_albedo_parameter.nc'%input the name of albedo file
H8_cloud_name='.\test data\Himawari-8_cloud_parameter.nc'%input the name of cloud product file


albedo_01=ncread(orign_H8_name,'albedo_01');%read abledo at band1. it's blue band
albedo_03=ncread(orign_H8_name,'albedo_03');%read abledo at band3. it's red band
albedo_01=albedo_01.';albedo_03=albedo_03.';
SOZ=ncread(orign_H8_name,'SOZ');%solar zenith angle
SOZ=SOZ.';
cos_SOZ=cos(SOZ/180*pi);
SAZ=ncread(orign_H8_name,'SAZ');%satellite zenith angle
SAZ=SAZ.';
SAA=ncread(orign_H8_name,'SAA');%satellite azimuth angle
SAA=SAA.';
SOA=ncread(orign_H8_name,'SOA');%solar azimuth angle
SOA=SOA.';
reflectance_01=albedo_01./cos_SOZ;%convert albedo into reflectance
reflectance_03=albedo_03./cos_SOZ;
relative_azimuth=abs(SOA-SAA);
china_reflectance_01=reflectance_01(125:850,1:1120);%choose the rows and columns 
china_reflectance_03=reflectance_03(125:850,1:1120);
china_soz=SOZ(125:850,1:1120);
china_saz=SAZ(125:850,1:1120);
china_raz=relative_azimuth(125:850,1:1120);
%%%%%%%%%%%%%
QA=ncread(H8_cloud_name,'QA');QA=QA.';%extract cloud mask ID
qa=dec2bin(QA);
QA=qa-'0';
cloud_phase=QA(:,12)*10+QA(:,13);%Cloud Retrieval Phase Flag: 00=Clear, 01=Liquid Water, 10=Mixed or Uncertain, 11=Ice;
cloud_phase=cloud_phase.';
phase=reshape(cloud_phase,2401,2401);
china_cloud_phase=phase(125:850,1:1120);
%%%%%%%%%%%%%%
 %land_flag==11 is the indicatior of land piexl£¬
 %only the pixel with land_flag==11 SOZ<80 , china_region_mask==1 and
 %elevation<2000  would be chosen, in order to reduce uncertainty
 [clear_x,clear_y]=find(china_cloud_phase==0&land_flag==11&china_soz<80&china_region_mask==1&elevation<2000);%clear_x and clear_y record the position of chosen pixel 
 t=1;
 %extract chosen pixels based on clear_x and clear_y list
 x=clear_x;y=clear_y;
 while t<=length(x)
     selet_b1(t,1)=china_reflectance_01(x(t,1),y(t,1));
     selet_b3(t,1)=china_reflectance_03(x(t,1),y(t,1));
     selet_soz(t,1)=china_soz(x(t,1),y(t,1));
     selet_saz(t,1)=china_saz(x(t,1),y(t,1));
     selet_raz(t,1)=china_raz(x(t,1),y(t,1));
     t=t+1;
 end
 
for t=1:length(x)
if selet_raz(t,1)>180
selet_raz(t,1)=360-selet_raz(t,1);
end
if selet_raz(t,1)<1
selet_raz(t,1)=1;
end
end
%%%%%%
leng=length(clear_x);



%convert the value of pixel to .txt format
for i=1:leng
ratiolist(i,1)=rb(clear_x(i,1),clear_y(i,1));
end

fid1=fopen('clear_x.txt','w');

for i=1:leng
fprintf(fid1,'%4.3f',clear_x(i,1));
fprintf(fid1,'\n');
end
fclose(fid1)
fid1=fopen('clear_y.txt','w');
for i=1:leng
fprintf(fid1,'%4.3f',clear_y(i,1));
fprintf(fid1,'\n');
end
fclose(fid1)

fid1=fopen('selet_b1.txt','w');
for i=1:leng
fprintf(fid1,'%4.3f',selet_b1(i,1));
fprintf(fid1,'\n');
end
fclose(fid1)

fid1=fopen('selet_b3.txt','w');
for i=1:leng
fprintf(fid1,'%4.3f',selet_b3(i,1));
fprintf(fid1,'\n');
end
fclose(fid1)



fid1=fopen('selet_soz.txt','w');
for i=1:leng
fprintf(fid1,'%4.3f',selet_soz(i,1));
fprintf(fid1,'\n');
end
fclose(fid1)

fid1=fopen('selet_saz.txt','w');
for i=1:leng
fprintf(fid1,'%4.3f',selet_saz(i,1));
fprintf(fid1,'\n');
end
fclose(fid1)

fid1=fopen('selet_raz.txt','w');
for i=1:leng
fprintf(fid1,'%4.3f',selet_raz(i,1));
fprintf(fid1,'\n');
end
fclose(fid1)

fid1=fopen('selet_rb.txt','w');
for i=1:leng
fprintf(fid1,'%4.3f',ratiolist(i,1));
fprintf(fid1,'\n');
end
fclose(fid1)


clear selet_b1
clear selet_b3
clear selet_raz
clear selet_saz
clear selet_soz
clear ratiolist

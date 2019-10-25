# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:42:37 2019

@author: Sarve
"""
import os
import numpy as np
from os import listdir
from PIL import Image
  
path="C:/DL_Dataset/Project_data"
path2="C:/DL_Dataset/NumpyImages_Project/"

for r, d, f in os.walk(path):
    direc=d
    break

np_images=[]

for d in direc:
    print(d)
    dic={}
    sub=[a for a in listdir(path+"/"+d)]
    flag=0
    for ele in sub:
        mypath = path+"/"+d+"/"+ele+"/"
        onlyfiles = [mypath+f for f in listdir(mypath)]
        temp=[]
        for addr in onlyfiles:
            temp.append(np.array(Image.open(addr)))   
        if len(temp)>0:
            if ele[0].lower()=='f':
                dic['father']=temp
            elif ele[0].lower()=='m':
                dic['mother']=temp
            elif ele.lower()=='child_male':
                dic['child']=temp    
                dic['gender']=np.zeros((temp[0].shape))
            elif ele.lower()=='child_female':
                dic['child']=temp    
                dic['gender']=np.ones((temp[0].shape))    
        else:
            flag=1
            break
        
    if flag!=1:
        for x in dic['father']:
            for y in dic['mother']:
                for z in dic['child']:
                    np_images.append([x,y,z,dic['gender']])


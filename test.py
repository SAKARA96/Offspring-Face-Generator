# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 22:32:31 2019

@author: Sarve
"""

import pandas as pd
import numpy as np
import os
import shutil
"""
1. go in folder Folder F0001-F1000
    counter=0
2. read mid.csv
3. search for 1 in 1,1 to end,:-2
4: get 2 indexes for 1 in the row i: 1 to end 
5: create a new folder in diff location for row with above condition:
end

"""
#path='F'
#for i in range(1,1001):
#    
#    
path="C:/FIDs_NEW"
path2="C:/DL_Dataset"

for r, d, f in os.walk(path):
    direc=d
    break

for d in direc:
    temp=path+"/"+d+"/mid.csv"
    print(d)
    print("---------------------------------------------")
    df=pd.read_csv(temp)
    df=df.to_numpy()
    counter=0
    for i in range(len(df)):
        parent=[]
        for j in range(1,len(df[i])):
            if df[i][j]==1:
                parent.append(j-1)
        if len(parent)==2:
            if (df[parent[0]][-2].lower()!=df[parent[1]][-2].lower()):
                counter+=1
                output=path2+"/"+d+"_"+str(counter)
                print(output)
                if(df[parent[0]][-2].lower() == "male"):
                    shutil.copy(path+"/"+d+"/MID"+str(parent[0]+1),output+"/Father")
                    shutil.copy(path+"/"+d+"/MID"+str(parent[1]+1),output+"/Mother")
                else:
                    shutil.copy(path+"/"+d+"/MID"+str(parent[0]+1),output+"/Mother")
                    shutil.copy(path+"/"+d+"/MID"+str(parent[1]+1),output+"/Father")
                shutil.copy(path+"/"+d+"/MID"+str(i+1),output+"/Child_"+df[i][-2].lower())
    
    break
                #copy 
                
                
#                print(i,parent[0],parent[1])
                
                
    

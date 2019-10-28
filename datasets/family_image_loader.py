from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import fnmatch
import glob

import numpy as np

from os import listdir
from PIL import Image


class Dataset(object):

    def __init__(self, ids, name='default',
                 h=224, w=224, data_augmentation=False,
                 centor_crop=True,
                 max_examples=None, is_train=True):
        self._ids = list(ids)
        self.name = name
        self.is_train = is_train
        self.h = h
        self.w = w
        #self.data_augmentation = data_augmentation
        #self.center_crop = centor_crop

        #if max_examples is not None:
        #    self._ids = self._ids[:max_examples]

    '''
    For a given family_id( = The directory of family itself),
    it returns dict of key = fam_id_imgNo and value= encoded images [This is a 4 layer tuple]
    for f*m*c images
    '''
    def get_data(self, dir_id):
        np_images={}
        
        dic={}
        sub=[a for a in listdir(path+"/"+dir_id)]
        flag=0

        for ele in sub:
            mypath = path+"/"+dir_id+"/"+ele+"/"
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
        fid = 1

        if flag!=1:
            for x in dic['father']:
                for y in dic['mother']:
                    for z in dic['child']:
                        np_images[dir_id+'_'+str(fid)] = [x,y,z,dic['gender']]
                        fid += 1
        return np_images

        

    @property
    def ids(self):
        return self._ids

    def __len__(self):
        return len(self.ids)

    def __repr__(self):
        return 'Dataset (%s, %d examples)' % (
            self.name,
            len(self)
        )


def create_default_splits(path, is_train=True, h=256, w=256):
    ids = all_ids(path)
    total_dataset_size = len(ids)
    print(total_dataset_size)
    test_size = 100  #these are 100 families which are made unseen during test
    training_size = total_dataset_size - test_size

    dataset_train = Dataset(ids[0:training_size], name='train', h=h, w=w, is_train=False)
    dataset_test = Dataset(ids[training_size:], name='test', h=h, w=w, is_train=False)
    return dataset_train, dataset_test

def all_ids(path):
    _ids = []

    for r, d, f in os.walk(path):
        _ids=d
        break

    rs = np.random.RandomState(123)
    rs.shuffle(_ids)
    return _ids
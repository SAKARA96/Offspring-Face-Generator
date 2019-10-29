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
        self.data = None
        #self.data_augmentation = data_augmentation
        #self.center_crop = centor_crop

        #if max_examples is not None:
        #    self._ids = self._ids[:max_examples]

    '''
    For a given family_id( = The directory of family itself),
    it returns dict of key = fam_id_imgNo and value= encoded images [This is a 4 layer tuple]
    for f*m*c images
    '''
    def get_data(self, id):
        return self.data[id]

        

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
    family_ids = all_ids(path)
    total_family_size = len(family_ids)
    test_families_size = 100  #these are 100 families which are made unseen during test
    training_families_size = total_family_size - test_families_size

    training_img = family_to_img_explosion(family_ids[0:training_families_size], path)
    dataset_train = Dataset(training_img.keys(), name='train', h=h, w=w, is_train=False)
    dataset_train.data = training_img

    test_img = family_to_img_explosion(family_ids[training_families_size:], path)
    dataset_test = Dataset(test_img.keys(), name='test', h=h, w=w, is_train=False)
    dataset_test.data = test_img

    return dataset_train, dataset_test

def family_to_img_explosion(family_ids, path):
    np_images={}

    for dir_id in family_ids:
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
        img_id = 1

        if flag!=1:
            for x in dic['father']:
                for y in dic['mother']:
                    for z in dic['child']:
                        np_images[dir_id+'_'+str(img_id)] = np.array([x,y,z,dic['gender']])
                        img_id += 1
    return np_images


def all_ids(path):
    family_ids = []

    for r, d, f in os.walk(path):
        family_ids=d
        break

    rs = np.random.RandomState(123)
    rs.shuffle(family_ids)
    return family_ids
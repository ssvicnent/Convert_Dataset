#coding=utf-8
'''
ICDAR20152015的数据集与VOC的格式有所不同，ICDAR2015的txt中每个框的坐标值共有8个>，分别代表的是顺时针方向的四个顶点的坐标，而VOC数据集中的坐标值只有4个，分别是左
上角顶点坐标和右下角顶点坐标。
'''
import os
import numpy as np
import math
import cv2 as cv
import imageio
import codecs

path='/home/xxx/img_result'
gt_path='/home/xxx/txt_result'

files = os.listdir(path)
files.sort()

for file in files:
    _,basename = os.path.split(file)
    if basename.lower().split('.') not in ['jpg', 'png']:
        continue
    stem, ext = os.path.splitext(basename)
    gt_file = os.path.join(gt_path, stem + '.txt')
    img_path = os.path.join(path, file)
    img = cv.imread(img_path)
    img_size = img.shape
    img_size_min = np.min(img_size[0:2])
    img_size_max = np.max(img_size[0:2])
    
    with open(gt_file, 'r') as f:
	lines = f.readlines()
    for line in lines:
	splitted_line = line.strip().split(',')
	'''
	下面这一步主要处理'\xef\xbb\xbf'的问题
	'''
	if splitted_line[0].startswith(codecs.BOM_UTF8):
	    splitted_line[0] = splitted_line[0].split('\xef\xbb\xbf')[1]
	pt_x = np.zeros((4, 1))
        pt_y = np.zeros((4, 1))
        pt_x[0, 0] = float(splitted_line[0]) 
        pt_y[0, 0] = float(splitted_line[1]) 
        pt_x[1, 0] = float(splitted_line[2]) 
        pt_y[1, 0] = float(splitted_line[3]) 
        pt_x[2, 0] = float(splitted_line[4]) 
        pt_y[2, 0] = float(splitted_line[5]) 
        pt_x[3, 0] = float(splitted_line[6]) 
        pt_y[3, 0] = float(splitted_line[7]) 
        
        ind_x = np.argsort(pt_x, axis=0)
        ind_y = np.argsort(pt_y, axis=0)
        
        if pt_x[ind_x[0]] < 0 :
            pt_x[ind_x[0]] = 0
        if pt_y[ind_y[0]] < 0:
            pt_y[ind_y[0]] = 0
        
        if pt_x[ind_x[-1]] > img_size[1] - 1:
            pt_x[ind_x[-1]] = img_size[1] -1
        if pt_y[ind_y[-1]] > img_size[0] - 1:
            pt_y[ind_y[-1]] = img_size[0] -1
	if not os.path.exists('/home/xxx/label_tmp'):
            os.makedirs('/home/xxx/label_tmp')
        with open(os.path.join('/home/xxx/label_tmp', stem) + '.txt', 'a') as f:
            #for i in range(len(x_left)):
            f.writelines("text\t")
            f.writelines(str(int( pt_x[0, 0])))
            f.writelines("\t")
            f.writelines(str(int( pt_y[0, 0])))
            f.writelines("\t")
            f.writelines(str(int( pt_x[1, 0])))
            f.writelines("\t")
            f.writelines(str(int( pt_y[1, 0])))
            f.writelines("\t")
            f.writelines(str(int( pt_x[2, 0])))
            f.writelines("\t")
            f.writelines(str(int( pt_y[2, 0])))
            f.writelines("\t")
            f.writelines(str(int( pt_x[3, 0])))
            f.writelines("\t")
            f.writelines(str(int( pt_y[3, 0])))                
            f.writelines("\n")

#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import os
import codecs
import h5py
import numpy as np
import cv2
import multiprocessing

num_cores_use = 1

#hesaff_threshold = "500"



# @20180602 descriptor とそれ以外のデータは別ファイルに保存するよう変更
def convert2h5(im_path, hesaff_path, sift_path, h5_desc_path, h5_attr_path):
    im = cv2.imread(im_path)
    height = im.shape[0]
    width  = im.shape[1]
    f = codecs.open(sift_path, "r", "utf-8")
    data = f.read().split("\n")
    f.close()
    ks     = []
    scales = []
    angles = []
    ds     = []
    for i in range(2,len(data)-1):
        #print(data[i])
        es = data[i].split(" ")
        ks.append(np.array([float(es[0]), float(es[1])]))
        scales.append(np.array([float(es[3])]))
        angles.append(np.array([float(es[4])]))
        ds.append(np.array([float(es[j]) for j in range(12, 140)]))
        #print(ds[i-2])
        #quit()
    ks     = np.array(ks)
    scales = np.array(scales)
    angles = np.array(angles)
    ds     = np.array(ds)

    f = codecs.open(hesaff_path, "r", "utf-8")
    data = f.read().split("\n")
    f.close()
    #ks     = []
    #scales = []
    pas = []
    pbs = []
    pcs = []
    for i in range(2,len(data)-1):
        #print(data[i])
        es = data[i].split(" ")
        #print(es)
        pas.append(np.array([float(es[2])]))
        pbs.append(np.array([float(es[3])]))
        pcs.append(np.array([float(es[4])]))
        #ds.append(np.array([float(es[j]) for j in range(12, 140)]))
        #print(ds[i-2])
        #quit()
    #ks     = np.array(ks)
    pas = np.array(pas)
    pbs = np.array(pbs)
    pcs = np.array(pcs)
    #print(pas.shape)
    #print(pbs.shape)
    #print(pcs.shape)
    #print(ks.shape)
    #print(scales.shape)
    #print(angles.shape)
    #print(ds.shape)
    #print(pas,pbs,pcs)
    #quit()
    # desc
    f = h5py.File(h5_desc_path, 'w')
    f.create_dataset('ds', data=ds)
    f.create_dataset('height', data=height)
    f.create_dataset('width', data=width)
    f.flush()
    f.close()
    # attr
    f = h5py.File(h5_attr_path, 'w')
    f.create_dataset('ks', data=ks)
    f.create_dataset('scales', data=scales)
    f.create_dataset('angles', data=angles)
    f.create_dataset('pas', data=pas)
    f.create_dataset('pbs', data=pbs)
    f.create_dataset('pcs', data=pcs)   
    f.create_dataset('height', data=height)
    f.create_dataset('width', data=width)
    f.flush()
    f.close()
    #quit()


#
def step1(im_path, ppm_path):
    print(im_path, ppm_path)
    im = cv2.imread(im_path)
    cv2.imwrite(ppm_path, im)

#
def step2(ppm_path, hesaff_path, hesaff_threshold):
    cmd = "./h_affine.ln.gz -hesaff -i " + ppm_path + " -o " + hesaff_path + " -thres " + hesaff_threshold
    print(cmd)
    os.system(cmd)

#
def step3(ppm_path, hesaff_path, sift_path):
    cmd = "./compute_descriptors.ln.gz -sift -i " + ppm_path + " -p1 " + hesaff_path + " -o2 " + sift_path
    print(cmd)
    os.system(cmd)

# 
def step4(im_path, hesaff_path, sift_path, h5_desc_path, h5_attr_path):
    convert2h5(im_path, hesaff_path, sift_path, h5_desc_path, h5_attr_path)

#
def extract_feature_in_dir(im_dir, ppm_dir, feat_dir, hesaff_threshold):

    # -> ppm
    arg_lists1 = []
    im_names   = os.listdir(im_dir)
    im_names.sort()
    for im_name in im_names:
        #print(im_name)
        im_path     = os.path.join(im_dir, im_name)
        ppm_path    = os.path.join(ppm_dir, im_name.split(".")[0]+".ppm")
        if not os.path.exists(ppm_path):
            arg_lists1.append((im_path, ppm_path))
    if num_cores_use > 1 and len(arg_lists1) > 1:
        with multiprocessing.Pool(processes=num_cores_use) as pool:
            pool.starmap(step1, arg_lists1)
    else:
        for arg_list in arg_lists1:
            step1(*arg_list)

    # -> hesaff
    arg_lists2 = []
    im_names  = os.listdir(im_dir)
    im_names.sort()
    for im_name in im_names:
        #print(im_name)
        ppm_path    = os.path.join(ppm_dir, im_name.split(".")[0]+".ppm")
        hesaff_path = os.path.join(feat_dir, im_name.split(".")[0]+".hesaff")
        if not os.path.exists(hesaff_path):
            arg_lists2.append((ppm_path, hesaff_path, hesaff_threshold))
    if num_cores_use > 1 and len(arg_lists2) > 1:
        with multiprocessing.Pool(processes=num_cores_use) as pool:
            pool.starmap(step2, arg_lists2)
    else:
        for arg_list in arg_lists2:
            step2(*arg_list)

    # -> sift
    arg_lists3 = []
    im_names  = os.listdir(im_dir)
    im_names.sort()
    for im_name in im_names:
        #print(im_name)
        ppm_path    = os.path.join(ppm_dir, im_name.split(".")[0]+".ppm")
        hesaff_path = os.path.join(feat_dir, im_name.split(".")[0]+".hesaff")
        sift_path   = os.path.join(feat_dir, im_name.split(".")[0]+".hesaff.sift")
        if not os.path.exists(sift_path):
            arg_lists3.append((ppm_path, hesaff_path, sift_path))
    if num_cores_use > 1 and len(arg_lists3) > 1:
        with multiprocessing.Pool(processes=num_cores_use) as pool:
            pool.starmap(step3, arg_lists3)
    else:
        for arg_list in arg_lists3:
            print(*arg_list)
            step3(*arg_list)

    # -> h5
    arg_lists4 = []
    im_names  = os.listdir(im_dir)
    im_names.sort()
    for im_name in im_names:
        #print(im_name)
        im_path      = os.path.join(im_dir, im_name)
        hesaff_path  = os.path.join(feat_dir, im_name.split(".")[0]+".hesaff")
        sift_path    = os.path.join(feat_dir, im_name.split(".")[0]+".hesaff.sift")
        #h5_path     = os.path.join(feat_dir, im_name.split(".")[0]+".h5")
        h5_desc_path = os.path.join(feat_dir, im_name.split(".")[0]+"_desc.h5")
        h5_attr_path = os.path.join(feat_dir, im_name.split(".")[0]+"_attr.h5")
        if os.path.exists(sift_path):
            if not os.path.exists(h5_desc_path) or not os.path.exists(h5_attr_path):
                arg_lists4.append((im_path, hesaff_path, sift_path, h5_desc_path, h5_attr_path))
    if num_cores_use > 1 and len(arg_lists4) > 1:
        with multiprocessing.Pool(processes=num_cores_use) as pool:
            pool.starmap(step4, arg_lists4)
    else:
        for arg_list in arg_lists4:
            step4(*arg_list)

    # check
    for im_name in im_names:
        #print(im_name)
        sift_path   = os.path.join(feat_dir, im_name.split(".")[0]+".hesaff.sift")
        if not os.path.exists(sift_path):
            print("{}".format(sift_path))



#
if __name__=="__main__":

    ts = ["500"]
    for hesaff_threshold in ts:
        #im_dir   = "/misc/tarasima/datasets/oxford100k/images_readable"
        #ppm_dir  = "/misc/tarasima/datasets/oxford100k/ppms"
        #feat_dir = "/misc/tarasima/datasets/oxford100k/feats_hesaff_t" + hesaff_threshold
        im_dir   = "/root/src/fsm/src_test/images"
        ppm_dir  = "/root/src/fsm/src_test/ppms"
        feat_dir = "/root/src/fsm/src_test/feats_hesaff_t" + hesaff_threshold
        if not os.path.exists(ppm_dir):
            os.makedirs(ppm_dir)
        if not os.path.exists(feat_dir):
            os.makedirs(feat_dir)
        extract_feature_in_dir(im_dir, ppm_dir, feat_dir, hesaff_threshold)



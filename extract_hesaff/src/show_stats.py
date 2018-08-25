#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import os
import h5py


#
def show_stats(im_dir, feat_dir):
    #print(im_dir)
    print(feat_dir)
    num_feats_all = 0
    num_images_nz = 0
    im_names = os.listdir(im_dir)
    im_names.sort()
    for im_name in im_names:
        feat_path = os.path.join(feat_dir, im_name.split(".")[0]+".h5")
        if os.path.exists(feat_path):
            f = h5py.File(feat_path, "r")
            num_feats = f["ks"].value.shape[0]
            num_feats_all += num_feats
            num_images_nz += 1
        else:
            print("[ALERT] {} have no keypoints".format(im_name))
    print("# of keypoints : {}, # of images : {}, average # of keypoints : {}".format(num_feats_all, num_images_nz, (num_feats_all/num_images_nz)))



#
if __name__=="__main__":

    im_dir   = "/misc/tarashima.shuhei/dockers/20180512-xxxxxxxx_bovw_fl32+47/dev1/fl32_data/database/images"
    feat_dir = "/misc/tarashima.shuhei/dockers/20180512-xxxxxxxx_bovw_fl32+47/dev1/fl32_data/database/feats_hesaff_t500"
    show_stats(im_dir, feat_dir)

    im_dir   = "/misc/tarashima.shuhei/dockers/20180512-xxxxxxxx_bovw_fl32+47/dev1/fl32_data/database/images"
    feat_dir = "/misc/tarashima.shuhei/dockers/20180512-xxxxxxxx_bovw_fl32+47/dev1/fl32_data/database/feats_hesaff_t400"
    show_stats(im_dir, feat_dir)

    im_dir   = "/misc/tarashima.shuhei/dockers/20180512-xxxxxxxx_bovw_fl32+47/dev1/fl32_data/database/images"
    feat_dir = "/misc/tarashima.shuhei/dockers/20180512-xxxxxxxx_bovw_fl32+47/dev1/fl32_data/database/feats_hesaff_t300"
    show_stats(im_dir, feat_dir)





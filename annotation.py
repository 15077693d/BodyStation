import numpy as np
import json
import cv2
from matplotlib import pyplot as plt
from constants import *
from utils import draw_size,bounding_box,zoomin_point,resize_point,bounding_box
import os

def annotation_condition(cv2_img,posedata, keypoint_min_score=0.5, min_keypoints=8,threshold_denoise = 0.03):
    # 1. keypoints_keep<min_keypoint -> False
    keypoints = posedata.keys()
    keypoints_keep = [keypoint for keypoint in keypoints \
        if posedata[keypoint]['conf'] >= keypoint_min_score] #only select keypoins with conf >= keypoint_min_score

    if len(keypoints_keep) <= min_keypoints:
        return [False]

    # 2. size proportion is small than -> False
    keypoint_list_x = [round(posedata[keypoint]['x']) for keypoint in keypoints]
    keypoint_list_y = [round(posedata[keypoint]['y']) for keypoint in keypoints]
    mean_xdiff = np.mean(abs(np.diff(keypoint_list_x)/cv2_img.shape[1])) #based on the weight
    mean_ydiff = np.mean(abs(np.diff(keypoint_list_y)/cv2_img.shape[0])) #based on the height

    if (mean_xdiff <= threshold_denoise and mean_ydiff<=threshold_denoise): 
        return [False]
    
    return [True,keypoints_keep]

def annotation (cv2_img, pose_dict,pose_id = '?',keypoints_keep=None,line =True,point =True, box =True):
    """
    keypoints_keep: list of string(key)
    'nose'
    'l_eye'
    'r_eye'
    'l_ear'
    'r_ear'
    'l_shoulder'
    'r_shoulder'
    'l_elbow'
    'r_elbow'
    'l_wrist'
    'r_wrist'
    'l_hip'
    'r_hip'
    'l_knee'
    'r_knee'
    'l_ankle'
    'r_ankle'
    'neck'
    """
    keypoint_list_x = [round(pose_dict[keypoint]['x']) for keypoint in pose_dict.keys()]
    keypoint_list_y = [round(pose_dict[keypoint]['y']) for keypoint in pose_dict.keys()]
    overlay = cv2_img.copy()
    alpha = 0.8
    if keypoints_keep==None:
        keypoints_keep = pose_dict.keys()
    # draw line
    if line:
        for keypoint1, keypoint2 in line_pair:
            if  keypoint1 in keypoints_keep and keypoint2 in keypoints_keep:
                keypoint1_xy = (int(round(pose_dict[keypoint1]['x'])), int(round(pose_dict[keypoint1]['y'])))
                keypoint2_xy = (int(round(pose_dict[keypoint2]['x'])), int(round(pose_dict[keypoint2]['y'])))
                lineThickness = draw_size(overlay)['lineThickness']
                cv2.line(overlay, keypoint1_xy, keypoint2_xy, color_dict[keypoint1], int(lineThickness))
                # cv2.imshow('yo',overlay)
                # cv2.waitKey(0)

    if point:
        # draw point
        for keypoint in keypoints_keep:
            keypoint_x = round(pose_dict[keypoint]['x'])
            keypoint_y = round(pose_dict[keypoint]['y'])
            circle_radius = draw_size(overlay)['circle_radius']
            cv2.circle(overlay,(int(keypoint_x), int(keypoint_y)), int(circle_radius)+10, color_dict[keypoint], -1)
            # cv2.imshow('yo',overlay)
            # cv2.waitKey(0)

    if box:
        # draw box
        pt1,pt2 = bounding_box(keypoint_list_x,keypoint_list_y,0.1)
        rec_color = np.random.rand(3) * 255
        lineThickness = draw_size(overlay)['lineThickness']
        space = draw_size(overlay)['space']
        thickness = draw_size(overlay)['thickness']
        fontScale = draw_size(overlay)['fontScale']
        cv2.rectangle(overlay, pt1, pt2, rec_color, int(lineThickness))
        # cv2.putText(overlay,f"id {pose_id}",(pt1[0],pt1[1]+20),cv2.FONT_HERSHEY_COMPLEX,fontScale,rec_color,int(thickness))

    new_img = cv2.addWeighted(overlay, alpha, cv2_img, 1 - alpha, 0) #transparent
        # cv2.imshow('yo',overlay)
        # cv2.waitKey(0)
        # cv2.imshow('yo',new_img)
        # cv2.waitKey(0)

    return new_img

def cut_part(keypoint,posedata,cv2_img,path = './_testset/cuted_img'):
    for pose_dict in posedata:
        x = pose_dict[keypoint]['x']
        y = pose_dict[keypoint]['y']
        pt1 = (int(x-100),int(y-100))
        pt2 = (int(x+100),int(y+100))
        cv2.imshow('yo',cv2_img[pt1[1]:pt2[1],pt1[0]:pt2[0]])
        cv2.waitKey(0)
    

if __name__ == "__main__":
    # for j in ['1f','2f','3f']:
    #     json_path = f'/Users/15077693d/Desktop/miro/miro_intern_week1/_testset/json_/0000{j}.json'
    #     img_path = f'/Users/15077693d/Desktop/miro/miro_intern_week1/_testset/{j}.jpg'
    #     cv2_img = cv2.imread(img_path)
    #     with open(json_path,'r') as doc:
    #         posedata_list = json.load(doc)['poses']
    #     for posedata in posedata_list:
    #         cv2_img = annotation(cv2_img, posedata,pose_id = '?',keypoints_keep=None)
    #     cv2.imshow('123',cv2_img)
    #     cv2.waitKey(0)
    json_path = '/Users/15077693d/Desktop/miro/miro_intern_week1/_testset/json_/00test.json'
    img_path = '/Users/15077693d/Desktop/miro/miro_intern_week1/_testset/test.jpg'
    cv2_img = cv2.imread(img_path)
    with open(json_path,'r') as doc:
        posedata = json.load(doc)['poses']
    print(len(posedata))
    cut_part('l_ankle',posedata,cv2_img,path = './_testset/cuted_img')
    cv2.imshow('123',annotation (cv2_img, posedata[0],pose_id = '?',keypoints_keep=None,line =True,point =True, box =True))
    cv2.waitKey(0)

        
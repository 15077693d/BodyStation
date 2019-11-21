import os,sys
cwdir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, cwdir.replace('/body_station',''))
from pose_models import LoadModel,PredictPose
from evaluate import Evaluate
from annotation import annotation
from utils import bounding_box
import numpy as np
import cv2

def point_2_square(point,side_length):
    change = side_length//2
    pt1_x = int(point['x'] - change)
    pt1_y = int(point['y'] - change)
    pt2_x = int(point['x'] + change)
    pt2_y = int(point['y'] + change)
    print('X',pt2_x-pt1_x)
    print('Y',pt2_y-pt1_y)
    return ((pt1_x,pt1_y),(pt2_x,pt2_y))

def color_difference(array1,array2):
    return(sum(sum(sum(array1 - array2))))

def check_person(pose_data,cv2_img,color_key = 'l_shoulder',side_length=50):
    flag = cv2.resize(cv2.imread('./other_image/sample.png'),(side_length,side_length))
    # print(flag.shape)
    # area is big 
    area_list = []
    color_list = []
    label_list = []
    # color
    for pose_dict in pose_data['poses']:
        list_x = [pose_dict[key]['x'] for key in list(pose_dict.keys())]
        list_y = [pose_dict[key]['y'] for key in list(pose_dict.keys())]
        ((pt1_x,pt1_y),(pt2_x,pt2_y))= bounding_box(list_x,list_y,0.1)
        # area
        area = (pt2_x - pt1_x)*(pt2_y - pt1_y)
        area_list.append(area)
        # color   
        ((pt1_x,pt1_y),(pt2_x,pt2_y))=point_2_square(pose_dict[color_key],side_length)
        print(((pt1_x,pt1_y),(pt2_x,pt2_y)))
        label = cv2_img[pt1_y:pt2_y,pt1_x:pt2_x]
        print(label.shape)
        label_list.append(label)
        color_list.append(color_difference(flag,label))

    return {'area_index':area_list.index(max(area_list)),
            'color_index':color_list.index(min(color_list)),
            'label':label_list[color_list.index(min(color_list))],
            'flag':flag}

model = LoadModel(weight_dir = '../model_')
cap = cv2.VideoCapture(0)
while True:
    pose_data, image_name, cv2_img = PredictPose(model,capture=cap,scale_factor=0.2)
    try:
        person_set = check_person(pose_data,cv2_img)
        area_target_index = person_set['area_index']
        color_target_index = person_set['color_index']
        # size match
        cv2_img = annotation(cv2_img, pose_data['poses'][area_target_index],line=False,point=False,keypoints_keep ='l_shoulder')
        cv2.putText(cv2_img, 'size match', (int(pose_data['poses'][area_target_index]['l_shoulder']['x']),int(pose_data['poses'][area_target_index]['l_shoulder']['y']))
                        , cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0) , 2, cv2.LINE_AA) 

        # color match
        cv2_img = annotation(cv2_img, pose_data['poses'][color_target_index],line=False,point=False,keypoints_keep ='r_shoulder')
        cv2.putText(cv2_img, 'color match',  (int(pose_data['poses'][color_target_index]['r_shoulder']['x']),int(pose_data['poses'][color_target_index]['r_shoulder']['y']))
                    , cv2.FONT_HERSHEY_SIMPLEX , 2, (255, 0, 0) , 2, cv2.LINE_AA) 
        
        # add flag,label:
        print(1)
        cv2_img = np.concatenate((cv2.resize(person_set['flag'],(50,cv2_img.shape[0])),cv2.resize(person_set['label'],(50,cv2_img.shape[0])),cv2_img),axis = 1)
        print(2)
    except Exception as e:
        print(e)
        pass
    cv2.imshow('cv2_img',cv2_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

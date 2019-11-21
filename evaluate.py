import numpy as np
import json
import os
import re
from utils import resize_point,zoomin_point,Normalize,cosine_similarity,rmse,mse,amse,weighted_mean_error
def Evaluate( Pose1, Pose2, normalize = True, new_width = 300, new_height = 500):
    '''
    Compute Similarity score between Pose1 and Pose2
    Args:
        normalize: resize, scale, and normalize Pose1 and Pose2
        new_width: width to resize
        new_height: height to resize
    '''
    vector_features = list(set(Pose1.keys()).intersection(set(Pose2.keys())))
    vector1 = []
    vector2 = []

    if normalize:
        # zoomin_point
        pt1_a,pt2_a,Pose1 = zoomin_point(Pose1)
        pt1_b,pt2_b,Pose2 = zoomin_point(Pose2)

        # resize
        Pose1 = resize_point(Pose1,new_width,new_height,pt1_a,pt2_a)
        Pose2 = resize_point(Pose2,new_width,new_height,pt1_b,pt2_b)

    vector1_key_weighted = []
    vector1_confidence_weighted = []
    weight_key = {
           'nose':1,
           'l_eye':1,
           'r_eye':1,
           'l_ear':1,
           'r_ear':1,
           'l_shoulder':1.5,
           'r_shoulder':1.5,
           'l_elbow':2,
           'r_elbow':2,
           'l_wrist':2,
           'r_wrist':2,
           'l_hip':1.5,
           'r_hip':1.5,
           'l_knee':2,
           'r_knee':2,
           'l_ankle':2,
           'r_ankle':2,
           'neck':1,
           }
    for feature in vector_features:
            vector1 += [Pose1[feature]['x'], Pose1[feature]['y']]
            vector2 += [Pose2[feature]['x'], Pose2[feature]['y']] 
            vector1_key_weighted += [weight_key[feature],weight_key[feature]]
            vector1_confidence_weighted += [Pose1[feature]['conf'],Pose1[feature]['conf']]

    # normalize
    if normalize:
        score =  (cosine_similarity(Normalize(vector1), Normalize(vector2)),
                                 rmse(Normalize(vector1),Normalize(vector2)),
                                 mse(Normalize(vector1),Normalize(vector2)),
                                amse(Normalize(vector1),Normalize(vector2)),
                                weighted_mean_error(vector1_confidence_weighted,Normalize(vector1),Normalize(vector2)),
                                weighted_mean_error(vector1_key_weighted,Normalize(vector1),Normalize(vector2))
                                 )   
    else:
        score =  (cosine_similarity(vector1, vector2),
                                 rmse(vector1,vector2),
                                 mse(vector1,vector2),
                                amse(vector1,vector2),
                                weighted_mean_error(vector1_confidence_weighted,vector1,vector2),
                                weighted_mean_error(vector1_key_weighted,vector1,vector2)
                                 )   
    return score

def PoseCompare( TargetPoseData, TestPoseData, normalize = False):
    '''
    Compare TestPoseData to TargetPoseData and returns
    number of False Positive, number of False Negative,
    number of average similarity score, and
    the individual pose comparison data
    '''
    target = TargetPoseData['poses']
    test = TestPoseData['poses']
    poser_location = locate_the_same_poser(target, test)
    # print(poser_location)

    fp_count = len(test) - len(poser_location)
    fn_count = len(target) - len(poser_location)
    # print(fp_count, fn_count)
    PoseMap = {}
    metadata = {}
    cosine_similarity = 0
    mae = 0 
    for target_index, test_index in poser_location:
        common_keypoints = set(target[target_index].keys()).intersection(set(test[test_index].keys()))
        keypoints_not_compared = {
                                    "target_unqine_key":[keypoint for keypoint in list(target[target_index].keys()) if keypoint not in common_keypoints],
                                    "test_unqine_key":[keypoint for keypoint in list(test[test_index].keys()) if keypoint not in common_keypoints]
                                    }
        cosine_similarity_, rmse_,mse_,mae_,weighted_confidence_mean_error_,weighted_keypoint_mean_error_ = Evaluate(target[target_index], test[test_index],normalize=normalize)
        cosine_similarity += cosine_similarity_
        mae += mae_
        

        PoseMap[test_index] = target_index
        metadata[test_index] = {'score':{'cosine_similarity':cosine_similarity_,'mae':mae_},
        'keypoints_compared': list(common_keypoints), 'keypoints_not_compared': keypoints_not_compared,
        'Normalize':normalize}
    
    if len(poser_location) > 0:
        ave_mae = mae / len(poser_location)
        ave_sim = cosine_similarity / len(poser_location)
    else:
        ave_mae = np.nan
        ave_sim = np.nan
    results = {'fp': fp_count, # pose that doesn't exist
               'fn': fn_count, # pose that's missed
               'map': PoseMap,
               'average_score': {'cosine_similarity': ave_sim, 'mae': ave_mae},
               'possible_matches': len(target),
               'metadata': metadata
              }
    return results

def locate_the_same_poser(target, test, benchmark = 20):
    '''
    Compare TestPoseData to TargetPoseData and returns
    poser location. 'benchmark' is a confident level to
    determine whether the poser from two pose data are the same
    '''  
    poser_location = []
    for pose1_ in range(len(target)):
        is_same_poser = 0 #indicator
        for pose2_ in range(len(test)):
            common_keypoints = set(target[pose1_].keys()).intersection(set(test[pose2_].keys()))
            for key_point in common_keypoints:
                pose1x = target[pose1_][key_point]['x'] #x coordinate of the key_point from target pose data
                pose1y = target[pose1_][key_point]['y'] #y coordinate of the key_point from target pose data
                pose2x = test[pose2_][key_point]['x'] #x coordinate of the key_point from test pose data
                pose2y = test[pose2_][key_point]['y'] #y coordinate of the key_point from test pose data
                if abs(pose1x - pose2x) <= benchmark and abs(pose1y - pose2y) <= benchmark: 
                    #only select the keypoint whose distance between two coordinates is below the benchmark
                    is_same_poser += 1 
                if is_same_poser >= 3: #make sure they are the same poser (with at least 3 similar key points )
                    break
            if is_same_poser >= 3:
                # print(f'\nPoser\'s index in model_1: {pose1_} corresponding to Poser\'s index in model_2: {pose2_}\n')
                poser_location.extend([(pose1_, pose2_)])
                break
    return poser_location

if __name__ == '__main__':
    for i in range(1,8):
        with open(os.getcwd() + f'/_testset/json/{i}.json','r') as doc:
            TargetPoseData = json.load(doc)
        with open(os.getcwd() + f'/_testset/json_/00000{i}.json','r') as doc:
            TestPoseData = json.load(doc)
        print(f'\n\nIn image {i}:\n\n')
        print(PoseCompare( TargetPoseData, TestPoseData, normalize = True))
        

        
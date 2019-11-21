import pyautogui
from motion_contants import *
import time
import numpy as np
import os
cwdir = os.path.dirname(os.path.realpath(__file__))
# utils
# save motion
def find_diff_index(time_list,time_interval,x_list = None,y_list = None,index_boolean = False):
        t0 = time_list[-1]
        for i in range(len(time_list)):
            index = None
            diff_time = t0 - time_list[::-1][i]
            if diff_time > time_interval:
                index = -i-1
                break
        if index_boolean:
            return index
        else:
            pass
        if index == None:
            diff_time = np.nan
            diff_x = np.nan
            diff_y = np.nan
        else:
            diff_x = x_list[-1] - x_list[index]
            diff_y = y_list[-1] - y_list[index]
        return {'diff_time':diff_time,'diff_x':diff_x,'diff_y':diff_y}  
class motion_record():
    def __init__(self,game,useGPU):
        # data
        self.motion_dict = motion_contants(game,useGPU)
        self.game = game
        self.run_count = 0
        # tetris
        self.down_flag = None
    # save motion
    def save_record(self,posedict):
        for keypoint,record_dict in self.motion_dict['keypoints'].items():
            if self.game == 'test':
                # general item
                record_dict['x'].append(posedict[keypoint]['x'])
                record_dict['y'].append(posedict[keypoint]['y'])
                record_dict['time'].append(time.time())
                # difference item
                diff_dict = find_diff_index(record_dict['time'],self.motion_dict['time_interval'],
                                                record_dict['x'],record_dict['y'])
                record_dict['diff_x'].append(diff_dict['diff_x'])
                record_dict['diff_y'].append(diff_dict['diff_y'])
                record_dict['diff_time'].append(diff_dict['diff_time'])
                record_dict['motion'].append(None)

            elif self.game in ['hooligans','tetris','relicrunway']:
                if keypoint == 'nose':
                    # general item
                    record_dict['x'].append(posedict[keypoint]['x'])
                    record_dict['y'].append(posedict[keypoint]['y'])
                    record_dict['time'].append(time.time())
                    # difference item
                    diff_l = posedict[keypoint]['y'] - posedict['l_wrist']['y']
                    diff_r = posedict[keypoint]['y'] - posedict['l_wrist']['y']
                    record_dict['diff_x'].append(np.nan)
                    record_dict['diff_y'].append(max([diff_l,diff_r]))
                    record_dict['diff_time'].append(np.nan)

                elif keypoint == 'neck':
                    # general item
                    record_dict['x'].append(posedict[keypoint]['x'])
                    record_dict['y'].append(posedict[keypoint]['y'])
                    record_dict['time'].append(time.time())
                    # difference item
                    diff_dict = find_diff_index(record_dict['time'],self.motion_dict['time_interval'],
                                                    record_dict['x'],record_dict['y'])
                    record_dict['diff_x'].append(diff_dict['diff_x'])
                    record_dict['diff_y'].append(diff_dict['diff_y'])
                    record_dict['diff_time'].append(diff_dict['diff_time'])
                    

                elif keypoint in ['l_wrist','r_wrist']:
                    # general item
                    record_dict['x'].append(posedict[keypoint]['x'])
                    record_dict['y'].append(posedict[keypoint]['y'])
                    record_dict['time'].append(time.time())
                    
                    if self.game == 'tetris':
                    # difference item
                        two_pt_diff_y = posedict[keypoint]['y'] - posedict['neck']['y']
                        diff_dict = find_diff_index(record_dict['time'],self.motion_dict['time_interval'],
                                                        record_dict['x'],record_dict['y'])
                        record_dict['diff_y'].append(two_pt_diff_y)
                        record_dict['diff_x'].append(np.nan)
                        record_dict['diff_time'].append(np.nan)
                    else:
                        pass
                else:
                    pass      
            else:
                pass                
                

    def motion_append(self):
        # check frame amount
        if self.run_count<2:
            self.run_count+=1
            for keypoint,record_dict in self.motion_dict['keypoints'].items():
                record_dict['motion'].append(None)
        else:
            # hooligans/relicrunway
            if self.game in ['hooligans','relicrunway']:
                # neck
                record_neck_dict = self.motion_dict['keypoints']['neck']
                # time 0 data
                diff_x_0 = record_neck_dict['diff_x'][-1] 
                diff_y_0 = record_neck_dict['diff_y'][-1]
                # condition1
                # up,down
                if abs(diff_y_0) > self.motion_dict['difference']['up'] and diff_y_0 < 0:
                    motion_0 = 'up'
                elif abs(diff_y_0) > self.motion_dict['difference']['down'] and diff_y_0 > 0:
                    motion_0 = 'down'
                elif abs(diff_x_0) > self.motion_dict['difference']['right'] and diff_x_0 > 0:
                    motion_0 = 'right'                   
                elif abs(diff_x_0) > self.motion_dict['difference']['left'] and diff_x_0 < 0:
                    motion_0 = 'left'                      
                else:
                    motion_0 = None

                # condition2
                if motion_0!= None:
                    index = find_diff_index(record_neck_dict['time'],self.motion_dict['hold_interval'],index_boolean = True)
                    if index == None:
                        record_neck_dict['motion'].append(None)
                    else:
                    # 2b: not same motion
                        if motion_0 not in record_neck_dict['motion'][index:]:
                            if motion_0 == 'up' and 'down' in record_neck_dict['motion'][index:]: 
                                print('*******   (Fail)New message\nCant up[up after down]: ',motion_0,'\nlist: ',record_neck_dict['motion'][index:],'\n')     
                                record_neck_dict['motion'].append(None)
                            elif motion_0 == 'down' and 'up' in record_neck_dict['motion'][index:]:
                                print('*******   (Fail)New message\nCant down[down after up]: ',motion_0,'\nlist: ',record_neck_dict['motion'][index:],'\n') 
                                record_neck_dict['motion'].append(None)
                            else:
                                print('*******   (Success)New message\nnew_motion: ',motion_0) 
                                record_neck_dict['motion'].append(motion_0)
                                if motion_0 in ['right','left']:
                                    print(f'1. x: {record_neck_dict["x"][index:]}')
                                    print(f"2. diff_x({self.motion_dict['difference'][motion_0]}): {diff_x_0}")
                                else:
                                    print(f'1. y: {record_neck_dict["y"][index:]}')
                                    print(f"2. diff_y({self.motion_dict['difference'][motion_0]}): {diff_y_0}")
                                print(f'3. past motion: {record_neck_dict["motion"][index:]}')
                                print(f'4. now motion: {record_neck_dict["motion"][-1]}\n')
                        else:
                            record_neck_dict['motion'].append(None)
                            print('*******   (Fail)New message\nCant motion[same motion]: ',motion_0,'\nlist: ',record_neck_dict['motion'][index:],'\n') 
                else:
                    record_neck_dict['motion'].append(None)
            # tetris
            elif self.game == 'tetris':
                    for keypoint, record_dict in self.motion_dict['keypoints'].items():
                        # neck
                        if keypoint == 'neck':
                            # time 0 data
                            diff_x_0 = record_dict['diff_x'][-1] 
                            diff_y_0 = record_dict['diff_y'][-1]
                            # condition1
                            # up,down
                            if abs(diff_y_0) > self.motion_dict['difference']['up'] and diff_y_0 < 0:
                                motion_0 = 'up'
                                self.down_flag = False
                            elif abs(diff_y_0) > self.motion_dict['difference']['down'] and diff_y_0 > 0:
                                motion_0 = 'down'
                                self.down_flag = True
                            elif abs(diff_x_0) > self.motion_dict['difference']['right'] and diff_x_0 > 0:
                                motion_0 = 'right' 
                                self.down_flag = False                  
                            elif abs(diff_x_0) > self.motion_dict['difference']['left'] and diff_x_0 < 0:
                                motion_0 = 'left'  
                                self.down_flag = False
                            elif self.down_flag:
                                motion_0 = 'down'                    
                            else:
                                motion_0 = None

                            # condition2
                            if motion_0!= None:
                                index = find_diff_index(record_dict['time'],self.motion_dict['hold_interval'],index_boolean = True)
                                if index == None:
                                    record_dict['motion'].append(None)
                                else:
                                # 2b: not same motion
                                    if motion_0 not in record_dict['motion'][index:] or self.down_flag:
                                        if motion_0 == 'up' and 'down' in record_dict['motion'][index:]: 
                                            self.down_flag = False
                                            print('*******   (Fail)New message\nCant up[up after down]: ',motion_0,'\nlist: ',record_dict['motion'][index:],'\n')     
                                            record_dict['motion'].append(None)
                                        elif motion_0 == 'down' and 'up' in record_dict['motion'][index:]:
                                            self.down_flag = False
                                            print('*******   (Fail)New message\nCant down[down after up]: ',motion_0,'\nlist: ',record_dict['motion'][index:],'\n') 
                                            record_dict['motion'].append(None)
                                        else:
                                            print('*******   (Success)New message\nnew_motion: ',motion_0) 
                                            record_dict['motion'].append(motion_0)
                                            if motion_0 in ['right','left']:
                                                print(f'1. x: {record_dict["x"][index:]}')
                                                print(f"2. diff_x({self.motion_dict['difference'][motion_0]}): {diff_x_0}")
                                            else:
                                                print(f'1. y: {record_dict["y"][index:]}')
                                                print(f"2. diff_y({self.motion_dict['difference'][motion_0]}): {diff_y_0}")
                                            print(f'3. past motion: {record_dict["motion"][index:]}')
                                            print(f'4. now motion: {record_dict["motion"][-1]}\n')
                                    else:
                                        record_dict['motion'].append(None)
                                        print('*******   (Fail)New message\nCant motion[same motion]: ',motion_0,'\nlist: ',record_dict['motion'][index:],'\n') 
                            else:
                                record_dict['motion'].append(None)
                        # wrist
                        elif "wrist" in keypoint:
                            direction = {'l':'left','r':'right'}
                            # press right
                            if record_dict['diff_y'][-1] <= 0:
                                motion_0 = direction[keypoint[0]]
                            else:
                                motion_0 = None

                            if motion_0!= None:
                                index = find_diff_index(record_dict['time'],self.motion_dict['time_interval'],index_boolean = True)
                                if index == None:
                                    record_dict['motion'].append(None)
                                else:
                                    if motion_0 not in record_dict['motion'][index:]:
                                        print('*******   (Success)New message\nnew_motion: ',motion_0) 
                                        print(f"1. {keypoint} vs neck: {record_dict['diff_y'][-1]}\n")
                                        record_dict['motion'].append(motion_0)
                                    else:
                                        record_dict['motion'].append(None)
                            else:
                                record_dict['motion'].append(None)
                        else:
                            pass

    # procress
    def motion_procress(self,posedict):
        # save motion
        self.save_record(posedict)
        # key append
        try:
            if self.game!='test':
                self.motion_append()
                # condition and action
                for keypoint, record_dict in self.motion_dict['keypoints'].items():
                    motion = str(record_dict['motion'][-1])
                    if record_dict['motion'][-1]!= None:
                        keypress = self.motion_dict['rule'][keypoint][motion]
                        pyautogui.press(keypress)
                    else:
                        pass
            else:
                pass
        except Exception as e:
            print(e)

if __name__ == "__main__":
       pass
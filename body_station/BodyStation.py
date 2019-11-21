# general 
import cv2
import numpy as np
import time
import pandas as pd

# excess posenet
import os,sys
cwdir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, cwdir.replace('/body_station',''))
from annotation import annotation as Annotation
from pose_models import PredictPose
from utils import overlay_transparent,check_person


# body station
from game_contants import *
from motion_record import motion_record
from selenium import webdriver
import pyautogui 

def open_game(game,driver_ ="geckodriveros"):
    '''
    0.geckodriverlinx 1.geckodrivermac 2.chromedriverwin
    3.chromedriverlinx 4.chromedrivermac 5.chromedriverwin
    '''
    window_width = pyautogui.size()[0]
    window_height = pyautogui.size()[1] 
    urls = {
        'hooligans':'https://gemioli.com/hooligans/',
        'tetris':'https://www.goodoldtetris.com/',
        'relicrunway':'https://gemioli.com/relicrunway/'
    }
    if 'win' in driver_:
        driver_ = f'{driver_}.exe'
        
    if 'geck' in  driver_:
        driver = webdriver.Firefox(executable_path = f'{cwdir}/driver/{driver_}')
    else:
        driver = webdriver.Chrome(executable_path = f'{cwdir}/driver/{driver_}')
   
    # Open main window with URL A
    driver.set_window_size(int(window_width*0.65), int(window_height))
    driver.set_window_position(int(window_width*0.35), 0)
    driver.get(urls[game])
    # if game == 'hooligans':
    #     time.sleep(7)
    #     print('1.click main page')
    #     pyautogui.click(window_width*0.6729166666666667,window_height*0.6622222222222223)
    #     time.sleep(2)
    #     print('2.accept agreement')
    #     pyautogui.click(window_width*0.6722222222222223,window_height*0.73)
    # else:
    #     pass
    print("Finish Setup: %s" %driver.title)
    return driver

class BodyStation():
    def __init__(self,model,game,driver_ = 'geckodriveros',useGPU=False,output_df=False):
        
        '''

        sum(ratio) == 1
    keypoints_keep: list of string(key)
    'nose','l_eye','r_eye'
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
    
    keypress = down,left,right,up
        '''
        # game info
        self.game = game

        # model
        scale_dict = {
            True:1,
            False:0.2
        }
        self.scale_factor = scale_dict[useGPU]
        self.model = model
        self.useGPU = useGPU

        # window info
        # window
        self.window_width = pyautogui.size()[0]
        self.window_height = pyautogui.size()[1] 

        # driver
        if game not in ['content','test']:
            driver = open_game(self.game,driver_ = driver_)
            self.driver = driver
        else:
            pass
        # box info
        self.capture = cv2.VideoCapture(0)
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # button info
        self.button_dict = game_contants(game,useGPU = useGPU)['button_dict']
        self.start_flag = False

        # annotation
        if game != 'test':
             self.img_dict = game_contants(game,setting = setting)['img_dict']
        else:
            pass
        self.start = time.time()
        self.start = time.time()

        # output df
        self.output_df = output_df
        if self.game != 'content':
            if output_df:
                if not os.path.exists(f'./motion_data/{game}'):
                        os.makedirs(f'./motion_data/{game}')
                flag = [int(item.name[:4]) for item in os.scandir(f'./motion_data/{game}') if item.path.endswith('.csv')]
                if len(flag)!=0:
                    str_num = str(max(flag)+1)
                    name = '0'*(4-len(str_num))+str_num+"_"+game
                else:
                    name = '0000'+"_"+game
                self.df_output_name = name
            else:
                pass
        else:
            pass

    # utils

    # control button
    def into_button(self,button,keypoint):
        pt1 = (
                int(self.width*self.button_dict[button]['location']['pt1'][0]),
                int(self.height*self.button_dict[button]['location']['pt1'][1])
                )
        pt2 = (
                int(self.width*self.button_dict[button]['location']['pt2'][0]),
                int(self.height*self.button_dict[button]['location']['pt2'][1])
                )
        if pt1[0] < keypoint['x'] and pt1[1] < keypoint['y'] and \
            pt2[0] > keypoint['x'] and pt2[1] > keypoint['y']:
            return 1
        else:
            return 0

    # mother
    def check_mother(self,button):
        now = time.time()
        if self.button_dict[button]['mother']['boolean'] and self.button_dict[button]['boolean']:
            if self.button_dict[button]['mother']['past'] == None:
                self.button_dict[button]['mother']['past'] = now
            else:
                diff_sec = now - self.button_dict[button]['mother']['past']
                if diff_sec < self.button_dict[button]['mother']['hold_sec']:
                    ratio = round(diff_sec/self.button_dict[button]['mother']['hold_sec'],3)
                    print(f"Button(mother): {button}[{self.button_dict[button]['mother']['boolean']}]({ratio})")
                else:
                    self.button_dict[button]['boolean'] = not self.button_dict[button]['boolean']
                    print(f'Button(mother): Press {button}')
                    self.button_dict[button]['past'] = None
                    self.button_dict[button]['mother']['past']= None
        else:
            pass
    
    # annotation
    def filp_pose_point(self,pose_dict):
        for key_point in list(pose_dict.keys()):
            pose_dict[key_point] = {
                'x':self.width - pose_dict[key_point]['x'],
                'y':pose_dict[key_point]['y']
            }
        return pose_dict

    def find_point_fixed(self,info_dict,url):
            pt1_x = int(info_dict['location']['pt1'][0]*self.width)
            pt1_y = int(info_dict['location']['pt1'][1]*self.height)
            pt2_x = int(info_dict['location']['pt2'][0]*self.width)
            pt2_y = int(info_dict['location']['pt2'][1]*self.height)
            img = cv2.imread(url,cv2.IMREAD_UNCHANGED)
            return img,pt1_x,pt1_y,pt2_x,pt2_y

    def find_point_variable(self,info_dict,pose_dict,url):
            pointdict = pose_dict[info_dict['keypoint']]
            new_mid_x = pointdict['x']/self.width
            new_mid_y = pointdict['y']/self.height
            old_pt1_x = info_dict['location']['pt1'][0]
            old_pt2_x = info_dict['location']['pt2'][0]
            old_pt1_y = info_dict['location']['pt1'][1]
            old_pt2_y = info_dict['location']['pt2'][1]
            old_mid_x = (old_pt1_x+ old_pt2_x)/2
            old_mid_y = (old_pt1_y+ old_pt2_y)/2
            x_change = new_mid_x - old_mid_x
            y_change = new_mid_y - old_mid_y
            info_dict['location']['pt1'] = [old_pt1_x+x_change,old_pt1_y+y_change]
            info_dict['location']['pt2'] = [old_pt2_x+x_change,old_pt2_y+y_change]       
            img,pt1_x,pt1_y,pt2_x,pt2_y = self.find_point_fixed(info_dict,url)
            return img,pt1_x,pt1_y,pt2_x,pt2_y

     # annotation
    def annotation(self,pose_dict,cv2_img,alpha = 255):
        for url,info_dict in self.img_dict.items():
            # button
            if info_dict['type'] == 'button':
                # son and change
                if info_dict['son'] and info_dict['change']:
                    mother_button = info_dict['mother_button']
                    if self.button_dict[mother_button]['boolean'] and \
                        info_dict['boolean'] == self.button_dict[info_dict['button']]['boolean']:
                            img,pt1_x,pt1_y,pt2_x,pt2_y = self.find_point_fixed(info_dict,url)
                    else:
                        img = None
                # son
                elif info_dict['son']:
                    mother_button = info_dict['mother_button']
                    if self.button_dict[mother_button]['boolean']:
                            img,pt1_x,pt1_y,pt2_x,pt2_y = self.find_point_fixed(info_dict,url)
                    else:
                        img = None
                # change
                elif info_dict['change']:
                    if info_dict['boolean'] == self.button_dict[info_dict['button']]['boolean']:
                        img,pt1_x,pt1_y,pt2_x,pt2_y = self.find_point_fixed(info_dict,url)
                    else:
                        img = None
                else:
                    img,pt1_x,pt1_y,pt2_x,pt2_y = self.find_point_fixed(info_dict,url)
            
            # fixed
            elif info_dict['type'] == 'fixed':
                # popup
                if info_dict['popup']:
                    keypoint = pose_dict[self.button_dict[info_dict['game']]['keypoint']]
                    mother_button = info_dict['mother_button']
                    if self.into_button(info_dict['game'],keypoint) and self.button_dict[mother_button]['boolean']:
                        img,pt1_x,pt1_y,pt2_x,pt2_y = self.find_point_fixed(info_dict,url)
                        try:
                            img = cv2.imread(url,cv2.IMREAD_UNCHANGED)
                        except:
                            img = cv2.imread(url)
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
                    else:
                        img = None
                else:
                    img,pt1_x,pt1_y,pt2_x,pt2_y = self.find_point_fixed(info_dict,url)
            
            # variable
            elif info_dict['type'] == 'variable':
                # ninja
                if info_dict['ninja']:
                    mother_button = info_dict['mother_button']
                    if self.button_dict[mother_button]['boolean']==info_dict['boolean']:
                        img,pt1_x,pt1_y,pt2_x,pt2_y = self.find_point_variable(info_dict,pose_dict,url)                    
                    else:
                        img = None
                else:
                    img,pt1_x,pt1_y,pt2_x,pt2_y = self.find_point_variable(info_dict,pose_dict,url)             
            else:
                img =None
            try:
                cv2_img = overlay_transparent(cv2_img, img, pt1_x, pt1_y, overlay_size=(pt2_x-pt1_x,pt2_y-pt1_y))
            except:
                pass
        # # FPS
        # text = f"FPS: {round((1/(time.time()-self.start)),2)}"
        # self.start = time.time()
        # color =(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
        # cv2_img = cv2.putText(cv2_img,text,((self.width*45)//100,(self.height*99)//100),cv2.FONT_HERSHEY_COMPLEX,1,color,2)

        if self.game !='content':
                cv2_img = cv2.resize(cv2_img,(int(self.window_width*0.35),int(self.window_height*0.6)))
        return cv2_img

    def annotation_test(self,pose_dict,cv2_img):
        #box and word
        for button,info_dict in self.button_dict.items():
            pt1_x = int(info_dict['location']['pt1'][0]*self.width)
            pt1_y = int(info_dict['location']['pt1'][1]*self.height)
            pt2_x = int(info_dict['location']['pt2'][0]*self.width)
            pt2_y = int(info_dict['location']['pt2'][1]*self.height)
            if self.button_dict[button]['boolean']:
                color = (255,0,0)
            else:
                color = (0,0,0)
            cv2.rectangle(cv2_img,(pt1_x,pt1_y),
                        (pt2_x,pt2_y),color,3)
            cv2.putText(cv2_img, button, (pt1_x,pt2_y),
                         cv2.FONT_HERSHEY_SIMPLEX, 3, color, 2, cv2.LINE_AA)
        #point
        cv2_img = Annotation(cv2_img, pose_dict,pose_id = '?',
                            keypoints_keep=['l_wrist','r_wrist'],
                            line =False,point =True, box =False)
        cv2_img = cv2.resize(cv2_img,(600,600))    
        return cv2_img

    # button
    def button_press(self,posedict):
        # content
        if self.game == 'content':
            if self.button_dict['bodystation']['boolean']:
                for button,info_dict in self.button_dict.items():
                        flag = self.into_button(button,posedict[info_dict['keypoint']])
                        if flag:
                            self.button_action(button)
                        else:
                            self.button_dict[button]['past'] = None
                
            else:
                info_dict = self.button_dict['bodystation']
                flag = self.into_button('bodystation',posedict[info_dict['keypoint']])
                if flag:
                    self.button_action('bodystation')
                else:
                    self.button_dict['bodystation']['past'] = None
        # test
        elif self.game == 'test':
           for button,info_dict in self.button_dict.items():
                        flag = self.into_button(button,posedict[info_dict['keypoint']])
                        if flag:
                            self.button_action(button)
                        else:
                            self.button_dict[button]['past'] = None
        # game
        else:
            if self.button_dict['menu']['boolean']:
                for button,info_dict in self.button_dict.items():
                    flag = self.into_button(button,posedict[info_dict['keypoint']])
                    self.check_mother(button)
                    if flag:
                        self.button_action(button)
                    else:
                        self.button_dict[button]['past'] = None

            else:
                info_dict = self.button_dict['menu']
                flag = self.into_button('menu',posedict[info_dict['keypoint']])
                self.check_mother('menu')
                if flag:
                    self.button_action('menu')
                else:
                    self.button_dict['menu']['past'] = None



    def button_action(self,button):
        now = time.time()
        # button press before
        if self.button_dict[button]['past'] != None:
            diff_sec = now - self.button_dict[button]['past']
            if diff_sec < self.button_dict[button]['hold_sec']:
                    ratio = round(diff_sec/self.button_dict[button]['hold_sec'],3)
                    print(f"Button: {button}[{self.button_dict[button]['boolean']}]({ratio})")
            else:
                self.button_dict[button]['boolean'] = not self.button_dict[button]['boolean']
                print(f'Button: Press {button}')
                if self.game not in ['content','test']:
                    if button =='start':
                        start_button(self.game,self.window_width,self.window_height)
                        if self.start_flag==False:
                            self.start_flag=True
                        else:
                            pass
                    elif button =='exit':
                        exit_button(self.driver)
                    elif button =='pause':
                        if self.start_flag == True:
                            pause_button(self.game,self.window_width,self.window_height)
                            self.start_flag = False
                            self.button_dict['start']['boolean'] = False
                        else:
                            pass
                    else:
                        pass
                

                self.button_dict[button]['past'] = None
        # button never press
        else:
            self.button_dict[button]['past'] = now
        
    def run(self,motion_record_object):

        while True:
            # prediction
            pose_data, image_name, cv2_img = PredictPose(self.model,capture = self.capture ,scale_factor=self.scale_factor,useGPU=self.useGPU)
            # filp the frame
            cv2_img = cv2.flip(cv2_img,1)
            try:
                pose_dict = self.filp_pose_point(check_person(pose_data))
                self.button_press(pose_dict)
                if self.game == 'test':
                    cv2_img = self.annotation_test(pose_dict,cv2_img)
                else:
                    cv2_img = self.annotation(pose_dict,cv2_img)

                if self.game == 'test':
                    if self.button_dict['control']['boolean']:
                        motion_record_object.motion_procress(pose_dict)
                    else:
                        pass
                # game
                elif self.game != 'content':
                    if self.start_flag:
                        motion_record_object.motion_procress(pose_dict)
                    else:
                        pass
                else:
                    pass
            except Exception as e:
                print(e)
                pass
            # display
            if self.game != 'content':
                cv2.namedWindow(self.game)
                cv2.moveWindow(self.game,0,0) 
                cv2.imshow(self.game,cv2_img)
                if cv2.waitKey(1) & 0xFF == ord('q') or self.button_dict['exit']['boolean']:
                    # output df
                    if self.output_df and self.game not in ['content']:
                        for keypoint, record_dict in motion_record_object.motion_dict['keypoints'].items():
                            path = f'{cwdir}/motion_data/{self.game}/{self.df_output_name+"_"+keypoint}.csv'
                            print(f'\n*******   output df:{path}')
                            pd.DataFrame(record_dict).to_csv(path,index = False)
                    self.capture.release()
                    cv2.destroyAllWindows()
                    break    
            else:
                cv2.namedWindow(self.game, cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty(self.game, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.moveWindow(self.game,0,0) 
                cv2.imshow(self.game,cv2_img)
                if cv2.waitKey(1) & 0xFF == ord('q') or self.button_dict['hooligans']['boolean'] or \
                    self.button_dict['tetris']['boolean'] or self.button_dict['relicrunway']['boolean'] or \
                    self.button_dict['exit']['boolean']:
                    self.capture.release()
                    cv2.destroyAllWindows()
                    break
            
        # go other game
        if self.game == 'test':
            return "exit"  
        elif self.game != 'content':
                return "content"    
        else:
            if self.button_dict['hooligans']['boolean']:
                return  "hooligans"
            elif self.button_dict['tetris']['boolean']:
                return "tetris"
            elif self.button_dict['relicrunway']['boolean']:
                return "relicrunway"
            elif self.button_dict['exit']['boolean']:
                return "exit"
            else:
                pass
            


                    
if __name__ == "__main__":
       pass
# game list
# 1.hooligans
# 2.tetris
# 3.relicrunway
import os
cwdir = os.path.dirname(os.path.realpath(__file__))
def motion_contants(game,useGPU):
    # common button dict
    # motion record
    motion_dict =  {
                'time_interval':0.2,
                'hold_interval':0.5,
                    }
    # keypoint
    if game == 'test':
                motion_dict['keypoints'] = {
                                    'l_wrist':{},
                                    'r_wrist':{}
                                    }

    elif game in ['hooligans','relicrunway']:
        motion_dict['keypoints'] = {'neck':{}}

    elif game == 'tetris':
        motion_dict['keypoints'] = {
                                    'l_wrist':{},
                                    'r_wrist':{},
                                    'neck':{}
                                    }
    else:
        pass

    if game != 'content':
        for keypoint, record_dict in motion_dict['keypoints'].items():
                record_dict['x'] = []
                record_dict['y'] = []
                record_dict['diff_x'] = []
                record_dict['diff_y'] = []
                record_dict['time'] = []
                record_dict['diff_time'] = []
                record_dict['motion'] = []
    else:
        pass
    
    # difference
    if useGPU:
        if game in ['hooligans','relicrunway']:
            motion_dict['difference']={'up':60,
                                        'down':60,
                                        'left':50,
                                        'right':50}
        elif game == 'tetris':
             motion_dict['difference']={'up':50,
                                        'down':60,
                                        'left':50,
                                        'right':50}
        else:
            pass
    else:
        if game in ['hooligans','relicrunway']:
            motion_dict['difference']={'up':60,
                                        'down':80,
                                        'left':70,
                                        'right':70}
        elif game == 'tetris':
            motion_dict['difference']={'up':70,
                                        'down':80,
                                        'left':70,
                                        'right':70}
        else:
            pass

    # motion press define
    if game in ['hooligans','relicrunway']:
        motion_dict['rule'] = {
                                'neck':{
                                            "up":"up",
                                            "down":"down",
                                            "left":"left",
                                            "right":"right",
                                        }
                                }
    elif game == 'tetris':
        motion_dict['rule'] = {
                                'neck':{
                                            "up":"space",
                                            "down":'down',
                                            "left":"up",
                                            "right":"up",
                                        },
                                'l_wrist':{
                                            "left":"left"
                                        },
                                'r_wrist':{
                                            "right":"right"

                                }
                                }
    else:
        pass
    
    return motion_dict

    
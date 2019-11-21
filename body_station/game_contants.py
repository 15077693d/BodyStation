# game list
# 1.hooligans
# 2.tetris
# 3.relicrunway
import os
cwdir = os.path.dirname(os.path.realpath(__file__))
import pyautogui
def game_contants(game,useGPU = False):
    if useGPU:
        fast_hold_sec = 0.5
        general_hold_sec = 1
        mother_hold_sec = 7
    else:
        fast_hold_sec = 1
        general_hold_sec = 1.5
        mother_hold_sec = 7
    # test
    if game == 'test':
        button_dict = {
        'control':
            {
                'location':{"pt1": [0, 0],
                            "pt2": [0.5, 0.2]},
                'keypoint':'l_wrist',
                'boolean':False,
                'past':None,
                'hold_sec': general_hold_sec
            },
        'exit':
        {
            'location':{"pt1": [0.5, 0],
                            "pt2": [1, 0.2]},
            'keypoint':'r_wrist',
            'boolean':False,
            'past':None,
            'hold_sec': general_hold_sec
        }
        }
        return  {
                'button_dict':button_dict
                }
    # content!
    elif  game == 'content':
        # common button dict
        button_dict =  {
                    'hooligans':
                    {
                        'location':{"pt1": [0.68268, 0.053086],
                                     "pt2": [0.95074, 0.266786333]},
                        'keypoint':'r_hand',
                        'boolean':False,
                        'past':None,
                        'hold_sec': general_hold_sec,
                        'mother':{
                                    'boolean':False,
                                }   
                    },
                    'tetris':
                    {
                        'location':{"pt1": [0.68268, 0.327566333],
                                     "pt2": [0.95074, 0.541266666]},
                        'keypoint':'r_hand',
                        'boolean':False,
                        'past':None,
                        'hold_sec': general_hold_sec,
                        'mother':{
                                    'boolean':False,
                                }  
                    },
                    'relicrunway':
                    {
                        'location':{"pt1": [0.68268, 0.60204666],
                                     "pt2": [0.95074, 0.815747]},
                        'keypoint':'r_hand',
                        'boolean':False,
                        'past':None,
                        'hold_sec': general_hold_sec,
                        'mother':{
                                    'boolean':False,
                                }  
                    },
                    'exit':
                    {
                        'location':{"pt1": [0.68268,0.876527],
                                     "pt2": [0.95074, 0.976527]},
                        'keypoint':'r_hand',
                        'boolean':False,
                        'past':None,
                        'hold_sec': general_hold_sec,
                        'mother':{
                                    'boolean':False,
                                }  
                    },
                    'bodystation':
                    {
                        'location':{"pt1": [0.04896, 0.053086],
                                     "pt2": [0.6337, 0.256789]},
                        'keypoint':'l_hand',
                        'boolean':False,
                        'past':None,
                        'hold_sec': general_hold_sec,
                        'mother':{
                                    'boolean':False,
                                }  
                    }
                    }

         # img_dict
        img_dict = {

                # button -> son/change
                f'{cwdir}/image/hooligans/hooligans.png':{
                                    'location':button_dict['hooligans']['location'],
                                    'type':'button',
                                    'button':'hooligans',
                                    'son':False,
                                    'change':False
                                },
                f'{cwdir}/image/tetris/tetris.png':{
                                    'location':button_dict['tetris']['location'],
                                    'type':'button',
                                    'button':'tetris',
                                    'son':False,
                                    'change':False
                                },
                 f'{cwdir}/image/relicrunway/relicrunway.png':{
                                    'location':button_dict['relicrunway']['location'],
                                    'type':'button',
                                    'button':'relicrunway',
                                    'son':False,
                                    'change':False
                                },
                 f'{cwdir}/image/content/exit.png':{
                                    'location':button_dict['exit']['location'],
                                    'type':'button',
                                    'button':'quit',
                                    'son':False,
                                    'change':False
                                },
                f"{cwdir}/image/content/bodystation_false.png":{
                                'location':button_dict['bodystation']['location'],
                                'type':'button',
                                'button':'bodystation',
                                'son':False,
                                'boolean':False,
                                'change':True
                                },
                f"{cwdir}/image/content/bodystation.png":{
                                'location':button_dict['bodystation']['location'],
                                'type':'button',
                                'button':'bodystation',
                                'son':False,
                                'boolean':True,
                                'change':True
                                },
                

                f"{cwdir}/image/common/miro.png":{
                                'type':'fixed',
                                'popup':False,
                                'location':{"pt1": [0.04896,0.901217], "pt2": [0.16896,0.976527]},
                                },
                f"{cwdir}/image/common/xccelerate.png":{
                                'type':'fixed',
                                'popup':False,
                                'location':{"pt1": [0.20386667,0.901217], "pt2": [0.32387333,0.976527]},
                                }, 
                f"{cwdir}/image/content/oscar.png":{
                                'type':'fixed',
                                'popup':False,
                                'location':{"pt1": [0.35877334,0.901217], "pt2": [0.47879,0.976527]},
                                }, 
                f"{cwdir}/image/content/kenneth.png":{
                                'type':'fixed',
                                'popup':False,
                                'location':{"pt1": [0.5137,0.901217], "pt2": [0.6337,0.976527]},
                                }, 
                f"{cwdir}/image/content/hooligans.png":{
                                'type':'fixed',
                                'popup':True,
                                'mother_button':'bodystation',
                                'game':'hooligans',
                                'location':{"pt1": [0.04896, 0.286416], "pt2": [0.6337, 0.877776]}
                                },
                f"{cwdir}/image/content/tetris.png":{
                                'type':'fixed',
                                'popup':True,
                                'mother_button':'bodystation',
                                'game':'tetris',
                                'location':{"pt1": [0.04896, 0.286416], "pt2": [0.6337, 0.877776]}
                                },
                f"{cwdir}/image/content/relicrunway.png":{
                                'type':'fixed',
                                'popup':True,
                                'mother_button':'bodystation',
                                'game':'relicrunway',
                                'location':{"pt1": [0.04896, 0.286416], "pt2": [0.6337, 0.877776]},
                                },
                # variable -> ninja
                f"{cwdir}/image/content/mouse.png":{
                                'type':'variable',
                                'ninja':True,
                                'mother_button':'bodystation',
                                'boolean':True,
                                'keypoint':'r_hand',
                                'location':{"pt1": [0.35195530726256985, 0.7079207920792079], "pt2": [0.4618249534450652, 0.8292079207920792]}
                                },
                f"{cwdir}/image/content/mouse_.png":{
                                'type':'variable',
                                'ninja':True,
                                'mother_button':'bodystation',
                                'boolean':False,
                                'keypoint':'l_hand',
                                'location':{"pt1": [0.35195530726256985, 0.7079207920792079], "pt2": [0.4618249534450652, 0.8292079207920792]}
                                }      
                    }

        return {
                'button_dict':button_dict,
                'img_dict':img_dict,
                }
    else:

        # game!
        # common button dict
        button_dict =  {
                        'menu':{
                            'location':{"pt1": [0.7746741154562383, 0.28386138613], 
                                            "pt2": [0.9683426443202979, 0.59029702969]},
                            'keypoint':'r_hand',
                            'boolean':False,
                            'past':None,
                            'hold_sec': general_hold_sec,
                            'mother':{
                                    'boolean':True,
                                    'past':None,
                                    'hold_sec':mother_hold_sec
                                }  
                            },
                        'exit':
                        {
                            'location':{"pt1": [0,0],
                                     "pt2": [1/3, 1/9]},
                            'keypoint':'l_hand',
                            'boolean':False,
                            'past':None,
                            'hold_sec': fast_hold_sec,
                            'mother':{
                                    'boolean':False,
                                }  
                        },
                        'pause':
                        {
                            'location':{"pt1": [1/3, 0],
                                     "pt2": [2/3, 1/9]},
                            'keypoint':'l_hand',
                            'boolean':False,
                            'past':None,
                            'hold_sec': fast_hold_sec,
                            'mother':{
                                    'boolean':False,
                                }  
                        },
                        'start':
                        {
                            'location':{"pt1": [2/3, 0],
                                     "pt2": [1, 1/9]},
                            'keypoint':'r_hand',
                            'boolean':False,
                            'past':None,
                            'hold_sec': fast_hold_sec,
                            'mother':{
                                    'boolean':False,
                                }  
                        }
                        }
        # img_dict
        img_dict = {
                f"{cwdir}/image/{game}/instruction.png":{
                                    'type':'fixed',
                                    'popup':False,
                                    'location':{"pt1": [0, 0], "pt2": [1, 1/9]}
                                    },
                # button ->change/son
                 f"{cwdir}/image/{game}/menu.png":{
                                'type':'button',
                                'location':{"pt1": [0.7746741154562383, 0.38386138613], 
                                            "pt2": [0.9683426443202979, 0.49029702969]},
                                'button':'menu',
                                'son':False,
                                'change':False
                                },
                f'{cwdir}/image/{game}/exit.png':{
                                    'location':button_dict['exit']['location'],
                                    'type':'button',
                                    'button':'exit',
                                    'son':True,
                                    'mother_button':'menu',
                                    'change':False,
                                },
                f'{cwdir}/image/{game}/pause.png':{
                                    'location':button_dict['pause']['location'],
                                    'type':'button',
                                    'button':'pause',
                                    'son':True,
                                    'mother_button':'menu',
                                    'change':False
                                },

                f'{cwdir}/image/{game}/start.png':{
                                    'location':button_dict['start']['location'],
                                    'type':'button',
                                    'button':'start',
                                    'son':True,
                                    'mother_button':'menu',
                                    'change':False,
                                    },
                # fixed -> popup 
                f"{cwdir}/image/{game}/{game}.png":{
                                'type':'fixed',
                                'popup':False,
                                'location':{"pt1": [0.7418435754189944, 0.7798019801980198], "pt2": [1, 1]}
                                },
                f"{cwdir}/image/common/miro.png":{
                                'type':'fixed',
                                'popup':False,
                                'location':{"pt1": [0.7746741154562383, 0.13138613861386139], "pt2": [0.9683426443202979, 0.22544554455445543]}
                                }, 
                f"{cwdir}/image/common/xccelerate.png":{
                                'type':'fixed',
                                'popup':False,
                                'location':{"pt1": [0.7746741154562383, 0.25514851485148514], "pt2": [0.9683426443202979, 0.3541584158415842]}
                                },
                # variable -> ninja
                f"{cwdir}/image/common/bodystation.png":{
                                'type':'variable',
                                'ninja':False,
                                'keypoint':'neck',
                                'location':{"pt1": [0.3128491620111732, 0.7227722772277227], "pt2": [0.5493482309124768, 0.8292079207920792]}
                                },
                f"{cwdir}/image/{game}/l_hand.png":{
                                'type':'variable',
                                'ninja':False,
                                'keypoint':'l_hand',
                                'location':{"pt1": [0.35195530726256985, 0.7079207920792079], "pt2": [0.4618249534450652, 0.8292079207920792]}
                                },
                f"{cwdir}/image/{game}/r_hand.png":{
                                'type':'variable',
                                'ninja':False,
                                'keypoint':'r_hand',
                                'location':{"pt1": [0.35195530726256985, 0.7079207920792079], "pt2": [0.4618249534450652, 0.8292079207920792]}
                                },
                }
                    
        return {
                'button_dict':button_dict,
                'img_dict':img_dict
                }

def pause_button(game,window_width,window_height):
        if game in ['hooligans','relicrunway']:
                print("**************Press esc(pause)")
                pyautogui.press('esc')

        elif game == 'tetris':
                print("**************Press p(pause)")
                pyautogui.press('p')
        else:
            pass

def start_button(game,window_width,window_height):
    if game in ['hooligans','relicrunway']:
            print("**************close ad")
            pyautogui.click(x=int(window_width*0.9409722222222222),
                            y=int(window_height*0.8211111111111111))

            print("**************start/restart game")
            pyautogui.click(x=int(window_width*0.6729166666666667),
                            y=int(window_height*0.7033333333333334))
    
    elif game == 'tetris':
            print("**************start/restart game")
            pyautogui.press('space')
    else:
        pass

def exit_button(driver):
        driver.close()
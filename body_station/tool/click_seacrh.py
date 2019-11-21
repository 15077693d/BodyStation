import pyautogui 
import time
import keyboard
from selenium import webdriver
import json
from argparse import ArgumentParser

name = input('what is your file name?')
game = input('what is the game?')
# window
window_width = pyautogui.size()[0]
window_height = pyautogui.size()[1] 

target_width = int(window_width*0.5)
target_height =  int(window_height*0.5)

game_dict = {
    0:'hooligans',
    1:'relicrunway',
    2:'tetris'
}
if game == 'general':
    click_dict={}
else:
    click_dict = {}
    click_dict[game] = {}
while True:
    ans= input('Continue?')
    if ans=='1':
        break
    elif ans=='2':
        game = game_dict[input('what is this game?(0:hooligans,1:relicrunway,2:tetris)')]
        click_dict[game] = {}
    print('Start move your mouse!')
    time.sleep(4)
    x,y = pyautogui.position()
    pyautogui.click(x=x,y=y)
    print('detected position!')
    window_width = pyautogui.size()[0]
    window_height = pyautogui.size()[1] 
    function = input('what is the fuction of this click?')
    print(f'\n**********store location: x={x/window_width},y={y/window_height}')
    print(f'function in {game}: {function}')
    if game =='general':
        click_dict[function] = [x/window_width,y/window_height]
    else:
        click_dict[game][function] = [x/window_width,y/window_height]

with open(f'./click_data/{name}.json','w') as doc:
    json.dump(click_dict,doc)
   
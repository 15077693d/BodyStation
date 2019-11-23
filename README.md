# BodyStation
![Alt Text](https://github.com/15077693d/readme_image/blob/master/bodystation/bodystation.jpeg)

# Introduction
- Game controller base on human movement
- 18 body keypoints detection by CNN model(**Posenet**) which is implemented by **rwightman**
- User Interface is implemented using **Opencv**
- Keyboard and mouse is connected by **PyAutoGUI**
- Web Browser Automation by **Selenium**
- Coordinate Checking and data analysis using **Pandas**

# Installation
- Clone or download this repository
- Google Chrome version: 78/ Firefox Browser version: 70
- Install required packages in requirements.txt

```
pip install -r requirements.txt
```
#### Arguments

 ``--argument`` : **Default | Options | Explanation**

------------
``--game`` : content | test/content/hooligans/tetris/relicrunway | -

``--output_df`` : False | True/False | Output movement data to folder``motion_data`` 

``--useGPU`` : False | True/False | -

``--driver`` : chromedrivermac |  A+B | -

 **A : Web driver name (Firefox: geckodriver/Google Chrome: chromedriver)
 B : Operation system name (linx/mac/win)**
- Run ```main.py``` in folder ```body_station```
- For example, Mac user uses firefox as web browser and activates GPU

```
 cd body_station
 python3 main.py --useGPU True --driver geckodrivermac
```
# Instruction
## Content page
| Button | Description (Hand)                |
| ------------- | ------------------------------ |
| `Exit`   | Teminate program (right)|

- Hold left hand on bodystation logo until "tab here" disappears 
- Hold right hand on target's game logo to access the game

![Alt Text](https://github.com/15077693d/readme_image/blob/master/bodystation/content.gif)

### Exit

- Clone or download this repository
- Google Chrome version: 78/ Firefox Browser version: 70
- Install required packages in requirements.txt

![Alt Text](https://github.com/15077693d/readme_image/blob/master/bodystation/quit.gif)

## Games

| Button | Description (Hand)                |
| ------------- | ------------------------------ |
| `Menu`      | Open Menu (right)      |
| `Start`   |  Start game (right)   |
| `Pause`   | Pause game  (left)   |
| `Exit`   | Exit game to content page  (left)  |

- Hold right hand on menu buttom and menu comes out
- Hold right hand on start buttom and game starts

### Skates Hooligans

| Action | Function              |
| ------------- | ------------------------------ |
| `Walk Left`   | Move left      |
| `Walk Right`  |  Move right   |
| `Jump`   | Move up   |
| `Squat`   | Move down  |


![Alt Text](https://github.com/15077693d/readme_image/blob/master/bodystation/hooligans.gif)

### Tetris

| Action | Function             |
| ------------- | ------------------------------ |
|`Rise left hand`|Move left|
|`Rise right hand`|Move right|
| `Walk Left`   | Rotate block      |
| `Walk Right`  |  Rotate block   |
| `Jump`   | Hard drop   |
| `Squat`   | Soft drop  |

![Alt Text](https://github.com/15077693d/readme_image/blob/master/bodystation/tetris.gif)

### Relic Runway
- Same as Skates Hooligans

# BodyStation
## Introduction
- Game controller base on human movement
- 18 body keypoints detection by CNN model(**Posenet**) which is implemented by **rwightman**
- User Interface is implemented using **Opencv**
- Keyboard and mouse is connected by **PyAutoGUI**
- Web Browser Automation by **Selenium**
- Coordinate Checking and data analysis using **Pandas**

## Installation
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
- For example, Mac user uses Firefox as web browser and activate GPU

```
 cd body_station
 python3 main.py --useGPU True --driver geckodrivermac
```
### Instruction
#### Content
#### Hooligans
#### Tetris
#### Relicrunway
#### Test

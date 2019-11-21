import os,sys
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
import numpy as np
import json

def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
	"""
	@brief      Overlays a transparant PNG onto another image using CV2
	
	@param      background_img    The background image
	@param      img_to_overlay_t  The transparent image to overlay (has alpha channel)
	@param      x                 x location to place the top-left corner of our overlay
	@param      y                 y location to place the top-left corner of our overlay
	@param      overlay_size      The size to scale our overlay to (tuple), no scaling if None
	
	@return     Background image with overlay on top
	"""
	
	bg_img = background_img.copy()
	
	if overlay_size is not None:
		img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

	# Extract the alpha mask of the RGBA image, convert to RGB 
	b,g,r,a = cv2.split(img_to_overlay_t)
	overlay_color = cv2.merge((b,g,r))
	
	# Apply some simple filtering to remove edge noise
	mask = cv2.medianBlur(a,5)

	h, w, _ = overlay_color.shape
	roi = bg_img[y:y+h, x:x+w]

	# Black-out the area behind the logo in our original ROI
	img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(),mask = cv2.bitwise_not(mask))
	
	# Mask out the logo from the logo image.
	img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)

	# Update the original image with our new ROI
	bg_img[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)

	return bg_img

# global constant
def line_select_callback(click,release):
    global image_dict
    image_dict[target_image]={'pt1':(int(click.xdata),int(click.ydata)),
                             'pt2':(int(release.xdata),int(release.ydata))}
    plt.close()

def to_ratio(point_dict, width, height):
    point_dict['pt1'] = (point_dict['pt1'][0]/width,point_dict['pt1'][1]/height)
    point_dict['pt2'] = (point_dict['pt2'][0]/width,point_dict['pt2'][1]/height)
    return point_dict

def onkeypress(event):
    global mode
    global target_image
    if event.key == 'q':
        mode = 'quit'
        plt.close()
    
    if event.key == 'd':
        print('Change mode: delete')
        mode = 'delete'
        plt.close()
        
    if event.key == 'c':
        print('Change mode: create')
        mode = 'create'
        plt.close()
    
    if event.key == 'x':
        print('Change image')
        text = ''
        for i in  range(len(list(image_dict.keys()))):
            text+= f"{i}: {list(image_dict.keys())[i]}\n"
        index = input(f'Which image do you want to add?\n\n{text}')
        target_image =  list(image_dict.keys())[int(index)]
        plt.close()

def toggle_selector(event):
    toggle_selector.RS.set_active(True)

def onclick(event):
    global image_dict
    x = event.xdata
    y = event.ydata
    for url, point_dict in image_dict.items():
        try:
            if point_dict['pt1'][0]< x and rectangle['pt1'][1]< y and rectangle['pt2'][0]> x and rectangle['pt2'][1]> y:
                print('Delete image: ',url)
                point_dict = None
        except:
            pass
    plt.close()


global target_image
global image_dict
mode = 'create'
url_list = ['/Users/15077693d/Desktop/FTDS/GitHub/Miro_Poject_Oscar/body_station/image/content/bodystation2.png',
            '/Users/15077693d/Desktop/FTDS/GitHub/Miro_Poject_Oscar/body_station/image/content/movenow_.png',
            '/Users/15077693d/Desktop/FTDS/GitHub/Miro_Poject_Oscar/body_station/image/content/movenow2.png',
            '/Users/15077693d/Desktop/FTDS/GitHub/Miro_Poject_Oscar/body_station/image/content/relicrunway.png',
            '/Users/15077693d/Desktop/FTDS/GitHub/Miro_Poject_Oscar/body_station/image/hooligans/hooligans.png',
            '/Users/15077693d/Desktop/FTDS/GitHub/Miro_Poject_Oscar/body_station/image/relicrunway/relicrunway.png']
image_dict = {url: None for url in url_list }
target_image = list(image_dict.keys())[0]

while True:
    fig, ax = plt.subplots(1)
    # backgroud
    backgroud = cv2.imread('/Users/15077693d/Desktop/FTDS/GitHub/Miro_Poject_Oscar/body_station/image/backgroud.png')
    backgroud = (np.ones((backgroud.shape[0],backgroud.shape[1],3))*(255.0,255.0,255.0)).astype('uint8')

    # print(backgroud)
    for url, point_dict in image_dict.items():
        try:  
            if point_dict!= None:
                img_to_overlay = cv2.imread(url)
                img_to_overlay = cv2.cvtColor(img_to_overlay, cv2.COLOR_BGR2BGRA)
                img_to_overlay[:, :, 3] = 255   
                overlay_size = (int(point_dict['pt2'][0]-point_dict['pt1'][0]),int(point_dict['pt2'][1]-point_dict['pt1'][1]))
                backgroud = overlay_transparent(backgroud, img_to_overlay, point_dict['pt1'][0], point_dict['pt1'][1], overlay_size=overlay_size)
        except Exception as e:
            print(e)
            pass
    
    print('target_image: ',target_image)
    backgroud = cv2.cvtColor(backgroud, cv2.COLOR_BGRA2RGB)
    plt.imshow(backgroud)
    key = plt.connect('key_press_event',onkeypress)
    if mode == 'create':
        toggle_selector.RS = RectangleSelector(
            ax,line_select_callback,
            drawtype='box',useblit=True,
            button=[1],minspanx=5,minspany=5,
            spancoords='pixels',interactive=True
            )
        bbox = plt.connect('key_press_event', toggle_selector)
        plt.show()
    
    elif mode == 'delete':
        fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()

    else:
        break
height, width, channel = backgroud.shape
for url in list(image_dict.keys()):
    image_dict[url] = to_ratio(image_dict[url], width, height)
name = input("what is the name of file?")
with open(f'/Users/15077693d/Desktop/FTDS/GitHub/Miro_Poject_Oscar/body_station/image/{name}.json','w') as doc:
    json.dump(image_dict,doc)
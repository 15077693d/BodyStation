import numpy as np
import cv2

# posenet
# image procressing

def resize_point(posedata,new_width,new_height,pt1=None,pt2=None,cv2_img=None):
    """
    posedata: cv2_img,1 pose dictionary output from json file
    output: resize_image,new_posedata
    """
    try:
        height = pt2[1] - pt1[1]
        width = pt2[0] - pt1[0]
    except:
        height,width,channel = cv2_img.shape
    keypoints = posedata.keys()
    keypoint_list_x = [round(posedata[keypoint]['x']) for keypoint in keypoints]
    keypoint_list_y = [round(posedata[keypoint]['y']) for keypoint in keypoints]
    keypoint_list_conf = [posedata[keypoint]['conf'] for keypoint in keypoints]

    x_ratio = new_width/width
    y_ratio = new_height/height
    # print("resize_point: ")
    # print("X_ratio: ",x_ratio)
    # print("Y_ratio: ",y_ratio)
    new_keypoint_list_x = np.array(keypoint_list_x)*x_ratio
    new_keypoint_list_y = np.array(keypoint_list_y)*y_ratio
    new_posedata = { list(keypoints)[i]:{'x':new_keypoint_list_x[i],
                                            'y':new_keypoint_list_y[i],
                                            'conf':keypoint_list_conf[i]} for i in range(len(new_keypoint_list_x))}

    if pt1==None:
        resize_image = cv2.resize(cv2_img,(new_width,new_height))
        return resize_image,new_posedata
    else:
        return new_posedata

def zoomin_point(posedata):
    """
    input: posedict: 1 pose dictionary output from json file
    output: pt1,pt2,new_posedict
    """
    keypoints = posedata.keys()
    keypoint_list_x = [round(posedata[keypoint]['x']) for keypoint in keypoints]
    keypoint_list_y = [round(posedata[keypoint]['y']) for keypoint in keypoints]
    keypoint_list_conf = [posedata[keypoint]['conf'] for keypoint in keypoints]
    pt1,pt2 = bounding_box(keypoint_list_x,keypoint_list_y,0.1)
    # if pt1[0]<0:
    #     print('pt1 x<0',pt1,pt2)
    # if pt1[1]<0:
    #     print('pt1 y<0')
    # if pt2[0]<0:
    #     print('pt2 x<0')
    # if pt2[1]<0:
    #     print('pt2 y<0')
    (x1,y1) = pt1
    
    new_keypoint_list_x = [x-x1   for x in keypoint_list_x]
    new_keypoint_list_y = [y-y1 for y in keypoint_list_y]
    new_posedata = { list(keypoints)[i]:{'x':new_keypoint_list_x[i],
                                        'y':new_keypoint_list_y[i],
                                        'conf':keypoint_list_conf[i]} for i in range(len(new_keypoint_list_x))}
    return pt1,pt2,new_posedata


def bounding_box(list_x,list_y,confidence):
        '''
        input -> list_x,list_y,confidence etc.0.1
        output -> pt1 (lefttop) pt2 (rightbottom) etc.x,y
        '''
        max_y = max(list_y)
        min_y = min(list_y)
        max_x = max(list_x)
        min_x = min(list_x)
        margin_y = round((max_y - min_y) * confidence)
        margin_x = round((max_x - min_x) * confidence)
        pt1 = (int(min_x - margin_x), int(min_y - margin_y))
        pt2 = (int(max_x + margin_x), int(max_y + margin_y))
        return (pt1,pt2)

def part_of_body(key_point_list,posedata):
    '''
    [ 'nose','l_eye','r_eye','l_ear','r_ear','l_shoulder','r_shoulder',
    'l_elbow','r_elbow','l_wrist','r_wrist','l_hip','r_hip','l_knee',
    'r_knee','l_ankle','r_ankle','neck']

    '''
    x_list = []
    y_list = []
    for key_point in key_point_list:
        x_list.append(posedata[key_point]['x'])
        y_list.append(posedata[key_point]['y'])
    return (x_list,y_list)

def draw_size(array):
    '''
    input -> array
    output ->  {
                'lineThickness':lineThickness,
                'circle_radius':circle_radius,
                'fontScale':fontScale,
                'space':space,
                'thickness':thickness
                }
    '''
    shape = array.shape  
    area = shape[0]*shape[1] 
             
    if area < 500000:
          # line
            lineThickness = 2
            # circle
            circle_radius = 3
            # text
            fontScale = 0.6
            space = 6
            thickness = 2
    elif area < 1000000:
            # line
            lineThickness = 3
            # circle
            circle_radius = 4
            # text
            fontScale = 0.6
            space = 9
            thickness = 2
    elif area < 5000000:
            # line
            lineThickness = 6
            # circle
            circle_radius = 6
            # text
            fontScale = 2
            space = 10
            thickness = 2
    else:
            # line
            lineThickness = 8
            # circle
            circle_radius = 10
            # text
            fontScale = 2
            space = 10
            thickness = 2
    
    draw_dict = {
                'lineThickness':lineThickness,
                'circle_radius':circle_radius,
                'fontScale':fontScale,
                'space':space,
                'thickness':thickness
                }

    return draw_dict

# Evaluate
def Normalize(array):
    array = np.array(array)
    magnitude = np.sqrt(sum(array**2))
    unit_vector = array/magnitude
    return unit_vector

def rmse(vector1,vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    return np.sqrt(sum((vector1-vector2)**2)/(len(vector1)))

def mse(vector1,vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    return sum((vector1-vector2)**2)/(len(vector1))

def amse(vector1,vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    return sum(abs(vector1-vector2))/(len(vector1))

def weighted_mean_error(weight_list,test_vector,target_vector):
    numerator = 0
    for i in range(len(weight_list)):
        numerator+=weight_list[i]*abs(test_vector[i]-target_vector[i])
    denominator = sum(weight_list)
    return numerator/denominator

def cosine_similarity(vector1,vector2):
   vector1 = np.array(vector1)
   vector2 = np.array(vector2)
   numerator = np.dot(vector1,vector2)
   denominator = np.sqrt(np.sum(vector1**2)*np.sum(vector2**2))
   return numerator/denominator


# body builder
def create_neck(x_l_shoulder,x_r_shoulder,y_l_shoulder,y_r_shoulder):
    x_neck = (x_l_shoulder+x_r_shoulder)/2
    y_neck = (y_l_shoulder+y_r_shoulder)/2
    return [x_neck,y_neck]

def create_hand(x_wrist,y_wrist,x_elbow,y_elbow,e_2_w,w_2_h):
    x_hand = (w_2_h*(x_wrist - x_elbow)/e_2_w)+x_wrist
    y_hand = (w_2_h*(y_wrist - y_elbow)/e_2_w)+y_wrist
    return [x_hand,y_hand]


# body station
def check_person(pose_data):
    # area is big 
    area_amount = []

    for pose_dict in pose_data['poses']:
        list_x = [pose_dict[key]['x'] for key in list(pose_dict.keys())]
        list_y = [pose_dict[key]['y'] for key in list(pose_dict.keys())]
        ((pt1_x,pt1_y),(pt2_x,pt2_y))= bounding_box(list_x,list_y,0.1)
        # area
        area = (pt2_x - pt1_x)*(pt2_y - pt1_y)
        area_amount.append(area)
 
    return pose_data['poses'][area_amount.index(max(area_amount))]

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

if __name__ == "__main__":
  pass

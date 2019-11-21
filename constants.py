keys = ['nose', 'l_eye', 'r_eye', 'l_ear', 'r_ear', 'l_shoulder', 
            'r_shoulder', 'l_elbow', 'r_elbow', 'l_wrist', 'r_wrist', 
            'l_hip', 'r_hip', 'l_knee', 'r_knee', 'l_ankle', 'r_ankle','neck','l_hand','r_hand']

color_BGR = [(60,33,181),(36,84,227),(181,146,33),(81,132,79),(161,179,227),(128,32,5),
                (155,100,0),(123,100,132),(92,8,65),(66,88,127),(210,179,196),
                (191,106,228),(152,151,197),(97,181,33),(128,111,5),
                (59,196,170),(128,68,5),(7,7,145),(13,24,56),(100,100,2)]

color_dict = dict(zip(keys,color_BGR))

line_pair = [('l_wrist','l_elbow'),('l_elbow','l_shoulder'),
            ('r_wrist','r_elbow'),('r_elbow','r_shoulder'),
            ('l_ankle','l_knee'),('l_knee','l_hip'),
            ('r_ankle','r_knee'),('r_knee','r_hip'),
            ('l_eye','l_ear'),('r_eye','r_ear'),
            ('l_shoulder','l_hip'),('r_shoulder','r_hip'),
            ('l_hip','r_hip'),('l_shoulder','r_shoulder'),('l_eye','r_eye'),
            ('l_eye','nose'),('r_eye','nose'),('nose','l_shoulder'),('nose','r_shoulder'),
            ('neck','nose'),('neck','l_shoulder'),('neck','r_shoulder'),
            ('l_wrist','l_hand'),('r_wrist','r_hand')]

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
            'l_hand':1,
            'r_hand':1
            }

punishment = {
            'nose':0,
            'l_eye':0,
            'r_eye':0,
            'l_ear':0,
            'r_ear':0,
            'l_shoulder':0.1,
            'r_shoulder':0.1,
            'l_elbow':0.2,
            'r_elbow':0.2,
            'l_wrist':0.2,
            'r_wrist':0.2,
            'l_hip':0.1,
            'r_hip':0.1,
            'l_knee':0.2,
            'r_knee':0.2,
            'l_ankle':0.2,
            'r_ankle':0.2,
            'neck':0,
            'l_hand':0,
            'r_hand':0
            }
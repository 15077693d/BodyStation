from argparse import ArgumentParser
import os,sys
cwdir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, cwdir +'/')
sys.path.insert(1, cwdir.replace('/body_station',''))
from motion_record import motion_record
from BodyStation import BodyStation
from pose_models import LoadModel
ap = ArgumentParser()
ap.add_argument("--game",type = str, default = "content",help = "test/content/hooligans/tetris/relicrunway")
ap.add_argument("--output_df",type = bool, default = False,help = "True/False")
ap.add_argument("--useGPU",type = bool, default = False,help = "True/False")
ap.add_argument("--driver",type = str, default = 'geckodrivermac',help =  "geckodriverlinx/geckodrivermac/chromedriverwin/chromedriverlinx/chromedrivermac/chromedriverwin")

args = vars(ap.parse_args())
# game list
# 1.hooligans
# 2.tetris
# 3.relicrunway
game_name = args['game']
model_oscar = LoadModel(weight_dir = f"{cwdir.replace('body_station','')}model_",useGPU = args['useGPU'])
while True:
    BodyStation1 = BodyStation(game = game_name,model = model_oscar,useGPU=args['useGPU'],
                                        output_df=args['output_df'],driver_=args['driver'])
    motion_record1 = motion_record(game_name,useGPU=args['useGPU']) 
    game_name = BodyStation1.run(motion_record1)
    if game_name == 'exit':
            break



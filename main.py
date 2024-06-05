import os
from Preprocess import Enhance_contrast
from Vesicle_detection import Multi_template_match
# from Vesicle_detection import CHT
# from Vesicle_detection import Template_match
# from batch_run import run_batch_files
# from utils import get_template, load_template
# import argparse
import numpy as np
import time
from batch_run import run_batch_files_templates

template1 = np.load('Templates/template_656, 640, 71, 71.npy')
template2 = np.load('Templates/Project_Whole Plate1_1024x1024_200Hz_1%Laser_800gain_B_5_R1.tif_enhance_482_20_56_56.npy')
template3 = np.load('Templates/1024x1024 - 4 point_no-z-stack - split 5 rows rows only_TileScan 1_C_11_R2.npy')
templates = [template1, template2, template3]
file_folder= 'Data/Test_0517'
PlateName='Plate_2024605'

def main():
    folder_path = f"Results_{PlateName}"
    os.makedirs(folder_path, exist_ok=True)
    # Record the start time
    start_time = time.time()
    run_batch_files_templates(file_folder, templates, PlateName, \
                    min_scale=0.3, max_scale=4, intervals=100, threshold = 0.5, Preprocess=False)

    # Record the end time
    end_time = time.time()

    # Calculate the running time
    running_time = end_time - start_time

    print("Script execution time:", running_time, "seconds")

if __name__=="__main__":
    main()
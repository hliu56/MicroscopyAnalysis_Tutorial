import os
from Preprocess import preprocess
from Preprocess import preprocess_enhance
from Vesicle_detection import CHT
from Vesicle_detection import Template_match
from batch_run import run_batch_files
from utils import get_template, load_template
import argparse
import numpy as np
from batch_run import run_batch_files_templates


# def main(method):
#     data_folder = input('Please specify the data folder: (e.g. Data/)')
#     filename = input('Please specify the file name: (e.g. seq0066.tif)')
#     PlateName='Plate1'

#     input_path = data_folder+filename

#     if method == 'CHT':
#         image_analysis = preprocess(input_path)
#         CHT(filename, image_analysis)
#     if method == 'TemplateMatch':
#         image_analysis = preprocess_enhance(input_path, 15, 45)
#         x, y, w, h = map(int, input('Please enter x, y, width, height (comma-separated): ').split(','))
#         template = get_template(filename, image_analysis, x, y, w, h)
#         Template_match(filename, image_analysis, template, min_scale=0.5, max_scale=1.2, intervals=10, threshold = 0.6)
#     if method == 'TemplateMatch_batch':
#         file_template = load_template(filename)
#         run_batch_files(data_folder, file_template, PlateName, \
#                 min_scale=0.3, max_scale=4.5, intervals=100, threshold = 0.5)




# if __name__=="__main__":
#     parser = argparse.ArgumentParser(description="Choosing different type of method")
#     parser.add_argument("method", choices=["CHT", "TemplateMatch", "TemplateMatch_batch"], help="Type of method")

#     args = parser.parse_args()
#     main(args.method)
template1 = np.load('Templates/template_656, 640, 71, 71.npy')
template2 = np.load('Templates/Project_Whole Plate1_1024x1024_200Hz_1%Laser_800gain_B_5_R1.tif_enhance_482_20_56_56.npy')
template3 = np.load('Templates/1024x1024 - 4 point_no-z-stack - split 5 rows rows only_TileScan 1_C_11_R2.npy')
templates = [template1, template2, template3]
file_folder= '/Users/haoliu/Documents/Hao/Fordham/Microscopy/Data/04-19-2024'
PlateName='Plate_20240423_1'

def main():
    folder_path = f"Results_{PlateName}"
    os.makedirs(folder_path, exist_ok=True)
    # file_template='Templates/Project_Whole Plate1_1024x1024_200Hz_1%Laser_800gain_B_5_R1.tif_enhance_482_20_56_56.npy'
    # Record the start time
    import time
    start_time = time.time()
    # file_template = load_template(template)
    run_batch_files_templates(file_folder, templates, PlateName, \
                    min_scale=0.3, max_scale=4, intervals=100, threshold = 0.5)

    # Record the end time
    end_time = time.time()

    # Calculate the running time
    running_time = end_time - start_time

    print("Script execution time:", running_time, "seconds")

if __name__=="__main__":
    main()
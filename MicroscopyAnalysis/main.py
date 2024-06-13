import os
import time
import numpy as np
import argparse
from MicroscopyAnalysis.batch_run import run_batch_files_templates

def main(file_folder, templates, PlateName):
    '''
    This is the main python module to run vesicles detection on batch images.
    '''
    folder_path = f"Results_{PlateName}"
    os.makedirs(folder_path, exist_ok=True)
    # Record the start time
    start_time = time.time()
    run_batch_files_templates(file_folder, templates, PlateName, \
                    min_scale=0.3, max_scale=4, intervals=100, threshold=0.5, Preprocess=False)

    # Record the end time
    end_time = time.time()

    # Calculate the running time
    running_time = end_time - start_time

    print("Script execution time:", running_time, "seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run vesicles detection on batch images.')
    parser.add_argument('file_folder', type=str, help='The folder containing the image files. Example: Data/Test_0517')
    parser.add_argument('PlateName', type=str, help='The name of the plate. Example: Plate_2024605')
    parser.add_argument('--templates', type=str, nargs='+', help='Optional: Paths to the template files.')

    args = parser.parse_args()

    if args.templates:
        # Load user-specified templates
        templates = [np.load(template_file) for template_file in args.templates]
    else:
        # Load default templates (hardcoded paths)
        template1 = np.load('Templates/template_656_640_71_71.npy')
        template2 = np.load('Templates/Project_Whole_Plate1_1024x1024_200Hz_1%Laser_800gain_B_5_R1.tif_enhance_482_20_56_56.npy')
        template3 = np.load('Templates/1024x1024_4_point_no-z-stack_split_5_rows_rows_only_TileScan_1_C_11_R2.npy')
        templates = [template1, template2, template3]

    main(args.file_folder, templates, args.PlateName)

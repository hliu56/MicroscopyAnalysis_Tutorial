

import cv2
import pandas as pd
import numpy as np
from Preprocess import Enhance_contrast
from Vesicle_detection import Multi_template_match, Template_match
from utils import load_template
from utils import calculate_area
import os


def run_batch_files(file_folder, file_template, PlateName, 
                    min_scale=0.2, max_scale=1.5, intervals=10, threshold = 0.5):
    
    filenames = []
    vesicle_numbers = []

    # Check if the file_folder exists
    if os.path.exists(file_folder):
        # Get the list of files in the folder
        files = os.listdir(file_folder)
        # Remove '.DS_Store' from the list of files if it exists
        # This file will accidently added when copy and paste files into folder
        if '.DS_Store' in files:
            files.remove('.DS_Store')

        for file in files:
            filepath = os.path.join(file_folder, file)
            template = load_template(file_template)
            # image_analysis, image_ori, filename = preprocess_enhance(filepath, filter_size1, filter_size2, image_type='RGB')
            image_analysis, image_ori, filename = Enhance_contrast(filepath, PlateName, image_type='RGB')

            results, number_vesicles = Template_match(filename, image_ori, image_analysis, template, \
                                    min_scale=min_scale, max_scale=max_scale, intervals=intervals, threshold = threshold)
            
            # Define the column names
            columns1 = ["x_center", "y_center", "box_length", "score"]
            filenames.append(file)
            print(file)
            vesicle_numbers.append(number_vesicles)

            # Create a DataFrame using the data and column names
            df1 = pd.DataFrame(results, columns=columns1)

            # Save the DataFrame to a CSV file
            df1.to_csv("Results/"+f"{filename}.csv", index=False)

        df2 = pd.DataFrame({'Filename': filenames, 'Vesicle_Number': vesicle_numbers})
        df2.to_csv("Results/"+f"{PlateName}_VesiclesNumber.csv", index=False)
    else:
        print(f"Folder '{file_folder}' does not exist.")

def run_batch_files_templates(file_folder, templates, PlateName, 
                    min_scale=0.2, max_scale=1.5, intervals=10, threshold = 0.5, Preprocess=True, sigma=50):
    
    filenames = []
    vesicle_numbers = []

    # Check if the file_folder exists
    if os.path.exists(file_folder):
        # Get the list of files in the folder
        files = os.listdir(file_folder)
        # Remove '.DS_Store' from the list of files if it exists
        # This file will accidently added when copy and paste files into folder
        if '.DS_Store' in files:
            files.remove('.DS_Store')

        dfs = []
        for file in files:
            filepath = os.path.join(file_folder, file)
            # template = load_template(file_template)
            # image_analysis, image_ori, filename = preprocess_enhance(filepath, filter_size1, filter_size2, image_type='RGB')
            if Preprocess:
                image_analysis, image_ori, filename = Enhance_contrast(filepath, PlateName, image_type='RGB', sigma_size=sigma)
            else:
                image_ori = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                filename = os.path.basename(filepath)
                image_analysis = image_ori

            results, number_vesicles = Multi_template_match(filename, image_ori, image_analysis, templates, PlateName,\
                                    min_scale=min_scale, max_scale=max_scale, intervals=intervals, threshold = threshold)
            
            # Define the column names
            columns1 = ["x_center", "y_center", "box_length", "score"]
            filenames.append(file)
            print(file)
            vesicle_numbers.append(number_vesicles)

            # Create a DataFrame using the data and column names
            df1 = pd.DataFrame(results, columns=columns1)

            # Save the DataFrame to a CSV file
            df1.to_csv(f"Results_{PlateName}/"+f"{filename}.csv", index=False)
            # Calculate vesicles area here?
            if number_vesicles == 0.:
                total_area = 0.
                area_percent = 0.
                num_rows = len(df1)
                # print('None vesicles found')
                # Create a DataFrame containing filename, total area, number of rows, and area percent
                area_df = pd.DataFrame({
                    'filename': [filename],
                    'num_vesicles': [num_rows],
                    'area_vesicles': [total_area],  
                    'area_percent': [area_percent]
                })
                dfs.append(area_df)
                
            else:
                df1['area'] = np.pi * (df1['box_length'] / 2)**2
                total_area = df1['area'].sum()
                area_percent = total_area / (image_analysis.shape[0] * image_analysis.shape[1])
                num_rows = len(df1)
                # print('None vesicles found')
                # Create a DataFrame containing filename, total area, number of rows, and area percent
                area_df = pd.DataFrame({
                    'filename': [filename],
                    'num_vesicles': [num_rows],
                    'area_vesicles': [total_area],  
                    'area_percent': [area_percent]
                })
                dfs.append(area_df)

        df2 = pd.concat(dfs, ignore_index=True)
        # df2 = pd.DataFrame({'Filename': filenames, 'Vesicle_Number': vesicle_numbers})
        df2.to_csv(f"Results_{PlateName}/"+f"{PlateName}_VesiclesSummary.csv", index=False)
    else:
        print(f"Folder '{file_folder}' does not exist.")
    

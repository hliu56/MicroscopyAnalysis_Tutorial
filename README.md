# MicroscopyAnalysis_Tutorial

This repository is used to showcase the basic usage of automated microscopy image analysis 
The automated iamge analysis pipeline include:
- Image preprocessing
- Vesicle detection
- Batch processing

# Installation

Follow these steps to set up the Microscopy Analysis Tutorial on your computer:

### Step 1: Install Python

#### Option 1: 
If you don't have Anaconda installed, download and install it from [anaconda.com](https://www.anaconda.com/products/distribution). Anaconda includes Python and Jupyter Notebook.
#### Option 2:
If you don't have Python installed, download and install it from [python.org](https://www.python.org/downloads/). Make sure to check the option to add Python to your PATH during installation.

We recommend to install Anaconda for non-coding experience user.

### Step 2: Download the Project Files

1. Go to the [GitHub repository](https://github.com/hliu56/MicroscopyAnalysis_Tutorial).
2. Click the green "Code" button and select "Download ZIP".
3. Extract the downloaded ZIP file to a folder on your computer.

### Step 3: Install Dependencies

#### Option 1: install dependencies from Anaconda

User should only need to install these packages: matplotlib numpy pandas scikit-image opencv-python
Open Anaconda, search the pacakges in 'Not installed' menu, check the packages and click apply. 
![Installation packages Example](https://github.com/hliu56/MicroscopyAnalysis_Tutorial/blob/main/Example/InstallationExample.png)

#### Option 2: install dependencies from terminal

1. Open a command prompt (Windows) or terminal (macOS/Linux).
2. Navigate to the folder where you extracted the project files. For example:
   ```bash
   cd path/to/MicroscopyAnalysis_Tutorial
3. Install the required Python packages by running:
   ```bash
   pip install matplotlib numpy pandas scikit-image opencv-python
   ```
   User should only need to install the above packages, if you need to know the full environment dependencies, you can check it in `MicroscopyAnalysis/requirements.txt`.
   

### Step 4: Run the scripts

1. Run the main script in terminal., use the following command in your terminal:

```bash
python main.py <file_folder> <PlateName> [--templates <template_file1> <template_file2> ... <template_fileN>]
```

#### Examples:
- Using Default Templates:
  ```bash
  python main.py Data/Test_0517 Plate_2024605
  ```
- Using Custom Templates:
  ```bash
  python main.py Data/Test_0517 Plate_2024605 --templates Templates/custom_template1.npy Templates/custom_template2.npy


2. Run the main script in jupyter notebook. Copy the code in the Usage section(Next section) and run.

## Usage

This section show the minimal code examples illustrating how to use the functions.
You can also check the [documentation site](https://hliu56.github.io/MicroscopyAnalysis_Tutorial/#).

Here we provide some example code to analysis batch images from a folder. Three parameters are needed for `main` function.
`file_folder`: The folder stored the images that needed to be analyzed
`templates`: A list of templates files
`PlateName`: Used for saving results

```python
import os
import time
import numpy as np

from MicroscopyAnalysis.batch_run import run_batch_files_templates
from MicroscopyAnalysis.main import main

# Adjust paths to the templates
template1 = np.load(os.path.join('Templates', 'template_656, 640, 71, 71.npy'))
template2 = np.load(os.path.join('Templates', 'Project_Whole Plate1_1024x1024_200Hz_1%Laser_800gain_B_5_R1.tif_enhance_482_20_56_56.npy'))
template3 = np.load(os.path.join('Templates', '1024x1024 - 4 point_no-z-stack - split 5 rows rows only_TileScan 1_C_11_R2.npy'))
templates = [template1, template2, template3]

# Adjust the path to the data folder
file_folder = os.path.join('Data', 'Test_0517')
PlateName = 'Plate_2024605'

# Example usage
main(file_folder, templates, PlateName)
```

![Microscopy Analysis Example](https://github.com/hliu56/MicroscopyAnalysis_Tutorial/blob/main/Example/PictureExample.png)

## License

Distributed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
See the `LICENSE` file for more information.

## Contact

Academic collaborations and extensions/improvements by the community are encouraged. Please contact [HL](hliu23@fordham.edu) by email if you have questions.

## Citations

TBD

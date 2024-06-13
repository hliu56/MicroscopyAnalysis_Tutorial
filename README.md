# MicroscopyAnalysis_Tutorial

This repository is used to showcase the basic usage of automated microscopy image analysis 
The automated iamge analysis pipeline include:
- Image preprocessing
- Vesicle detection
- Batch processing

# Installation

Follow these steps to set up the Microscopy Analysis Tutorial on your computer:

### Step 1: Install Python

If you don't have Python installed, download and install it from [python.org](https://www.python.org/downloads/). Make sure to check the option to add Python to your PATH during installation.

### Step 2: Download the Project Files

1. Go to the [GitHub repository](https://github.com/hliu56/MicroscopyAnalysis_Tutorial).
2. Click the green "Code" button and select "Download ZIP".
3. Extract the downloaded ZIP file to a folder on your computer.

### Step 3: Install Dependencies

1. Open a command prompt (Windows) or terminal (macOS/Linux).
2. Navigate to the folder where you extracted the project files. For example:
   ```bash
   cd path/to/MicroscopyAnalysis_Tutorial

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

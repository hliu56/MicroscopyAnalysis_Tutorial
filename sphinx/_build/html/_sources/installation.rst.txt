.. _installation:

Installation
============

Follow these steps to set up the Microscopy Analysis Tutorial on your computer:

Step 1: Install Python
----------------------

**Option 1:**

If you don't have Anaconda installed, download and install it from [Anaconda](https://www.anaconda.com/products/distribution). Anaconda includes Python and Jupyter Notebook.

**Option 2:**

If you don't have Python installed, download and install it from [Python.org](https://www.python.org/downloads/). Make sure to check the option to add Python to your PATH during installation.

We recommend installing Anaconda for users without coding experience.

Step 2: Download the Project Files
----------------------------------

1. Go to the [GitHub repository](https://github.com/hliu56/MicroscopyAnalysis_Tutorial).
2. Click the green "Code" button and select "Download ZIP".
3. Extract the downloaded ZIP file to a folder on your computer.

Step 3: Install Dependencies
----------------------------

**Option 1: Install dependencies from Anaconda**

Users should only need to install these packages: `matplotlib`, `numpy`, `pandas`, `scikit-image`, `opencv-python`.

Open Anaconda, search the packages in the 'Not installed' menu, check the packages, and click apply.

.. image:: https://raw.githubusercontent.com/hliu56/MicroscopyAnalysis_Tutorial/blob/main/Example/InstallationExample.png
    :alt: Installation packages example

**Option 2: Install dependencies from terminal**

1. Open a command prompt (Windows) or terminal (macOS/Linux).
2. Navigate to the folder where you extracted the project files. For example:
   `cd path/to/MicroscopyAnalysis_Tutorial`
3. Install the required Python packages by running:
   `pip install matplotlib numpy pandas scikit-image opencv-python`

   User should only need to install the above packages, if you need to know the full environment dependencies, you can check it in `MicroscopyAnalysis/requirements.txt`.

Step 4: Run the scripts
----------------------------------

1. Run the main script in jupyter notebook. Copy the code in the Usage section(Next section) and run.

2. Run the main script in terminal, use the following command in your terminal:

`python main.py <file_folder> <PlateName> [--templates <template_file1> <template_file2> ... <template_fileN>]`

**Examples:**

* Using Default Templates:

    `python main.py Data/Test_0517 Plate_2024605`

* Using Custom Templates:

    `python main.py Data/Test_0517 Plate_2024605 --templates Templates/custom_template1.npy Templates/custom_template2.npy`



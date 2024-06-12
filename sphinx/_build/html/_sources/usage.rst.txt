Usage Examples
==============

Basic Usage
-----------

Here is a simple example of how to use the main function of the package:

.. code-block:: python

    import os
    import numpy as np
    import time
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

    

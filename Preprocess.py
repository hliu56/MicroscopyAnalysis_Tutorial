import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import Image_blur
from utils import Image_enhance
from skimage.filters import gaussian

from datetime import datetime
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

def Enhance_contrast(path, PlateName, image_type, sigma_size=50):
    '''
    This function is used to preprocessing the original images, 
    include several steps:
    background subtraction
    CLAHE contrast enhance
    noise suppression
    '''
    # Load the TIFF image
    if image_type == 'gray':
        image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    elif image_type == 'RGB':
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        raise ValueError("Unsupported image type. Please specify either 'gray' or 'RGB'.")
    
    filename = os.path.basename(path)
    # Background subtraction
    background_gaussian = gaussian(image, sigma=sigma_size, preserve_range=True)
    image_gaussian = image - background_gaussian
    image_gaussian = np.clip(image_gaussian, 0, 255).astype(np.uint8)
    # Enhance contrast
    clahe = cv2.createCLAHE(clipLimit=5)
    image_clahe = clahe.apply(image_gaussian)
    # Noise suppression
    std_dev=0.5
    noise_suppressed = cv2.GaussianBlur(image_clahe, (0, 0), std_dev)

    fig, axs = plt.subplots(1, 5, figsize=(10,10))
    
    # Plot original image in the first subplot
    axs[0].imshow(image, cmap='gray')
    axs[0].set_title("Original")
    axs[0].axis('off')
    
    # Plot background (gaussian) in the second subplot
    axs[1].imshow(background_gaussian, cmap='gray')
    axs[1].set_title("Background (gaussian)")
    axs[1].axis('off')
    
    # Plot background subtracted image in the third subplot
    axs[2].imshow(image_gaussian, cmap='gray')
    axs[2].set_title("Background subtracted")
    axs[2].axis('off')
    
    axs[3].imshow(image_clahe, cmap='gray')
    axs[3].set_title("CLAHE enhance")
    axs[3].axis('off')
    
    axs[4].imshow(noise_suppressed, cmap='gray')
    axs[4].set_title("Suppress noise")
    axs[4].axis('off')

    plt.tight_layout()
    plt.savefig(f'Results_{PlateName}/'+f'{filename}_enhance_{formatted_datetime}.png')
    plt.close(fig)

    return noise_suppressed, image, filename



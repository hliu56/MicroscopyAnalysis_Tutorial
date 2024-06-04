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

def preprocess(path):
    # Load the TIFF image
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    filename = os.path.basename(path)
    # Convert to floating-point for scaling and normalization
    uint16_image_float = image.astype(np.float32)

    # Scale the pixel values to the range [0, 1] or [0, 255] depending on your needs
    scaled_image = (uint16_image_float - np.min(uint16_image_float)) / (np.max(uint16_image_float) - np.min(uint16_image_float))

    # Convert back to uint8 if needed (depends on the operation you plan to perform)
    scaled_image_uint8 = (scaled_image * 255).astype(np.uint8)

    min_intensity = np.min(scaled_image_uint8)
    max_intensity = np.max(scaled_image_uint8)
    stretched_image = 255 * (scaled_image_uint8 - min_intensity) / (max_intensity - min_intensity)

    # Normalize the stretched_image values to the range [0, 255]
    stretched_image_normalized = 255- (stretched_image - np.min(stretched_image)) / (np.max(stretched_image) - np.min(stretched_image)) * 255
    # color flipped
    # stretched_image_normalized_flip =  (stretched_image - np.min(stretched_image)) / (np.max(stretched_image) - np.min(stretched_image)) * 255

    # Convert to uint8
    stretched_image_uint8 = stretched_image_normalized.round().astype(np.uint8)
    denoised_image = cv2.fastNlMeansDenoising(stretched_image_uint8, None, h=10, searchWindowSize=21)

    # Display the results
    plt.figure(figsize=(15, 5))
    plt.subplot(121), plt.imshow(scaled_image_uint8, cmap='gray',label='Original image'), plt.title('Original Image')
    plt.subplot(122), plt.imshow(denoised_image, cmap='gray',label='Denoised image'), plt.title('After preprocess')
    plt.tight_layout()
    plt.savefig('Results/'+f'{filename}_preprocess_{formatted_datetime}.png')
    # plt.show()
    return denoised_image

def preprocess_enhance(path, filter_size1, filter_size2, image_type):
    '''
    This function is used to enhance the contrast between signal and background
    Parameters:
    - path: specify the file path
    - filter_size1: the filter_size for gaussian blur
    - filter_size2: the filter_size for image enhance

    Returns:
    - Enhanced image in uint8 format
    '''
    # Load the TIFF image
    if image_type == 'gray':
        image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    elif image_type == 'RGB':
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        raise ValueError("Unsupported image type. Please specify either 'gray' or 'RGB'.")
    
    filename = os.path.basename(path)

    # Normalize uint16 image values to 0-1 range
    normalized_image = image / np.max(image)
    # Apply Gaussian blur
    blurred_image = Image_blur(normalized_image, filter_size1)

    enhanced_image, _ = Image_enhance(blurred_image, filter_size = filter_size2)# watch out how many output?
    enhanced_image_uint8 = (enhanced_image * 255).astype(np.uint8)

    # Display the results
    plt.figure(figsize=(15, 5))
    plt.subplot(121), plt.imshow(image, cmap='gray',label='Original image'), plt.title('Original Image')
    plt.subplot(122), plt.imshow(enhanced_image_uint8, cmap='gray',label='Enhanced iamge'), plt.title('After enhance')
    plt.tight_layout()
    plt.savefig('Results/'+f'{filename}_enhance_{formatted_datetime}.png')
    # plt.show()
    plt.close()

    return enhanced_image_uint8, image, filename

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
    # Adjust layout for better visualization
    plt.tight_layout()
    
    plt.savefig(f'Results_{PlateName}/'+f'{filename}_enhance_{formatted_datetime}.png')
    # plt.show()
    plt.close(fig)
    # Show the plot
    # plt.show()

    return noise_suppressed, image, filename



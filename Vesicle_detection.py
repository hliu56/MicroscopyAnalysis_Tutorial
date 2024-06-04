import cv2
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import matplotlib.patches as patches
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H")
#formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H")

def CHT(filename, input_image):

    image = input_image
    output = image.copy()
    # image = cv2.medianBlur(image,5)
    height, width = image.shape[:2]
    maxRadius = int(1.1*(width/4)/2)
    minRadius = int(0.9*(width/12)/2)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(image=image, 
                            method=cv2.HOUGH_GRADIENT, 
                            dp=0.7, 
                            minDist=2*minRadius,
                            param1=10,
                            param2=30,
                            minRadius=minRadius,
                            maxRadius=maxRadius                           
                            )

    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circlesRound = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circlesRound:
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)

        plt.imshow(output, cmap='gray')
        plt.savefig('Results/'+f'{filename}_CHT_{formatted_datetime}.png')
        print('Vesicles found')
    else:
        print ('No Vesicles found')

    
def Template_match(filename, original_image, image, template, min_scale=0.5, max_scale=1.2, intervals=10, threshold = 0.6):
    '''
    threshold is to specify the criteria for choosing matching shape
    '''
    # Generate a linear space of scales
    scales = np.linspace(min_scale, max_scale, intervals)
    scales = np.round(scales, decimals=2)
    h_o, w_o = image.shape[0], image.shape[1]

    x_center=[]
    y_center=[]
    scale_select=[]
    match_value=[]

    #  iterate different templates?
    for scale in scales:
        template_scale = cv2.resize(template, None, fx=scale, fy=scale)
        h, w = template_scale.shape[0], template_scale.shape[1]
        if w >= w_o or h >= h_o:
            break

        result = cv2.matchTemplate(image, template_scale, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)

        x_center.extend(loc[1] + w/2)
        y_center.extend(loc[0] + h/2)
        scale_select.extend(w + 0*loc[0])
        match_value.extend(result[loc[0], loc[1]])
   
    x_center=np.array(x_center)
    y_center=np.array(y_center)
    scale_select=np.array(scale_select)
    match_value=np.array(match_value)

    # Remove overlapping bounding boxes
    mask = np.zeros(image.shape, dtype = float)
    index = np.argsort(match_value)
    match_sort = match_value[index[::-1]]
    x_s = [int(x) for x in x_center[index[::-1]]]
    y_s = [int(x) for x in y_center[index[::-1]]]
    bbox = [int(x) for x in scale_select[index[::-1]]]

    x_center_n = []
    y_center_n=[]
    bbox_n=[]
    match_value_n=[]

    for x, y, b, m in zip(x_s, y_s, bbox, match_sort):
        if mask[y,x] == 0:
            y_u=int(y-b/2)
            y_d=int(y+b/2)
            x_l=int(x-b/2)
            x_r=int(x+b/2)
            # cope with boundaries
            if y_u<0: y_u=0
            if x_l<0: x_l=0
            if y_d>mask.shape[0]: y_d=mask.shape[0]
            if x_r>mask.shape[1]: x_r=mask.shape[1]

            mask[y_u:y_d, x_l:x_r] = m
            x_center_n.append(x)
            y_center_n.append(y)
            bbox_n.append(b)
            match_value_n.append(m)
    # Filtered values of center in x,y and bounding box size
    if len(match_value_n) < 1:
        match_results = None
        len_match_results = 0.
        print('None vesicles found')
    else: 
        match_results = np.stack((np.array(x_center_n), np.array(y_center_n),
                                np.array(bbox_n), np.array(match_value_n)), axis = 1)
        print(f'{len(match_results)} vesicles found')         
        len_match_results = len(match_results)

        #result_image = image.copy()

        # # Loop over all the bounding boxes detected to draw rectangles
        # for x, y, s, _ in match_results:
        #     x1 = int(x - s / 2)
        #     y1 = int(y - s / 2)
        #     x2 = int(x + s / 2)
        #     y2 = int(y + s / 2)

        #     # Draw rectangle on the result image
        #     cv2.rectangle(result_image, (x1, y1), (x2, y2), (255, 255, 0), 5)
        # # Assuming result_image and mat_image are your images with rectangles and the original image
        # blended_image = cv2.addWeighted(result_image, 0.1, image, 0.9, 0)
        # Create a figure and axis
        fig, ax = plt.subplots()

        # Display the image
        ax.imshow(original_image, cmap='gray')
        ax.set_title(filename)

        # Plot each box
        for box in match_results:
            x_center, y_center, length = box[:3]
            x_min = x_center - length / 2
            y_min = y_center - length / 2
            rect = patches.Rectangle((x_min, y_min), length, length, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

        # Show the plot
        plt.gca().set_aspect('equal', adjustable='box')

        # Display the result image with rectangles
        # plt.imshow(blended_image, cmap='gray')
        plt.savefig('Results/'+f'{filename}_TemplateMatch_{formatted_datetime}.png')
        # plt.title('Detected Objects with Rectangles')
        # plt.show()

    return match_results, len_match_results

def Multi_template_match(filename, original_image, image, templates, PlateName, \
                         min_scale=0.5, max_scale=1.2, intervals=10, threshold = 0.6):
    '''
    templates is the list of different templates
    threshold is to specify the criteria for choosing matching shape
    
    '''
    # Generate a linear space of scales
    scales = np.linspace(min_scale, max_scale, intervals)
    scales = np.round(scales, decimals=2)
    h_o, w_o = image.shape[0], image.shape[1]

    x_center=[]
    y_center=[]
    scale_select=[]
    match_value=[]

    #  iterate different templates?
    for template in templates:
        for scale in scales:
            template_scale = cv2.resize(template, None, fx=scale, fy=scale)
            h, w = template_scale.shape[0], template_scale.shape[1]
            if w >= w_o or h >= h_o:
                break

            result = cv2.matchTemplate(image, template_scale, cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)

            x_center.extend(loc[1] + w/2)
            y_center.extend(loc[0] + h/2)
            scale_select.extend(w + 0*loc[0])
            match_value.extend(result[loc[0], loc[1]])
   
    x_center=np.array(x_center)
    y_center=np.array(y_center)
    scale_select=np.array(scale_select)
    match_value=np.array(match_value)

    # Remove overlapping bounding boxes
    mask = np.zeros(image.shape, dtype = float)
    index = np.argsort(match_value)
    match_sort = match_value[index[::-1]]
    x_s = [int(x) for x in x_center[index[::-1]]]
    y_s = [int(x) for x in y_center[index[::-1]]]
    bbox = [int(x) for x in scale_select[index[::-1]]]

    x_center_n = []
    y_center_n=[]
    bbox_n=[]
    match_value_n=[]

    for x, y, b, m in zip(x_s, y_s, bbox, match_sort):
        if mask[y,x] == 0:
            y_u=int(y-b/2)
            y_d=int(y+b/2)
            x_l=int(x-b/2)
            x_r=int(x+b/2)
            # cope with boundaries
            if y_u<0: y_u=0
            if x_l<0: x_l=0
            if y_d>mask.shape[0]: y_d=mask.shape[0]
            if x_r>mask.shape[1]: x_r=mask.shape[1]

            mask[y_u:y_d, x_l:x_r] = m
            x_center_n.append(x)
            y_center_n.append(y)
            bbox_n.append(b)
            match_value_n.append(m)
    # Filtered values of center in x,y and bounding box size
    if len(match_value_n) < 1:
        match_results = None
        len_match_results = 0.
        print('None vesicles found')
    else: 
        match_results = np.stack((np.array(x_center_n), np.array(y_center_n),
                                np.array(bbox_n), np.array(match_value_n)), axis = 1)
        print(f'{len(match_results)} vesicles found')         
        len_match_results = len(match_results)

        fig, ax = plt.subplots()

        # Display the image
        ax.imshow(original_image, cmap='gray')
        ax.set_title(filename)

        # Plot each box
        for box in match_results:
            x_center, y_center, length = box[:3]
            x_min = x_center - length / 2
            y_min = y_center - length / 2
            rect = patches.Rectangle((x_min, y_min), length, length, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

        # Show the plot
        # plt.gca().set_aspect('equal', adjustable='box')

        # Display the result image with rectangles
        # plt.imshow(blended_image, cmap='gray')
        plt.savefig(f'Results_{PlateName}/'+f'{filename}_TemplateMatch_{formatted_datetime}.png')
        # plt.title('Detected Objects with Rectangles')
        # plt.show()
        plt.close(fig)

    return match_results, len_match_results
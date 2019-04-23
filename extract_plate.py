################################### packages ################################
import cv2
import numpy as np
from matplotlib import pyplot as plt

def extract_plate(input_image_path,input_template_path):
    
   


    # Load the original car image
    orig_img = cv2.imread(input_image_path)
    img_height = orig_img.shape[0]
    img_width = orig_img.shape[1]
    
    img = cv2.resize(orig_img, (800, int((img_height * 800) / img_width)))
    #diff_height = 400 - img_height
    #vertical_diff_height = int(diff_height/2)
    #diff_width = 800 - img_width
    #horizontal_diff_width = int(diff_width/2)
    # Add a border to the image for processing sake
    img = cv2.copyMakeBorder(orig_img,  50, 50, 50, 50, cv2.BORDER_CONSTANT)
    plt.imshow(img),plt.show()

   
    #Split out each channel
    blue, green, red = cv2.split(img)

    # Run canny edge detection on each channel
    blue_edges = cv2.Canny(blue, 200, 250)
    green_edges = cv2.Canny(green, 200, 250)
    red_edges = cv2.Canny(red, 200, 250)

    # Join edges back into image
    edges = blue_edges | green_edges | red_edges

    
      
    #plt.imshow(new_image,cmap='gray')
    #plt.show()
    # blur a bit to improve ocr accuracy
    new_image = cv2.blur(edges, (2, 2))
    #new_image = cv2.bilateralFilter(new_image, 11, 17, 17)
    #kernel = np.ones((5,5),np.uint8)
    #new_image = cv2.morphologyEx(new_image, cv2.MORPH_CLOSE, kernel)
    

    #################plate_image_template########################################
    plate_image_template = cv2.imread(input_template_path,0)
     
    scale = 5
    width = 35*scale
    height = 17*scale
    dim = (width, height)
    # resize image
    resized_plate_image_template = cv2.resize(plate_image_template, dim,interpolation = cv2.INTER_AREA)
    edges_plate_image_template = cv2.Canny(resized_plate_image_template,90,100)
    plt.imshow(edges_plate_image_template,cmap='gray'),plt.show()
    #edges_plate_image_template = cv2.blur(edges_plate_image_template, (2, 2))

    # Apply template Matching
    h = edges_plate_image_template.shape[0]
    w = edges_plate_image_template.shape[1]
    result = cv2.matchTemplate(new_image,edges_plate_image_template,cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    cv2.rectangle(orig_img , max_loc , (max_loc[0]+1,max_loc[1]+1) , 255, 5)
    plt.imshow(orig_img),plt.show()
    top_left = (int(max_loc[0] - w/2) , int(max_loc[1] - h/2))
    bottom_right = (int(max_loc[0] + w) , int(max_loc[1] + h/2))
    diff_height = 400 - img_height
    vertical_diff_height = int(diff_height/2)
    diff_width = 800 - img_width
    horizontal_diff_width = int(diff_width/2)
    h_min = top_left[1]
    h_max = bottom_right[1]
    w_min = top_left[0]
    w_max = bottom_right[0]

    orig_img = orig_img [h_min : h_max , w_min : w_max ]
    #cv2.rectangle(orig_img,top_left, bottom_right, 255, 2)

    #plt.imshow(result,cmap = 'gray')
    #plt.show()

    return orig_img

#############################################################################################
#test 
plate = extract_plate("sample8.JPG","template_num.JPG")
cv2.imwrite("extracted_plate.png",plate)

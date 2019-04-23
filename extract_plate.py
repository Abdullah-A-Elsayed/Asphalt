################################### packages ################################
import cv2
import numpy as np
from matplotlib import pyplot as plt

def extract_plate(input_image_path,input_template_path):
    
    # Determine pixel intensity
    # Apparently human eyes register colors differently.
    # TVs use this formula to determine
    # pixel intensity = 0.30R + 0.59G + 0.11B
    def pixel_intensity(pixel_width, pixel_height):
        
        if pixel_height >= img_height or pixel_width >= img_width:
            #print "pixel out of bounds ("+str(y)+","+str(x)+")"
            return 0
        pixel = img[pixel_height][pixel_width]
        return 0.30 * pixel[2] + 0.59 * pixel[1] + 0.11 * pixel[0]


    # A quick test to check whether the contour is
    # a connected shape
    def connected(contour):
        first = contour[0][0]
        last = contour[len(contour) - 1][0]
        return abs(first[0] - last[0]) <= 1 and abs(first[1] - last[1]) <= 1


    # Helper function to return a given contour
    def c(index):
        
        return contours[index]


    # Count the number of real children
    def count_children(index, h_, contour):
        # No children
        if h_[index][2] < 0:
            return 0
        else:
            #If the first child is a contour we care about
            # then count it, otherwise don't
            if keep(c(h_[index][2])):
                count = 1
            else:
                count = 0

                # Also count all of the child's siblings and their children
            count += count_siblings(h_[index][2], h_, contour, True)
            return count


    # Quick check to test if the contour is a child
    def is_child(index, h_):
        return get_parent(index, h_) > 0


    # Get the first parent of the contour that we care about
    def get_parent(index, h_):
        parent = h_[index][3]
        while not keep(c(parent)) and parent > 0:
            parent = h_[parent][3]

        return parent


    # Count the number of relevant siblings of a contour
    def count_siblings(index, h_, contour, inc_children=False):
        # Include the children if necessary
        if inc_children:
            count = count_children(index, h_, contour)
        else:
            count = 0

        # Look ahead
        p_ = h_[index][0]
        while p_ > 0:
            if keep(c(p_)):
                count += 1
            if inc_children:
                count += count_children(p_, h_, contour)
            p_ = h_[p_][0]

        # Look behind
        n = h_[index][1]
        while n > 0:
            if keep(c(n)):
                count += 1
            if inc_children:
                count += count_children(n, h_, contour)
            n = h_[n][1]
        return count


    # Whether we care about this contour
    def keep(contour):
        return keep_box(contour) and connected(contour)


    # Whether we should keep the containing box of this
    # contour based on it's shape
    def keep_box(contour):
        pixel_width, pixel_height, w_, h_ = cv2.boundingRect(contour)

        # width and height need to be floats
        w_ *= 1.0
        h_ *= 1.0

        # Test it's shape - if it's too oblong or tall it's
        # probably not a real character
        if w_ / h_ < 0.1 or w_ / h_ > 10:
            return False
        
        # check size of the box
        if ((w_ * h_) > ((img_width * img_height) / 5)) or ((w_ * h_) < 15):

            return False

        return True


    def include_box(index, h_, contour):


        if is_child(index, h_) and count_children(get_parent(index, h_), h_, contour) <= 2:

            return False

        if count_children(index, h_, contour) > 2:

            return False



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

    # Find the contours
    contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
   
    hierarchy = hierarchy[0]

    processed = edges.copy()
    rejected = edges.copy()

    # These are the boxes that we are determining
    keepers = []

    # For each contour, find the bounding rectangle and decide
    # if it's one we care about
    for index_, contour_ in enumerate(contours):
        
        x, y, w, h = cv2.boundingRect(contour_)
        # Check the contour and it's bounding box
        if keep(contour_) and include_box(index_, hierarchy, contour_):
            # It's a winner!
            keepers.append([contour_, [x, y, w, h]])
            
            cv2.rectangle(processed, (x, y), (x + w, y + h), (100, 100, 100), 1)
            cv2.putText(processed, str(index_), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        else:
            
            cv2.rectangle(rejected, (x, y), (x + w, y + h), (100, 100, 100), 1)
            cv2.putText(rejected, str(index_), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))

    # Make a white copy of our image
    
    new_image = edges.copy()

    
    #new_image.fill(255)
    

    boxes = []

    # For each box, find the foreground and background intensities
    for index_, (contour_, box) in enumerate(keepers):

        # Find the average intensity of the edge pixels to
        # determine the foreground intensity
        fg_int = 0.0
        for p in contour_:
            fg_int += pixel_intensity(p[0][0], p[0][1])

        fg_int /= len(contour_)


        # Find the intensity of three pixels going around the
        # outside of each corner of the bounding box to determine
        # the background intensity
        x_, y_, width, height = box
        bg_int = \
            [
                # bottom left corner 3 pixels
                pixel_intensity(x_ - 1, y_ - 1),
                pixel_intensity(x_ - 1, y_),
                pixel_intensity(x_, y_ - 1),

                # bottom right corner 3 pixels
                pixel_intensity(x_ + width + 1, y_ - 1),
                pixel_intensity(x_ + width, y_ - 1),
                pixel_intensity(x_ + width + 1, y_),

                # top left corner 3 pixels
                pixel_intensity(x_ - 1, y_ + height + 1),
                pixel_intensity(x_ - 1, y_ + height),
                pixel_intensity(x_, y_ + height + 1),

                # top right corner 3 pixels
                pixel_intensity(x_ + width + 1, y_ + height + 1),
                pixel_intensity(x_ + width, y_ + height + 1),
                pixel_intensity(x_ + width + 1, y_ + height)
            ]

        # Find the median of the background
        # pixels determined above
        bg_int = np.median(bg_int)



        # Determine if the box should be inverted
        if fg_int >= bg_int:
            fg = 255
            bg = 0
        else:
            fg = 0
            bg = 255

            # Loop through every pixel in the box and color the
            # pixel accordingly
        for x in range(x_, x_ + width):
            for y in range(y_, y_ + height):
                if y >= img_height or x >= img_width:

                    continue
                if pixel_intensity(x, y) > fg_int:
                    new_image[y][x] = bg
                else:
                    new_image[y][x] = fg

    #plt.imshow(new_image,cmap='gray')
    #plt.show()
    # blur a bit to improve ocr accuracy
    new_image = cv2.blur(new_image, (2, 2))
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
plate = extract_plate("sample1.JPG","template_num.JPG")
cv2.imwrite("extracted_plate.png",plate)

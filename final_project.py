import numpy as np
import argparse
import cv2
import sys

def getWatershedImage(img, markers):
    """
    A function to generate the output image (w/ red contours around heart wall) from markers used in watershed algorithm.

    ### markers => result image:
    marker = -1 --> Watershed boundaries. Change the color of corresponding pixels into red to generate red contours.

    Note that watershed algorithm in OpenCV will also see four borders of image as watershed boundaries,
    which are not what we want. Therefore, we need to eliminate these unwanted boundaries before generating red contours.
    """
    # Generate watershed boundaries with markers used in watershed algorithm
    watershed_line = np.zeros(markers.shape, dtype=np.uint8)
    watershed_line[markers == -1] = 255
    # Remove unwanted boundaries (four borders of image)
    watershed_line[0,:] = 0
    watershed_line[-1,:] = 0
    watershed_line[:,0] = 0
    watershed_line[:,-1] = 0
    # Make watershed boundaries thicker
    kernel = np.ones((2,2), dtype=np.uint8)
    watershed_line = cv2.dilate(watershed_line, kernel, iterations=1)
    # Change the color of corresponding pixels into red to generate red contours in the image
    img[watershed_line > 0, 0] = 0
    img[watershed_line > 0, 1] = 0
    img[watershed_line > 0, 2] = watershed_line[watershed_line > 0]
    return img

def heartSeg(file_name):
    # img_blur = cv2.GaussianBlur(img_origin, (3,3), 0, 0)
    # img_blur = cv2.blur(img_origin, (5,5))
    # Input the image
    img_origin_name = 'public/data/' + file_name
    img_origin = cv2.imread(img_origin_name, 1)
    img_origin_singlechannel = cv2.imread(img_origin_name, 0)
    
    # Image smoothing (also reduce noise)
    img_medianblur = cv2.medianBlur(img_origin_singlechannel, 5)
    
    # Apply thresholding to the image twice to get the desired grayscale interval (between 50~145)
    thresh_val_high = 145
    thresh_val_low = 50
    ret, thresh = cv2.threshold(img_medianblur, thresh_val_high, 255, cv2.THRESH_TOZERO_INV)
    ret, img_binary = cv2.threshold(thresh, thresh_val_low, 255, cv2.THRESH_BINARY)
    
    # Apply morphology opening to binary image to eliminate small objects
    kernel = np.ones((3,3), dtype=np.uint8)
    img_obj = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Find the absolute foreground (i.e. objects) by eroding all objects
    fg = cv2.erode(img_obj, kernel, iterations=3)
    # Specify heart wall foreground with the condition of object window size
    fg_labels_num, fg_labels_img, fg_stats, fg_centroids = cv2.connectedComponentsWithStats(fg)
    muscle_fg_idx = 0
    for muscle_fg_idx in range(fg_labels_num):
        if fg_stats[muscle_fg_idx,cv2.CC_STAT_WIDTH] > 80 and fg_stats[muscle_fg_idx,cv2.CC_STAT_WIDTH] < 120 \
        and fg_stats[muscle_fg_idx,cv2.CC_STAT_HEIGHT] > 100 and fg_stats[muscle_fg_idx,cv2.CC_STAT_HEIGHT] < 140:
            break
    fg_labels_img[fg_labels_img != muscle_fg_idx] = 0
    fg_labels_img[fg_labels_img == muscle_fg_idx] = 1
    muscle_fg = fg_labels_img.astype('uint8')
    muscle_fg = cv2.erode(muscle_fg, kernel, iterations=2)
    
    # Specify heart wall region with the condition of object window size
    bg = img_obj
    bg_labels_num, bg_labels_img, bg_stats, bg_centroids = cv2.connectedComponentsWithStats(bg)
    muscle_bg_idx = 0
    for muscle_bg_idx in range(bg_labels_num):
        if bg_stats[muscle_bg_idx,cv2.CC_STAT_WIDTH] > 120 and bg_stats[muscle_bg_idx,cv2.CC_STAT_WIDTH] < 160 \
        and bg_stats[muscle_bg_idx,cv2.CC_STAT_HEIGHT] > 120 and bg_stats[muscle_bg_idx,cv2.CC_STAT_HEIGHT] < 160:
            break
    bg_labels_img[bg_labels_img != muscle_bg_idx] = 0
    bg_labels_img[bg_labels_img == muscle_bg_idx] = 1
    muscle_bg = bg_labels_img.astype('uint8')
    # Find the absolute background by dilating heart wall region
    muscle_bg = cv2.dilate(muscle_bg, kernel, iterations=7)
    
    muscle_fg = muscle_fg.astype('int32')
    muscle_bg = muscle_bg.astype('int32')
    # The area between heart wall object and background is unknown area TBD with watershed algorithm
    muscle_unknown = np.copy(muscle_bg)
    muscle_unknown[muscle_fg > 0] = 0
    
    '''
    markers:
    >1: absolute foreground (heart wall object)
    1: absolute background
    0: unknown area (TBD with watershed algorithm)
    (all 0 will become 1 (bg) or >1 (fg) after watershed algorithm applied)
    -1: watershed boundaries (generated with watershed algorithm)
    '''
    markers = muscle_fg + 1
    markers[muscle_unknown > 0] = 0
    
    # Apply watershed algorithm on Gaussian-blurred image (not the origin one, because the noise is massive)
    img_gaussblur = cv2.GaussianBlur(img_origin, (3,3), 0, 0)
    markers = cv2.watershed(img_gaussblur, markers)
    
    # Use our function to generate the image where heart wall region is specified
    img_out = getWatershedImage(img_origin, markers)
    import os
    if (os.path.isdir("/result")):
        os.mkdir('result')
    cv2.imwrite('result/result_'+file_name, img_out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help='image path ')
    args = parser.parse_args()

    heartSeg(args.image)

    print('result_'+args.image)

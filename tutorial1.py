import cv2 as cv
import numpy as np

haystack_img = cv.imread('foxhole_coal_field.jpg', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('foxhole_coal.jpg', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

# Get best match position
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

print("Best match top left position: %s" % str(max_loc))
print("Best match bottom right position: %s" % str((max_loc[0] + needle_img.shape[1], max_loc[1] + needle_img.shape[0])))
print("Best match confidence: %s" % max_val)

threshold = 0.8

if max_val >= threshold:
    print("Found needle.")

    # get dimensions of needle image
    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)


    # Draw rectangle around best match
    cv.rectangle(haystack_img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
    
    cv.imshow('Result', haystack_img)
    cv.waitKey()
else:
    print("Needle not found.")

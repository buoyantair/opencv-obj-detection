import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def findClickPositions(needle_image_path, haystack_image_path, threshold=0.175, debug_mode=None):
  haystack_img = cv.imread(haystack_image_path, cv.IMREAD_UNCHANGED)
  needle_img = cv.imread(needle_image_path, cv.IMREAD_UNCHANGED)

  needle_w = needle_img.shape[1]
  needle_h = needle_img.shape[0]

  method = cv.TM_CCOEFF_NORMED
  result = cv.matchTemplate(haystack_img, needle_img, method)

  locations = np.where(result >= threshold)

  locations = list(zip(*locations[::-1]))

  rectangles = []

  # first we need to create the list of [x, y, w, h] rectangles
  for loc in locations:
    rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
    rectangles.append(rect)
    rectangles.append(rect)

  rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

  points = []
  if len(rectangles):
    print('Found needle.')

    
    line_color = (0, 255, 0)
    line_type = cv.LINE_4


    # Loop over all the rectagles and draw their rectangle
    for (x, y, w, h) in rectangles:

      # Determine the center position
      center_x = x + int(w/2)
      center_y = y + int(h/2)

      # Save the points
      points.append((center_x, center_y))

      if debug_mode == 'rect':
        # Determine the box positions
        top_left = (x, y)
        bottom_right = (x + w, y + h)

        # Draw the box
        cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
      elif debug_mode == 'point':
        # Draw the center point
        cv.drawMarker(haystack_img, (center_x, center_y), line_color, markerType=cv.MARKER_CROSS, markerSize=10, thickness=1, line_type=line_type)

    if debug_mode:
      cv.imshow('Matches', haystack_img)
      cv.waitKey()

  else:
    print('Needle not found.')

  return points


points = findClickPositions('foxhole_scrap.jpg', 'foxhole_scrap_field.jpg', debug_mode='point')
print(points)
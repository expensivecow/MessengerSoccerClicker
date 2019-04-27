import os
import pyautogui
import cv2
import numpy as np

# PREREQ - DOWNLOAD DIRECTORY FOLDER HAS FOLDERS 'YEAR' FOR ALL YEARS TO DOWNLOAD
def main():
    print('Hello World')
    main_dir = os.path.dirname(os.path.realpath(__file__))

    img_path = os.path.join(main_dir, '..', '..','imgs')
    find_initial_screen(img_path)

def find_initial_screen(img_path):
    full_screen = pyautogui.screenshot(os.path.join(img_path, 'full_screen.png'))

    full_screen_template = cv2.imread(os.path.join(img_path, 'full_screen.png'), 0)
    mobile_screen_template = cv2.imread(os.path.join(img_path, 'screen_without_score.png'), 0)

    w, h = mobile_screen_template.shape[::-1]

    method = cv2.TM_SQDIFF_NORMED
    res = cv2.matchTemplate(full_screen_template, mobile_screen_template, method)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(full_screen_template,top_left, bottom_right, 255, 2)

    cv2.imshow('hello', full_screen_template)
    while(True):
        if (cv2.waitKey(25) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break
    #full_screen.save(os.path.join(img_path, 'full_screen.png'))

if __name__ == "__main__":
    main()

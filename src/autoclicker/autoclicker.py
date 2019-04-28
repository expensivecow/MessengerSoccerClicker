import os
import pyautogui
import cv2
import numpy as np
import mss
import mss.tools
import time

thresh = 0.3

# PREREQ - DOWNLOAD DIRECTORY FOLDER HAS FOLDERS 'YEAR' FOR ALL YEARS TO DOWNLOAD
def main():
    print('Hello World')
    main_dir = os.path.dirname(os.path.realpath(__file__))

    img_path = os.path.join(main_dir, '..', '..','imgs')
    top_left_coords, bottom_right_coords, image_width, image_height = find_initial_screen(img_path)

    print(top_left_coords)
    print(str(image_width))
    print(str(image_height))

    points = 0
    while(True):
        output = track_soccer_ball(img_path, top_left_coords, image_width, image_height)
        cv2.imshow('hello', output)
        cv2.waitKey(1)
        #center_of_ball_x = (top_left_coords[0]) + ((top_left[0] + bottom_right[0]) / 2)
        #center_of_ball_y = (top_left_coords[1]) + ((top_left[1] + bottom_right[1]) / 2)

        #print(str(center_of_ball_x))
        #print(str(center_of_ball_y))

        #pyautogui.click(center_of_ball_x, center_of_ball_y, button='left')

def track_soccer_ball(img_path, top_left_coords, image_width, image_height):
    screen_portion_img_path = os.path.join(img_path, 'portion_of_screen.png')
    soccer_ball_img_path = os.path.join(img_path, 'soccer_ball.png')

    with mss.mss() as sct:
        region = {'top': top_left_coords[1], 'left': top_left_coords[0], 'width': image_width, 'height': image_height}

        img = sct.grab(region)

        mss.tools.to_png(img.rgb, img.size, output=screen_portion_img_path)

    return perform_sift_matching(screen_portion_img_path, soccer_ball_img_path)


    '''
    phone_mat = cv2.imread(screen_portion_img_path)
    cv2.rectangle(phone_mat, top_left, bottom_right, (0,0,255), 3)
    cv2.imshow('hello', phone_mat)
    cv2.waitKey(1)
    '''

def perform_sift_matching(img_path, img_template_path):
    orb = cv2.ORB_create()

    img = cv2.imread(img_path, 0)
    img_template = cv2.imread(img_template_path, 0)

    kp1, des1 = orb.detectAndCompute(img_template, None)
    kp2, des2 = orb.detectAndCompute(img, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)


    output = cv2.drawMatches(img_template, kp1, img, kp2, matches[:10], flags=2, outImg=None)

    return output

def debug_mat(mat):
    cv2.imshow('debug img', mat)

    while (True):
        if (cv2.waitKey(25) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break

def find_template_match(img, template_img, method):
    image = cv2.imread(img, 0)
    template_image = cv2.imread(template_img, 0)

    w, h = template_image.shape[::-1]

    res = cv2.matchTemplate(image, template_image, method)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = None
    bottom_right = None
    image_width_size = None
    image_height_size = None

    if (max_val > thresh):
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        image_width_size = (bottom_right[0] - top_left[0])
        image_height_size = (bottom_right[1] - top_left[1])

        # coords from top left, top right, bottom left, bottom right are
        # top left = [top_left[0], top_left[1]]
        # top right = [bottom_right[0], top_left[1]]
        # bottom left = [top_left[0], bottom_right[1]]
        # bottom right = [bottom_right[0], bottom_right[1]]

        '''For debugging purposes
        cv2.imshow('hello', full_screen_template)
        while(True):
            if (cv2.waitKey(25) & 0xFF == ord('q')):
                cv2.destroyAllWindows()
                break
        #full_screen.save(os.path.join(img_path, 'full_screen.png'))
        '''

    return top_left, bottom_right, image_width_size, image_height_size

def find_initial_screen(img_path):
    with mss.mss() as sct:
        img = sct.shot(output=os.path.join(img_path, 'full_screen.png'))

    return find_template_match(os.path.join(img_path, 'full_screen.png'), os.path.join(img_path, 'screen_without_score.png'), cv2.TM_SQDIFF_NORMED)

if __name__ == "__main__":
    main()

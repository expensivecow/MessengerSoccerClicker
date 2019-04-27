import os
import pyscreenshot as imagegrab
import cv2


# PREREQ - DOWNLOAD DIRECTORY FOLDER HAS FOLDERS 'YEAR' FOR ALL YEARS TO DOWNLOAD
def main():
    print('Hello World')
    main_dir = os.path.dirname(os.path.realpath(__file__))

    img_path = os.path.join(main_dir, '..', '..','imgs')
    find_screen(img_path)

def find_screen(img_path):
    full_screen = imagegrab.grab()
    full_screen.save(os.path.join(img_path, 'full_screen.png'))

if __name__ == "__main__":
    main()

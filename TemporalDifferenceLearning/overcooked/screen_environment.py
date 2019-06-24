import time
import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui
from direct_keys import press_key, release_key


def screen_record():
    screen = np.array(ImageGrab.grab(bbox=(0, 40, 1280, 720)))
    return screen


def process_img(image):
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1 = 200, threshold2=300)
    return processed_img


if __name__ == "__main__":
    # define controls
    key_up = 0xC8
    key_down = 0xD0
    key_left = 0xCB
    key_right = 0xCD

    for i in list(range(5))[::-1]:
        print(i + 1)
        time.sleep(1)
    #while True:
    for i in range(10):
        screen = screen_record()
        new_screen = process_img(screen)
        #cv2.imshow('window', new_screen)
        press_key(key_down)
        time.sleep(1)
        release_key(key_down)
        time.sleep(1)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

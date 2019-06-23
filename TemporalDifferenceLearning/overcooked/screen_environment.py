import numpy as np
from PIL import ImageGrab
import cv2

def screen_record():
    for i in range(20):
        print("Iteration {}".format(i))
        printscreen =  np.array(ImageGrab.grab(bbox=(0,40,1280,720)))
        cv2.imshow('window',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def process_img(image):
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1 = 200, threshold2=300)
    return processed_img


if __name__ == "__main__":
    while True:
        screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
        new_screen = process_img(screen)
        cv2.imshow('window', new_screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

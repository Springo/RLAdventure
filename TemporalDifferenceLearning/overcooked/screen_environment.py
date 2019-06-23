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

if __name__ == "__main__":
    screen_record()

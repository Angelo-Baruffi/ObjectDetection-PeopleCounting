import numpy as np
import cv2
def dumpclean(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print k
                dumpclean(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print v
    else:
        print obj

#cap = cv2.VideoCapture('inputs/PETS09-S2L1.mp4')
cap = cv2.VideoCapture(0)
dic = {
    'fps' : cap.get(cv2.CAP_PROP_FPS),
    'width' : cap.get(cv2.CAP_PROP_FRAME_WIDTH),
    'height' : cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
    'total_frames' : cap.get(cv2.CAP_PROP_FRAME_COUNT)
}

print('-----------------------------------------')
dumpclean(dic)
cap.release()
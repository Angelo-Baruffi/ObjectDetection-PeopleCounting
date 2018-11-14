# import the necessary packages
from threading import Thread
import datetime
import cv2
import numpy as np
import matplotlib.pyplot as plt

class FPS:
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self
    
    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()

    
class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self
 
    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
                    
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
 
    def read(self):
        # return the frame most recently read
        return self.grabbed, self.frame
 
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    def getWidth(self):
        # Get the width of the frames
        return int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))

    def getHeight(self):
        # Get the height of the frames
        return int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def getFPS(self):
        # Get the frame rate of the frames
        return int(self.stream.get(cv2.CAP_PROP_FPS))

    def isOpen(self):
        # Get the frame rate of the frames
        return self.stream.isOpened()

    def setFramePosition(self, framePos):
        self.stream.set(cv2.CAP_PROP_POS_FRAMES, framePos)

    def getFramePosition(self):
        return int(self.stream.get(cv2.CAP_PROP_POS_FRAMES))

    def getFrameCount(self):
        return int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT))

class Utils:
    def __init__(self, im_width=320,im_height=320):
        self.im_width = im_width
        self.im_height = im_height

    def getBoxes(self, boxes, scores, classes): #def size of video to get the position of boxes
        #Return  the person boxes and the score of these boxes
        im_width = self.im_width
        im_height = self.im_height
        indexs = np.where(scores[0] > 0.5)
        if(len(indexs[0])):
            indexs = np.array([index if result==1 else -1 for index, result in enumerate(classes[0][indexs])])
            #Tem os indexs que sao pessoas que passaram. Tem indexs nulos
            indexs = indexs[np.where(indexs >= 0)]
            boxes = boxes[0][indexs]
            result = []
            if(len(boxes)):
                for box in boxes:
                    (ymin, xmin, ymax, xmax) = box
                    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                                    ymin * im_height, ymax * im_height)
                    result.append([left, right, top, bottom])

            return result, scores[0][indexs]
        else:
            return(None, None)


class Record:
    def __init__(self):
        self.positions = []
        self.scores = []
        self.y = []
        self.x = []

        plt.figure(2)
        plt.ion()


    def putFrame(self, frame_number, boxes, score):
        if(boxes):
            self.positions.append([frame_number, boxes])
            self.scores.append(score)
            
            if(0): #print boxes
                print('------------Frame Number {} -------- Number of people {}----------'.format(frame_number, len(boxes)))
                print(boxes)
            
            self.plot(frame_number, len(boxes))


    def save(self, file_name='output'):        
        #Create a table to save the results
        rows = []
        for index,pos in enumerate(self.positions):
            frame_n = pos[0]
            [rows.append([frame_n, box[0],box[1],box[2],box[3], self.scores[index][index2]]) for index2,box in enumerate(pos[1])]
        
        rows = np.array(rows)
        np.savetxt('outputs/'+file_name+".csv", rows, delimiter=";")


        #Finish plot
        plt.show(block=True) 

    def plot(self, frame_number, people):
        
        self.y.append(people)
        self.x.append(frame_number)    

        # plt.gca().cla() # optionally clear axes
        plt.plot(self.x, self.y)
        plt.title(str(people))
        plt.draw()

        

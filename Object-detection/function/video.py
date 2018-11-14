from __future__ import print_function
from utils.app_utils import *
from utils.objDet_utils import *
import argparse
import multiprocessing
from multiprocessing import Queue, Pool
from queue import PriorityQueue
import cv2


def video(args):
    """
    Read and apply object detection to input video stream
    """

    # Set the multiprocessing logger to debug if required
    if args["logger_debug"]:
        logger = multiprocessing.log_to_stderr()
        logger.setLevel(multiprocessing.SUBDEBUG)

    # Multiprocessing: Init input and output Queue, output Priority Queue and pool of workers
    input_q = Queue(maxsize=args["queue_size"])
    output_q = Queue(maxsize=args["queue_size"])
    output_pq = PriorityQueue(maxsize=3*args["queue_size"])
    pool = Pool(args["num_workers"], worker, (input_q,output_q))
    
    # created a threaded video stream and start the FPS counter
    vs = cv2.VideoCapture("inputs/{}".format(args["input_videos"]))
    fps = FPS().start()

    im_width = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
    im_height = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print('Size of video: {} x {}'.format(im_width,
                                          im_height))

    # Define the codec and create VideoWriter object
    if args["output"]:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('outputs/{}.avi'.format(args["output_name"]),
                              fourcc, vs.get(cv2.CAP_PROP_FPS),
                              (int(vs.get(cv2.CAP_PROP_FRAME_WIDTH)),
                               int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    # Start reading and treating the video stream
    if args["display"] > 0:
        print()
        print("=====================================================================")
        print("Starting video acquisition. Press 'q' (on the video windows) to stop.")
        print("=====================================================================")
        print()

    countReadFrame = 0
    countWriteFrame = 1
    nFrame = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
    firstReadFrame = True
    firstTreatedFrame = True
    firstUsedFrame = True
    record = Record()

    while True:
        # Check input queue is not full
        if not input_q.full():
            # Read frame and store in input queue
            ret, frame = vs.read()
            if ret:
                countReadFrame = countReadFrame + 1
                arguments = (countReadFrame, im_width, im_height)
                
                input_q.put((int(vs.get(cv2.CAP_PROP_POS_FRAMES)),frame ,arguments))
                
                if firstReadFrame:
                    print(" --> Reading first frames from input file. Feeding input queue.\n")
                    firstReadFrame = False

        # Check output queue is not empty
        if not output_q.empty():
            # Recover treated frame in output queue and feed priority queue
            output = output_q.get()
            frame_number = output[2]
            boxes = output[1][1][0]
            score = output[1][1][1]
            output = (output[0],output[1][0])

            record.putFrame(frame_number, boxes, score)

            output_pq.put(output)
            if firstTreatedFrame:
                print(" --> Recovering the first treated frame.\n")
                firstTreatedFrame = False
                
        # Check output priority queue is not empty
        if not output_pq.empty():
            prior, output_frame = output_pq.get()
            if prior > countWriteFrame:
                output_pq.put((prior, output_frame))
            else:
                countWriteFrame = countWriteFrame + 1
                output_rgb = cv2.cvtColor(output_frame, cv2.COLOR_RGB2BGR)

                # Write the frame in file
                if args["output"]:
                    out.write(output_rgb)
                    

                # Display the resulting frame
                if args["display"]:
                    cv2.imshow('frame', output_rgb)
                    fps.update()

                if firstUsedFrame:
                    print(" --> Start using recovered frame (displaying and/or writing).\n")
                    firstUsedFrame = False

                
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("Read frames: %-3i %% -- Write frame: %-3i %%" % (int(countReadFrame/nFrame * 100), int(countWriteFrame/nFrame * 100)), end ='\r')
        if((not ret) & input_q.empty() & output_q.empty() & output_pq.empty()):
            break


    print("\nFile have been successfully read and treated:\n  --> {}/{} read frames \n  --> {}/{} write frames \n".format(countReadFrame,nFrame,countWriteFrame-1,nFrame))
    
    # When everything done, release the capture
    fps.stop()
    pool.terminate()
    vs.release()
    if args["output"]:
        out.release()
    cv2.destroyAllWindows()
    record.save()
    

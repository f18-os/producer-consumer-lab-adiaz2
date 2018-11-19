#!/usr/bin/env python3

import threading
import cv2
import time
import numpy as np
import base64
import queue

# globals
outputDir    = 'frames'
clipFileName = 'clip.mp4'

global finishedExtracting
finishedExtracting = False
global finishedConverting
finishedConverting = False

def extractFrames(fileName, outputBuffer):
    # Initialize frame count 
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()
    
    print("Reading frame {} {} ".format(count, success))
    while success:
        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)

        #encode the frame as base 64 to make debugging easier
        jpgAsText = base64.b64encode(jpgImage)

        # add the frame to the buffer
        outputBuffer.put(jpgAsText)
       
        success,image = vidcap.read()
        print('Reading frame {} {}'.format(count, success))
        count += 1
        time.sleep(0.01)
    print("Frame extraction complete")
    global finishedExtracting
    finishedExtracting = True
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")



def convertFrames(inputBuffer, outputBuffer):
    # initialize frame count
    count = 0    
    global finishedExtracting
    while True:
        while not inputBuffer.empty():
            print("Converting frame {}".format(count))

                # load the next file
            frameAsText = inputBuffer.get()

            # decode the frame 
            jpgRawImage = base64.b64decode(frameAsText)

            # convert the raw frame to a numpy array
            jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)

            inputFrame = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)

            # convert the image to grayscale
            grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)

            success, jpgImage = cv2.imencode('.jpg', grayscaleFrame)

            #encode the frame as base 64 to make debugging easier
            jpgAsText = base64.b64encode(jpgImage)

            # add the frame to the buffer
            outputBuffer.put(jpgAsText)

            time.sleep(0.01)
            
            count += 1

        if finishedExtracting:
            global finishedConverting
            finishedConverting = True
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            return




def displayFrames(inputBuffer):
    # initialize frame count
    count = 0
    while True:
        # go through each frame in the buffer until the buffer is empty
        while not inputBuffer.empty():
            # get the next frame
            frameAsText = inputBuffer.get()

            # decode the frame 
            jpgRawImage = base64.b64decode(frameAsText)

            # convert the raw frame to a numpy array
            jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)
            
            # get a jpg encoded frame
            img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)

            print("Displaying frame {}".format(count))        

            # display the image in a window called "video" and wait 42ms
            # before displaying the next frame
            cv2.imshow("Video", img)
            if cv2.waitKey(24) and 0xFF == ord("q"):
                break
            time.sleep(0.001)
            count += 1

        if finishedExtracting and finishedConverting:
            print("Finished displaying all frames")
            # cleanup the windows
            cv2.destroyAllWindows()
            return



    

# filename of clip to load
filename = 'clip.mp4'

# shared queue  
extractionQueue = queue.Queue()

grayscaleQueue = queue.Queue()


extract = threading.Thread(name='extract', target=extractFrames, args=(filename, extractionQueue))
convert = threading.Thread(name='conver', target=convertFrames, args=(extractionQueue, grayscaleQueue))
display = threading.Thread(name='display', target=displayFrames, args=(grayscaleQueue))

extract.start()
convert.start()
displayFrames(grayscaleQueue)





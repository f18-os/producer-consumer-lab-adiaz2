This is a lab that showcases the producer consumer situation using python

The way this works, is that it creates a thread that populates a queue with decoded frames of a video.

At the same time, a second thread is reading each frame that gets put into the queue and converts them to grayscale and puts it into another queue

At the same time, a third thread is taking the grayscale images from the grayscale queue and displaying them

To run the program, simply run the Lab.py file, and make sure that you have opencv installed in your environment to properly run the lab
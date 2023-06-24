from vncdotool import api
import cv2
import numpy as np

# connect to the VNC server
client = api.connect('localhost::5902')

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))

# capture frames and write to file
for i in range(3500):
    # capture a frame
    frame = client.captureScreen()

    # convert the frame to an array and resize to match VideoWriter
    img = np.array(frame)
    img = cv2.resize(img, (1980, 1024))

    # write the frame
    out.write(img)

# release the VideoWriter
out.release()

# disconnect from the VNC server
client.disconnect()


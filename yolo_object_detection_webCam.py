import os
import cv2
import numpy as np
import time
import pyautogui, sys
import pyAutoGui as pg
# Open the device at the ID 0

net = cv2.dnn.readNet("./weight/yolov4-tiny-nose_best.weights", "yolov4-tiny-testing.cfg")
classes = [""]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

cap = cv2.VideoCapture(1)


# set start time to current time
start_time = time.time()
# displays the frame rate every 2 second
display_time = 2
# Set primarry FPS to 0
fps = 0

#Check whether user selected camera is opened successfully.
if not (cap.isOpened()):
    print('Could not open video device')

#To set the resolution

#cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)

#cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
count=0
while(True):
        
    count=count+1
    if(count%10==0):
                # Capture frame-by-frame

        ret, frame = cap.read()

        # Display the resulting frame
        frame = cv2.flip(frame, 1)
        img = cv2.resize(frame, None, fx=1.0, fy=1.0, interpolation=cv2.INTER_AREA)
        height, width, channels = img.shape

        # print(img.shape)
        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (288, 288), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

            # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    # Object detected
                    print("Label ",class_id)
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    
                    #pyautogui.moveTo(center_x, center_y)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    # print("x,y = "+str(x)+", "+str(y))

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                try:
                    x, y, w, h = boxes[i]
                    print("x1, y1 = "+str(x)+", "+str(y))
                    # pg.mouseMovement(int(x), int(y))
                    label = str(classes[class_ids[i]])
                    color = colors[class_ids[i]]
                    if (label == 0):
                        cv2.circle(img, (x, y), 2, color, 5)
                    # cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    i = int(x+w/2)
                    j = int(y+h/2)
                    print(i,j)
                    cv2.circle(img, (i, j), 5, color, -1)
                    pg.mouseMovement(i-300, j-300)
                    # cv2.rectangle(img, (280, 200), (330,250), color, 2)
                    cv2.putText(img, label, (x, y + 30), font, 3, color, 2)
                    croppedImg = img[y:y+h, x:x+w]
                    print("Label ",label)
                	# cv2.imshow("Cropped", croppedImg)

                except:
                	pass

        cv2.imshow("Image", img)
        #Waits for a user input to quit the application
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # calculate FPS
    fps += 1
    TIME = time.time() - start_time
    if TIME > display_time:
        print("FPS: ", fps/TIME)
        fps = 0
        start_time = time.time()


# When everything done, release the capture

cap.release()

cv2.destroyAllWindows()

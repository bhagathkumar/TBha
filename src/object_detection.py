# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import glob
import os
import time


textFileObj = open("Object detection result.txt", 'w')


def object_detection(net, image, frame_count):

    image = cv2.resize(image, (320, 240))  # to run faster
    (H, W) = image.shape[:2]

    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(
        image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    # print(layerOutputs)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    idxs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > 0.3:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
                idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
                # ensure at least one detection exists
    if len(idxs) > 0:
                    # loop over the indexes we are keeping
        for i in idxs.flatten():

            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            # draw a bounding box rectangle and label on the image
            color = [int(c) for c in COLORS[classIDs[i]]]
            textFileObj.write("Frame: {}, ".format(frame_count))
            textFileObj.write("BBox: {}, ".format(x, y, x + w, y + h))
            textFileObj.write("Label: {}, ".format(LABELS[classIDs[i]]))
            textFileObj.write("confidense: {:.2f}\n".format(confidences[i]))
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            cv2.putText(image, text, (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return image


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--video", help="path to input image")
ap.add_argument("--image", help="path to input image")
ap.add_argument("--live", help="path to input image")
ap.add_argument("--batch", help="path to Folder")
args = vars(ap.parse_args())

if __name__ == '__main__':
    videoFlag = False
    imageFlag = False
    liveFlag = False
    batchFlag = False
    skip_frame = 0  # process on frame interval to make fast
    print("something")
    if args["image"] is not None:
        imageFlag = True
    if args["video"] is not None:
        videoFlag = True
    if args["live"] is not None:
        liveFlag = True
    if args["batch"] is not None:
        batchFlag = True

    # load the COCO class labels our YOLO model was trained on
    modelPath = "/work/work1/yolo3/"
    labelsPath = modelPath + "/coco.names"
    LABELS = open(labelsPath).read().strip().split("\n")
    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
    # derive the paths to the YOLO weights and model configuration
    weightsPath = modelPath + "/yolov3.weights"
    configPath = modelPath + "/yolov3.cfg"

    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from model path...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

    # load our input image and grab its spatial dimensions
    frame_count = 1
    if videoFlag:
        videoObject = cv2.VideoCapture(args["video"])
        if videoObject.isOpened():
            success, image = videoObject.read()
            while success:
                ret, image = videoObject.read()
                if (frame_count % (skip_frame + 1)) == 0:
                    print("Frame Numper: {}".format(frame_count))
                    if ret:
                        DetectedImage = object_detection(
                            net, image, frame_count)
                        frame_count = frame_count + 1
                        print(frame_count)
                        cv2.imshow("Output Window", DetectedImage)
                        key = cv2.waitKey(20)
                        print(key)
                        if key == 27:
                            exit(0)
                    else:
                        print("Video ended")
                        break
                else:
                    frame_count = frame_count + 1
        else:
            print("video is not available")
    elif imageFlag:
        image = cv2.imread(args['image'])
        DetectedImage = object_detection(net, image, 1)
        cv2.imshow("Output Window", DetectedImage)
        cv2.waitKey(0)
    elif batchFlag:
        print("Batch", args["batch"])
        while True:
            a = glob.glob(args["batch"]+"/*.jpg")
            for fn in a:
                print(fn)
                image = cv2.imread(fn)
                DetectedImage = object_detection(net, image, 1)
                #cv2.imshow("Output Window", DetectedImage)
                cv2.waitKey(0)
                print("Processed")
                p,f=os.path.split(fn)
                os.rename(fn,"/work/work1/out2/"+f)
            print("sleeping")
            time.sleep(2)
            

    elif liveFlag:
        liveObject = cv2.VideoCapture(int(args["live"]))
        if liveObject.isOpened():
            success, image = liveObject.read()
            frame_count = 0
            while success:
                ret, image = liveObject.read()
                if ret:
                    DetectedImage = object_detection(net, image, frame_count)
                    frame_count = frame_count + 1
                    print(frame_count)
                    cv2.imshow("Output Window", DetectedImage)
                    key = cv2.waitKey(40)
                    print(key)
                    if key == 27:
                        exit(0)
                else:
                    print("Live ended")
                    break

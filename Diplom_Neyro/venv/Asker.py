from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import torch.nn as nn
import torch.nn.functional as F
import Models
from torchvision import datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from PIL import *
import numpy as np
import cv2
import time
import base64
import os
from io import BytesIO
import pickle
import onnxruntime as rt
import math
import matplotlib.pyplot as plt

mtcnn0 = MTCNN(image_size=240, margin=0, keep_all=False, min_face_size=40) # keep_all=False
mtcnn = MTCNN(image_size=240, margin=0, keep_all=True, min_face_size=40) # keep_all=True
resnet = InceptionResnetV1(pretrained='vggface2').eval()
load_data = torch.load('Data.pt')
embedding_list = load_data[0]
name_list = load_data[1]
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
#
MODEL = "Models/model.onnx"
PROTOTXT = 'coco.prototxt'
os.environ['CUDA_VISIBLE_DEVICES'] = "-1"
coco_classes = []

with open(PROTOTXT) as lines:
    for line in lines:
        coco_classes.append(line.strip())

def ask_face(ima):
    rezult = []
    im_arr = np.frombuffer(ima, dtype=np.uint8)  # im_arr is one-dim Numpy array
    frame = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    img = Image.fromarray(frame)
    img_cropped_list, prob_list = mtcnn(img, return_prob=True)
    if img_cropped_list is not None:
        boxes, _ = mtcnn.detect(img)
        for i, prob in enumerate(prob_list):
            if prob > 0.90:
                emb = resnet(img_cropped_list[i].unsqueeze(0)).detach()
                dist_list = []  # list of matched distances, minimum distance is used to identify the person
                for idx, emb_db in enumerate(embedding_list):
                    dist = torch.dist(emb, emb_db).item()
                    dist_list.append(dist)
                min_dist = min(dist_list)  # get minumum dist value
                min_dist_idx = dist_list.index(min_dist)  # get minumum dist index
                name = name_list[min_dist_idx]  # get name corrosponding to minimum dist
                box = boxes[i]
                original_frame = frame.copy()  # storing copy of frame before drawing on it
                frame = cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
                if min_dist < 0.90:
                    frame = cv2.putText(frame, name, (box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
                    frame = cv2.putText(frame, name, (box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    result, sframe = cv2.imencode('.jpg', frame)
    return base64.b64encode(sframe).__str__()
    #rezult.append(base64.encodestring(frame))
    #rezult.append(img_cropped_list is not None)

def ask_isface(ima):
    im_arr = np.frombuffer(ima, dtype=np.uint8)
    frame = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    img = Image.fromarray(frame)
    img_cropped_list, prob_list = mtcnn(img, return_prob=True)
    return img_cropped_list is not None



# body detect
sess = rt.InferenceSession(MODEL)
def ask_body(ima):
    im_arr = np.frombuffer(ima, dtype=np.uint8)
    frame = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    img = Image.fromarray(frame)
    img_data = np.array(img.getdata()).reshape(img.size[1], img.size[0], 3)
    img_data = np.expand_dims(img_data.astype(np.uint8), axis=0)
    outputs = ["detection_boxes:0", "detection_classes:0", "detection_scores:0", "num_detections:0"]
    result = sess.run(outputs, {"image_tensor:0": img_data})
    detection_boxes, detection_classes, detection_scores, num_detections = result
    batch_size = num_detections.shape[0]
    draw = ImageDraw.Draw(img)
    for batch in range(0, batch_size):
        for detection in range(0, int(num_detections[batch])):
            c = detection_classes[batch][detection]
            if(c.astype('int32') - 1 == 0):
                d = detection_boxes[batch][detection]
                return draw_detection(draw, d, c)
    return None


def ask_isbody(ima):
    return True

def draw_detection(draw, d, c):
    res = []
    width, height = draw.im.size
    # the box is relative to the image size so we multiply with height and width to get pixels.
    top = d[0] * height
    left = d[1] * width
    bottom = d[2] * height
    right = d[3] * width
    top = max(0, np.floor(top + 0.5).astype('int32'))
    left = max(0, np.floor(left + 0.5).astype('int32'))
    bottom = min(height, np.floor(bottom + 0.5).astype('int32'))
    right = min(width, np.floor(right + 0.5).astype('int32'))
    res.append(coco_classes[c.astype('int32') - 1])
    res.append(math.fabs(left - right).__str__())
    res.append(math.fabs(top - bottom).__str__())
    return res
#! /usr/bin/env python

import argparse
import os
import cv2
import imutils
import numpy as np
from tqdm import tqdm
from preprocessing import parse_annotation
from utils import draw_boxes
from frontend import YOLO
import json
from keras import backend as K
import tensorflow as tf

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"




def predict_num(img_path):
    

    image_path   = img_path
    config_path  = 'config.json'
    weights_path = 'model.h5'
    # image_path   = img_path

    # K.clear_session()
    # tf.reset_default_graph()


    with open(config_path) as config_buffer:    
        config = json.load(config_buffer)

    yolo = YOLO(backend             = config['model']['backend'],
                    input_size          = config['model']['input_size'], 
                    labels              = config['model']['labels'], 
                    max_box_per_image   = config['model']['max_box_per_image'],
                    anchors             = config['model']['anchors'])

    yolo.load_weights(weights_path)

    ###############################
    #   Make the model 
    ###############################
    

    ###############################
    #   Load trained weights
    ###############################    

    

    ###############################
    #   Predict bounding boxes 
    ###############################

    # K.clear_session()
    # tf.reset_default_graph()

    if image_path[-4:] == '.mp4':
        video_out = image_path[:-4] + '_detected' + image_path[-4:]
        video_reader = cv2.VideoCapture(image_path)

        nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_h = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_w = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))

        video_writer = cv2.VideoWriter(video_out,
                               cv2.VideoWriter_fourcc(*'MPEG'), 
                               50.0, 
                               (frame_w, frame_h))

        for i in tqdm(range(nb_frames)):
            _, image = video_reader.read()
            
            boxes = yolo.predict(image)
            image = draw_boxes(image, boxes, config['model']['labels'])

            video_writer.write(np.uint8(image))

        video_reader.release()
        video_writer.release()  
    else:
        image = cv2.imread(image_path)
        # image = imutils.rotate(image,90)
        # boxes = 0
        # count = 0
        boxes = yolo.predict(image)
        image,count = draw_boxes(image, boxes, config['model']['labels'])

        K.clear_session()
        tf.reset_default_graph()

        print(count, 'boxes are found')

        cv2.imwrite(image_path[:-4] + '_detected' + image_path[-4:], image)
        return count

if __name__ == '__main__':
    _main_()

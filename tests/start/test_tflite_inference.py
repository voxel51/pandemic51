'''
Test script for interface with a TFLite model.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
import glob

import numpy as np
import tensorflow as tf
from PIL import Image


# Parameters
MODEL_PATH = "model/detect.tflite"
LABELMAP_PATH = "model/labelmap.txt"
INPUT_PATTERN = "out/img/time_square/*.png"


class Detector(object):
    '''The model takes an image as input. The expected image is 300x300 pixels,
    with three channels (red, blue, and green) per pixel. This should be fed to
    the model as a flattened buffer of 270,000 byte values (300x300x3). Since
    the model is quantized, each value should be a single byte representing a
    value between 0 and 255.
    '''

    def __init__(self, model_path, labelmap_path):
        # Load labelmap
        with open(labelmap_path, "r") as text_file:
            self.labelmap = [a.strip("\n") for a in text_file.readlines()]

        # Load TFLite model and allocate tensors
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        # Get input and output tensors
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict(self, img):
        img = self._preprocess(img)

        self.interpreter.set_tensor(self.input_details[0]["index"], img)
        self.interpreter.invoke()

        return self._get_outputs()

    def _preprocess(self, img):
        input_shape = self.input_details[0]["shape"]

        processed_img = np.asarray(img, dtype=np.uint8)

        if len(processed_img.shape) < 4:
            processed_img = np.expand_dims(processed_img, axis=0)

        assert all(processed_img.shape == input_shape), \
            "Invalid input shape. Expected: {} Actual: {}".format(
                input_shape, processed_img.shape)

        return processed_img

    def _get_outputs(self):
        bboxes = self.interpreter.get_tensor(
            self.output_details[0]["index"]).squeeze()
        class_idxs = self.interpreter.get_tensor(
            self.output_details[1]["index"]).squeeze()
        confidences = self.interpreter.get_tensor(
            self.output_details[2]["index"]).squeeze()

        classes = [self.labelmap[int(idx)] for idx in class_idxs]

        return {
            "classes": classes,
            "bboxes": bboxes,
            "confidences": confidences,
        }


# Instantiate detector
detector = Detector(MODEL_PATH, LABELMAP_PATH)

# Test model on random input data
#img = np.array(np.random.random_sample((1, 300, 300, 3)), dtype=np.uint8)

# Load image
img_path = glob.glob(INPUT_PATTERN)[0]
img = Image.open(img_path)

# Perform inference
result = detector.predict(img)

# Parse result
classes = result["classes"]
bboxes = result["bboxes"]
confidences = result["confidences"]

# Print result
print("class | confidence | bbox")
for idx in range(len(classes)):
    print("{} | {} | {}".format(
        classes[idx],
        confidences[idx],
        bboxes[idx],
    ))

'''

Input:
The model takes an image as input. The expected image is 300x300 pixels, with
three channels (red, blue, and green) per pixel. This should be fed to the model
as a flattened buffer of 270,000 byte values (300x300x3). Since the model is
quantized, each value should be a single byte representing a value between 0 and
255.
'''
import numpy as np
import tensorflow as tf


##############
# PARAMETERS #
##############


model_path = "model/detect.tflite"
labelmap_path = "model/labelmap.txt"


########
# CODE #
########

class Detector(object):
    def __init__(self, model_path, labelmap_path):
        # load labelmap
        with open(labelmap_path, "r") as text_file:
            self.labelmap = [a.strip("\n") for a in text_file.readlines()]

        # Load TFLite model and allocate tensors.
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict(self, img):
        img = self._preprocess(img)

        self.interpreter.set_tensor(self.input_details[0]['index'], img)
        self.interpreter.invoke()

        return self._get_outputs()

    def _preprocess(self, img):
        input_shape = self.input_details[0]['shape']

        # TODO Test model on random input data.
        return np.array(np.random.random_sample(input_shape), dtype=np.uint8)

    def _get_outputs(self):
        bboxes = self.interpreter.get_tensor(
            self.output_details[0]['index']).squeeze()
        class_idxs = self.interpreter.get_tensor(
            self.output_details[1]['index']).squeeze()
        confidences = self.interpreter.get_tensor(
            self.output_details[2]['index']).squeeze()

        classes = [self.labelmap[int(idx)] for idx in class_idxs]

        return {
            "classes": classes,
            "bboxes": bboxes,
            "confidences": confidences
        }

detector = Detector(model_path, labelmap_path)

result = detector.predict(None)

classes = result["classes"]
bboxes = result["bboxes"]
confidences = result["confidences"]

print("class | confidence | bbox")
for idx in range(len(classes)):
    print("{} | {} | {}".format(
        classes[idx],
        confidences[idx],
        bboxes[idx]
    ))

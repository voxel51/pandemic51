'''

'''
from PIL import Image

from pandemic51.core.detector import Detector


# parameters
model_path = "model/detect.tflite"
labelmap_path = "model/labelmap.txt"
img_path = "data/test.png"

# instantiate detector
detector = Detector(model_path, labelmap_path)

# Test model on random input data.
# img = np.array(np.random.random_sample((1, 300, 300, 3)), dtype=np.uint8)

# load the image
img = Image.open(img_path)

# make prediction
result = detector.predict(img)

# parse result
classes = result["classes"]
bboxes = result["bboxes"]
confidences = result["confidences"]

# print result
print("class | confidence | bbox")
for idx in range(len(classes)):
    print("{} | {} | {}".format(
        classes[idx],
        confidences[idx],
        bboxes[idx]
    ))

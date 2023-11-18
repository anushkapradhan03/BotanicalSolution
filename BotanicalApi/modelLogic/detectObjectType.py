import os
from django.conf import Settings


import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

basepath = os.path.dirname(__file__)
labelMapRelativePath = 'objectLable/label_map.txt'
lable_map = os.path.join(basepath, labelMapRelativePath)




# Load a pre-trained object detection model from TensorFlow Hub
def load_object_detection_model_from_url(model_url):
    return hub.load(model_url)

# Detect objects in an image using the loaded model
def detect_objects(model, image_path):
    image = tf.image.decode_image(tf.io.read_file(image_path))
    image = tf.image.convert_image_dtype(image, tf.float32)[tf.newaxis, ...]

    # Perform object detection
    detections = model(image)

    return detections

# Get the labels and scores for detected objects
def get_object_labels_and_scores(detections, confidence_threshold=0.5):
    labels = detections['detection_classes'][0].numpy().astype(int)
    scores = detections['detection_scores'][0].numpy()

    # Filter objects based on confidence threshold
    valid_indices = scores >= confidence_threshold
    labels = labels[valid_indices]
    scores = scores[valid_indices]

    return labels, scores

# Main function to detect and classify objects in an image
def detect_and_classify_objects(model, image_path, label_map_path, confidence_threshold=0.5):
    # Load label mapping (convert class indices to object labels)
    label_map = load_label_map(label_map_path)

    # Detect objects in the image
    detections = detect_objects(model, image_path)

    # Get the labels and scores for detected objects
    labels, scores = get_object_labels_and_scores(detections, confidence_threshold)

    # Map class indices to object labels
    object_labels = [label_map[label] for label in labels]

    return object_labels, scores

# Load label mapping
def load_label_map(label_map_path):
    label_map = {}
    with open(label_map_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2:
                label_map[int(parts[0])] = parts[1]
    return label_map



def getObectTypeResult(image_path):
    model_url = "https://tfhub.dev/tensorflow/efficientdet/d4/1"
    label_map_path = lable_map  # Provide a label map file with class indices and labels

    print(label_map_path)
    try:
        print("trying")
        model = load_object_detection_model_from_url(model_url)

        object_labels, scores = detect_and_classify_objects(model, image_path, label_map_path)

        result = {}
        for label, score in zip(object_labels, scores):
            print(f"Object: {label}, Confidence: {score:.4f}")
            result[label] = score

        return result
    except:
        return "error"




def find_highest_score_for_leaf(result):
    if 'leaf' in result:
        highest_score = max(result.values())
        if result['leaf'] == highest_score:
            return True
    return False


def create_key_value_string(result):
    key_value_string = ""
    for key, value in result.items():
        key_value_string += f"{key}: {value:.4f}, "

    # Remove the trailing comma and space
    if key_value_string:
        key_value_string = key_value_string[:-2]

    return key_value_string

def detectIsLeaf(image_path):
    result = {'leaf': 0.9532, 'flower': 0.8965, 'tree': 0.6231}
    result = getObectTypeResult(image_path)
    if(result=="error"):
       message = "Fail To Load"
       isPlant = False
    else:
        isPlant = find_highest_score_for_leaf(result)
        message = create_key_value_string(result)
        print(message)

    return message, isPlant




# if __name__ == '__main__':
#     print('importing objectModel')
import TensorFlow1 as tf
from TensorFlow1 import keras
import tensorflow_hub as hub



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


if __name__ == '__main__':
    print('importing obhejctModel')
    model_url = "https://tfhub.dev/tensorflow/efficientdet/d4/1"
    label_map_path = "label_map.txt"  # Provide a label map file with class indices and labels

    model = load_object_detection_model_from_url(model_url)
    image_path = "example_image.jpg"  # Replace with the path to your image

    object_labels, scores = detect_and_classify_objects(model, image_path, label_map_path)

    for label, score in zip(object_labels, scores):
        print(f"Object: {label}, Confidence: {score:.4f}")
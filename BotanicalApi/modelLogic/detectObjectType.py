import os
from django.conf import Settings



basepath = os.path.dirname(__file__)
labelMapRelativePath = 'objectLable/label_map.txt'
lable_map = os.path.join(basepath, labelMapRelativePath)

def getObectTypeResult(image_path):
    model_url = "https://tfhub.dev/tensorflow/efficientdet/d4/1"
    label_map_path = lable_map  # Provide a label map file with class indices and labels

    print(label_map_path)
    try:
        print("trying")
        # model = load_object_detection_model_from_url(model_url)

        # object_labels, scores = detect_and_classify_objects(model, image_path, label_map_path)

        result = {}
        # for label, score in zip(object_labels, scores):
        #     print(f"Object: {label}, Confidence: {score:.4f}")
        #     result[label] = score

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
    # result = getObectTypeResult(image_path)
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
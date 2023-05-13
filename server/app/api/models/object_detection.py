import numpy as np
from typing import List,Dict,Union,Tuple
import yolov5
import math

class ObjectDetector:

    def __init__(self, model_path="yolov5s.pt"):
        """
        Initializes the ObjectDetector instance.

        Args:
            model_path: Path to the YOLOv5 model state dictionary file.
        """
        # load pretrained model
        self.model = yolov5.load(model_path)
        
        # set model parameters
        self.model.conf = 0.25  # NMS confidence threshold
        self.model.iou = 0.45  # NMS IoU threshold
        self.model.agnostic = False  # NMS class-agnostic
        self.model.multi_label = False  # NMS multiple labels per box
        self.model.max_det = 1000  # maximum number of detections per image

    def detect(self, image: np.ndarray) -> List[Dict[str, Union[str, float, Tuple[int, int, int, int]]]]:
        """
        Detects objects in the input image.

        Args:
            image: Input image as a numpy array.

        Returns:
            A list of dictionaries, where each dictionary corresponds to an object detected in the image and contains the label,
            confidence score, and bounding box coordinates.
        """
        # detect objects in the image
        result = self.model(image) #send the image as an input to the model, and get the output of the detection
                
        # parse results
        predictions = result.pred[0]
        boxes = predictions[:, :4] # x1, y1, x2, y2
        scores = predictions[:, 4]
        categories = predictions[:, 5]
       
        # convert predictions to list of dictionaries
        detections = []
        for i in range(predictions.shape[0]):
            # for each detection calculate the label, confidence score, and bounding box coordinates
            label = result.names[int(categories[i])] #label name for detection
            confidence = float(scores[i]) #confidence score for detection
            bbox = tuple(map(int, boxes[i])) #x1, y1, x2, y2
            detection = {'label': label, 'confidence': confidence, 'bbox': bbox} #dictionary object 
            detections.append(detection) #add to list of detections
        
        return detections #return list of detections
    
    def find_closest_object(self, x, y, objects):
        """
        Find the closest object to the given x,y coordinates among the list of objects.

        Parameters:
        x (int): The x coordinate.
        y (int): The y coordinate.
        objects (list): A list of objects, each represented as a dictionary with a 'bbox' key containing the bounding box 
                        coordinates and a 'width' and 'height' key containing the dimensions of the bounding box.

        Returns:
        dict: The closest object to the given coordinates, represented as a dictionary with the same keys as the input objects.

        """
        min_distance = math.inf  # Initialize the minimum distance to infinity.
        closest_object = None  # Initialize the closest object to None.
        for obj in objects:
            bounding_box = obj['bbox']  # Get the bounding box coordinates of the object.
            obj_x = bounding_box[0]  # Get the x coordinate of the bounding box.
            obj_y = bounding_box[1]  # Get the y coordinate of the bounding box.
            center_x = obj_x + obj.width / 2  # Calculate the center x coordinate of the object.
            center_y = obj_y + obj.height / 2  # Calculate the center y coordinate of the object.
            distance = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)  # Calculate the distance between the object and the given coordinates.
            if distance < min_distance:  # If the distance is less than the minimum distance so far,
                min_distance = distance  # update the minimum distance to the current distance,
                closest_object = obj  # and update the closest object to the current object.
        return closest_object  # Return the closest object found.


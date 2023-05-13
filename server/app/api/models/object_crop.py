from typing import List, Tuple, Dict, Union
import cv2
import numpy as np
import torch
import torchvision.transforms as T

class ObjectCropper:
    
    def __init__(self, output_size: Tuple[int, int] = (224, 224)):
        """
        Initializes the ObjectCropper instance.

        Args:
            output_size: A tuple (height, width) representing the size to which each object is resized.
        """
        self.output_size = output_size
        
        # Load segmentation model
        self.model = torch.hub.load('pytorch/vision:v0.9.0', 'deeplabv3_resnet101', pretrained=True)
        self.model.eval()

    
    def segment_object(self,img, threshold=0.5):
        """
        Segments the object in the input image.

        Args:
            img: Input image as a numpy array.
            threshold: Threshold for the segmentation mask.

        Returns:
            A numpy array representing the segmented object.
        """

        # Convert image to tensor
        img_tensor = T.ToTensor()(img)

        # Run segmentation model on image tensor
        output = self.model(img_tensor.unsqueeze(0))

        # Get the predicted segmentation mask
        seg_mask = output['out'][0].argmax(0).byte().cpu().numpy()

        # Apply binary threshold to the mask to get a binary mask
        binary_mask = (seg_mask > threshold).astype(np.uint8)

        # Find contours in binary mask
        contours, hierarchy = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Crop object from image using contour
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            object_mask = np.zeros_like(binary_mask)
            cv2.drawContours(object_mask, [contour], -1, 255, -1)
            object_crop = img.copy()
            object_crop[object_mask == 0] = 0
            object_crop = object_crop[y:y+h, x:x+w]

        return object_crop

        
    def crop_objects(self, image: np.ndarray, detections: List[Dict[str, Union[str, float, Tuple[int, int, int, int]]]]) -> List[np.ndarray]:
        """
        Crops the objects from the input image specified by the given bounding boxes.

        Args:
            image: Input image as a numpy array.
            detections: A list of dictionaries, where each dictionary corresponds to an object detected in the image and contains the label,
            confidence score, and bounding box coordinates.

        Returns:
            A list of numpy arrays, each representing a cropped object.
        """
        objects = []
        for detection in detections:
            bbox = detection['bbox']
            x,y,w,h = bbox
            obj = self.segment_object(image[y:y+h, x:x+w])
            
            objects.append(obj)
        return objects

    



# import base64
# import gzip
# # create instances of ObjectDetector and ObjectCropper
# detector = ObjectDetector()
# cropper = ObjectCropper()
# with open("C:\\temp\\Projects\\AR_Snipper\\ai\\coco2017\\val2017\\000000019924.jpg",'rb') as image_file:
#     image_data = image_file.read()
#     print(base64.b64decode(gzip.compress(image_data)))
#     image_file.close()
# # load an image
# image = cv2.imread("C:\\temp\\Projects\\AR_Snipper\\ai\\coco2017\\val2017\\000000019924.jpg")
# # detect objects in the image
# lt= detector.detect(image)
# boxes = []
# for item in lt:
#     boxes.append(item['bbox'])
# # crop the detected objects

# # print(boxes)
# cropped_objects = cropper.crop_objects(image,lt)
# # print(len(cropped_objects))
# # display the cropped objects
# for obj in cropped_objects:
#     cv2.imshow("Object", obj)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
    
    
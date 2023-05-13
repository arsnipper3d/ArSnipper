from api.models.object_crop import ObjectCropper
from api.models.object_detection import ObjectDetector
from flask import Blueprint,jsonify

import base64
import numpy as np
import gzip

object_detect = Blueprint('object_detect', __name__)


detector = ObjectDetector()
cropper = ObjectCropper()

object_detect.route('/',methods=['GET'])
object_detect.route('/detect/{img}{x},{y}',methods=['GET'])
def detect(img,x,y):
    # decode the image after decompressing it
    img = base64.b64decode(gzip.decompress(img))
    # convert the image to a numpy array
    img = np.array(img)
    # detect the objects in the image using the object detector(model)
    objects = detector.detect(img)
    
    # send error message if no objects are found
    if len(objects) == 0:
        return jsonify({'status':'500','message':'No objects found'})
    # get the object that the user searched for
    searched_item = detector.find_closest_object(objects,x,y)
    # crop the object
    item_cropped = cropper.crop_objects(img,[searched_item])[0]
    # encode the cropped image after compressing it to send it to the client
    img = base64.b64encode(gzip.compress(item_cropped))
    
    return jsonify({'status':'200','message':'Success','data':img})




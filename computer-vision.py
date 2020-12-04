import os
import sys
import requests
from datetime import datetime
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from PIL import Image, ExifTags
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from credential import *

# client setup
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY))
searching_object = "chair"
confidence_threshold = 0.9

# Function for analyzing image, gives inferred description, categories, and tags
def image_analysis(image_path):
    local_image = open(image_path, "rb")
    # Call API
    image_analysis = computervision_client.analyze_image_in_stream(local_image,         
                                    visual_features=[
                                        VisualFeatureTypes.image_type,
                                        VisualFeatureTypes.categories,
                                        VisualFeatureTypes.tags,
                                        VisualFeatureTypes.description
                                    ])

    print("This image can be described as: {}\n".format(
        image_analysis.description.captions[0].text))

    print("Tags associated with this image:\nTag\t\tConfidence")
    for tag in image_analysis.tags:
        # print("{}\t\t{}".format(tag.name, tag.confidence))
        # keep image if contain desired tag value
        if (tag.name in searching_object) and (tag.confidence >= confidence_threshold):
            print("{}\t\t{}".format(tag.name, tag.confidence))
            print("keeping image")
            return True
 
    print("No", searching_object)
    return False

def fix_orientation(image):
    for orientation in ExifTags.TAGS.keys() : 
        if ExifTags.TAGS[orientation]=='Orientation' : break 
    exif=dict(image._getexif().items())

    if exif[orientation] == 3 : 
        image=image.rotate(180, expand=True)
    elif exif[orientation] == 6 : 
        image=image.rotate(270, expand=True)
    elif exif[orientation] == 8 : 
        image=image.rotate(90, expand=True)
    return image

# Function for object detection
def object_detection(image_path):
    local_image_objects = open(image_path, "rb")
    detect_objects = computervision_client.detect_objects_in_stream(local_image_objects)
    print("io object")
    print(local_image_objects)

    # read in image to be plotted
    img = mpimg.imread(local_image_objects)
    plt.imshow(img)

    print(detect_objects)

    print("Detecting objects in image:")
    if len(detect_objects.objects) == 0:
        print("No objects detected.")
    else:
        file_dir = os.getcwd().replace("\\","/")
        for object in detect_objects.objects:
            # print("Object")
            # print(object)
            print("Object label:", object.object_property)
            print("Confidence:", object.confidence)

            print("object at location {}, {}, {}, {}".format( \
            object.rectangle.x, object.rectangle.x + object.rectangle.w, \
            object.rectangle.y, object.rectangle.y + object.rectangle.h))
            
            # Overlay detected objects on image
            plt.gca().add_patch(Rectangle((object.rectangle.x, object.rectangle.y), object.rectangle.w, object.rectangle.h,
                                edgecolor='red',
                                facecolor='none',
                                lw=2))
            # Crop image to the detected object portion only and save
            image = Image.open(image_path)
            image = fix_orientation(image)
            cropped_img = image.crop((object.rectangle.x, object.rectangle.y, object.rectangle.x + object.rectangle.w, object.rectangle.y + object.rectangle.h))
            output_image_name = file_dir+"/objects/output_"+str(datetime.now().strftime("%Y%m%d%H%M%S"))+".jpg"

            cropped_img.save(output_image_name, "JPEG")

            analysis_result = image_analysis(output_image_name) # need to use this
            if analysis_result is not False:
                cropped_img.save(file_dir+"/desired_object/output_"+str(datetime.now().strftime("%Y%m%d%H%M%S"))+".jpg", "JPEG")

local_image_path_objects = "C:/Users/lisiq.DESKTOP-6HN025I/Documents/Drone/full_chair_side_full_other.JPG"
local_image_objects = open(local_image_path_objects, "rb")

object_detection(local_image_path_objects)
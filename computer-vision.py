import os
import sys
import requests
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from PIL import Image, ExifTags
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

# client setup
subscription_key = "198ed8835a984941bc40400c920fcf90"
endpoint = "https://dronetest.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
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
            return image_path
    # when detected object is not the one we are searching for
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

    # read in image to be plotted
    img = mpimg.imread(local_image_objects)
    plt.imshow(img)

    print(detect_objects)

    print("Detecting objects in image:")
    if len(detect_objects.objects) == 0:
        print("No objects detected.")
    else:
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
            image = Image.open(image_path)
            image = fix_orientation(image)

            analysis_result = image_analysis(image_path) # need to use this
            # attempt convert pillow image to io stream
            # if analysis_result != False: # could this be != null?
            im1 = image.crop((object.rectangle.x, object.rectangle.y, object.rectangle.x + object.rectangle.w, object.rectangle.y + object.rectangle.h))
            #     img_byte_arr = io.BytesIO()
            #     im1.save(img_byte_arr, format='JPEG')
            #     im1_obj = open(img_byte_arr)
            #     detect_objects = computervision_client.detect_objects_in_stream(im1_obj)
            #     print(detect_objects)
            im1.save("output.jpg", "JPEG")
            # im1.show()

    # plt.axis("off")
    plt.show()

local_image_path_objects = "C:/Users/lisiq.DESKTOP-6HN025I/Documents/Drone/full_chair_side_full_other.JPG"
local_image_objects = open(local_image_path_objects, "rb")

object_detection(local_image_path_objects)
# image_analysis(local_image_path_objects, "chair", 0.9)

# coding: utf-8

# # Object Detection Demo
# Welcome to the object detection inference walkthrough!  This notebook will walk you step by step through the process of using a pre-trained model to detect objects in an image. Make sure to follow the [installation instructions](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md) before you start.

# # Imports

# In[22]:


import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import shutil # file movement
from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from pil import Image
# from IPython import get_ipython
# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.9.0'):
  raise ImportError('Please upgrade your TensorFlow installation to v1.9.* or later!')

# get_ipython().run_line_magic('matplotlib', 'inline')


import cv2


from utils import label_map_util

from utils import visualization_utils as vis_util
import sqlite3 as sql


conn = sql.connect("PWP_details.db")
curr = conn.cursor()
curr.execute('''
    create table if not exists pwp_stats(
        id integer primary key AUTOINCREMENT,
        image_name varchar(100) not null,
        brand_name varchar(100) not null,
        number_objects integer not null,
        created_date datetime default current_timestamp
    )
''')



# What model to download.
MODEL_NAME = 'output_inference_graph_v1.pb'
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH = 'C:\\pwp18\\Tensorflow\\workspace3\\training_demo\\trained-inference-graphs\\output_inference_graph_v1.pb\\frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('C:\\pwp18\\Tensorflow\\workspace3\\training_demo', 'label_map.pbtxt')



detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)



def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


# # Detection

# In[31]:


# For the sake of simplicity we will use only 2 images:
# image1.jpg
# image2.jpg
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = 'C:\\pwp18\\Tensorflow\\workspace3\\training_demo\\test'
#TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpeg'.format(i)) for i in range(1,2) ]
PATH1 = 'C:\\pwp18\\Tensorflow\\workspace3\\training_demo\\tested'
# destination for not detected
PATH2 = 'C:\\pwp18\\Tensorflow\\workspace3\\training_demo\\others'


# trial (detected with label)
PATH3 = "C:\\pwp18\\tensorflow\\workspace3\\training_demo\\detected_with_label"

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)


# In[32]:


def run_inference_for_single_image(image, graph):
  with graph.as_default():
    with tf.Session() as sess:
      # Get handles to input and output tensors
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks'
      ]:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
              tensor_name)
      if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

      # Run inference
      output_dict = sess.run(tensor_dict,
                             feed_dict={image_tensor: np.expand_dims(image, 0)})

      # all outputs are float32 numpy arrays, so convert types as appropriate
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
  return output_dict


# In[33]:

def main_function():

  for image_path in os.listdir(PATH_TO_TEST_IMAGES_DIR):#TEST_IMAGE_PATHS:
    saved_image = image_path
    image = Image.open(os.path.join(PATH_TO_TEST_IMAGES_DIR,image_path))
    print(image)
  #   image_name = image_path.split("\\")[-1]

    # the array based representation of the image will be used later in order to prepare the
    # result image with boxes and labels on it.
    image_np = load_image_into_numpy_array(image)
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    # Actual detection.
    output_dict = run_inference_for_single_image(image_np, detection_graph)
    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        output_dict['detection_boxes'],
        output_dict['detection_classes'],
        output_dict['detection_scores'],
        category_index,
        instance_masks=output_dict.get('detection_masks'),
        use_normalized_coordinates=True,
        line_thickness=4)

    
    count = vis_util.count_dede()
    
    for items in count:
      curr.execute(f"insert into pwp_stats(image_name,brand_name,number_objects) values('{image_path}','{items}',{count[items]})")
      conn.commit()
      
    # moving tested images
    if(count):
      saved_image = str(saved_image.split('.')[0]) + ".png"
      plt.figure(figsize=IMAGE_SIZE)

      # save the detected image
      saved_image = os.path.join(PATH3,saved_image)
      im = Image.fromarray(image_np)
      im.save(saved_image)
      
      # we can delete the file instead of moving it as we are keeping detected images with label
      shutil.move(os.path.join(PATH_TO_TEST_IMAGES_DIR,image_path),PATH1)
    else:
      shutil.move(os.path.join(PATH_TO_TEST_IMAGES_DIR,image_path),PATH2)
    
      
  #   plt.figure(figsize=IMAGE_SIZE)
    # plt.imshow(image_np)
      
  print("The count:",vis_util.count_dede())
  exit()

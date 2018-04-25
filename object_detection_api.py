# _*_ coding:utf-8 _*_
import numpy as np
import os
import tensorflow as tf
import json
import time
from PIL import Image
try:
    import urllib.request as ulib
except Exception as e:
    import urllib as ulib
import re
from object_detection.utils import label_map_util    ### CWH: Add object_detection path

if tf.__version__ < '1.6.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.6.0!')


## 官方模型---start
# 模型地址
# https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md
MODEL_NAME = 'data/models/faster_rcnn_inception_resnet_v2_atrous_coco_2018_01_28'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('data/pbtxt','mscoco_label_map.pbtxt')  # CWH: Add object_detection path
# data下mscoco_label_map.pbtxt最大item.id
NUM_CLASSES = 90
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
with detection_graph.as_default():
  config = tf.ConfigProto()
  config.gpu_options.allow_growth = True
  with tf.Session(graph=detection_graph,config=config) as sess:
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
## 官方模型----end

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

# added to put object in JSON
class Object(object):
    def toJSON(self):
        return json.dumps(self.__dict__)
        
# 下载文件
def download_image(url):
    path = parse.urlparse(url).path
    path_arr = path.split('/')
    file_name = path_arr[len(path_arr)-1]
    # 刪除 文件名 方便建立目錄
    del path_arr[len(path_arr)-1]
    # 去除首尾 /
    _path = '/'.join(path_arr).strip('/')
    base_path = os.path.abspath(os.path.dirname(__file__))
    tmp_img_path = os.path.join(base_path,'upload/download/')
    file_name = tmp_img_path+_path+'/'+file_name
    if tf.gfile.Exists(file_name):
        return file_name
    # 創建目錄
    tf.gfile.MakeDirs(tmp_img_path+_path)
    # 下載文件
    ulib.urlretrieve(url, file_name)
    return file_name
# 获取内存(MB)
def memory_usage_psutil():
    import psutil
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem

# image 图片绝对路径 threshold 准确度阀值
def get_objects(file_name, threshold=0.5):
    result = {};
    startTime = time.time()
    if re.match(r'^https?:/{2}\w.+$', file_name):
        file_name = download_image(file_name)
    # 判断文件是否存在
    if not tf.gfile.Exists(file_name):
        result['status'] = 0
        result['msg'] = file_name + ' image file not found'
        return json.dumps(result)
    image = Image.open(file_name)
    # 判断文件是否是jpeg格式
    if not image.format=='JPEG':
        result['status'] = 0
        result['msg'] = file_name+ ' is ' + image.format + ' ods system allow jpeg or jpg'
        return result
    image_np = load_image_into_numpy_array(image)
    image_np_expanded = np.expand_dims(image_np, axis=0)
    output = []
    ## 官方数据
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    classes = np.squeeze(classes).astype(np.int32)
    scores = np.squeeze(scores)
    boxes = np.squeeze(boxes)
    for c in range(0, len(classes)):
        if scores[c] >= threshold:
            item = Object()
            item.class_name = category_index[classes[c]]['name']
            item.score = float(scores[c])
            item.y1 = float(boxes[c][0])
            item.x1 = float(boxes[c][1])
            item.y2 = float(boxes[c][2])
            item.x2 = float(boxes[c][3])
            output.append(item)
    outputJson = json.dumps([ob.__dict__ for ob in output])
    return outputJson

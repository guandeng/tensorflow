#!/bin/bash

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
cd $DIR

echo "rcnn Dowloading..."

cd data/models/
wget -c http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_resnet_v2_atrous_coco_2018_01_28.tar.gz

echo "rcnn Extracting..."
tar -zxvf faster_rcnn_inception_resnet_v2_atrous_coco_2018_01_28.tar.gz
rm faster_rcnn_inception_resnet_v2_atrous_coco_2018_01_28.tar.gz 

echo "tensorflow models Dowloading..."
cd ../tf_models/
git clone --depth=1 https://github.com/tensorflow/models
cp models/research/object_detection/data/*.pbtxt ../pbtxt
cd models/research/
protoc object_detection/protos/*.proto --python_out=.

echo 'Done...'
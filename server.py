# _*_ coding:utf-8 _*_
#coding=utf-8
import os
from PIL import Image
from flask import Flask, request, Response,send_from_directory,render_template
import time

app = Flask(__name__,static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT']=1
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


@app.route('/local')
def local():
    return render_template("local.html")

@app.route('/video')
def video():
    return render_template("video.html")
    
@app.route('/upload')
def upload():
    return render_template("upload.html")


@app.route('/')
def index():
    import object_detection_api
    PATH_TO_TEST_IMAGES_DIR = 'test_images'  # cwh
    TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(3, 4)]
    image = Image.open(TEST_IMAGE_PATHS[0])
    objects = object_detection_api.get_objects(image)
    return objects

# 网页上传图片
@app.route('/image', methods=['POST','GET'])
def image():
    import object_detection_api
    startTime = time.time()
    if request.method=='POST':
        #保存上传图片
        image_file = request.files['file']
        base_path = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(base_path,'static/upload/')
        file_name = upload_path + image_file.filename
        image_file.save(file_name)
        threshold = request.form.get('threshold',0.5)
        objects = object_detection_api.get_objects(file_name, threshold)
        print("-------total time: %f" % (time.time() - startTime))
        return render_template('index.html',json_data = objects,img=image_file.filename)
    return 'method error'

# 服务器图片路径
@app.route('/getObject/', methods=['GET'])
def getObject():
    startTime = time.time()
    import object_detection_api
    if request.method=='GET':
        threshold = request.args.get('threshold',0.5)
        file_name = request.args.get('file_name')
        objects = object_detection_api.get_objects(file_name, threshold)
        print("-------getObject total time: %f" % (time.time() - startTime))
        return objects
    return 'method error'

# 摄像头|视频
@app.route('/check', methods=['POST', 'GET'])
def check():
    startTime = time.time()
    import object_detection_api
    if request.method == 'POST':
        image_file = request.files['file']
        base_path = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(base_path, 'static/upload/')
        file_name = upload_path + image_file.filename
        image_file.save(file_name)
        threshold = float(request.form.get('threshold',0.5))
        objects = object_detection_api.get_objects(file_name, threshold)
        return objects
    return 'method error'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

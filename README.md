## Tensorflow图像物体识别api
提供官网模型和自己训练模型同时识别物体

## 环境要求
- Python3
-Tensorflow >= 1.6
- Numpy


## 安装和启动
```
$ pip3 install -r requirements.txt
$ git clone https://github.com/guandeng/tensorflow.git
$ sh sh/download_data.sh
$ echo 'export PYTHONPATH=$PYTHONPATH:`pwd`/data/tf_models/models/research'>> ~/.bashrc && source ~/.bashrc 
$ python3 server.py &
```

## 接口使用说明
```
curl http://0.0.0.0:5000/getObject/?file_name=https://cp1.100.com.tw/service/active/2018/03/27/152214075820684207_1500x1040xscale1xsid8788.jpg&threshold=0.5
```
- filename 图片链接
- threshold  准确度阀值（0-1）之间
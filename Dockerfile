FROM gcr.io/tensorflow/tensorflow:latest-gpu

WORKDIR /tmp

# 升级pip 
RUN pip install --upgrade pip

# 安装pip3
RUN wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate \
    && python3 get-pip.py

# 安装tensorflow-gpu
RUN pip3 install tensorflow-gpu==1.6.0

# 安装cuda-9.0
WORKDIR /home/docker 
RUN wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.0.176-1_amd64.deb && \
    dpkg -i cuda-repo-ubuntu1604_9.0.176-1_amd64.deb && \
    apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub && \
    apt-get update && \
    apt-get install cuda-9.0 -y

# 安装cudnn
RUN tar -zxvf cudnn-9.0-linux-x64-v7.tgz && \
    cp -rf cuda/lib64/libcudnn.so* /usr/local/cuda-9.0/lib64/ && \
    cp cuda/include/* /usr/local/cuda-9.0/include/ && \
    export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# 安装git
RUN apt-get update -y && \
    apt-get install git wget protobuf-compiler python-pil python-lxml python-tk -y && \
    apt-get install dpkg -y && \
    pip3 install --user pillow lxml jupyter matplotlib

# 装python模块
RUN pip3 install pillow \
    && pip3 install flask \
    && apt install protobuf-compiler \ 
    && apt-get install python3-dev
# FROM ubuntu:18.04

# ENV DEBIAN_FRONTEND=noninteractive

# RUN apt-get update \
#   && apt-get -y install tesseract-ocr \
#   && apt-get install -y python=3.8 python3-distutils python3-pip \
#   && cd /usr/local/bin \
#   && ln -s /usr/bin/python3 python \
#   && pip3 --no-cache-dir install --upgrade pip \
#   && rm -rf /var/lib/apt/lists/*

# #RUN apt update \
# #  && apt-get install ffmpeg libsm6 libxext6 -y
# RUN pip3 install pytesseract
# RUN pip3 install opencv-python
# #RUN pip3 install pillow

# COPY . /app
# WORKDIR /app

# RUN pip install -r requirements.txt
# ENV LC_ALL=C.UTF-8
# ENV LANG=C.UTF-8
FROM python:3.8

RUN apt-get update
RUN apt-get -y install tesseract-ocr libgl1-mesa-dev
#    tesseract-ocr-jpn \
#    libgl1-mesa-dev; 
RUN apt-get clean

RUN pip install --upgrade pip; \
    pip install \
#    pillow \
    opencv-python \
    pytesseract
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
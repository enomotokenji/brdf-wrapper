FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    build-essential \
    git \
    curl \
    wget \
    zip \
    unzip \
    ca-certificates \
    libffi-dev \
    libtbb2 \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libtbb-dev \
    libtiff-dev \
    libjpeg-dev \
    libpng-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libavformat-dev \
    libpq-dev \
    libxrender-dev \
    htop && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN wget https://github.com/Kitware/CMake/releases/download/v3.16.5/cmake-3.16.5.tar.gz && \
    tar -zxvf cmake-3.16.5.tar.gz && \
    cd cmake-3.16.5 && \
    ./bootstrap && \
    make && \
    make install && \
    cd /

RUN apt update && \
    apt -y upgrade && \
    apt install -y python3-pip

RUN pip3 install numpy opencv-python==4.2.0.34 tqdm joblib pytest pybind11


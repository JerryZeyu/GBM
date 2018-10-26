#!/usr/bin/env bash
# Download data
DATA_DIR=./data
mkdir -p $DATA_DIR
wget https://www.kaggle.com/c/icdar2013-gender-prediction-from-handwriting/download/train.zip -O $DATA_DIR/train.zip
wget https://www.kaggle.com/c/icdar2013-gender-prediction-from-handwriting/download/test.zip -O $DATA_DIR/test.zip
unzip $DATA_DIR/train.zip -d $DATA_DIR
unzip $DATA_DIR/test.zip -d $DATA_DIR

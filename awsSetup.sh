#!/bin/bash

# setup script for testStrips image processing

#Steps
# 1) ssh -i "myTestKey.pem" ubuntu@ec2-34-229-128-58.compute-1.amazonaws.com
 ## Collin has original pem
# 2) run this script to set up directory structure
# 3) once
# create deep learning ami instance with aws

cd ~
mkdir -p ~/scripts
mkdir -p ~/images
mkdir -p ~/images/processed_shards
mkdir -p ~/images/raw-data
mkdir -p ~/images/raw-data/4.0-6.0
mkdir -p ~/images/raw-data/6.5-7.5
mkdir -p ~/images/raw-data/8.0-9.0
ls ~/images/raw-data/ > labels.txt
mv labels.txt ~/images/raw-data/

aws configure
# AWSAccessKeyId=AKIAJCZI77S6ZRTFVTYQ
# AWSSecretKey=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
# Default_region=us-east-1

if [ -z "$(ls -A images/raw-data/4.0-6.0)" ]; then
	echo "Enter these when promted"
	echo "AWSAccessKeyId=AKIAJCZI77S6ZRTFVTYQ"
    echo "AWSSecretKey=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"
    echo "Default_region=us-east-1"
    ## configure to pull from s3
	aws configure
	## pull from s3
	aws s3 cp s3://teststripts4.0-6.0 ~/images/raw-data/4.0-6.0
	aws s3 cp s3://teststripts6.5-7.5 ~/images/raw-data/6.5-7.5
	aws s3 cp s3://teststrips8.0-9.0 ~/images/raw-data/8.0-9.0
fi

## clone tensorflow from git if doesnt exist
if [ ! -z ~/models ]; then
	git clone https://github.com/tensorflow/models.git
	cd models/inception/inception
fi

## build other models if desired
# bazel build //inception:imagenet_train

######################
## build shards
set -e

# Create the output and temporary directories.
BASE_DIR="/home/ubuntu/"
DATA_DIR="${BASE_DIR}/images/"
OUTPUT_DIRECTORY="${DATA_DIR}/processed_shards"
SCRATCH_DIR="${DATA_DIR}/raw-data"
WORK_DIR="${BASE_DIR}/models/inception/inception/data"
OUTPUT_DIRECTORY="${DATA_DIR}"

# Note the locations of the train and validation data.
TRAIN_DIRECTORY="${SCRATCH_DIR}/train"
VALIDATION_DIRECTORY="${SCRATCH_DIR}/validation"

LABELS_FILE="${SCRATCH_DIR}/labels.txt"
# Generate the validation data set.
while read LABEL; do
  echo "$LABEL"
  VALIDATION_DIR_FOR_LABEL="${VALIDATION_DIRECTORY}/${LABEL}"
  TRAIN_DIR_FOR_LABEL="${TRAIN_DIRECTORY}/${LABEL}"
  # Move the first randomly selected 25 images to the validation set (we want this to be at least 100)
  mkdir -p "${VALIDATION_DIR_FOR_LABEL}"
  VALIDATION_IMAGES=$(ls -1 "${TRAIN_DIR_FOR_LABEL}" | shuf | head -25)
  for IMAGE in ${VALIDATION_IMAGES}; do
    mv -f "${TRAIN_DIRECTORY}/${LABEL}/${IMAGE}" "${VALIDATION_DIR_FOR_LABEL}"
  done
done < "${LABELS_FILE}"

# Build the TFRecords version of the image data.
BUILD_SCRIPT="${WORK_DIR}/build_image_data.py"
python "${BUILD_SCRIPT}" \
  --train_directory="${TRAIN_DIRECTORY}" \
  --validation_directory="${VALIDATION_DIRECTORY}" \
  --output_directory="${OUTPUT_DIRECTORY}" \

## move shards to s3 so we can easily read them when running training model
aws s3 mb s3://shards
aws s3 sync ~/images/processed_shards s3://shards



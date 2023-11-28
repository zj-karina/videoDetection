import json
import os
from random import choice
import shutil
from google_drive_downloader import GoogleDriveDownloader as gdd

# Load Kaggle credentials
with open('kaggle.json', 'r') as f:
    data = json.load(f)
    os.environ['KAGGLE_USERNAME'] = data["username"]
    os.environ['KAGGLE_KEY'] = data["key"]

# Download and unzip dataset
os.system("kaggle datasets download -d valentynsichkar/traffic-signs-dataset-in-yolo-format")
os.system("unzip traffic-signs-dataset-in-yolo-format.zip")

# Setup directory names
train_path = "train"
val_path = "val"
crs_path = "ts/ts"

# Decide the ratio in which the dataset needs to be divided
train_ratio = 0.8
val_ratio = 0.2

# Total count of images
total_img_count = len(os.listdir(crs_path))/2

# Sort count of images
imgs = [f for f in os.listdir(crs_path) if not f.endswith(".txt")]
xmls = [f for f in os.listdir(crs_path) if f.endswith(".txt")]

# Count range for cycles
count_for_train = int(len(imgs) * train_ratio)
count_for_val = int(len(imgs) * val_ratio)
print("Training images are : ", count_for_train)
print("Validation images are : ", count_for_val)

# Create directories in kaggle/working path
train_image_path = "dataset/images/train"
train_label_path = "dataset/labels/train"
val_image_path = "dataset/images/val"
val_label_path = "dataset/labels/val"

for path in [train_image_path, train_label_path, val_image_path, val_label_path]:
    if not os.path.isdir(path):
        os.makedirs(path)

# For training images
for _ in range(count_for_train):
    file_jpg = choice(imgs)
    file_xml = file_jpg[:-4] + ".txt"
    
    shutil.copy(os.path.join(crs_path, file_jpg), os.path.join(train_image_path, file_jpg))
    shutil.copy(os.path.join(crs_path, file_xml), os.path.join(train_label_path, file_xml))
    
    imgs.remove(file_jpg)
    xmls.remove(file_xml)

# For validation images
for _ in range(count_for_val):
    file_jpg = choice(imgs)
    file_xml = file_jpg[:-4] + ".txt"
    
    shutil.copy(os.path.join(crs_path, file_jpg), os.path.join(val_image_path, file_jpg))
    shutil.copy(os.path.join(crs_path, file_xml), os.path.join(val_label_path, file_xml))
    
    imgs.remove(file_jpg)
    xmls.remove(file_xml)

# Download dataset.yaml
gdd.download_file_from_google_drive(file_id='1KtlDXpLCfqoklUTdrnVASNbxL_AK9qnx',
                                    dest_path='dataset/dataset.yaml')
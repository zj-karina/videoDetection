# videoDetection

## Libraries
Download all necessary libraries to start the project
```
cd yolov5
pip install -r requirements.txt
pip install googledrivedownloader
```
## Data preparation
Prepare data before training
```
python3 preprocess_data.py
```
## For train
```
CUDA_VISIBLE_DEVICES=<number of card> python3 train.py --img 415 --batch 16 --data dataset/dataset.yaml --weights yolov5x.pt --workers 16
```
## For inference
```
CUDA_VISIBLE_DEVICES=<number of card> python3 detect.py --source "dataset/images/val/00879.jpg" --weights runs/train/exp3/weights/best.pt --data dataset/dataset.yaml
```

You can find a separate use case for the finished model in the directory `notebook`

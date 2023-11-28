import os
os.environ['CURL_CA_BUNDLE'] = ''
import torch
import gradio as gr
import cv2

RETURN_FREQ = 10

model = torch.hub.load("ultralytics/yolov5", "yolov5s")


def process_video(input_video):
    cap = cv2.VideoCapture(input_video)

    output_path = "output.mp4"

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    iterating, frame = cap.read()
    i = 0
    while iterating:
        
        # flip frame vertically
        result = model(frame)
        display_frame =  result.render()[0] 

        video.write(frame)
        if i % RETURN_FREQ == RETURN_FREQ -1:
            yield display_frame, None
        i += 1
        

        iterating, frame = cap.read()

    video.release()
    yield display_frame, output_path

with gr.Blocks() as demo:
    with gr.Row():
        input_video = gr.Video(label="input")
        processed_frames = gr.Image(label="last frame")
        output_video = gr.Video(label="output")

    with gr.Row():
        examples = gr.Examples(["/home/maksim/Videos/test_cut.mp4"], inputs=input_video)
        process_video_btn = gr.Button("process video")

    process_video_btn.click(process_video, input_video, [processed_frames, output_video])

demo.queue()
demo.launch()


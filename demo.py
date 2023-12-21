from argparse import ArgumentParser
import torch
import gradio as gr
from video_processing import VideoProcessor




def run_demo(example_path, process_video):
    with gr.Blocks() as demo:
        with gr.Row():
            input_video = gr.Video(label="input")
            processed_frames = gr.Image(label="last frame")
            output_video = gr.Video(label="output")

        with gr.Row():
            examples = gr.Examples([example_path], inputs=input_video)
            process_video_btn = gr.Button("process video")

        process_video_btn.click(process_video, input_video, [processed_frames, output_video])

    demo.queue()
    demo.launch()



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--checkpoint_path", type=str, default="./checkpoints/yolov5s.pt")
    parser.add_argument("--example_path", type=str, default="./examples/test_vid.mp4")
    parser.add_argument("--return_freq", type=int, default=10)
    args = parser.parse_args()
    
    checkpoint_path = args.checkpoint_path
    example_path = args.example_path
    return_freq = args.return_freq
    
    
    model = torch.hub.load('./yolov5', 'custom', path=checkpoint_path, source='local', force_reload=True) 
    processor = VideoProcessor(model=model, 
                               return_freq=return_freq)

    
    run_demo(example_path=example_path,
             process_video=processor.process_video)
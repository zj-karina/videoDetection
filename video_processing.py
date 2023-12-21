import cv2


class VideoProcessor:
    def __init__(self, model, return_freq, output_path="output.mp4") -> None:
        self.model = model 
        self.return_freq = return_freq
        self.output_path = output_path

    def process_video(self, input_video):
        cap = cv2.VideoCapture(input_video)


        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        video = cv2.VideoWriter(self.output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

        iterating, frame = cap.read()
        i = 0
        while iterating:
            # flip frame vertically
            result = self.model(frame)
            display_frame =  result.render()[0] 
            display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)


            video.write(frame)
            if i % self.return_freq == self.return_freq -1:
                yield display_frame, None
            i += 1
            

            iterating, frame = cap.read()

        video.release()
        yield display_frame, self.output_path
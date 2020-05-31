"""
Dveloper: Sungjun Yoon
E-mail: sjyoon1671@gmail.com
Github: https://github.com/vujadeyoon
Date: May 31, 2020.

Title: main_writing_video.py
Version: 0.1
Description: A main test file for writing a video after reading a video.
"""


import os
import argparse
import cv2
from vujade import vujade_utils as utils_
from vujade import vujade_videocv as videocv_
from vujade import vujade_imgcv as imgcv_
from vujade.vujade_utils import str2bool


parser = argparse.ArgumentParser(description='Test for python based video processing')
parser.add_argument('--name_video_src', type=str, default='test_1.mp4', help='The name of test video to be read')
parser.add_argument('--name_video_dst', type=str, default='test_1.avi', help='The name of test video to be written')
parser.add_argument('--num_batch', type=int, default=5, help='batch size')
parser.add_argument('--num_proc', type=int, default=4, help='The number of processes')
parser.add_argument("--opt_reading_opencv", type=str2bool, default=True, help='Video-imread: i) True: opencv-python, ii) False: FFmpeg-python')
parser.add_argument("--opt_writing_opencv", type=str2bool, default=False, help='Video-imwrite: i) True: opencv-python, ii) False: FFmpeg-python')
args = parser.parse_args()


if __name__ == "__main__":
    # python3 main_writing_video.py --opt_reading_opencv True --opt_writing_opencv True

    # Load parameters
    option_imread_cv2 = args.opt_reading_opencv
    option_imread_ffmpeg = not option_imread_cv2
    option_imwrite_cv2 = args.opt_writing_opencv
    option_imwrite_ffmpeg = not option_imwrite_cv2
    option_imread = list(filter(None, ['opencv-python' * option_imread_cv2, 'FFmpeg-python' * option_imread_ffmpeg]))[0]
    option_imwrite = list(filter(None, ['opencv-python' * option_imwrite_cv2, 'FFmpeg-python' * option_imwrite_ffmpeg]))[0]

    eps_val = 1e-9

    path_video_src = os.path.join(os.getcwd(), 'test_input', args.name_video_src)
    path_video_dst = os.path.join(os.getcwd(), 'test_output', args.name_video_dst)

    avgmeter_time = utils_.avgmeter_time(_num_batch=args.num_batch)

    # Open videos and processes
    if option_imread == 'opencv-python':
        cv_video_src = videocv_.VideoReaderCV(_path_video=path_video_src)
        if option_imwrite == 'opencv-python':
            cv_video_dst = videocv_.VideoWriterCV(_path_video=path_video_dst, _resolution=(cv_video_src.height, cv_video_src.width), _fps=30.0)
        else:
            ffmpeg_video_dst = videocv_.VideoWriterFFmpeg(_path_video=path_video_dst, _resolution=(cv_video_src.height, cv_video_src.width), _fps=cv_video_src.fps, _qp_val=0, _pix_fmt='bgr24')
    else:
        FFmpeg_video_src = videocv_.VideoReaderFFmpeg(_path_video=path_video_src, _channel=3, _pix_fmt='bgr24')
        if option_imwrite == 'opencv-python':
            cv_video_dst = videocv_.VideoWriterCV(_path_video=path_video_dst, _resolution=(FFmpeg_video_src.height, FFmpeg_video_src.width), _fps=30.0)
        else:
            ffmpeg_video_dst = videocv_.VideoWriterFFmpeg(_path_video=path_video_dst, _resolution=(FFmpeg_video_src.height, FFmpeg_video_src.width), _fps=FFmpeg_video_src.fps, _qp_val=0, _pix_fmt='bgr24')

    # Process
    if option_imread == 'opencv-python':
        while cv_video_src.is_not_eof:
            avgmeter_time.tic()
            frames_src = cv_video_src.imread(_num_batch_frames=args.num_batch, _trans=None, _set_idx_frame=None)

            if option_imwrite == 'opencv-python':
                cv_video_dst.imwrite(_list_img=list(frames_src))
            else:
                ffmpeg_video_dst.imwrite(_list_img=frames_src)
            avgmeter_time.toc()
    else:
        while True:
            avgmeter_time.tic()
            frames_src = FFmpeg_video_src.imread(_num_batch_frames=args.num_batch, _trans=None)

            if option_imwrite == 'opencv-python':
                cv_video_dst.imwrite(_list_img=list(frames_src))
            else:
                ffmpeg_video_dst.imwrite(_list_img=frames_src)

            avgmeter_time.toc()

            if FFmpeg_video_src.is_eof is True:
                break

    # Close videos and processes
    if option_imread == 'opencv-python':
        cv_video_src.close()

    if option_imwrite == 'opencv-python':
        cv_video_dst.close()
    else:
        ffmpeg_video_dst.close()
    
    print('Video-imread: {} / Frame-imwrite: {}'.format(option_imread, option_imwrite))
    print('Total: {:.2f} [{:.2f} FPS] / AVG: {:.2f} [{:.2f} FPS]'.format(avgmeter_time.time_total, avgmeter_time.fps_total, avgmeter_time.time_avg, avgmeter_time.fps_avg))

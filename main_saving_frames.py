"""
Dveloper: Sungjun Yoon
E-mail: sjyoon1671@gmail.com
Github: https://github.com/vujadeyoon
Date: May 31, 2020.

Title: main_saving_frames.py
Version: 0.1
Description: A main test file for saving all frames after reading a video.
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
parser.add_argument('--num_batch', type=int, default=5, help='batch size')
parser.add_argument('--num_proc', type=int, default=4, help='The number of processes')
parser.add_argument("--opt_reading_opencv", type=str2bool, default=True, help='Video-imread: i) True: opencv-python, ii) False: FFmpeg-python')
parser.add_argument("--opt_writing_single_proc", type=str2bool, default=False, help='Frame-imwrite: i) True: single-process, ii) False: multi-process')
args = parser.parse_args()


if __name__ == "__main__":
    # Load parameters
    option_imread_cv2 = args.opt_reading_opencv
    option_imread_ffmpeg = not option_imread_cv2
    option_imwrite_proc_single = args.opt_writing_single_proc
    option_imwrite_proc_multi = not option_imwrite_proc_single
    option_imread = list(filter(None, ['opencv-python' * option_imread_cv2, 'FFmpeg-python' * option_imread_ffmpeg]))[0]
    option_imwrite = list(filter(None, ['single-process' * option_imwrite_proc_single, 'multi-process' * option_imwrite_proc_multi]))[0]

    eps_val = 1e-9

    path_video_src = os.path.join(os.getcwd(), 'test_input', args.name_video_src)
    path_img_dst = os.path.join(os.getcwd(), 'test_output')

    avgmeter_time = utils_.avgmeter_time(_num_batch=args.num_batch)

    # Open videos and processes
    if option_imread == 'opencv-python':
        cv_video_src = videocv_.VideoReaderCV(_path_video=path_video_src)
    else:
        FFmpeg_video_src = videocv_.VideoReaderFFmpeg(_path_video=path_video_src, _channel=3, _pix_fmt='bgr24')

    if option_imwrite == 'multi-process':
        imwriterMP = imgcv_.ImwriterMP(_num_proc=args.num_proc)

    # Process
    if option_imread == 'opencv-python':
        while cv_video_src.is_not_eof:
            avgmeter_time.tic()
            frames_src = cv_video_src.imread(_num_batch_frames=args.num_batch, _trans=None, _set_idx_frame=None)

            if option_imwrite == 'single-process':
                list_frames, list_idx_frames = imgcv_.get_list_frames(_ndarr_frames=frames_src, _idx_frame_curr=cv_video_src.idx_frame_curr)
                for idx, (frame, idx_frame) in enumerate(zip(list_frames, list_idx_frames)):
                    cv2.imwrite(filename=os.path.join(path_img_dst, 'frame_CV_SP_{:08d}.png'.format(idx_frame)), img=frame)
            else:
                list_frames, list_idx_frames = imwriterMP.get_list_frames(_ndarr_frames=frames_src, _idx_frame_curr=cv_video_src.idx_frame_curr)
                imwriterMP.imwrite(_list_img=list_frames, _path_img=os.path.join(path_img_dst, 'frame_CV_MP.png'), _list_postfix_num=list_idx_frames, _img_extension='.png')
            avgmeter_time.toc()

    else:
        while True:
            avgmeter_time.tic()
            frames_src = FFmpeg_video_src.imread(_num_batch_frames=args.num_batch, _trans=None)

            if option_imwrite == 'single-process':
                list_frames, list_idx_frames = imgcv_.get_list_frames(_ndarr_frames=frames_src, _idx_frame_curr=FFmpeg_video_src.idx_frame_curr)
                for idx, (frame, idx_frame) in enumerate(zip(list_frames, list_idx_frames)):
                    cv2.imwrite(filename=os.path.join(path_img_dst, 'frame_FFmpeg_SP_{:08d}.png'.format(idx_frame)), img=frame)
            else:
                list_frames, list_idx_frames = imwriterMP.get_list_frames(_ndarr_frames=frames_src, _idx_frame_curr=FFmpeg_video_src.idx_frame_curr)
                imwriterMP.imwrite(_list_img=list_frames, _path_img=os.path.join(path_img_dst, 'frame_FFmpeg_MP.png'), _list_postfix_num=list_idx_frames, _img_extension='.png')

            avgmeter_time.toc()

            if FFmpeg_video_src.is_eof is True:
                break


    # Close videos and processes
    if option_imread == 'opencv-python':
        cv_video_src.close()
    if option_imwrite == 'multi-process':
        imwriterMP.close()

    print('Video-imread: {} / Frame-imwrite: {}'.format(option_imread, option_imwrite))
    print('Total: {:.2f} [{:.2f} FPS] / AVG: {:.9f} [{:.2f} FPS]'.format(avgmeter_time.time_total, avgmeter_time.fps_total, avgmeter_time.time_avg, avgmeter_time.fps_avg))

"""
Dveloper: Sungjun Yoon
E-mail: sjyoon1671@gmail.com
Github: https://github.com/vujadeyoon
Date: May 31, 2020.

Title: vujade_imgcv.py
Version: 0.1
Description: Image processing with computer vision module
"""


import os
import cv2
from vujade import vuajde_multiprocess as multiprocess_


class _ImwriterMP(multiprocess_._BaseMultiProcess):
    def __init__(self, _num_proc=os.cpu_count()):
        super(_ImwriterMP, self).__init__(_target_method=self._target_method, _num_proc=_num_proc)

    def _target_method(self, queue):
        # Todo: To be coded.
        while True:
            if not queue.empty():
                filename, ndarr = queue.get()
                if filename is None:
                    break
                cv2.imwrite(filename=filename, img=ndarr)


    def proc_enqueue(self, _list_img, _path_img, _list_postfix_num=None, _img_extension='.png'):
        # Todo: To be coded.
        for idx, (img, postfix_num) in enumerate(zip(_list_img, _list_postfix_num)):
            if _list_postfix_num is None:
                path = '{}{}'.format(_path_img, _img_extension)
            else:
                path = _path_img.replace(_img_extension, '_{:08d}{}'.format(postfix_num, _img_extension))

            self.queue.put((path, img))


class ImwriterMP(_ImwriterMP):
    def __init__(self, _num_proc):
        super(ImwriterMP, self).__init__(_num_proc=_num_proc)
        self._proc_setup()

    def imwrite(self, _list_img, _path_img, _list_postfix_num, _img_extension):
        self.proc_enqueue(_list_img=_list_img, _path_img=_path_img, _list_postfix_num=_list_postfix_num, _img_extension=_img_extension)

    def close(self):
        self._proc_release()

    def get_list_frames(self, _ndarr_frames, _idx_frame_curr):
        list_frames = list(_ndarr_frames)

        idx_frame_start = _idx_frame_curr - (len(list_frames) - 1)
        idx_frame_end = idx_frame_start + len(list_frames)
        list_idx_frames = list(range(idx_frame_start, idx_frame_end))

        return list_frames, list_idx_frames


def get_list_frames(_ndarr_frames, _idx_frame_curr):
    list_frames = list(_ndarr_frames)

    idx_frame_start = _idx_frame_curr - (len(list_frames) - 1)
    idx_frame_end = idx_frame_start + len(list_frames)
    list_idx_frames = list(range(idx_frame_start, idx_frame_end))

    return list_frames, list_idx_frames
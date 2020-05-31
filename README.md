# Fast Video Processing in Python 
- Fast video processing in python using batch-processing and multi-processing.
  - Fast reading a video
  - Fast writing a video
  - Fast saving frames in a video


## Table of contents
1.  [Notice](#notice)
2.  [License](#license)
3.  [Development envrionment](#envs)
4.  [Preparation to run a demo code](#preparation)
5.  [Run a demo code](#demo)
6.  [Experiment result](#exp_res)
7.  [Revision history](#revision_history)


## 1. Notice <a name="notice"></a>
- I recommend that you should ignore the commented instructions with an octothorpe, #.
- Modified date: May 31, 2020.
- Developed version: 200531a


## 2. License <a name="license"></a>
- All providen codes comply with the MIT license.


## 3. Development environment <a name="envs"></a>
- Operating System (OS): Ubuntu MATE 18.04.3 LTS (Bionic)
- CPU: Intel Core i7-7700 CPU @ 3.60GHz x 8
- Main memory: 32GB
- GPU: Titan XP, 1ea
- Python version: Python 3.7.6
- Python main package:
    - opencv-python: 4.1.2.30 
    - ffmpeg-python: 0.2.0 


## 4. Preparation to run a demo code <a name="preparation"></a>
A. Reference to the website,
<a href="https://github.com/vujadeyoon/DL-UbuntuMATE18.04LTS-Installation#pip_virtualenv" title="virtualenv-python">
virtualenv-python</a>,
<a href="https://pypi.org/project/opencv-python/" title="opencv-python">
opencv-python</a>
and
<a href="https://github.com/kkroening/ffmpeg-python" title="ffmpeg-python">
ffmpeg-python</a>.
<br />
- If you don't have installed Python, please refer to the site, virtualenv-python, above.

B. Activate a virtualenv.<br />
- The root directory for the virtualenv: /home/usrname/pip3_virtualenv
- The name of virtualenv to be activated: virenv_dl
```bash
usrname@hostname:~/curr_path$ source /home/usrname/pip3_virtualenv/virenv_dl/bin/activate
```

C. Install the required main packages.<br />
```bash
(virenv_dl) usrname@hostname:~/curr_path$ pip3 install opencv-python
(virenv_dl) usrname@hostname:~/curr_path$ pip3 install ffmpeg-python
```


## 5. Run a demo code <a name="demo"></a>
- A demo code is a test code that reads a video and saves all frames in the video or writes another video.
- The measured time is the time including all the prcoessing time (e.g. reading, saving or writing).
- I use a HD1080 video (i.e. ./test_input/test_1.mp4) as a test video source.
- Please note that I cannot provide a test video, but you can test any video you want.
- Please note that you should check the arguemnts in the main python script. Some examples are as follows.
  - name_video_src: The name of test video source.
  - num_batch: The numebr of batch size for batch-processing in reading a video.
  - num_proc:  The numebr of processes for multi-processing in wrting frames.

A. Reading a vdieo: opencv-python, Saving frames: opencv-python (single-process)
```bash
(virenv_dl) usrname@hostname:~/curr_path$ python3 main_saving_frames.py --opt_reading_opencv True --opt_writing_single_proc True
```
B. Reading a vdieo: opencv-python, Saving frames: opencv-python (multi-process)
```bash
(virenv_dl) usrname@hostname:~/curr_path$ python3 main_saving_frames.py --opt_reading_opencv True --opt_writing_single_proc False
```
C. Reading a vdieo: ffmpeg-python, Saving frames: opencv-python (single-process)
```bash
(virenv_dl) usrname@hostname:~/curr_path$ python3 main_saving_frames.py --opt_reading_opencv False --opt_writing_single_proc True
```
D. Reading a vdieo: ffmpeg-python, Saving frames: opencv-python (multi-process)
```bash
(virenv_dl) usrname@hostname:~/curr_path$ python3 main_saving_frames.py --opt_reading_opencv False --opt_writing_single_proc False
```
E. Reading a vdieo: opencv-python, Writing a video: opencv-python
```bash
(virenv_dl) usrname@hostname:~/curr_path$ python3 main_writing_video.py --opt_reading_opencv True --opt_writing_opencv True
```
F. Reading a vdieo: opencv-python, Writing a video: ffmpeg-python
```bash
(virenv_dl) usrname@hostname:~/curr_path$ python3 main_writing_video.py --opt_reading_opencv True --opt_writing_opencv False
```
G. Reading a vdieo: ffmpeg-python, Writing a video: opencv-python
```bash
(virenv_dl) usrname@hostname:~/curr_path$ python3 main_writing_video.py --opt_reading_opencv False --opt_writing_opencv True
```
H. Reading a vdieo: ffmpeg-python, Writing a video: ffmpeg-python
```bash
(virenv_dl) usrname@hostname:~/curr_path$ python3 main_writing_video.py --opt_reading_opencv False --opt_writing_opencv False
```


## 6. Experiment result <a name="exp_res"></a>
|No.  |Description                                               |Total time [Sec.]|Total FPS|Averaged time [Sec.]|Averaged FPS|
|:---:|:--------------------------------------------------------:|:---------------:|:-------:|:------------------:|:----------:|
|1    |Reading a video with<br/>opencv-python                    |1.94             |0.52     |0.01                |188.42      |
|2    |Reading a video with<br/>ffmpeg-python                    |2.59             |0.39     |0.01                |140.84      |
|3    |Saving all frames with<br/>opencv-python (single-process) |17.77            |0.06     |0.05                |20.54       |
|4    |Saving all frames with<br/>opencv-python (multi-process)  |0.01             |89.66    |3.1e-5              |32726.30    |
|5    |Writing a video with<br/>opencv-python                    |5.44             |0.18     |0.01                |67.15       |
|6    |Writing a video with<br/>ffmpeg-python                    |3.27             |0.31     |0.01                |111.65      |

- As far as I mentioned in section 5, the measured time is the time including all the prcoessing time (e.g. reading, saving or writing).
- In the table, the meaning of the word in the cell, averaged, is the average processing time per frame.  
- The test envrionment including main arguemnts are as follows:
  - The resolution of the video: HD1080
  - The FPS of the video: about 23 FPS
  - The duration of the video: 15 seconds
  - The number of total frames in the video: 361 
  - The unit for batch-processing (i.e. num_batch): 5
  - The unit for multi-processing (i.e. num_proc): 4


## 7. Revision history <a name="revision_history"></a>
|Version |Description                            |Modifier  |
|:------:|:-------------------------------------:|:--------:|
|200531a |Release the code for the first time.   |vujadeyoon|

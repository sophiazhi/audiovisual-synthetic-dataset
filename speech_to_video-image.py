# ## Instructions before running this script ###
# > git clone https://github.com/zabique/Wav2Lip

# download the pretrained model
# > wget 'https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/_layouts/15/download.aspx?share=EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA' -O 'Wav2Lip/checkpoints/wav2lip_gan.pth'
# > wget 'https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/Eb3LEzbfuKlJiR600lQWRxgBIY27JZg80f7V9jtMfbNDaQ?e=TBFBVW' -O 'Wav2Lip/checkpoints/wav2lip.pth'

# > pip install https://raw.githubusercontent.com/AwaleSajil/ghc/master/ghc-1.0-py3-none-any.whl

# > cd Wav2Lip && pip install -r requirements.txt

# download pretrained model for face detection
# > wget "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth" -O "Wav2Lip/face_detection/detection/sfd/s3fd.pth"

# > pip install -q youtube-dl ### skipped this step for now, seems like just a colab thing
# > pip install ffmpeg-python
# > pip install av

# TODO: read video list from input file, not hardcoded

# ## Script ###

import subprocess
import torch
from torchvision.io import read_image, write_jpeg
from torch.nn.functional import interpolate
import av
import os
import soundfile as sf
import math
from tqdm import tqdm
import time
import json
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Parse arguments for speech to video pipeline')
    parser.add_argument('--audio_list', help='Path to json list of audio files')
    # parser.add_argument('--base_video', help='Path to base video', default='/om2/user/szhi/synthetic_dataset/IMG_7033_120.MOV')
    parser.add_argument('--base_image', help='Path to base image', default='/om2/user/szhi/synthetic_dataset/IMG_7093.jpg')
    parser.add_argument('--fps', help='Frames per second of generated video', default=120)
    parser.add_argument('--video_corpus', help='Path to video corpus', default='/om2/user/szhi/corpora/childes_synthetic_video_120fps')

    args = parser.parse_args()
    return args


# def load_base_video(base_video_path):
#     base_video_info = read_video(base_video_path, pts_unit="sec")
#     base_video = base_video_info[0]
#     base_video_len = base_video.shape[0]
#     fps = base_video_info[2]['video_fps']
#     base_video_len_sec = base_video_len / fps
    
#     return base_video, base_video_len_sec, fps


# def make_input_video(base_video_tuple, target_length_sec, input_video_path):
#     """
#     !pip3 install imageio==2.4.1
    
#     from moviepy.editor import VideoFileClip ?
#     """
#     base_video, base_video_len_sec, fps = base_video_tuple

#     if base_video_len_sec < target_length_sec:
#         input_video = torch.concat(
#             (
#                 base_video, 
#                 base_video[-1:].tile((math.ceil((target_length_sec-base_video_len_sec)*fps),1,1,1))
#             )
#         )
#     else:
#         input_video = base_video[:int(target_length_sec * fps)]

#     # input_video = torch.permute(input_video, (0, 2, 1, 3))
#     write_video(filename=input_video_path, video_array=input_video, fps=fps)

def make_input_image(iphone_image, input_image_path):
    image_tensor = read_image(iphone_image)
    print(image_tensor.shape) # torch.Size([3, 2316, 3088])
    image_tensor = torch.unsqueeze(image_tensor, 0)
    image_tensor = interpolate(image_tensor, (720, 960))
    image_tensor = torch.squeeze(image_tensor, 0)
    image_tensor = image_tensor.permute((0,2,1))
    print(image_tensor.shape)
    write_jpeg(image_tensor, input_image_path)

def generate_deepfake(audio_path, input_image_path, fps, output_video_path):
    # !cd Wav2Lip && python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face "/content/sample_data/input_video.mp4" --audio "/content/sample_data/input_audio.wav --resize_factor 2"
    command = f'cd Wav2Lip && python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face "{input_image_path}" --fps {fps} --audio "{audio_path}" --outfile "{output_video_path}"'
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    audio_corpus_path = "/om2/user/szhi/corpora/childes_synthetic_audio" # "~/corpora/childes_synthetic_audio"
    # video_corpus_path = "/om2/user/szhi/corpora/childes_synthetic_video" # "~/corpora/childes_synthetic_video"
    
    args = parse_args()
    video_corpus_path = args.video_corpus
    
    # read all audio files
    # audio_paths = [
    #     "23473/17294705.wav", 
    #     "23478/17306075.wav", 
    #     "23488/17326120.wav", 
    #     "23488/17334699.wav",
    #     "23497/17435388.wav",
    #     "23497/17443674.wav",
    #     "23497/17458175.wav",
    #     "23497/17481797.wav",
    #     "23511/17556425.wav",
    #     "23511/17639691.wav",
    # ]
    with open(args.audio_list, 'r') as f:
        audio_paths = json.load(f)
    
    # read base video
    # base_video_tuple = load_base_video("IMG_6233.MOV")
    # base_video_tuple = load_base_video(args.base_video)
    base_image_name, base_image_ext = os.path.splitext(args.base_image)
    input_image_path = f"{base_image_name}_temp{base_image_ext}"
    make_input_image(args.base_image, input_image_path)
    
    # make temp folders and speaker folders
    # subprocess.run(f"mkdir {os.path.join(video_corpus_path, 'temp')}", shell=True)
    for speaker_id in set([path.split("/")[0] for path in audio_paths]):
        # new_temp_dir = os.path.join(video_corpus_path, "temp", str(speaker_id))
        # subprocess.run(f"mkdir {new_temp_dir}", shell=True)
        new_speaker_dir = os.path.join(video_corpus_path, str(speaker_id))
        subprocess.run(f"mkdir {new_speaker_dir}", shell=True)
    
    print("Generating deepfakes")
    t = time.time()
    # call make_input_video(audio_len) for each audio
    # call generate_deepfake(audio_path, video_path) for each audio,video pair
    for audio_path in tqdm(audio_paths):
        ### NEW, pad the end of audio with 0.5s silence so output video isn't too short
        audio_global_path = os.path.join(audio_corpus_path, audio_path)
        input_audio_path = os.path.join(video_corpus_path, "temp", audio_path)
        # subprocess.run(f'ffmpeg -i {audio_global_path} -af "apad=pad_dur=500ms" {input_audio_path}', shell=True) # only pad at end of audio
        subprocess.run(f'ffmpeg -f lavfi -t 0.5 -i anullsrc=channel_layout=mono:sample_rate=44100 -i {audio_global_path} -filter_complex "[0:a][1:a][0:a]concat=n=3:v=0:a=1" {input_audio_path}', shell=True)
        ### END NEW
        
        # input_video_path = os.path.join(video_corpus_path, "temp", os.path.splitext(audio_path)[0] + ".mp4")
        # input_image_path = args.base_image
        output_video_path = os.path.join(video_corpus_path, os.path.splitext(audio_path)[0] + ".mp4")
        
        # print(input_video_path)
        print(output_video_path)
        
        audio_global_path = os.path.join(audio_corpus_path,audio_path)
        # audio = sf.SoundFile(audio_global_path)
        # target_length_sec = audio.frames / audio.samplerate
        
        # make_input_video(base_video_tuple, target_length_sec, input_video_path)
        generate_deepfake(audio_global_path, input_image_path, args.fps, output_video_path)
    
    print(f"Took {time.time()-t} seconds")
    
    # delete all the temporary videos from make_input_video
    # subprocess.run(f"rm -r {os.path.join(corpus_path, 'temp')}", shell=True)


from torchvision.io import read_video
import json
import os
import soundfile as sf
import argparse
from tqdm import tqdm
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description='Parse arguments for speech to video pipeline')
    parser.add_argument('audio_list', help='Path to json list of audio files')
    parser.add_argument('--audio_corpus', help='Path to corpus of audios extracted from deepfakes', default='/om2/user/szhi/corpora/childes_deepfake_audio_doublepad60fps')
    parser.add_argument('--video_corpus', help='Path to video corpus', default='/om2/user/szhi/corpora/childes_synthetic_video_doublepad60fps')

    args = parser.parse_args()
    return args

def get_video_list(audio_list):
    with open(audio_list, 'r') as f:
        video_list = json.load(f)
    video_list = [s[:-3]+'mp4' for s in video_list]
    return video_list

def make_subdirs(audio_corpus, video_list):
    # make speaker folders
    for speaker_id in set([path.split("/")[0] for path in video_list]):
        new_speaker_dir = os.path.join(audio_corpus, str(speaker_id))
        subprocess.run(f"mkdir {new_speaker_dir}", shell=True)

def extract_audios(video_list, video_corpus, audio_corpus):
    for filename in tqdm(video_list):
        video_path = os.path.join(video_corpus, filename)
        if not os.path.exists(video_path):
            print(f"Missing {filename}")
            continue
        video_info = read_video(video_path, pts_unit='sec')
        audio_fps = video_info[2]['audio_fps']
        audio_signal = video_info[1].squeeze()
        sf.write(os.path.join(audio_corpus, filename[:-3]+"wav"), audio_signal, audio_fps)

if __name__ == '__main__':
    args = parse_args()
    video_list = get_video_list(args.audio_list)
    make_subdirs(args.audio_corpus, video_list)
    extract_audios(video_list, args.video_corpus, args.audio_corpus)
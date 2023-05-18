import argparse
import json
from tqdm import tqdm
import os
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description='Parse arguments for file deletion')
    
    parser.add_argument('audio_json',) # input file name
    parser.add_argument('--video_corpus', default='/om2/user/szhi/corpora/childes_synthetic_video_example60fps') # model file name

    args = parser.parse_args()
    return args

def read_json(audio_json):
    with open(audio_json, 'r') as f:
        audio_list = json.load(f)
    return audio_list

def delete_results(audio_list, video_corpus):
    for filename in tqdm(audio_list):
        filename = os.path.splitext(filename)[0]
        
        # delete the audio file in temp/
        temp_audio_path = os.path.join(video_corpus, "temp", filename+".wav")
        if os.path.exists(temp_audio_path):
            subprocess.run(f"rm {temp_audio_path}", shell=True)
        
        # delete the video file in temp/
        temp_video_path = os.path.join(video_corpus, "temp", filename+".mp4")
        if os.path.exists(temp_video_path):
            subprocess.run(f"rm {temp_video_path}", shell=True)
        
        # delete the deepfake file 
        deepfake_path = os.path.join(video_corpus, filename+".mp4")
        if os.path.exists(deepfake_path):
            subprocess.run(f"rm {deepfake_path}", shell=True)

if __name__ == "__main__":
    args = parse_args()
    audio_list = read_json(args.audio_json)
    delete_results(audio_list, args.video_corpus)
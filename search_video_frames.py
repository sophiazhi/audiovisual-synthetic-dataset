import pandas as pd
from torchvision.io import read_video
import json
import os
import math
import torch
import matplotlib.pyplot as plt
from pathlib import Path

def aidx2phone(a_idx, alignment_df):
    a_time = ( 10*a_idx + 25.0/2 ) / 1000.0
    phone_match = alignment_df[alignment_df['Begin'] <= a_time]
    phone_match = phone_match[phone_match['End'] >= a_time]
    if len(phone_match) == 0:
        return 'SIL'
    phone_label = phone_match['Label'].iloc[0]
    return phone_label

def a2v_idx_offset(audio_idx, video_fps, offset):
    """ does not necessarily return an index >= 0 """
    time_ms = audio_idx * 10 + 25/2 - offset
    time_between_vidx = 1000 / video_fps
    video_idx = int(time_ms // time_between_vidx)
    # print(audio_idx, video_idx)
    return video_idx

def find_phone(phone, audio_json):
    with open(audio_json, 'r') as f:
        audio_list = json.load(f)
    phone_instances = []
    for audio_file in audio_list:
        alignment_file = os.path.join('/om2/user/szhi/corpora/childes_synthetic_audio_alignment', audio_file[:-3]+'csv')
        alignment_df = pd.read_csv(alignment_file)
        alignment_df['file'] = audio_file
        phone_instances.append(alignment_df[alignment_df['Label'] == phone])
    phone_instances_df = pd.concat(phone_instances)
    
    for idx, instance in phone_instances_df.iterrows():
        video_path = os.path.join('/om2/user/szhi/corpora/childes_synthetic_video_example60fps', instance['file'][:-3]+"mp4")
        video_info = read_video(video_path, pts_unit='sec')
        video_fps = video_info[2]['video_fps']
        begin, end = instance['Begin'], instance['End']
        # for each a_idx st begin <= (10*a_idx+12.5)/1000 <= end
        # for each a_idx st (1000*begin - 12.5)/10 <= a_idx <= (1000*end - 12.5)/10
        a_idx_min = math.ceil((1000*begin - 12.5)/10)
        a_idx_max = math.ceil((1000*end - 12.5)/10)
        for a_idx in range(a_idx_min, a_idx_max):
            v_idx = a2v_idx_offset(a_idx, video_fps, offset=120)
            if v_idx is None:
                continue
            
            curr_frame = video_info[0][v_idx]
            prev_frame = torch.zeros(video_info[0][v_idx].shape) if v_idx < 1 else video_info[0][v_idx-1]
            next_frame = torch.zeros(video_info[0][v_idx].shape) if v_idx >= len(video_info[0])-1 else video_info[0][v_idx+1]
            
            f, axarr = plt.subplots(1,3)
            axarr[0].imshow(prev_frame/255.0)
            axarr[1].imshow(curr_frame/255.0)
            axarr[2].imshow(next_frame/255.0)
            plt.savefig("frame_visualizations/{}_{}_{}.png".format(phone, Path(instance['file']).stem, a_idx))
            plt.clf()
            plt.close()

if __name__ == '__main__':
    find_phone('P', 'audio_jsons/first10.json')